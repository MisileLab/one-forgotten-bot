import os  #disable=missing-module-docstring
import disnake
from disnake.ext import commands
from disnake.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionNotLoaded
import disnake.ext.commands.errors as errors
from disnake.ext.commands import Context
import koreanbots
from cogs.modules import module1 as md1
from cogs.modules import module2 as md2
from dotenv import dotenv_values

dotenvvalues = dotenv_values(".env")
koreanbotstoken = dotenvvalues["koreanbotstoken"]
token = dotenvvalues["token"]

devserver = [812339145942237204, 635336036465246218, 863950154055155712]
Client = commands.Bot(command_prefix="/", intents=disnake.Intents.all(), help_command=None)
Client1 = koreanbots.Koreanbots(Client, koreanbotstoken, run_task=True)

icecreamhappydiscord = [635336036465246218]
ignore_error = commands.CommandNotFound, disnake.errors.NotFound
message_error = errors.MissingPermissions, errors.application_commands.BotMissingPermissions, \
                errors.application_commands.CommandOnCooldown


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        Client.load_extension(f"cogs.{file[:-3]}")
        print(f"cogs.{file[:-3]} - 로드 성공!")


@Client.event
async def on_ready():
    """just on ready event"""
    print("Slash Client Ready!")


# noinspection PyUnusedLocal
@Client.event
async def on_command_error(error):
    """not slash command error"""
    if not isinstance(error, ignore_error):
        raise error


@Client.event
async def on_slash_command_error(inter, error):
    """slash command error"""
    if not isinstance(error, ignore_error):
        if isinstance(error, message_error):
            await md2.sub_error_handler(error, inter).ErrorHandling()
        else:
            raise error


@Client.event
async def on_member_join(member: disnake.Member):
    """
    when member join event
    :param member: disnake.Member object
    """
    embed = md2.make_member_join_embed(member)
    getchannel = md1.serverdata("insaname", member.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["insaname"])
    except (AttributeError, disnake.HTTPException, disnake.NotFound):
        pass
    else:
        await channel.send(embed=embed)
        if getchannel["recaptcha"] != 0:
            await md1.auth_recaptcha(member, getchannel)


@Client.event
async def on_member_remove(member: disnake.Member):
    """same as on_member_join except this is member remove event"""
    embed = md2.make_member_remove_embed(member)
    getchannel = md1.serverdata("insaname", member.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["insaname"])
    except (AttributeError, disnake.HTTPException, disnake.NotFound):
        pass
    else:
        await channel.send(embed=embed)


@Client.event
async def on_message_delete(message: disnake.Message):
    """
    on member delete event
    :param message disnake.Member object
    """
    if message.author.bot is False:
        embed1 = disnake.Embed(name="메시지가 삭제되었어요!")
        embed1.add_field(name="삭제된 메시지의 내용", value=message.content, inline=False)
        embed1.add_field(name="삭제된 메시지를 보낸 사람", value=f"<@{message.author.id}>", inline=False)
        embed1.add_field(name="삭제된 메시지가 보내진 채널", value=message.channel.mention, inline=False)
        embed1.set_footer(text=md1.todaycalculate())
        getchannel = md1.serverdata("logid", message.guild.id, 123, True)
        try:
            channel = await Client.fetch_channel(getchannel["logid"])
        except (AttributeError, disnake.HTTPException, disnake.NotFound):
            pass
        else:
            await channel.send(embed=embed1)


@Client.event
async def on_message_edit(before: disnake.Message, after: disnake.Message):
    """
    on message edit event
    :param before: no edit message
    :type disnake.Message: Message
    :param after: edited message
    :type disnake.Message: Message
    """
    if after.author.bot is True:
        return
    try:
        attachmentsurl = after.attachments[0].url
    except IndexError:
        pass
    else:
        if attachmentsurl is not None:
            embed1 = md1.get_message_edit_embed(before, after)
            getchannel = md1.serverdata("logid", after.guild.id, 123, True)
            try:
                channel = await Client.fetch_channel(getchannel["logid"])
            except (AttributeError, disnake.errors.HTTPException):
                pass
            else:
                await channel.send(embed=embed1)


@Client.command(name="hellothisisverification")
async def oneforgottendiscordslashcommandkoreanbotlistnoslashcommandlol(ctx):
    """koreanbots looks like sus lol"""
    await ctx.send("Misile#1231")


@Client.command(name="cogs", guild_ids=devserver)
async def _cogs(inter: Context):
    """just cogs"""
    pass  # empty cause this command is need to subcommand

unloadoption = md2.NoneSlashCommand()
unloadoption.add_option(name="cogname", description="cog name", required=True)


@_cogs.sub_command(name="unload", description="unload cog", options=unloadoption.options, guild_ids=devserver)
async def _unloadcogs(inter: Context):
    """
    unload cogs
    :param inter: Context object
    """
    cogname = inter.get_option("unload").get("cogname")
    try:
        Client.unload_extension(f"cogs.{cogname}")
    except ExtensionNotFound:
        await inter.reply("그 cogs는 없는 것 같습니다.")
    except ExtensionNotLoaded:
        await inter.reply("그 cogs는 이미 로드되지 않았습니다.")
    except Exception:
        print(f'cogs.{cogname} error')
        raise
    else:
        await inter.reply("cogs가 정상 언로드되었습니다.")


@_cogs.sub_command(name="load", description="load cog", options=unloadoption.options, guild_ids=devserver)
async def _loadcogs(inter: Context):
    """same as unload cogs except this is load cogs"""
    cogname = inter.get_option("load").get("cogname")
    try:
        Client.load_extension(f"cogs.{cogname}")
    except ExtensionNotFound:
        await inter.reply("그 cogs는 없는 것 같습니다.")
    except ExtensionAlreadyLoaded:
        await inter.reply("그 cogs는 이미 로드되었습니다.")
    except Exception:
        print(f'cogs.{cogname} error')
        raise
    else:
        await inter.reply("cogs가 정상 로드되었습니다.")


@_cogs.sub_command(name="reload", description="reload cogs", guild_ids=devserver)
async def _reloadcogs(inter: Context):
    """same as reload cogs except this is load cogs"""
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                Client.unload_extension(f"cogs.{file[:-3]}")
                Client.load_extension(f"cogs.{file[:-3]}")
            except Exception:
                print(f'cogs.{file[:-3]} error')
                raise
            else:
                print(f"cogs.{file[:-3]} - 리로드 성공!")
    await inter.reply("리로드 성공!")


Client.run(token)
