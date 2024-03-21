##Project by Michael Yang
#This is a stable diffusion bot that utilises comfyUI and stable diffusion model xl.

import asyncio
import os
from dotenv import load_dotenv
import discord
import StableDiffusion
import queue
from discord.ext import commands

load_dotenv()
serverid = os.getenv('SERVER_ID')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',intents = intents)
prompt_ = ""
IN_USE = False

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.tree.sync()

def setEmbed(title, description, field1Name="", field1Value=""):
    embed = discord.Embed(title=title, description=description)
    if field1Name != "" and field1Value != "":
        embed.add_field(name=field1Name, value=field1Value)
    return embed

class styleMenu(discord.ui.View):
    @discord.ui.select(placeholder="Pick a style", options=
    [discord.SelectOption(label="Anime", value="sai-anime"),
     discord.SelectOption(label="Hyperrealism", value="artstyle-hyperrealism"),
     discord.SelectOption(label="Cyberpunk", value="game-cyberpunk game"),
     discord.SelectOption(label="Pixel art", value="sai-pixel art"),
     discord.SelectOption(label="Low Poly", value="sai-lowpoly"),
     discord.SelectOption(label="Graffiti", value="artstyle-graffiti"),
     discord.SelectOption(label="Minecraft", value="game-minecraft"),
     discord.SelectOption(label="Manga", value="misc-manga"),
     discord.SelectOption(label="Cinematic", value="sai-cinematic"),
     discord.SelectOption(label="Origami", value="sai-origami"),
     discord.SelectOption(label="Kawaii", value="misc-kawaii"),
     discord.SelectOption(label="Horror", value="misc-horror")
     ])

    async def select_style(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        global imageRequestsQueue
        global prompt_
        global IS_GENERATING
        style = select_item.values[0]
        styles = {"sai-anime": "Anime",
                  "artstyle-hyperrealism": "Hyperrealism",
                  "game-cyberpunk game": "Cyberpunk",
                  "artstyle-graffiti": "Graffiti",
                  "sai-pixel art": "Pixel art",
                  "sai-lowpoly": "Low Poly",
                  "game-minecraft": "Minecraft",
                  "misc-manga": "Manga",
                  "sai-cinematic": "Cinematic",
                  "sai-origami": "Origami",
                  "misc-kawaii": "Kawaii",
                  "misc-horror": "Horror"
                  }
        if (imageRequestsQueue.qsize() == 0):
            QUEUE_IS_EMPTY = True
        imageRequestsQueue.put(style+"~~"+prompt_)
        await interaction.response.defer()
        orig_msg = await interaction.original_response()
        await orig_msg.edit(content="Your request has been added to the queue.", view=None)
        if(QUEUE_IS_EMPTY == True and IS_GENERATING == False):
            IS_GENERATING = True
            while(imageRequestsQueue.qsize()>=1):
                promptFromQ = imageRequestsQueue.get()
                curStyle = getStyle(promptFromQ)
                image_Prompt = promptFromQ[len(curStyle)+2:]
                await interaction.followup.send("Now generating "+ image_Prompt)
                try:
                    image = await StableDiffusion.generate_image(prompt_=image_Prompt, style_=curStyle)
                    await interaction.followup.send(
                        content=f"[**ARTSTYLE**: **{styles.get(curStyle)}**] {interaction.user.name} generated: **{image_Prompt}**",
                        file=discord.File(image))
                except:
                    await interaction.followup.send("An error has occurred, most likely the stable diffusion model is not on.")
        IS_GENERATING = False


@bot.tree.command(name="genimage", description="Generate an image")
async def func(interaction: discord.Interaction, prompt: str):
    global prompt_
    global IN_USE
    if(not IN_USE):
        IN_USE = True
        prompt_ = prompt
        await interaction.response.send_message(view=styleMenu())
    else:
        await interaction.response.send_message("The bot is busy right now, please wait.")


bot.run(os.getenv("TOKEN"))
