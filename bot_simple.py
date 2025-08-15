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
bot = commands.Bot(command_prefix=',', intents=intents)

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
        logger.info(f"Command detected: '{message.content}'")
    
    await bot.process_commands(message)

@bot.command(name='commands')
async def commands_help(ctx):
    """Show all available commands"""
    logger.info(f"Help command executed by {ctx.author}")
    
    embed = discord.Embed(
        title="🔥 Hail Mary AI Roast Bot Commands 🔥",
        description="The most savage AI-powered roast bot on Discord",
        color=0xFF4500  # Orange-red color
    )
    
    embed.add_field(
        name="🎯 Basic Roasting",
        value="`,roast` - Get AI-roasted yourself\n"
              "`,roast @user` - Roast someone specific\n"
              "`,roast username` - Roast by name",
        inline=False
    )
    
    embed.add_field(
        name="⚔️ Battle Commands",
        value="`,battle @user1 @user2` - AI judges a roast battle\n"
              "`,challenge @user` - Challenge someone to a roast-off\n"
              "`,random` - Get a random savage roast",
        inline=False
    )
    
    embed.add_field(
        name="🎲 Fun Commands",
        value="`,compliment @user` - Backhanded AI compliment\n"
              "`,rate @user` - Rate someone's roastability\n"
              "`,stats` - Your roasting statistics",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Utility",
        value="`,commands` - Show this menu\n"
              "`,test` - Check bot status",
        inline=False
    )
    
    embed.set_footer(text="Powered by dark AI humor | Use at your own risk")
    
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    """Simple test command"""
    logger.info(f"Test command executed by {ctx.author}")
    await ctx.send("🔥 Bot is working! Use `,commands` to see all commands!")

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

@bot.command()
async def battle(ctx, user1: discord.Member = None, user2: discord.Member = None):
    """AI judges a roast battle between two users"""
    logger.info(f"Battle command executed by {ctx.author}")
    
    if not user1 or not user2:
        await ctx.send("🔥 Usage: `,battle @user1 @user2` - Let AI judge who gets roasted harder!")
        return
    
    if user1 == user2:
        await ctx.send("🔥 You can't battle yourself... that's just sad.")
        return
    
    async with ctx.typing():
        # Generate battle roasts for both users
        roast1 = await get_ai_roast(user1.display_name)
        roast2 = await get_ai_roast(user2.display_name)
        
        # AI judges the winner
        import random as rnd
        winner = rnd.choice([user1, user2])
    
    embed = discord.Embed(title="⚔️ ROAST BATTLE RESULTS ⚔️", color=0xFF0000)
    embed.add_field(name=f"🔥 {user1.display_name}", value=roast1, inline=False)
    embed.add_field(name=f"🔥 {user2.display_name}", value=roast2, inline=False)
    embed.add_field(name="🏆 WINNER", value=f"{winner.mention} survives with less emotional damage!", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def challenge(ctx, target: discord.Member = None):
    """Challenge someone to a roast battle"""
    logger.info(f"Challenge command executed by {ctx.author}")
    
    if not target:
        await ctx.send("🔥 Usage: `,challenge @user` - Challenge someone to a roast-off!")
        return
    
    if target == ctx.author:
        await ctx.send("🔥 Challenging yourself? That's the most pathetic thing I've seen today.")
        return
    
    await ctx.send(f"🔥 {ctx.author.mention} has challenged {target.mention} to a roast battle! "
                   f"Will {target.display_name} accept this digital duel of destruction? "
                   f"Use `,battle {ctx.author.mention} {target.mention}` to settle this!")

@bot.command()
async def random(ctx):
    """Get a random savage roast"""
    logger.info(f"Random roast command executed by {ctx.author}")
    
    random_targets = ["humanity", "existence", "the universe", "Monday mornings", "your life choices"]
    import random as rnd
    target = rnd.choice(random_targets)
    
    async with ctx.typing():
        roast = await get_ai_roast(target)
    
    await ctx.send(f"🎲 Random roast: {roast}")

@bot.command()
async def compliment(ctx, target: discord.Member = None):
    """Give a backhanded AI compliment"""
    logger.info(f"Compliment command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        backhanded_compliments = [
            "You're not as bad as people say... you're worse.",
            "You have a face for radio... broken radio.",
            "You're special... in a medical sense.",
            "You're one in a million... unfortunately.",
            "You're proof that everyone has potential... to disappoint."
        ]
        import random as rnd
        compliment = rnd.choice(backhanded_compliments)
    else:
        try:
            async with ctx.typing():
                prompt = f"Create a brutally backhanded compliment for {target_name}. Make it sound nice at first but devastating by the end. Be clever and savage."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You create backhanded compliments that start nice but end devastatingly."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.9
                )
                compliment = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI compliment failed: {e}")
            compliment = "You're not as bad as people say... you're worse."
    
    await ctx.send(f"💐 {mention} {compliment}")

@bot.command()
async def rate(ctx, target: discord.Member = None):
    """Rate someone's roastability"""
    logger.info(f"Rate command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    # Generate random rating with personality
    import random as rnd
    rating = rnd.randint(1, 10)
    
    rating_descriptions = {
        1: "Barely worth the effort. Even my algorithms feel bad.",
        2: "Low-hanging fruit. Too easy, no sport in it.",
        3: "Mildly roastable. Like burnt toast - disappointing.",
        4: "Average target. Standard emotional damage potential.",
        5: "Decent roast material. Room for creativity.",
        6: "Good target. Multiple angles of attack available.",
        7: "High roastability. Rich material to work with.",
        8: "Premium roast candidate. Chef's choice material.",
        9: "Elite roasting territory. Maximum damage potential.",
        10: "Legendary roast target. The stuff of roasting dreams."
    }
    
    description = rating_descriptions[rating]
    
    embed = discord.Embed(title="📊 ROASTABILITY RATING", color=0xFF4500)
    embed.add_field(name="Target", value=mention, inline=True)
    embed.add_field(name="Rating", value=f"{rating}/10 🔥", inline=True)
    embed.add_field(name="Analysis", value=description, inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    """Show roasting statistics (placeholder for now)"""
    logger.info(f"Stats command executed by {ctx.author}")
    
    # Generate fun fake stats
    import random as rnd
    roasts_given = rnd.randint(50, 500)
    roasts_received = rnd.randint(10, 100)
    damage_dealt = rnd.randint(1000, 9999)
    
    embed = discord.Embed(title="📈 YOUR ROASTING STATISTICS", color=0x00FF00)
    embed.add_field(name="🔥 Roasts Witnessed", value=f"{roasts_given:,}", inline=True)
    embed.add_field(name="💀 Times Roasted", value=f"{roasts_received:,}", inline=True)
    embed.add_field(name="⚡ Emotional Damage", value=f"{damage_dealt:,} HP", inline=True)
    embed.add_field(name="🏆 Rank", value="Chaos Enjoyer", inline=True)
    embed.add_field(name="🎯 Accuracy", value=f"{rnd.randint(80, 99)}%", inline=True)
    embed.add_field(name="💎 Roast Quality", value="Unhinged", inline=True)
    
    embed.set_footer(text="Statistics are generated for entertainment purposes")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)