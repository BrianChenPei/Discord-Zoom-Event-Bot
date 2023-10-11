import discord
from discord.ext import commands, tasks
import requests
import datetime
import openai

TOKEN = "ADD_TOKEN_HERE"
ZOOM_TOKEN = "ADD_TOKEN_HERE"
intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True # If you ticked the SERVER MEMBERS INTENT

bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def create_event(ctx, title: str, time: str, repetition: str = None):
    # Generate Zoom link
    zoom_link = create_zoom_link()
    
    # Create event
    event_time = datetime.datetime.strptime(time, '%H:%M').time()
    event_description = f"Title: {title}\nTime: {event_time}\nZoom Link: {zoom_link}\nRepetition: {repetition if repetition else 'No Repetition'}"
    
    await ctx.send(f"Event Created!\n{event_description}")

def create_zoom_link():
    # Use Zoom API to create a new meeting and return the join URL
    headers = {
        "Authorization": f"Bearer {ZOOM_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "topic": "Discord Event Meeting",
        "type": 2
    }

    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["join_url"]
    else:
        return "Zoom link generation failed."

bot.run(TOKEN)
