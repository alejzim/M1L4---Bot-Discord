import discord
from discord.ext import commands
from discord import app_commands
import random
from pathlib import Path
import asyncio

# =========================
# VARIABLES
# =========================

TOKEN = "TOKEN"
GUILD_ID = ID_SERVIDOR # Remplazar por el ID de tu servidor

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="$",
    intents=intents
)

CARPETA = Path(__file__).parent


# =========================
# INICIO DEL BOT
# =========================

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        print(f"{bot.user} inició sesión y está listo.")
        print(f"✅ {len(synced)} comandos sincronizados.")

        for comando in synced:
            print(f" - /{comando.name}")

    except Exception as error:
        print(f"❌ Error sincronizando comandos: {error}")


# =========================
# /SALUDO
# =========================

@bot.tree.command(
    name="saludo",
    description="El bot te saluda."
)
async def saludo(interaction: discord.Interaction):

    await interaction.response.send_message(
        "¡Hola! ¿Cómo estás?"
    )


# =========================
# /SUMAR
# =========================

@bot.tree.command(
    name="sumar",
    description="Suma dos números."
)
@app_commands.describe(
    num1="Primer número",
    num2="Segundo número"
)
async def sumar(
    interaction: discord.Interaction,
    num1: float,
    num2: float
):

    resultado = num1 + num2

    await interaction.response.send_message(
        f"El resultado de {num1} + {num2} es **{resultado}**"
    )


# =========================
# /NUMERO_ALEATORIO
# =========================

@bot.tree.command(
    name="numero_aleatorio",
    description="Genera un número aleatorio."
)
@app_commands.describe(
    num1="Número mínimo",
    num2="Número máximo"
)
async def numero_aleatorio(
    interaction: discord.Interaction,
    num1: int = 1,
    num2: int = 100
):

    if num1 > num2:
        await interaction.response.send_message(
            "❌ El número mínimo no puede ser mayor que el máximo.",
            ephemeral=True
        )
        return

    # Easter egg 67
    if num1 == 67 and num2 == 67:

        await interaction.response.send_message(
            "# ¡Six Seven!"
        )

        imagen = CARPETA / "67.jpg"

        if imagen.exists():
            await interaction.followup.send(
                file=discord.File(imagen)
            )
        else:
            await interaction.followup.send(
                "❌ No encontré el archivo `67.jpg`."
            )

        return

    numero = random.randint(num1, num2)

    await interaction.response.send_message(
        f"🎲 Tu número aleatorio entre **{num1}** y **{num2}** "
        f"está siendo generado..."
    )

    await asyncio.sleep(2)

    mensaje2 = await interaction.followup.send(
        "✅ Tu número aleatorio se ha generado correctamente...",
        wait=True
    )

    await asyncio.sleep(1)

    await interaction.followup.send(
        f"🎯 Tu número aleatorio entre **{num1}** y **{num2}** es: **{numero}**"
    )

    await mensaje2.delete()

    # Dado aleatorio
    dado_numero = random.randint(1, 6)

    archivo_dado = CARPETA / f"dado{dado_numero}.jpg"

    if archivo_dado.exists():

        await interaction.followup.send(
            content=f"🎲 Dado: **{dado_numero}**",
            file=discord.File(archivo_dado)
        )

    else:

        await interaction.followup.send(
            f"🎲 Dado: **{dado_numero}**\n"
            f"⚠️ No encontré `dado{dado_numero}.jpg`."
        )


# =========================
# /BORRAR_MENSAJES
# =========================

@bot.tree.command(
    name="borrar_mensajes",
    description="Borra mensajes del canal."
)
@app_commands.describe(
    cantidad="Cantidad de mensajes que querés borrar"
)
@app_commands.checks.has_permissions(manage_messages=True)
async def borrar_mensajes(
    interaction: discord.Interaction,
    cantidad: int = 1
):

    if cantidad < 1:

        await interaction.response.send_message(
            "❌ La cantidad debe ser al menos 1.",
            ephemeral=True
        )

        return

    if cantidad > 100:

        await interaction.response.send_message(
            "❌ Solo podés borrar hasta 100 mensajes de una vez.",
            ephemeral=True
        )

        return

    await interaction.response.defer(
        ephemeral=True
    )

    deleted = await interaction.channel.purge(
        limit=cantidad
    )

    await interaction.followup.send(
        f"🗑️ Se borraron **{len(deleted)} mensajes**.",
        ephemeral=True
    )


# Error de /borrar_mensajes
@borrar_mensajes.error
async def borrar_mensajes_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    if isinstance(error, app_commands.MissingPermissions):

        await interaction.response.send_message(
            "❌ No tenés permisos para borrar mensajes.",
            ephemeral=True
        )

    else:

        print(f"Error en /borrar_mensajes: {error}")

        if not interaction.response.is_done():

            await interaction.response.send_message(
                "❌ Ocurrió un error intentando borrar los mensajes.",
                ephemeral=True
            )


# =========================
# /SPAM
# =========================

@bot.tree.command(
    name="spam",
    description="Envía varias veces un mensaje."
)
@app_commands.describe(
    cantidad="Cantidad de mensajes (máximo 10)",
    mensaje="Mensaje que querés enviar"
)
async def spam(
    interaction: discord.Interaction,
    cantidad: int,
    mensaje: str
):

    # Validar cantidad
    if cantidad < 1 or cantidad > 67:

        await interaction.response.send_message(
            "⚠️ La cantidad debe estar entre **1 y 67**.",
            ephemeral=True
        )

        return

    # Validar mensaje vacío
    if not mensaje.strip():

        await interaction.response.send_message(
            "❌ El mensaje no puede estar vacío.",
            ephemeral=True
        )

        return

    # Validar largo
    if len(mensaje) > 2000:

        await interaction.response.send_message(
            "❌ El mensaje no puede tener más de **2000 caracteres**.",
            ephemeral=True
        )

        return

    # Confirmación privada
    await interaction.response.send_message(
        f"✅ Enviando **{cantidad} mensajes**...",
        ephemeral=True
    )

    try:

        for _ in range(cantidad):

            await interaction.channel.send(mensaje)

            await asyncio.sleep(0.8)

    except discord.Forbidden:

        await interaction.followup.send(
            "❌ No tengo permisos para enviar mensajes en este canal.",
            ephemeral=True
        )

    except discord.HTTPException as error:

        await interaction.followup.send(
            "❌ Discord produjo un error mientras intentaba enviar los mensajes.",
            ephemeral=True
        )

        print(f"Error HTTP en /spam: {error}")

    except Exception as error:

        await interaction.followup.send(
            "❌ Ocurrió un error inesperado en `/spam`.",
            ephemeral=True
        )

        print(f"Error inesperado en /spam: {error}")


# =========================
# ERROR GLOBAL
# =========================

@bot.tree.error
async def error_global(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    print(f"Error de comando: {error}")

    # Evita responder dos veces si el comando ya manejó el error
    if interaction.response.is_done():
        return

    await interaction.response.send_message(
        "❌ Ocurrió un error ejecutando el comando.",
        ephemeral=True
    )


# =========================
# EJECUCIÓN
# =========================

print("Bot is starting...")

bot.run(TOKEN)
