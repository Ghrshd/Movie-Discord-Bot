from configparser import MissingSectionHeaderError
from os import O_SEQUENTIAL
import string
from sys import prefix
from discord.message import Message
from imdb import IMDb
import discord
from discord.ext import commands
import random
import json
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
    print(img)


@client.command(aliases=['c'])
async def cast(ctx, *, question):
    ia = IMDb()
    movies = ia.search_movie(question)
    ida = movies[0].movieID
    cast = []
    movie = ia.get_movie(ida)
    for i in range(5):
        actor = movie['cast'][i]
        actorAndRoll = f"**{actor['name']}** as {actor.currentRole} \n \n"
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
    actor = ia.get_person(
        ida, info=['biography', 'other works', 'awards', 'trivia', 'birth date'])
    trivia = actor['trivia']
    tlen = len(trivia)
    print(tlen)
    topMovies = []
    titleref = bio['titlesRefs']

    titleStrings = ','.join(map(str, titleref))
    li = list(titleStrings.split(","))
    stringCast = " "

    triviaoutput = random.randint(1, tlen)
    output = f"***age:***{actor['birth date']} \n ***trivia:*** {trivia[triviaoutput]} \n \n ***stared in:*** {li[0]}, {li[1]}, {li[2]}, {li[3]}, {li[4]}"
    #?awards, stars in , main ganres
    actor_results = ia.get_person_filmography(ida)
    #print(actor.summary())
    movies_acted = actor.get('actor')
    #print(actor.summary())
    a = len(actor['other works'])
    #print(actor['awards'])
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
#?game


@client.command(aliases=['quiz'])
async def Quiz(ctx):
    temp = []
    main = []

    def Getmovie():
        error = 0
        ia = IMDb()
        #? loop though 4 times
        #? append to list
        #? append list to main list
        for i in range(5):
            temp = []

            ran = random.randint(0, 250)

            top = ia.get_top250_movies()
            picked = f"{top[ran]}"
            movies = ia.search_movie(picked)
            ida = movies[0].movieID
            movie = ia.get_movie(ida)
            cast = []
            actor = movie['cast'][0]
            actorAndRoll = f"{actor['name']} as {actor.currentRole}"
            cast.append(actorAndRoll)

            temp.append(movie.data['title'])
            temp.append(movie.data['rating'])
            temp.append(movie.data['year'])
            temp.append(actor['name'])
            temp.append(f"{actor.currentRole}")
            try:
                temp.append(movie['box office']['Cumulative Worldwide Gross'])
                main.append(temp)
                temp = []

            except:
                error = "no boxOffice"
                temp = []
        return error

    Getmovie()
    print(Getmovie())

    if Getmovie() == "no boxOffice":
        typeQuest = random.randint(1, 4)
        print("yeet code")
        typeQuestList = typeQuest
    else:
        typeQuest = random.randint(1, 5)
        typeQuestList = typeQuest

    print("typeQuest before", typeQuest)
    print(main)
    EmojiList = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

    possAnswers = []
    #* possAnswers = [main[0][0], main[1][0], main[2][0], main[3][0], main[4][0]]
    i = 0
    QuestionNumber = 0
    TotalRight = 0
    #? sort the array so i dont need to use these
    if typeQuest == 1:
        typeQuestList = 0
    if typeQuest == 2:
        typeQuestList = 1
    if typeQuest == 3:
        typeQuestList = 3
    if typeQuest == 4:
        typeQuestList = 2
    if typeQuest == 5:
        typeQuestList = 5
    #? make a more effective random system
    print("Listval = ", typeQuestList)
    possAnswers = [main[0][typeQuestList], main[1][typeQuestList], main[2]
                   [typeQuestList], main[3][typeQuestList], main[4][typeQuestList]]
    print("pos ans =", possAnswers)
    RandomAns = random.sample(possAnswers, 5)
    answerIndex = RandomAns.index(main[QuestionNumber][typeQuestList])
    print("index", answerIndex)
    RightEmoji = EmojiList[answerIndex]
    #answer = RandomAns[answerIndex]
    #print("answer:", answer)
    FullQuestion = []

    def GetQuestion(main, QuestionNumber, RandomAns, TotalRight):
        if typeQuest == 1:
            question = f"what movie stars {main[QuestionNumber][3]} as {main[QuestionNumber][4]}"

        if typeQuest == 2:
            question = f"what is the IMDB rating of {main[QuestionNumber][0]}"
        if typeQuest == 3:
            question = f"who plays as {main[QuestionNumber][4]} in {main[QuestionNumber][0]}"
        if typeQuest == 4:
            question = f"what years was {main[QuestionNumber][0]} released"
        if typeQuest == 5:
            question = f"how much did {main[QuestionNumber][0]} gross"
        print("typeQuestion", typeQuest)
        output = f":one: - {RandomAns[0]} \n :two: - {RandomAns[1]} \n :three: - {RandomAns[2]} \n :four: - {RandomAns[3]} \n :five: - {RandomAns[4]}"
        FullQuestion.append(question)
        FullQuestion.append(output)
        FullQuestion.append(TotalRight)
        FullQuestion.append(QuestionNumber)

    GetQuestion(main, QuestionNumber, RandomAns, TotalRight)
    #output = "k"
    print("2nd", RandomAns)
    print("final list val = ", typeQuestList)

    #print(f"aadada what years was {main[1][0]} released")
    print("question ", FullQuestion[0])
    embed = discord.Embed(
        title=FullQuestion[0],
        description=FullQuestion[1],
        colour=discord.Colour.red()
    )
    #* get the amount anwered right and username + time taken
    img = "https://beta-visuals.com/wp-content/uploads/2019/03/Logo-beta-copiafinal.png"
    embed.set_footer(text=f"{QuestionNumber + 1}/5")
    embed.set_thumbnail(url=img)
    message = ctx.send(embed=embed)
    await message
    await ctx.message.add_reaction(emoji=f'{EmojiList[0]}')
    await ctx.message.add_reaction(emoji=f'{EmojiList[1]}')
    await ctx.message.add_reaction(emoji=f'{EmojiList[2]}')
    await ctx.message.add_reaction(emoji=f'{EmojiList[3]}')
    await ctx.message.add_reaction(emoji=f'{EmojiList[4]}')

    @client.event
    async def on_reaction_add(reaction, user,):
        if reaction.emoji == RightEmoji:
            print("right")
            FullQuestion[2] += 1
            FullQuestion[3] += 1  # adding 1 to the question count
            #?take away the reaction
            await message.edit('b')
        else:
            FullQuestion[3] += 1
            pass

    def NextQuestion():
        pass

    #?year
    #? rating (closer better)
