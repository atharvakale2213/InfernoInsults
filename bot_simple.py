import discord
from discord.ext import commands
import random
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Built-in savage roasts
roasts = [
    "{target}, your existence is so bland that even vanilla ice cream calls you basic.",
    "{target}, I've seen more personality in a Windows error message.",
    "{target}, you're the human equivalent of a participation trophy - technically there, but nobody's impressed.",
    "{target}, your life is like a broken pencil - completely pointless.",
    "{target}, if stupidity was a superpower, you'd be the entire Justice League.",
    "{target}, you're proof that even God makes rough drafts.",
    "{target}, I'd call you a tool, but that would be insulting to useful objects.",
    "{target}, your brain must be made of the same material as a black hole - nothing gets out.",
    "{target}, you're like a software update - nobody wants you, but you show up anyway.",
    "{target}, calling you a clown would be unfair to professional entertainers."
]

@bot.event
async def on_ready():
    logger.info(f'Bot logged in as {bot.user}')
    print("🔥 Hail Mary AI Roast Bot is online and ready to burn egos 🔥")
    print(f"Bot is in {len(bot.guilds)} servers")
    print(f"Command prefix: '{bot.command_prefix}'")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    logger.info(f"Received message: '{message.content}' from {message.author}")
    
    if message.content.startswith('!'):
        logger.info(f"Command detected: '{message.content}'")
    
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    """Simple test command"""
    logger.info(f"Test command executed by {ctx.author}")
    await ctx.send("🔥 Bot is working! Use `!roast` to get roasted!")

@bot.command()
async def roast(ctx, *, target=None):
    """Roast command"""
    logger.info(f"Roast command executed by {ctx.author}, target: {target}")
    
    # Determine target
    if target:
        if ctx.message.mentions:
            target_name = ctx.message.mentions[0].display_name
            mention_tag = ctx.message.mentions[0].mention
        else:
            target_name = target
            mention_tag = None
    else:
        target_name = ctx.author.display_name
        mention_tag = ctx.author.mention
    
    # Get random roast
    roast_template = random.choice(roasts)
    roast_text = roast_template.format(target=target_name)
    
    # Send response
    if mention_tag and target:
        response = f"🔥 {mention_tag} {roast_text}"
    else:
        response = f"🔥 {roast_text}"
    
    await ctx.send(response)
    logger.info(f"Roast sent to {target_name}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)