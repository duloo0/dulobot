# Import necessary libraries
import discord
import requests
import os
from discord.ext import commands

# Discord bot setup
message_counter = {}  # Stores message counts per channel
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load your Infermatic API key from environment variables
INFERMATIC_API_KEY = os.getenv("INFERMATIC_API_KEY")
INFERMATIC_API_URL = "https://api.totalgpt.ai/v1/chat/completions"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Respond only every 3 messages
    if message.channel.id not in message_counter:
        message_counter[message.channel.id] = 0

    message_counter[message.channel.id] += 1

    if message_counter[message.channel.id] % 3 != 0:
        await bot.process_commands(message)
        return
    if message.author == bot.user:
        return

    if not INFERMATIC_API_KEY:
        await message.channel.send("Infermatic API key is not set. Please check your environment variables.")
        return

    try:
        # Making the request to Infermatic API
        headers = {
            "Authorization": f"Bearer {INFERMATIC_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "Midnight-Miqu-70B-v1.5",
            "messages": [
                {
                    "role": "user",
                    "content": f"Dulo Bot is an AI chatbot created by Dulo, currently in the Discord server 'Brick Factory'. Dulo Bot responds directly and honestly, using humor and some profanity if appropriate. Dulo Bot is not overly enthusiastic and should act pretty chill. The user's message is: {message.content}"
                }
            ],
            "max_tokens": 150,
            "temperature": 0.9
        }
        response = requests.post(INFERMATIC_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Get the AI response from Infermatic API
        ai_response = response.json().get("choices")[0].get("message", {}).get("content")

        # Send response back to Discord
        if ai_response:
            await message.reply(ai_response)
        else:
            await message.reply("I'm sorry, I couldn't understand that.")

    except requests.exceptions.RequestException as e:
        await message.reply(f"Error: {str(e)}")

    await bot.process_commands(message)

@bot.command()
async def models(ctx):
    if not INFERMATIC_API_KEY:
        await ctx.send("Infermatic API key is not set. Please check your environment variables.")
        return

    try:
        # Making the request to Infermatic API to get available models
        headers = {
            "Authorization": f"Bearer {INFERMATIC_API_KEY}",
            "Content-Type": "application/json"
        }
        models_url = "https://api.totalgpt.ai/v1/models"
        response = requests.get(models_url, headers=headers)
        response.raise_for_status()

        # Get the list of models
        models_list = response.json().get("data")
        if models_list:
            models_names = [model.get("id") for model in models_list]
            await ctx.send(f"Available models: {', '.join(models_names)}")
        else:
            await ctx.send("No models found.")

    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching models: {str(e)}")

# Running the bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("Discord token is not set. Please check your environment variables.")