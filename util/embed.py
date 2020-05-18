"""
Embed functions
"""
import discord

def make(title: str, desc: str) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, colour=0xc1c100)
    return embed

def make_error(message: str) -> discord.Embed:
    embed = discord.Embed(title="Error", description=message, colour=0xf84722)
    return embed

def make_field(title: str, desc: str, field_name: str, field_val: str, inline: bool = True) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, colour=0xc1c100)
    embed.add_field(name=field_name, value=field_val, inline=inline)
    return embed

def make_fields(title: str, desc: str, *fields: tuple) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, colour=0xc1c100)
    for name, value in fields:
        embed.add_field(name=name, value=value)
    return embed

def make_fields_footer(title: str, desc: str, footer: str, *fields: tuple) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, colour=0xc1c100)
    embed.set_footer(text=footer)
    for name, value in fields:
        embed.add_field(name=name, value=value)
    return embed

def make_fields_ninl(title: str, desc: str, *fields: tuple) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, colour=0xc1c100, inline=False)
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)
    return embed

def make_image(title: str, path: str) -> (discord.Embed, discord.File):
    embed = discord.Embed(title=title, colour=0xc1c100)
    attachment = discord.File(path, filename="image.png")
    embed.set_image(url='attachment://image.png')
    return (embed, attachment)