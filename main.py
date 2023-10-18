import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from time import sleep
import uuid

client = commands.Bot(command_prefix=',', intents=discord.Intents.all())

bot_stat = cycle(["Generating keys", "1000 Keys"])

@tasks.loop(seconds=15)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_stat)))

@client.event
async def on_ready():
    print("Gen Bot Online")
    change_status.start()

@client.command()
async def gen(ctx, amount):
    key_amt = range(int(amount))
    f = open("keys.txt", "a")
    show_key = ''
    for x in key_amt:
        key = str(uuid.uuid4())
        show_key += "\n" + key
        f.write(key)
        f.write("\n")

    if len(str(show_key)) == 37:
        show_key = show_key.replace('\n', '')
        await ctx.message.author.send(f"Key: {show_key}")
        return 0
    if len(str(show_key)) > 37:
        await ctx.send("Something is wrong!")

@client.command()
async def redeem(ctx, key):
    if len(key) == 36:
        with open("used keys.txt") as f:
            if key in f.read():
                em = discord.Embed(color=0xff0000)
                em.add_field(name="Invalid Key", value="Inputed key has already been used!")
                await ctx.send(embed=em)
                return 0
        with open("keys.txt") as f:
            if key in f.read():
                role = discord.utils.get(ctx.guild.roles, name='Main')
                await ctx.author.add_roles(role)
                em = discord.Embed(color=0x008525)
                em.add_field(name=" Key Redeemed", value="Key has now been redeemed")
                await ctx.send(embed=em)
                f = open("used keys.txt", 'w')
                f.write(key)
                f.write('\n')
            else:
                em = discord.Embed(color=0xff0000)
                em.add_field(name="Invalid Key", value="Inputted key ahs already been used")
                await ctx.send(embed=em)
    else:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="Invalid Key", value="Inputted key has alraedy been redeemed")
        await ctx.send(embed=em)

client.run("KEY")