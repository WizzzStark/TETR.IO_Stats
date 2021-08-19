# -------------------------------------- IMPORTAR MODULOS Y CONFIGURACION ----------------------------------------------------------
import aiohttp 
import discord
from discord.ext import commands
from discord import Embed
from tools.dataIO import fileIO 
from tools.emotes import * 
import pprint

config_location = fileIO("config/config.json", "load")
Prefix = config_location["Prefix"]
Shards = config_location["Shards"]

bot = commands.AutoShardedBot(command_prefix=Prefix)
bot.remove_command('help')

# ------------------------------------ REGISTRO DEL BOT ---------------------------------------------

@bot.event 
async def on_ready():
    print("-----------")
    print(f"ID: {bot.user.id}")
    print(f"Username: {bot.user.name}")
    print("Conenctado a TETR.IO API!")
    print("-----------")
    await bot.change_presence(activity=discord.Game(name="!stats <nombre>"))

@bot.event
async def on_command(command):
	info = fileIO("config/config.json", "load")
	info["Commands_used"] = info["Commands_used"] + 1
	fileIO("config/config.json", "save", info)

# ------------------------------------ COMANDOS ---------------------------------------------


@bot.command(aliases=["usuario", "player","user", "User", "estadísiticas", "estadisticas", "Stats"])
async def stats(ctx, user="Debes introducir un nombre de usuario!"):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://ch.tetr.io/api/users/{user}') as r:
            res = await r.json()

            #utilities
            str = ''
            user = res['data']['user']
            league = res['data']['user']['league']

            #info
            username = user['username']
            country = user['country']
            try:
                c2 = country.lower()
                country= ":flag_" + c2
            except AttributeError:
                pass
            

            #user
            support = user['supporter_tier']
            verified = user['verified']
            role = user['role']
            games = user['gamesplayed']
            if games == -1:
                games = "No se pudo obtener"
            wins = user['gameswon']
            if wins == -1:
                wins = "No se pudo obtener"
            gametime = int(user['gametime'])
            gt = int(gametime / 3600)
            xp = int(user['xp'])

            #league
            lgames = int(league['gamesplayed'])
            won = int(league['gameswon'])
            apm = float(league['apm'])
            pps = float(league['pps'])
            vs = float(league['vs'])
            rank = league['percentile_rank']
            puntos =int(league['rating'])

            #badges
            for i in user['badges']:
                if i['id'] == '20tsd':
                    a = i['label']
                    str += tsd
                    str += " "
                    str += a + '\n'
                if i['id'] == 'secretgrade':
                    a = i['label']
                    str += sg
                    str += " "
                    str += a + '\n'
                if i['id'] == '100player':
                    a = i['label']
                    str += hundred
                    str += " "
                    str += a + '\n'
                if i['id'] == 'kod_founder':
                    a = i['label']
                    str += kod
                    str += " "
                    str += a + '\n'
                if i['id'] == 'early-supporter':
                    a = i['label']
                    str += early
                    str += " "
                    str += a + '\n'
                if i['id'] == 'superlobby':
                    a = i['label']
                    str += superlobby
                    str += " "
                    str += a + '\n'
                if i['id'] == 'founder':
                    a = i['label']
                    str += founder
                    str += " "
                    str += a + '\n'

            #Pequeño error handler
            if str == '':
                str = "Este jugador no tiene insignias"

            #Embed
            embed = discord.Embed(
            title=f"Estadísticas en TETR.IO ",
            description= "Información relevante de la cuenta, si lleva mucho tiempo inactiva puede dar errores al recoger algunos datos.",
            color=0x7033ff
            )
            embed.add_field(name=f"{user_} `Información de la cuenta`", 
                            value=f"\n**Usuario: **{username}\n**País:** {country}:\n**Supporter Tier:** {support}\n**Verificado: **{verified}\n**Rol: **{role}",
                            inline=True)
            
            embed.add_field(name=f"{game} `Información de juego`",
                            value=f"\n**Partidas jugadas:** {games}\n**Partidas ganadas:** {wins}\n**Tiempo jugado:** {gt} horas\n**XP obtenido:** {xp}",
                            inline=False)
            
            embed.add_field(name=f"{tleague} `Tetra League`", 
                            value=f"\n**Partidas jugadas:** {lgames}\n**Partidas ganadas:** {won}\n**APM:** {apm}\n**PPS:** {pps}\n**VS:** {vs}\n**TR/Puntos:** {puntos}\n**Rank:** {rank}",
                            inline=True)
            
            embed.add_field(name=f"{badges} `Badges del jugador`",
                            value=f"{str}\n", 
                            inline=False)


            embed.set_thumbnail(url=f"https://tetr.io/user-content/avatars/{res['data']['user']['_id']}.jpg?rv=AVATAR_REVISION")
            embed.set_footer(text="Developed by @WizzzStark")
            #embed.set_footer(text="Solicitado por: {}".format(ctx.author.display_name))
            embed.set_image(url="https://media.giphy.com/media/hqrNeKv56gNNQPyHZI/giphy.gif")
            await ctx.send(embed=embed)



@bot.command(aliases=["r"])
async def info(ctx, user="Debes introducir un nombre de usuario!"):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://ch.tetr.io/api/users/{user}') as r:
            res = await r.json()
            pprint.pprint(res)


bot.run(config_location["Token"])