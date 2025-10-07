import discord
from discord.ext import commands
from settings import settings
import random

description = '''An example bot to showcase the discord.ext.commands extension module.'''

# Configurar los privilegios del bot

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='#', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def saludo(ctx, *, mensaje: str = None):
    """Saluda al usuario si el mensaje contiene la palabra 'hola'."""
    if mensaje is None:
        await ctx.send("Debes escribir un saludo, por ejemplo: `#saludo hola`")
        return

    if "hola" in mensaje.lower():
        await ctx.send(f'¡Hola, {ctx.author.name}! 👋')
    else:
        await ctx.send("Recuerda incluir la palabra **hola** en tu saludo 😅")

@bot.command()
async def add(ctx, left: str = None, right: str = None):
    """Suma dos números."""
    if left is None or right is None:
        await ctx.send("⚠️ Debes escribir dos números, por ejemplo: `#add 5 7`")
        return

    try:
        left = int(left)
        right = int(right)
        await ctx.send(f"La suma es: {left + right}")
    except ValueError:
        await ctx.send("⚠️ Debes escribir solo números válidos, por ejemplo: `#add 5 7`")

@bot.command()
async def ocho(ctx, *, pregunta: str = None):
    """Responde preguntas como una bola mágica."""
    respuestas = [
        "Sí", "No", "Tal vez", "Pregunta más tarde",
        "Definitivamente sí", "Definitivamente no", "No estoy seguro 🤔"
    ]

    # Caso 1: no escribió nada
    if pregunta is None:
        await ctx.send("Debes hacerme una pregunta, por ejemplo: `#ocho ¿Voy a ganar?`")
        return

    # Caso 2: pregunta muy corta
    if len(pregunta.split()) <= 2:
        await ctx.send("Tu pregunta es muy corta 😅, hazla más larga para poder entender lo que quieres decir")
        return

    # Caso 3: no termina con signo de pregunta
    if not pregunta.strip().endswith("?"):
        await ctx.send("Parece que olvidaste el signo de pregunta ❓ al final.")
        return

    # Respuesta aleatoria
    await ctx.send(f'🎱 {random.choice(respuestas)}')

@bot.command()
async def roll(ctx, dice: str = None):
    """Tira un dado en formato NdN."""
    if dice is None:
        await ctx.send("🎲 Debes darme un formato NdN, por ejemplo: `#roll 2d6`")
        return
    
    try:
        rolls, limit = map(int, dice.split('d'))
    except (ValueError, TypeError):
        await ctx.send('⚠️ El formato tiene que ser NdN, por ejemplo: `#roll 4d7')
        return
    
    if rolls <= 0 or limit <= 0:
        await ctx.send("🚫 Los números deben ser mayores que cero.")
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(f"🎯 Resultados: **{result}**")


@bot.command(description="Escoge entre varias opciones.")
async def choose(ctx, *choices: str):
    """Escoge entre varias opciones."""
    # Caso 1: no hay opciones
    if not choices:
        await ctx.send("❗ Debes darme opciones para elegir. Ejemplo: `#choose pizza hamburguesa pasta`")
        return

    # Caso 2: solo una opción
    if len(choices) == 1:
        await ctx.send(f"🤔 Solo me diste una opción: **{choices[0]}**. ¡Dame al menos dos para elegir!")
        return

    # Caso 3: elegir una al azar
    eleccion = random.choice(choices)
    await ctx.send(f"🎯 Elijo: **{eleccion}**")


@bot.command()
async def repeat(ctx, times: str = None, *, content: str = None):
    """Repite un mensaje varias veces."""
    # Validación: si falta algo
    if times is None or content is None:
        await ctx.send("❗ Debes escribir un número y un mensaje. Ejemplo: `#repeat 3 Hola!`")
        return

    # Verificar que el número sea válido
    if not times.isdigit():
        await ctx.send("⚠️ El primer argumento debe ser un número. Ejemplo: `#repeat 3 Hola!`")
        return

    times = int(times)

    # Validar el rango del número
    if times <= 0:
        await ctx.send("⚠️ El número de repeticiones debe ser mayor que cero.")
        return
    if times > 30:
        await ctx.send("⚠️ Ese número es demasiado alto. Intenta con un valor menor o igual a 30.")
        return

    # Repetir el mensaje
    for _ in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member = None):
    """Muestra cuándo un usuario se unió al servidor."""
    # Si no mencionan a nadie, usar al autor del comando
    if member is None:
        member = ctx.author

    # Formatear la fecha de ingreso
    fecha = discord.utils.format_dt(member.joined_at, style='F')
    await ctx.send(f"📅 **{member.name}** se unió al servidor el {fecha}.")

bot.run(settings["TOKEN"])
