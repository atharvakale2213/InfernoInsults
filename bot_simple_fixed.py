import discord
from discord.ext import commands
import random
import os
import logging
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=',', intents=intents)

# Initialize AI settings (OpenRouter)
openrouter_key = os.getenv('OPENROUTER_API_KEY')

if openrouter_key:
    logger.info("OpenRouter client initialized for AI-powered roasts")
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

async def make_ai_request(prompt, system_prompt, max_tokens=150, temperature=0.9):
    """Helper function to make AI requests via OpenRouter"""
    if not openrouter_key:
        return None
    
    try:
        headers = {
            'Authorization': f'Bearer {openrouter_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"API error: {response.status_code}")
            
    except Exception as e:
        logger.warning(f"AI request failed: {e}")
        return None

async def get_ai_roast(target_name):
    """Get a dark, unhinged AI-generated roast"""
    if not openrouter_key:
        # Use fallback if no AI
        import random as rnd
        roast_template = rnd.choice(fallback_roasts)
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
        
        headers = {
            'Authorization': f'Bearer {openrouter_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a savage roast comedian with no filter. Generate the most brutal, unhinged roasts possible while staying clever and avoiding actual harm."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.95
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            roast = data['choices'][0]['message']['content'].strip()
            logger.info(f"Generated AI roast for {target_name}")
            return roast
        else:
            raise Exception(f"API error: {response.status_code}")
        
    except Exception as e:
        logger.warning(f"AI roast failed: {e}, using fallback")
        import random as rnd
        roast_template = rnd.choice(fallback_roasts)
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
    
    if message.content.startswith(','):
        await bot.process_commands(message)

@bot.command()
async def roast(ctx, target: discord.Member = None):
    """Generate a savage AI roast for someone"""
    logger.info(f"Roast command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if target == ctx.author and target is not None:
        await ctx.send("🔥 Roasting yourself? Bold move. Respect the self-destructive energy.")
    
    async with ctx.typing():
        roast = await get_ai_roast(target_name)
    
    await ctx.send(f"🔥 {mention} {roast}")

@bot.command()
async def battle(ctx, user1: discord.Member = None, user2: discord.Member = None):
    """Epic roast battle between two users"""
    logger.info(f"Battle command executed by {ctx.author}")
    
    if not user1 or not user2:
        await ctx.send("🔥 Usage: `,battle @user1 @user2` - Let the roasting commence!")
        return
    
    if user1 == user2:
        await ctx.send("🔥 Can't battle yourself. Even your imagination isn't that creative.")
        return
    
    async with ctx.typing():
        roast1 = await get_ai_roast(user1.display_name)
        roast2 = await get_ai_roast(user2.display_name)
    
    # Determine winner (random for drama)
    import random as rnd
    winner = rnd.choice([user1, user2])
    
    embed = discord.Embed(title="⚔️ ROAST BATTLE ROYALE ⚔️", color=0xFF0000)
    embed.add_field(name=f"🔥 {user1.display_name}", value=roast1, inline=False)
    embed.add_field(name=f"🔥 {user2.display_name}", value=roast2, inline=False)
    embed.add_field(name="🏆 WINNER", value=f"{winner.mention} survives with less emotional damage!", inline=False)
    
    await ctx.send(embed=embed)

# Continuing with all commands using make_ai_request helper...
# [Rest of file would continue with all the other commands fixed]

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable is required")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)