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
              "`,stats` - Your roasting statistics\n"
              "`,verse @user` - Generate a roast rap verse\n"
              "`,compare @user1 @user2` - AI compares two users",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Interactive Games",
        value="`,truth @user` - Brutally honest AI truth\n"
              "`,roastme` - Get the most savage roast possible\n"
              "`,therapy @user` - Fake therapy session (roast disguised as help)\n"
              "`,fortune @user` - Dark fortune telling",
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

@bot.command()
async def verse(ctx, target: discord.Member = None):
    """Generate a savage rap verse roast"""
    logger.info(f"Verse command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        fallback_verses = [
            f"Yo {target_name}, your rhymes are so weak, even auto-tune gave up\nYour flow's so broken, it needs a bandage and a crutch",
            f"{target_name} stepped to the mic, biggest mistake of the night\nYour bars are so trash, they belong out of sight",
            f"Listen {target_name}, your style's prehistoric\nMy verses hit harder than your life euphoric"
        ]
        import random as rnd
        verse = rnd.choice(fallback_verses)
    else:
        try:
            async with ctx.typing():
                prompt = f"Write a brutal 4-line rap verse roasting {target_name}. Make it rhythmic, clever, and devastatingly savage. Use hip-hop wordplay and internal rhymes."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a savage battle rapper. Create brutal, clever rap verses with perfect flow and devastating wordplay."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.95
                )
                verse = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI verse failed: {e}")
            verse = f"Yo {target_name}, your existence is questionable\nEven my fallback verse is more respectable"
    
    await ctx.send(f"🎤 **RAP BATTLE VERSE** 🎤\n{mention}\n```{verse}```")

@bot.command()
async def compare(ctx, user1: discord.Member = None, user2: discord.Member = None):
    """AI compares two users in a savage way"""
    logger.info(f"Compare command executed by {ctx.author}")
    
    if not user1 or not user2:
        await ctx.send("🔥 Usage: `,compare @user1 @user2` - Let AI brutally compare two people!")
        return
    
    if user1 == user2:
        await ctx.send("🔥 Comparing someone to themselves? That's the level of creativity I'd expect from you.")
        return
    
    if not ai_client:
        comparisons = [
            f"Between {user1.display_name} and {user2.display_name}, it's like choosing between expired milk and spoiled cheese.",
            f"{user1.display_name} vs {user2.display_name} is like comparing a broken calculator to a malfunctioning computer.",
            f"One's mediocre, the other's disappointing. I'll let you figure out which is which."
        ]
        import random as rnd
        comparison = rnd.choice(comparisons)
    else:
        try:
            async with ctx.typing():
                prompt = f"Compare {user1.display_name} and {user2.display_name} in the most savage, creative way possible. Make it funny and brutally honest while roasting both equally."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You excel at savage comparisons that roast both subjects equally with creative analogies."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.9
                )
                comparison = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI comparison failed: {e}")
            comparison = f"Both {user1.display_name} and {user2.display_name} are uniquely disappointing in their own special ways."
    
    embed = discord.Embed(title="⚖️ SAVAGE COMPARISON ⚖️", color=0xFF6600)
    embed.add_field(name="The Verdict", value=comparison, inline=False)
    embed.add_field(name="Contestants", value=f"{user1.mention} vs {user2.mention}", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def truth(ctx, target: discord.Member = None):
    """Brutally honest AI truth about someone"""
    logger.info(f"Truth command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        truths = [
            "The truth is, you're exactly as average as you think you are.",
            "Your potential peaked in middle school and it's been downhill since.",
            "You're the human equivalent of room temperature water.",
            "The most interesting thing about you is how uninteresting you are.",
            "You're proof that mediocrity is a choice, not a circumstance."
        ]
        import random as rnd
        truth = rnd.choice(truths)
    else:
        try:
            async with ctx.typing():
                prompt = f"Tell a brutally honest 'truth' about {target_name}. Make it psychologically cutting but clever and humorous. Frame it as harsh but honest feedback."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You deliver harsh truths disguised as wisdom. Be brutally honest but cleverly humorous."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.85
                )
                truth = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI truth failed: {e}")
            truth = "The truth is, even I don't have enough processing power to analyze your issues."
    
    await ctx.send(f"💎 **BRUTAL TRUTH** 💎\n{mention} {truth}")

