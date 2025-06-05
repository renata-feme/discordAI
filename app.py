import discord, os, clases
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("dt")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$",intents=intents)

@bot.event
async def on_ready():
    print(f"Hemos iniciado sesión como {bot.user}")


@bot.command(name="predict")
async def classify(ctx):
    if ctx.message.attachments:
        for ath in ctx.message.attachments:
            fileName = f"./{ath.filename}"
            fileURL = ath.url
            class_name, confidence_score = clases.getClass("keras_model.h5", ath.filename, "labels.txt")
            percentage = confidence_score * 100
            await ath.save(f"./{ath.filename}")
            embed = discord.Embed(
                title = "RESULTADOS", 
                description= f"**Clase predicha: **{class_name} \n **Confianza: ** {percentage:.2f}%",
                color= 0x27548A
            )
            embed.set_footer(text="Analizado con Tensroflow.")
            embed.set_author(name="Ren :)")
            embed.set_thumbnail(url=fileURL)
            embed.add_field(name="Si la predicción no fue exacta, pues lo siento.",value="😅", inline=True)
            embed.set_image(url="https://i.postimg.cc/59wXfSPt/snoopy.webp")

            await ctx.send(embed = embed)
    else:
        await ctx.send("Olvidaste el archivo, lol")



bot.run(token)