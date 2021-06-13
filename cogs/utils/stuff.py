import discord 
from discord.ext import commands
import re
import random
import string
import datetime
import asyncio
import discord
from discord.ext.commands import Paginator as CommandPaginator
from discord.ext import menus
import io

class _ContextDBAcquire:
    __slots__ = ('ctx', 'timeout')

    def __init__(self, ctx, timeout):
        self.ctx = ctx
        self.timeout = timeout

    def __await__(self):
        return self.ctx._acquire(self.timeout).__await__()

    async def __aenter__(self):
        await self.ctx._acquire(self.timeout)
        return self.ctx.db

    async def __aexit__(self, *args):
        await self.ctx.release()





class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._db = None

    async def entry_to_code(self, entries):
        width = max(len(a) for a, b in entries)
        output = ['```']
        for name, entry in entries:
            output.append(f'{name:<{width}}: {entry}')
        output.append('```')
        await self.send('\n'.join(output))

    async def indented_entry_to_code(self, entries):
        width = max(len(a) for a, b in entries)
        output = ['```']
        for name, entry in entries:
            output.append(f'\u200b{name:>{width}}: {entry}')
        output.append('```')
        await self.send('\n'.join(output))

    def __repr__(self):
        # we need this for our cache key strategy
        return '<Context>'

    @property
    def session(self):
        return self.bot.session

    @discord.utils.cached_property
    def replied_reference(self):
        ref = self.message.reference
        if ref and isinstance(ref.resolved, discord.Message):
            return ref.resolved.to_reference()
        return None

    async def disambiguate(self, matches, entry):
        if len(matches) == 0:
            raise ValueError('No results found.')

        if len(matches) == 1:
            return matches[0]

        await self.send('There are too many matches... Which one did you mean? **Only say the number**.')
        await self.send('\n'.join(f'{index}: {entry(item)}' for index, item in enumerate(matches, 1)))

        def check(m):
            return m.content.isdigit() and m.author.id == self.author.id and m.channel.id == self.channel.id

        await self.release()

        # only give them 3 tries.
        try:
            for i in range(3):
                try:
                    message = await self.bot.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    raise ValueError('Took too long. Goodbye.')

                index = int(message.content)
                try:
                    return matches[index - 1]
                except:
                    await self.send(f'Please give me a valid number. {2 - i} tries remaining...')

            raise ValueError('Too many tries. Goodbye.')
        finally:
            await self.acquire()

    async def prompt(self, message, *, timeout=60.0, delete_after=True, reacquire=True, author_id=None):
        """An interactive reaction confirmation dialog.
        Parameters
        -----------
        message: str
            The message to show along with the prompt.
        timeout: float
            How long to wait before returning.
        delete_after: bool
            Whether to delete the confirmation message after we're done.
        reacquire: bool
            Whether to release the database connection and then acquire it
            again when we're done.
        author_id: Optional[int]
            The member who should respond to the prompt. Defaults to the author of the
            Context's message.
        Returns
        --------
        Optional[bool]
            ``True`` if explicit confirm,
            ``False`` if explicit deny,
            ``None`` if deny due to timeout
        """

        if not self.channel.permissions_for(self.me).add_reactions:
            raise RuntimeError('Bot does not have Add Reactions permission.')

        fmt = f'{message}\n\nReact with \N{WHITE HEAVY CHECK MARK} to confirm or \N{CROSS MARK} to deny.'

        author_id = author_id or self.author.id
        msg = await self.send(fmt)

        confirm = None

        def check(payload):
            nonlocal confirm

            if payload.message_id != msg.id or payload.user_id != author_id:
                return False

            codepoint = str(payload.emoji)

            if codepoint == '\N{WHITE HEAVY CHECK MARK}':
                confirm = True
                return True
            elif codepoint == '\N{CROSS MARK}':
                confirm = False
                return True

            return False

        for emoji in ('\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'):
            await msg.add_reaction(emoji)

        if reacquire:
            await self.release()

        try:
            await self.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            confirm = None

        try:
            if reacquire:
                await self.acquire()

            if delete_after:
                await msg.delete()
        finally:
            return confirm
        
    def tick(self, opt, label=None):
        lookup = {
            True: '<:greenTick:847079742763171850>',
            False: '<:redTick:847088288174440459>',
            None: '<:greyTick:847088761891979275>',
        }
        emoji = lookup.get(opt, '<:redTick:847088288174440459>')
        if label is not None:
            return f'{emoji}: {label}'
        return emoji
    @property
    def db(self):
        return self._db if self._db else self.pool

    async def _acquire(self, timeout):
        if self._db is None:
            self._db = await self.pool.acquire(timeout=timeout)
        return self._db

    def acquire(self, *, timeout=300.0):
        """Acquires a database connection from the pool. e.g. ::
            async with ctx.acquire():
                await ctx.db.execute(...)
        or: ::
            await ctx.acquire()
            try:
                await ctx.db.execute(...)
            finally:
                await ctx.release()
        """
        return _ContextDBAcquire(self, timeout)

    async def release(self):
        """Releases the database connection from the pool.
        Useful if needed for "long" interactive commands where
        we want to release the connection and re-acquire later.
        Otherwise, this is called automatically by the bot.
        """
        # from source digging asyncpg source, releasing an already
        # released connection does nothing

        if self._db is not None:
            await self.bot.pool.release(self._db)
            self._db = None

    async def show_help(self, command=None):
        """Shows the help command for the specified command if given.
        If no command is given, then it'll show help for the current
        command.
        """
        cmd = self.bot.get_command('help')
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)

    async def safe_send(self, content, *, escape_mentions=True, **kwargs):
        """Same as send except with some safe guards.
        1) If the message is too long then it sends a file with the results instead.
        2) If ``escape_mentions`` is ``True`` then it escapes mentions.
        """
        if escape_mentions:
            content = discord.utils.escape_mentions(content)

        if len(content) > 2000:
            fp = io.BytesIO(content.encode())
            kwargs.pop('file', None)
            return await self.send(file=discord.File(fp, filename='message_too_long.txt'), **kwargs)
        else:
            return await self.send(content)



