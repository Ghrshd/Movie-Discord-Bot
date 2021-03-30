import string
from sys import prefix
from imdb import IMDb
import discord
from discord.ext import commands
import random
import json
from token.py import *

client = commands.Bot(command_prefix='|')


@client.event
async def on_ready():
    print("Bot Ready")

def mlengh(movie):
    lengh = str(movie.data['runtimes'])
    lenin = int(lengh.replace('[', '').replace("'", '').replace("]", ''))
    if lenin < 60:
        hours = 0
        minues = lenin
    hours = round(lenin/60)
    minues = (round(lenin % 60))
    mlengh.time = f"{hours} hours, {minues} minues"

@client.command(aliases=['s'])
async def rating(ctx, *, question):

    ia = IMDb()
    movies = ia.search_movie(question)
    ida = movies[0].movieID
    movie = ia.get_movie(ida)
    rating = movie.data['rating']
    description = movie.get('plot outline')
    mlengh(movie)
    output = f'⭐ {rating}\n{description}'
    img = movie['cover url']
    embed = discord.Embed(
        title=question,
        description=output,
        colour=discord.Colour.red()
    )
    embed.set_footer(text=mlengh.time)
    embed.set_thumbnail(url=img)
    await ctx.send(embed=embed)


@client.command(aliases=['c'])
async def cast(ctx, *, question):
    ia = IMDb()
    movies = ia.search_movie(question)
    ida = movies[0].movieID
    cast = []
    movie = ia.get_movie(ida)
    for i in range(5):
        actor = movie['cast'][i]
        actorAndRoll = f"{actor['name']} as {actor.currentRole} \n \n"
        cast.append(actorAndRoll)
    stringCast = " "
    output = stringCast.join(cast)

    embed = discord.Embed(
        title=question,
        description=output,
        colour=discord.Colour.red()
    )
    img = movie['cover url']
    embed.set_thumbnail(url=img)
    await ctx.send(embed=embed)


#? person search
@client.command(aliases=['as'])
async def actorSearch(ctx, *, question):
    ia = IMDb()
    actorSear = ia.search_person(question)
    ida = actorSear[0].personID
    bio = ia.get_person_biography(ida)
    actor = ia.get_person(ida, info=['biography', 'other works','awards','trivia','birth date'])
    trivia = actor['trivia']
    tlen = len(trivia)
    print(tlen)
    topMovies = []
    titleref = bio['titlesRefs']

    titleStrings = ','.join(map(str, titleref))
    li = list(titleStrings.split(","))
    stringCast = " "

    triviaoutput = random.randint(1,tlen)
    output = f"***age:***{actor['birth date']} \n ***trivia:*** {trivia[triviaoutput]} \n \n ***stared in:*** {li[0]}, {li[1]}, {li[2]}, {li[3]}, {li[4]}"
    #?awards, stars in , main ganres 
    actor_results = ia.get_person_filmography(ida)
    movies_acted = actor.get('actor')
    a =len(actor['other works'])
    x = 5
    works = []
    while x != 0:
        i = len(actor['other works']) - x
        works.append(actor['other works'][x])
        x = x - 1
    print(works)

    embed = discord.Embed(
        title=question,
        description=output,
        colour=discord.Colour.red()
    )
    img = actor['headshot']
    embed.set_thumbnail(url=img)
    await ctx.send(embed=embed)

#?suggest
    #? genre

#? top movies

#?top indian

#?bottom 

client.run(f'{Token}')

#* https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for
#* https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
