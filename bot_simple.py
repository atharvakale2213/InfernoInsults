import discord
from discord.ext import commands
import random
import os
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize AI client (OpenRouter or OpenAI)
ai_client = None
openrouter_key = os.getenv('OPENROUTER_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

if openrouter_key:
    # Use OpenRouter with custom base URL
    ai_client = OpenAI(
        api_key=openrouter_key,
        base_url="https://openrouter.ai/api/v1"
    )
    logger.info("OpenRouter client initialized for AI-powered roasts")
elif openai_key:
    # Fallback to direct OpenAI
    ai_client = OpenAI(api_key=openai_key)
    logger.info("OpenAI client initialized for AI-powered roasts")
else:
    logger.warning("No AI API key found - using fallback roasts")

# Fallback roasts (used if AI fails)
fallback_roasts = [
    "{target}, your existence is so meaningless that even the void feels sorry for you.",
    "{target}, I've seen more personality in a funeral home brochure.",
    "{target}, you're what happens when mediocrity gets tired of trying.",
    "{target}, your life is like a broken calculator - even the errors don't add up.",
    "{target}, if disappointment was an art form, you'd be the Mona Lisa.",
    "{target}, you're proof that natural selection sometimes takes a coffee break.",
    "{target}, calling you pathetic would be an upgrade from your current status.",
    "{target}, your brain operates on the same frequency as elevator music - barely there and deeply annoying.",
    "{target}, you're like a participation trophy that even pity won't claim.",
    "{target}, existence itself cringes when you enter a room."
]

async def get_ai_roast(target_name):
    """Get a dark, unhinged AI-generated roast"""
    if not ai_client:
        # Use fallback if no AI
        roast_template = random.choice(fallback_roasts)
        return roast_template.format(target=target_name)
    
    try:
        # Ultra-dark, unhinged roast prompt
        prompt = f"""Create an absolutely savage, dark humor roast for someone named '{target_name}'. 
        
Make it:
- Brutally unhinged and creative
- Dark psychological humor
- Devastatingly clever wordplay
- Absurdly specific and weird
- Maximum emotional damage
- Absolutely ruthless

Rules: No slurs, no threats, no real-world tragedies. Just pure psychological warfare through humor.
Be completely unhinged but clever. Make it so brutal that even the AI feels bad for generating it.

Target: {target_name}"""
        
        # Choose model based on provider
        model = "gpt-4o"  # Works for both OpenRouter and OpenAI
        if os.getenv('OPENROUTER_API_KEY'):
            # OpenRouter supports many models - using GPT-4o for consistency
            model = "openai/gpt-4o"
        
        response = ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a savage roast comedian with no filter. Generate the most brutal, unhinged roasts possible while staying clever and avoiding actual harm."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.95  # Maximum creativity for unhinged responses
        )
        
        roast = response.choices[0].message.content.strip()
        logger.info(f"Generated AI roast for {target_name}")
        return roast
        
    except Exception as e:
        logger.warning(f"AI roast failed: {e}, using fallback")
        roast_template = random.choice(fallback_roasts)
        return roast_template.format(target=target_name)

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
    """Dark, unhinged AI-powered roast command"""
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
    
    # Show typing indicator for dramatic effect
    async with ctx.typing():
        # Get AI-powered dark roast
        roast_text = await get_ai_roast(target_name)
    
    # Send response
    if mention_tag and target:
        response = f"🔥 {mention_tag} {roast_text}"
    else:
        response = f"🔥 {roast_text}"
    
    await ctx.send(response)
    logger.info(f"Dark AI roast sent to {target_name}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)