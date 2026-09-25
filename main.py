import discord 
from discord.ext import commands 
import random 
from pathlib import Path
import asyncio
 
# Variables 
 
TOKEN = "TOKEN"
intents = discord.Intents.default() 
intents.message_content = True  
bot = commands.Bot(command_prefix="/", intents=intents) 

CARPETA = Path(__file__).parent
 
# Comandos del bot 
 
@bot.event 
async def on_ready(): 
    print(f"{bot.user} iniciado sesión y listo para usar.") 
 
@bot.command() 
async def saludo(ctx): 
    await ctx.send("¡Hola! ¿Cómo estás?") 
 
#Comando Sumar 
@bot.command() 
async def sumar(ctx, num1:float=0, num2:float=0): 
    resultado = num1 + num2 
    await ctx.send(f"El resultado de {num1} + {num2} es {resultado}") 
 
# Numero aleatorio entre 1 y 100 
@bot.command()
async def numero_aleatorio(ctx, num1: int = 1, num2: int = 100):
    numero = random.randint(num1, num2)

    mensaje = await ctx.send(f"Tu numero aleatorio entre {num1} y {num2} esta siendo generado...")
    await asyncio.sleep(2)
    mensaje2 = await ctx.send("Tu numero aleatorio se ha generado correctamente...")
    await asyncio.sleep(1)
    if num1 != 67 and num2 != 67:
        await ctx.send(f"Tu número aleatorio entre {num1} y {num2} es: {numero}")
    await mensaje.delete()
    await mensaje2.delete()

    if num1 == 67 and num2 == 67:
        await ctx.send("# ¡Six Seven!")
        await ctx.send(file=discord.File(CARPETA / "67.jpg"))
        return

    dado_numero = random.randint(1, 6)

    if dado_numero == 1:
        await ctx.send(file=discord.File(CARPETA / "dado1.jpg"))
    elif dado_numero == 2:
        await ctx.send(file=discord.File(CARPETA / "dado2.jpg"))
    elif dado_numero == 3:
        await ctx.send(file=discord.File(CARPETA / "dado3.jpg"))
    elif dado_numero == 4:
        await ctx.send(file=discord.File(CARPETA / "dado4.jpg"))
    elif dado_numero == 5:
        await ctx.send(file=discord.File(CARPETA / "dado5.jpg"))
    elif dado_numero == 6:
        await ctx.send(file=discord.File(CARPETA / "dado6.jpg"))
        
@bot.command()
async def borrar_mensajes(ctx, cantidad:int=1):
    if cantidad < 1:
        await ctx.send("La cantidad de mensajes a borrar debe ser al menos 1.")
        return
    else:
        deleted = await ctx.channel.purge(limit=cantidad)
        await ctx.send(f"Se han borrado {len(deleted)} mensajes.", delete_after=5)

# Ejecución del bot 
 
print("Bot is starting...") 
 
bot.run(TOKEN)