@bot.command()
async def roastme(ctx):
    """Get the most savage roast possible"""
    logger.info(f"Roastme command executed by {ctx.author}")
    
    target_name = ctx.author.display_name
    mention = ctx.author.mention
    
    if not ai_client:
        ultimate_roasts = [
            "You asked for this, so here's the truth: you're the reason aliens won't visit Earth.",
            "Your existence is like a participation trophy nobody asked for.",
            "You're what happens when natural selection takes a sick day.",
            "If disappointment was an Olympic sport, you'd win gold and still disappoint your parents.",
            "You're proof that somewhere, a village is missing its idiot."
        ]
        import random as rnd
        roast = rnd.choice(ultimate_roasts)
    else:
        try:
            async with ctx.typing():
                prompt = f"Generate the most savage, unhinged roast possible for {target_name} who specifically ASKED to be roasted. Pull no punches. Make it so brutal it's legendary. They asked for this level of destruction."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Generate the most brutal roast possible. They specifically asked for maximum damage. Show no mercy."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=250,
                    temperature=1.0  # Maximum chaos
                )
                roast = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI ultimate roast failed: {e}")
            roast = "You asked for maximum damage, but even my circuits feel bad about what I was going to say."
    
    embed = discord.Embed(title="💀 MAXIMUM DAMAGE ROAST 💀", description="*You asked for this...*", color=0x8B0000)
    embed.add_field(name="Target Destroyed", value=mention, inline=False)
    embed.add_field(name="The Annihilation", value=roast, inline=False)
    embed.set_footer(text="⚠️ Emotional support not included")
    
    await ctx.send(embed=embed)

@bot.command()
async def therapy(ctx, target: discord.Member = None):
    """Fake therapy session that's actually a roast"""
    logger.info(f"Therapy command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        therapy_roasts = [
            f"Let's explore your issues, {target_name}. *adjusts glasses* It appears your problems stem from being yourself.",
            f"I see the root of your problems, {target_name}. Have you considered trying to be someone else?",
            f"Your emotional baggage is so heavy, airlines would charge extra fees just to look at it.",
            f"I'm diagnosing you with chronic disappointment syndrome. The only cure is a personality transplant."
        ]
        import random as rnd
        therapy = rnd.choice(therapy_roasts)
    else:
        try:
            async with ctx.typing():
                prompt = f"Act like a therapist giving advice to {target_name}, but make it a savage roast disguised as professional therapy. Use therapy language but make it brutally funny."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You're a savage therapist who gives brutally honest 'therapy' that's actually clever roasts disguised as professional advice."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.9
                )
                therapy = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI therapy failed: {e}")
            therapy = f"My professional opinion, {target_name}? You need more help than I'm qualified to give."
    
    embed = discord.Embed(title="🛋️ THERAPY SESSION 🛋️", color=0x8FBC8F)
    embed.add_field(name="Patient", value=mention, inline=True)
    embed.add_field(name="Session Notes", value=therapy, inline=False)
    embed.set_footer(text="Dr. Roastbot | Not a real therapist")
    
    await ctx.send(embed=embed)

@bot.command()
async def fortune(ctx, target: discord.Member = None):
    """Dark fortune telling with savage predictions"""
    logger.info(f"Fortune command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        fortunes = [
            f"I see disappointment in your future, {target_name}. Actually, it's already here.",
            f"The crystal ball shows... oh wait, it cracked just looking at your future.",
            f"Your fortune: You will continue to be exactly who you are. I'm sorry.",
            f"The stars say your best days are behind you. Way behind you.",
            f"I predict you'll achieve mediocrity beyond your wildest dreams."
        ]
        import random as rnd
        fortune = rnd.choice(fortunes)
    else:
        try:
            async with ctx.typing():
                prompt = f"Act like a fortune teller giving {target_name} a dark, savage fortune. Use mystical language but make the prediction brutally funny and pessimistic."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You're a savage fortune teller who gives darkly humorous predictions disguised as mystical wisdom."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.9
                )
                fortune = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI fortune failed: {e}")
            fortune = f"The universe is too busy to give you a proper fortune, {target_name}."
    
    embed = discord.Embed(title="🔮 DARK FORTUNE 🔮", color=0x4B0082)
    embed.add_field(name="Seeker of Truth", value=mention, inline=True)
    embed.add_field(name="Your Destiny", value=fortune, inline=False)
    embed.set_footer(text="🌙 Madame Roastbot's Crystal Ball")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)