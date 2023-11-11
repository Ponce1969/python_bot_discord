import discord 
from discord.ext import commands
from googleapiclient.discovery import build
import datetime
import pytz
from dotenv import load_dotenv
import os
import  requests
import re



# clave discord.
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Configura tu clave API aquí
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

youtube_api = build('youtube', 'v3', developerKey=youtube_api_key)

intents = discord.Intents.default()
intents.message_content = True
bot= commands.Bot(command_prefix='>', description="Esto es un bot de ayuda", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')



@bot.command()
async def saludo(ctx, nombre: str = None):
    if nombre:
        await ctx.send(f"Hola,  {nombre}!! \n Bienvenido al Servidor de Gonzalo Ponce.")
    else:
        await ctx.send("Hola! Por favor, dime tu nombre para saludarte correctamente, asi \n >saludo y tu nombre")



@bot.command()
async def sum(ctx, numero_uno: int, numero_dos: int):
    await ctx.send(numero_uno + numero_dos)

@bot.command()
async def resta(ctx, numero_uno: int, numero_dos: int):
    await ctx.send(numero_uno - numero_dos)


@bot.command()
async def info(ctx):
    # Obten la hora actual en la zona horaria de Uruguay
    uruguay_time = datetime.datetime.now(pytz.timezone('America/Montevideo'))

    if ctx.guild is None:
        title = "Mensaje Directo"
    else:
        title = ctx.guild.name

    # Crea el embed con el título y la hora de Uruguay
    embed = discord.Embed(title=title, 
        description="Aprendiendo Python y sus librerias",
        timestamp=uruguay_time, color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def mult(ctx, numero_uno: int, numero_dos: int):
    await ctx.send(numero_uno * numero_dos)


@bot.command()
async def div(ctx, numero_uno: int, numero_dos: int):
    await ctx.send(numero_uno // numero_dos)


@bot.command()
async def resto(ctx, numero_uno: int, numero_dos: int):
    await ctx.send(numero_uno % numero_dos)



#Eventos
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorial de Mouredev",
    url="http://www.twitch.tv/mouredev/videos"))
    print("Mi Bot esta en linea")


# peticiones a youtube.
@bot.command()
async def youtube(ctx, *, search):
    request = youtube_api.search().list(
        part="snippet",
        maxResults=1,
        q=search
    )
    response = request.execute()

    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        await ctx.send('https://www.youtube.com/watch?v=' + video_id)
    else:
        await ctx.send('No se encontraron videos para tu búsqueda.')




bot.run(token)