class RoboPages(menus.MenuPages):
    def __init__(self, source):
        super().__init__(source=source, check_embeds=True)
        self.input_lock = asyncio.Lock()

    async def finalize(self, timed_out):
        try:
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()
        except discord.HTTPException:
            pass

    @menus.button('\N{INFORMATION SOURCE}\ufe0f', position=menus.Last(3))
    async def show_help(self, payload):
        """shows this message"""
        embed = discord.Embed(title='Paginator help', description='Hello! Welcome to the help page.')
        messages = []
        for (emoji, button) in self.buttons.items():
            messages.append(f'{emoji}: {button.action.__doc__}')

        embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)
        embed.set_footer(text=f'We were on page {self.current_page + 1} before this message.')
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_page(self.current_page)

        self.bot.loop.create_task(go_back_to_current_page())

    @menus.button('\N{INPUT SYMBOL FOR NUMBERS}', position=menus.Last(1.5), lock=False)
    async def numbered_page(self, payload):
        """lets you type a page number to go to"""
        if self.input_lock.locked():
            return

        async with self.input_lock:
            channel = self.message.channel
            author_id = payload.user_id
            to_delete = []
            to_delete.append(await channel.send('What page do you want to go to?'))

            def message_check(m):
                return m.author.id == author_id and \
                       channel == m.channel and \
                       m.content.isdigit()

            try:
                msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
            except asyncio.TimeoutError:
                to_delete.append(await channel.send('Took too long.'))
                await asyncio.sleep(5)
            else:
                page = int(msg.content)
                to_delete.append(msg)
                await self.show_checked_page(page - 1)

            try:
                await channel.delete_messages(to_delete)
            except Exception:
                pass

class FieldPageSource(menus.ListPageSource):
    """A page source that requires (field_name, field_value) tuple items."""
    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)
        self.embed = discord.Embed(colour=discord.Colour.blurple())

    async def format_page(self, menu, entries):
        self.embed.clear_fields()
        self.embed.description = discord.Embed.Empty

        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=False)

        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            self.embed.set_footer(text=text)

        return self.embed

class TextPageSource(menus.ListPageSource):
    def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
        pages = CommandPaginator(prefix=prefix, suffix=suffix, max_size=max_size - 200)
        for line in text.split('\n'):
            pages.add_line(line)

        super().__init__(entries=pages.pages, per_page=1)

    async def format_page(self, menu, content):
        maximum = self.get_max_pages()
        if maximum > 1:
            return f'{content}\nPage {menu.current_page + 1}/{maximum}'
        return content

class SimplePageSource(menus.ListPageSource):
    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)
        self.initial_page = True

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{index + 1}. {entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            menu.embed.set_footer(text=footer)

        if self.initial_page and self.is_paginating():
            pages.append('')
            pages.append('Confused? React with \N{INFORMATION SOURCE} for more info.')
            self.initial_page = False

        menu.embed.description = '\n'.join(pages)
        return menu.embed

class SimplePages(RoboPages):
    """A simple pagination session reminiscent of the old Pages interface.
    Basically an embed with some normal formatting.
    """

    def __init__(self, entries, *, per_page=12):
        super().__init__(SimplePageSource(entries, per_page=per_page))
        self.embed = discord.Embed(colour=discord.Colour.blurple())