"""    #? 
#?change prefix
def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixs = json.load(file)

    return prefixs[str(message.guild.id)]

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixs = json.load(file)

    prefixs[str(guild.id)] = '|'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixs, file, indent=4)

@client.event



client = commands.Bot(command_prefix= get_prefix)
"""
#?suggest
#? genre

#? top movies


@client.command(aliases=['top'])
async def GetTop(ctx):
    main = []

    def GetTop():
        for i in range(10):
            ia = IMDb()
            top = ia.get_top250_movies()
            movies = ia.search_movie(f"{top[i]}")
            ida = movies[0].movieID
            movie = ia.get_movie(ida)
            rate = movie.data['rating']
            main.append(f"**{top[i]}**  --  {rate} \n")
        stringCast = " "
        output = stringCast.join(main)
        return output

    embed = discord.Embed(
        title="top Movies",
        description=GetTop(),
        colour=discord.Colour.red()
    )
    #? split into pages of 10
    message = ctx.send(embed=embed)
    await message
#?top indian


@client.command(aliases=['topin'])
async def Topin(ctx):
    main = []

    def GetTopin():
        ia = IMDb()
        for i in range(10):
            top = ia.get_top250_indian_movies()
            movies = ia.search_movie(f"{top[i]}")
            ida = movies[0].movieID
            movie = ia.get_movie(ida)
            rate = movie.data['rating']
            #? get rating of I
            main.append(f"**{top[i]} ** -- {rate} \n")
        print(main)
        stringCast = " "
        output = stringCast.join(main)
        return output

    embed = discord.Embed(
        title="top Indian Movies",
        description=GetTopin(),
        colour=discord.Colour.red()
    )
    #? split into pages of 10
    #* get the amount anwered right and username + time taken
    img = "https://beta-visuals.com/wp-content/uploads/2019/03/Logo-beta-copiafinal.png"
    embed.set_footer(text=f"1/5")
    embed.set_thumbnail(url=img)
    message = ctx.send(embed=embed)
    await message
#?bottom

#?vote system
#? what movie, time
client.run(f'{Token}')

#* https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for
#* https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
