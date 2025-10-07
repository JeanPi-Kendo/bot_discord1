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
    """Saluda al usuario si escribe 'hola'."""
    if mensaje is None:
        await ctx.send("Debes escribir un saludo, por ejemplo: `#saludo hola`")
        return

    if mensaje.lower() == "hola":
        await ctx.send(f'¡Hola, {ctx.author.name}! 👋')
    else:
        await ctx.send("Recuerda saludar escribiendo **hola** 😅")

@bot.command()
async def add(ctx, left, right):
    """Suma dos números."""
    try:
        left = int(left)
        right = int(right)
        await ctx.send(f"La suma es: {left + right}")
    except ValueError:
        await ctx.send("⚠️ Debes escribir solo números, por ejemplo: `#add 5 7`")

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
    if len(pregunta.split()) < 2:
        await ctx.send("Tu pregunta es muy corta 😅, intenta algo más completo como: `#ocho ¿Voy a aprobar el examen?`")
        return

    # Caso 3: no termina con signo de pregunta
    if not pregunta.strip().endswith("?"):
        await ctx.send("Parece que olvidaste el signo de pregunta ❓ Intenta así: `#ocho ¿Me irá bien?`, o algo parecido.")
        return

    # Respuesta aleatoria
    await ctx.send(f'🎱 {random.choice(respuestas)}')

@bot.command()
async def roll(ctx, dice: str):
    """Tira un dado en formato NdN."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except (ValueError, TypeError):
        await ctx.send('Formato tiene que ser NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


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
async def repeat(ctx, times: int, *, content: str = None):
    """Repite un mensaje varias veces."""
    # Validación: si el usuario no escribe texto
    if content is None:
        await ctx.send("❗Debes escribir un mensaje para repetir. Ejemplo: `#repeat 3 Hola!`")
        return

    # Validación: si el número es menor o igual a 0
    if times <= 0:
        await ctx.send("⚠️ El número de repeticiones debe ser mayor que cero.")
        return

    # Envía el mensaje las veces indicadas
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Avisa cuando un usuario se unió."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

bot.run(settings["TOKEN"])
