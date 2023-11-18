import discord 
from discord.ext import commands
from googleapiclient.discovery import build
import datetime
import pytz
from dotenv import load_dotenv
import os
import asyncio
import database



# clave discord.
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Configura tu clave API aquí
youtube_api_key = os.getenv('YOUTUBE_API_KEY')



youtube_api = build('youtube', 'v3', developerKey=youtube_api_key)

intents = discord.Intents.default()
intents.message_content = True
bot= commands.Bot(command_prefix='>', description="Esto es un bot de ayuda", intents=intents)

# Declaración global de connection al principio del script
global connection
connection = None


# Evento on_ready combinado
@bot.event
async def on_ready():
    global connection
    connection = database.db_connect()
    await bot.change_presence(activity=discord.Streaming(name="Tutorial de Mouredev", url="http://www.twitch.tv/mouredev/videos"))
    print("Bot is ready")
    print("Mi Bot esta en linea")


# Comando register
@bot.command(help="registrate en la database")
async def register(ctx):
    global connection  # Usa la variable global
    flag = database.verify_id(connection, str(ctx.author.id))
    if flag:
        await ctx.send("Usted se encuentra registrado en la base de datos")
    else:
        database.register(connection, ctx)
        await ctx.send("Te has registrado correctamente en la base de datos")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def ayuda(ctx):
    ayuda_msg = """
    Hola! Soy tu bot de Discord. Aquí están las cosas que puedo hacer:

    1. **Buscar canciones de YouTube**: Usa `>youtube <nombre de la canción>` para buscar una canción en YouTube.
    2. **Operaciones matemáticas**: Puedo sumar, restar, multiplicar y dividir;
        Usa `>sum <número 1> <número 2>` para sumar dos números, y así para >div , >mult , >resto, >resta
    3. **Saludar**: Usa `>saludo` y te devolveré un saludo!
    4. **info**: Usa '>info' y te devolvere informacion y hora del servidor.
    Si tienes alguna otra pregunta, no dudes en preguntar!
    """
    await ctx.send(ayuda_msg)




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


# peticiones a youtube.
@bot.command()
async def youtube(ctx, *, search):
    request = youtube_api.search().list(
        part="snippet",
        maxResults=5,
        q=search,
        type="video"  # Asegúrate de buscar solo videos
    )
    response = request.execute()

    if response['items']:
        options = []
        for i, item in enumerate(response['items']):
            if item['id']['kind'] == "youtube#video":  # Verifica que sea un video
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                options.append(f"{i + 1}: {title}")

        if not options:
            await ctx.send('No se encontraron videos para tu búsqueda.')
            return

        options_message = "\n".join(options)
        await ctx.send("Elije un video:\n" + options_message)

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 0 < int(m.content) <= len(options)

        try:
            choice = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send('No se recibió respuesta, cancelando operación.')
            return

        selected = int(choice.content) - 1
        video_id = response['items'][selected]['id']['videoId']
        await ctx.send('https://www.youtube.com/watch?v=' + video_id)
    else:
        await ctx.send('No se encontraron videos para tu búsqueda.')



bot.run(token)
