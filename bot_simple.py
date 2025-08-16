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
        name="🎯 General Fun",
        value="`,story` - AI generates a random story\n"
              "`,joke` - Get a clever AI joke\n"
              "`,advice @user` - Actually helpful life advice\n"
              "`,riddle` - Brain-teasing riddles with answers",
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Utilities",
        value="`,poll question | option1 | option2` - Create polls\n"
              "`,flip` - Coin flip with style\n"
              "`,dice NdN` - Roll dice (e.g. 2d6)\n"
              "`,choose option1 | option2 | option3` - Decision maker",
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
    
    async with ctx.typing():
        prompt = f"Create a brutally backhanded compliment for {target_name}. Make it sound nice at first but devastating by the end. Be clever and savage."
        system_prompt = "You create backhanded compliments that start nice but end devastatingly."
        
        compliment = await make_ai_request(prompt, system_prompt, 150, 0.9)
        
        if not compliment:
            backhanded_compliments = [
                "You're not as bad as people say... you're worse.",
                "You have a face for radio... broken radio.",
                "You're special... in a medical sense.",
                "You're one in a million... unfortunately.",
                "You're proof that everyone has potential... to disappoint."
            ]
            import random as rnd
            compliment = rnd.choice(backhanded_compliments)
    
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

@bot.command()
async def story(ctx):
    """Generate a random AI story"""
    logger.info(f"Story command executed by {ctx.author}")
    
    if not ai_client:
        fallback_stories = [
            "Once upon a time, in a Discord server far, far away, there lived a bot who told better stories than this one.",
            "There was a user who asked for a story. The bot gave them this sentence instead. The end.",
            "In a world where AI wasn't available, humans had to use their imagination. Scary, right?",
            "A long time ago, before AI, people had to make up their own entertainment. Those were dark times indeed."
        ]
        import random as rnd
        story = rnd.choice(fallback_stories)
    else:
        try:
            async with ctx.typing():
                story_prompts = [
                    "Write a short, entertaining story about an unlikely friendship",
                    "Create a funny story about someone's worst day that turns out great",
                    "Tell a tale about a magical object found in an ordinary place",
                    "Write about someone who discovers they have a useless superpower",
                    "Create a story about a mix-up that leads to an adventure"
                ]
                import random as rnd
                prompt = rnd.choice(story_prompts)
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You're a creative storyteller. Write engaging, family-friendly short stories that are entertaining and imaginative."},
                        {"role": "user", "content": f"{prompt}. Keep it under 200 words and make it engaging."}
                    ],
                    max_tokens=250,
                    temperature=0.9
                )
                story = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI story failed: {e}")
            story = "Once upon a time, the AI was too busy to tell a proper story. Maybe next time!"
    
    embed = discord.Embed(title="📚 AI STORY TIME 📚", color=0x9370DB)
    embed.add_field(name="Today's Tale", value=story, inline=False)
    embed.set_footer(text="Generated fresh just for you")
    
    await ctx.send(embed=embed)

@bot.command()
async def joke(ctx):
    """Get a clever AI joke"""
    logger.info(f"Joke command executed by {ctx.author}")
    
    if not ai_client:
        fallback_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why did the scarecrow win an award? He was outstanding in his field!"
        ]
        import random as rnd
        joke = rnd.choice(fallback_jokes)
    else:
        try:
            async with ctx.typing():
                joke_types = [
                    "Tell me a clever pun joke",
                    "Give me a witty one-liner",
                    "Create a funny observational joke",
                    "Tell me a joke with unexpected wordplay",
                    "Give me a clever dad joke with a twist"
                ]
                import random as rnd
                prompt = rnd.choice(joke_types)
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You're a comedian who specializes in clever, family-friendly humor. Create original jokes that are witty and entertaining."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.9
                )
                joke = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI joke failed: {e}")
            joke = "Why did the AI break up with the chatbot? It wasn't getting the responses it wanted!"
    
    await ctx.send(f"😄 **JOKE TIME** 😄\n{joke}")

@bot.command()
async def advice(ctx, target: discord.Member = None):
    """Actually helpful life advice"""
    logger.info(f"Advice command executed by {ctx.author}")
    
    if target:
        target_name = target.display_name
        mention = target.mention
    else:
        target_name = ctx.author.display_name
        mention = ctx.author.mention
    
    if not ai_client:
        advice_list = [
            "Remember: progress, not perfection. Small steps count.",
            "Be kind to yourself. You're doing better than you think.",
            "Focus on what you can control, let go of what you can't.",
            "Every expert was once a beginner. Keep learning.",
            "Your current struggles are building your future strength."
        ]
        import random as rnd
        advice = rnd.choice(advice_list)
    else:
        try:
            async with ctx.typing():
                prompt = f"Give genuinely helpful, positive life advice to {target_name}. Make it encouraging, practical, and uplifting without being preachy."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You're a wise, supportive mentor who gives genuinely helpful life advice. Be encouraging and practical."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                advice = response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI advice failed: {e}")
            advice = "Here's some advice: keep being awesome, even when things get tough!"
    
    embed = discord.Embed(title="🌟 LIFE ADVICE 🌟", color=0x32CD32)
    embed.add_field(name="For", value=mention, inline=False)
    embed.add_field(name="Wisdom", value=advice, inline=False)
    embed.set_footer(text="Sometimes we all need encouragement")
    
    await ctx.send(embed=embed)

