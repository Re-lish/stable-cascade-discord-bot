##Project by Michael Yang
#This is a stable diffusion bot that utilises comfyUI and stable diffusion model xl.
##
import asyncio
import os
from dotenv import load_dotenv
import discord
import StableDiffusion
from discord.ext import commands


load_dotenv()
serverid = os.getenv('SERVER_ID')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',intents = intents)

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.tree.sync()

def setEmbed(title, description, field1Name="", field1Value=""):
    embed = discord.Embed(title=title, description=description)
    if field1Name != "" and field1Value != "":
        embed.add_field(name=field1Name, value=field1Value)
    return embed

current_song = ""



@bot.tree.command(name="genimage", description="Generate an image")
async def func(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        image = await StableDiffusion.genImg(prompt_=prompt)
        await interaction.followup.send(
            content=f"{interaction.user.name} generated: **{prompt}**",
            file=discord.File(image))
        os.remove("output.png")
    except:
        await interaction.followup.send("An error has occurred, most likely the stable diffusion model is not on.")


bot.run(os.getenv("TOKEN"))