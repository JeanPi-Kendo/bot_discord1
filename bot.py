import discord
from settings import settings
from bot_logic import * # Importamos el módulo entero

# Configurar los privilegios del bot
intents = discord.Intents.default()
intents.message_content = True

# Crear el cliente
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('¡Hola! Soy Keinox, ¿en qué puedo ayudarte?')
    elif message.content.startswith('$smile'):
        await message.channel.send(gen_emoji())
    elif message.content.startswith('$coin'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('$pass'):
        await message.channel.send(crear_password(10))
    else:
        await message.channel.send("No puedo procesar este comando, ¡lo siento!")

# Ejecutar el bot
client.run(settings["TOKEN"])