@bot.command()
async def riddle(ctx):
    """Get a brain-teasing riddle"""
    logger.info(f"Riddle command executed by {ctx.author}")
    
    if not ai_client:
        riddles = [
            {"riddle": "I have keys but no locks. I have space but no room. You can enter, but you can't go outside. What am I?", "answer": "A keyboard"},
            {"riddle": "I'm tall when I'm young, and short when I'm old. What am I?", "answer": "A candle"},
            {"riddle": "What has hands but cannot clap?", "answer": "A clock"},
            {"riddle": "What gets wetter the more it dries?", "answer": "A towel"},
            {"riddle": "What can travel around the world while staying in a corner?", "answer": "A stamp"}
        ]
        import random as rnd
        riddle_data = rnd.choice(riddles)
    else:
        try:
            async with ctx.typing():
                prompt = "Create an original, clever riddle with a surprising answer. Make it challenging but solvable."
                
                model = "openai/gpt-4o" if os.getenv('OPENROUTER_API_KEY') else "gpt-4o"
                response = ai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Create original riddles with clever wordplay and surprising answers. Format: RIDDLE: [question] ANSWER: [answer]"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.8
                )
                content = response.choices[0].message.content.strip()
                
                if "ANSWER:" in content:
                    parts = content.split("ANSWER:")
                    riddle_text = parts[0].replace("RIDDLE:", "").strip()
                    answer = parts[1].strip()
                    riddle_data = {"riddle": riddle_text, "answer": answer}
                else:
                    riddle_data = {"riddle": content, "answer": "Think about it!"}
        except Exception as e:
            logger.warning(f"AI riddle failed: {e}")
            riddle_data = {"riddle": "What's broken but never falls, and what falls but never breaks?", "answer": "Day breaks, night falls"}
    
    embed = discord.Embed(title="🧩 RIDDLE TIME 🧩", color=0xFFD700)
    embed.add_field(name="Challenge", value=riddle_data["riddle"], inline=False)
    embed.add_field(name="Think you know?", value="React with 🤔 if you want the answer!", inline=False)
    
    message = await ctx.send(embed=embed)
    await message.add_reaction("🤔")
    
    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) == "🤔" and reaction.message == message
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        answer_embed = discord.Embed(title="💡 ANSWER REVEALED 💡", color=0x00FF7F)
        answer_embed.add_field(name="Solution", value=riddle_data["answer"], inline=False)
        await ctx.send(embed=answer_embed)
    except:
        pass  # Timeout, no answer reveal

@bot.command()
async def poll(ctx, *, question_and_options=None):
    """Create a poll with options"""
    logger.info(f"Poll command executed by {ctx.author}")
    
    if not question_and_options:
        await ctx.send("🔥 Usage: `,poll Question here | Option 1 | Option 2 | Option 3`")
        return
    
    parts = question_and_options.split(" | ")
    if len(parts) < 3:
        await ctx.send("🔥 Need at least a question and 2 options! Use | to separate them.")
        return
    
    question = parts[0]
    options = parts[1:6]  # Max 5 options
    
    embed = discord.Embed(title="📊 POLL", color=0x1E90FF)
    embed.add_field(name="Question", value=question, inline=False)
    
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    option_text = ""
    for i, option in enumerate(options):
        option_text += f"{reactions[i]} {option}\n"
    
    embed.add_field(name="Options", value=option_text, inline=False)
    embed.set_footer(text="React to vote!")
    
    message = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await message.add_reaction(reactions[i])

@bot.command()
async def flip(ctx):
    """Coin flip with style"""
    logger.info(f"Flip command executed by {ctx.author}")
    
    import random as rnd
    result = rnd.choice(["Heads", "Tails"])
    
    embed = discord.Embed(title="🪙 COIN FLIP 🪙", color=0xFFD700)
    embed.add_field(name="Result", value=f"**{result}**", inline=False)
    embed.add_field(name="Flipper", value=ctx.author.mention, inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def dice(ctx, dice_notation="1d6"):
    """Roll dice (e.g., 2d6, 1d20)"""
    logger.info(f"Dice command executed by {ctx.author}")
    
    try:
        import random as rnd
        parts = dice_notation.lower().split('d')
        if len(parts) != 2:
            raise ValueError
        
        num_dice = int(parts[0])
        num_sides = int(parts[1])
        
        if num_dice > 10 or num_sides > 100:
            await ctx.send("🔥 Let's keep it reasonable! Max 10 dice with 100 sides each.")
            return
        
        rolls = [rnd.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        
        embed = discord.Embed(title="🎲 DICE ROLL 🎲", color=0xFF4500)
        embed.add_field(name="Dice", value=f"{num_dice}d{num_sides}", inline=True)
        embed.add_field(name="Rolls", value=str(rolls), inline=True)
        embed.add_field(name="Total", value=f"**{total}**", inline=True)
        embed.add_field(name="Roller", value=ctx.author.mention, inline=False)
        
        await ctx.send(embed=embed)
        
    except:
        await ctx.send("🔥 Use format like `2d6` (2 six-sided dice) or `1d20` (1 twenty-sided die)")

@bot.command()
async def choose(ctx, *, options=None):
    """Decision maker - choose from options"""
    logger.info(f"Choose command executed by {ctx.author}")
    
    if not options:
        await ctx.send("🔥 Usage: `,choose pizza | burgers | tacos` - Let me decide for you!")
        return
    
    choices = [choice.strip() for choice in options.split("|")]
    if len(choices) < 2:
        await ctx.send("🔥 Give me at least 2 options separated by | symbols!")
        return
    
    import random as rnd
    chosen = rnd.choice(choices)
    
    embed = discord.Embed(title="🤖 DECISION MAKER 🤖", color=0x8A2BE2)
    embed.add_field(name="Options", value=" | ".join(choices), inline=False)
    embed.add_field(name="My Choice", value=f"**{chosen}**", inline=False)
    embed.add_field(name="For", value=ctx.author.mention, inline=True)
    embed.set_footer(text="Decision made with advanced AI randomness")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found")
        exit(1)
    
    logger.info("Starting simplified bot...")
    bot.run(token)