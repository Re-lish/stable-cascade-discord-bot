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
    
def getStyle(prompt):
    curStyle = ""
    for i in range(len(prompt)):
        curStyle += prompt[i]
        if (prompt[i + 1] == "~" and prompt[i + 2] == "~"):
            return curStyle

def getUserName(prompt):
    name = ""
    index = 0
    for i in range(len(prompt)):
        if(prompt[i+1] == ";" and prompt[i+2] == ";"):
            index = i+3
            break
    for i in range(index, len(prompt)):
        name += prompt[i]
    return name
    
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
        global QUEUE_IS_EMPTY
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
        imageRequestsQueue.put(style+"~~"+prompt_+";;"+interaction.user.name)
        await interaction.response.defer()
        orig_msg = await interaction.original_response()
        await orig_msg.edit(content="Your request has been added to the queue.", view=None)
        if(QUEUE_IS_EMPTY == True and IS_GENERATING == False):
            IS_GENERATING = True
            while(imageRequestsQueue.qsize()>=1):
                promptFromQ = imageRequestsQueue.queue[0]
                curStyle = getStyle(promptFromQ)
                userName = getUserName(promptFromQ)
                image_Prompt = promptFromQ[len(curStyle)+2:len(promptFromQ)-len(userName)-2]
                await interaction.followup.send("Now generating "+ image_Prompt)
                try:
                    image = await StableDiffusion.generate_image(prompt_=image_Prompt, style_=curStyle)
                    await interaction.followup.send(
                        content=f"[**ARTSTYLE**: **{styles.get(curStyle)}**] {userName} generated: **{image_Prompt}**",
                        file=discord.File(image))
                    imageRequestsQueue.get()
                except:
                    await interaction.followup.send("An error has occurred, most likely the stable diffusion model is not on.")
        IS_GENERATING = False

@tree.command(name="viewqueue", description="Shows the current queue",guild=discord.Object(id=serverid))
async def showQueue(interaction: discord.Interaction):
    global imageRequestsQueue
    s = ""
    if imageRequestsQueue.qsize()==0:
        await interaction.response.send_message("The queue is empty.")
    else:
        for i in range(imageRequestsQueue.qsize()):
            prompt = imageRequestsQueue.queue[i]
            userName = getUserName(prompt)
            style = getStyle(prompt)
            prompt = prompt[len(style)+2:len(prompt)-len(userName)-2]
            s+=f"{i+1}. {prompt}. By **{userName}** in **{style}** style\n"
        await interaction.response.send_message(embed=setEmbed("Current queue", "View the current queue of image generation requests", field1Name="List",field1Value=s))
        
@bot.tree.command(name="genimage", description="Generate an image")
async def func(interaction: discord.Interaction, prompt: str):
    global prompt_
    if(imageRequestsQueue.qsize() < 10):
        prompt_ = prompt
        await interaction.response.send_message(view=styleMenu())
    else:
        await interaction.response.send_message("The queue is full, please wait.")


bot.run(os.getenv("TOKEN"))
