import discord
from discord.ext import commands
import requests
import asyncio
import logging
import random
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoastBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Load environment variables - these will be set by the user
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.ai_api_url = os.getenv('AI_API_URL')  # Optional - will use fallback roasts if not provided
        self.ai_api_key = os.getenv('AI_API_KEY')  # Optional - will use fallback roasts if not provided
        
        # Validate required environment variables at startup
        if not self.discord_token:
            logger.error("DISCORD_BOT_TOKEN environment variable is required")
            raise ValueError("Discord bot token not provided")
        
        # AI API is optional - bot will work with built-in roasts if not provided
        if not self.ai_api_url or not self.ai_api_key:
            logger.warning("AI API URL or key not provided - using built-in savage roasts")
            self.use_fallback_roasts = True
        else:
            self.use_fallback_roasts = False
        
        # Built-in savage roasts for when AI API isn't available
        self.savage_roasts = [
            "{target}, your existence is so bland that even vanilla ice cream calls you basic.",
            "{target}, I've seen more personality in a Windows error message.",
            "{target}, you're the human equivalent of a participation trophy - technically there, but nobody's impressed.",
            "{target}, your life is like a broken pencil - completely pointless.",
            "{target}, if stupidity was a superpower, you'd be the entire Justice League.",
            "{target}, you're proof that even God makes rough drafts.",
            "{target}, I'd call you a tool, but that would be insulting to useful objects.",
            "{target}, your brain must be made of the same material as a black hole - nothing gets out.",
            "{target}, you're like a software update - nobody wants you, but you show up anyway.",
            "{target}, calling you a clown would be unfair to professional entertainers.",
            "{target}, your IQ is so low, you'd lose a debate with a goldfish.",
            "{target}, you're the reason aliens won't visit Earth.",
            "{target}, if ignorance is bliss, you must be the happiest person alive.",
            "{target}, your personality has all the depth of a puddle in the desert.",
            "{target}, you're like a WiFi password - completely forgettable and nobody wants to share you.",
            "{target}, I've met brick walls with more emotional intelligence than you.",
            "{target}, your sense of humor is drier than the Sahara and twice as empty.",
            "{target}, you're the human equivalent of a 'Skip Ad' button - everyone wants you gone.",
            "{target}, if awkwardness was an art form, you'd be the Mona Lisa.",
            "{target}, your life choices make a random number generator look strategic."
        ]
        
        logger.info("Environment variables loaded successfully")

    async def on_ready(self):
        """Called when the bot has successfully logged in and is ready"""
        logger.info(f'Bot logged in as {self.user}')
        print("🔥 Hail Mary AI Roast Bot is online and ready to burn egos 🔥")

    async def get_ai_roast(self, target: str):
        """
        Get a brutal roast from AI API or fallback to built-in roasts
        
        Args:
            target: The name/person to roast
            
        Returns:
            Roast string (AI-generated or built-in)
        """
        # Use fallback roasts if AI API is not configured
        if self.use_fallback_roasts:
            roast_template = random.choice(self.savage_roasts)
            roast = roast_template.format(target=target)
            logger.info(f"Generated built-in roast for: {target}")
            return roast
            
        # Try to use AI API if configured
        try:
            # Craft the savage roast prompt - made extra brutal as requested
            prompt = f"Roast {target} in an extremely savage, dark-humor style. Make it creative, absurd, and sarcastic. Be brutally unhinged but clever. No slurs, no NSFW, no real-world tragedies. Maximum savagery and wit required. Make it devastatingly funny and brutal."
            
            # Prepare the API request headers
            headers = {
                'Authorization': f'Bearer {self.ai_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Generic payload structure - user will need to adjust based on their AI API
            # Common formats work with OpenAI, Anthropic, and similar APIs
            payload = {
                'prompt': prompt,
                'max_tokens': 150,
                'temperature': 0.9  # High temperature for more creative/savage responses
            }
            
            logger.info(f"Making AI API request to roast: {target}")
            
            # Make the API request with timeout - ensure URL is not None
            if not self.ai_api_url:
                logger.warning("AI API URL is not configured, falling back to built-in roasts")
                roast_template = random.choice(self.savage_roasts)
                return roast_template.format(target=target)
                
            response = requests.post(
                self.ai_api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Try common response formats used by different AI APIs
                roast = None
                
                # OpenAI format
                if 'choices' in data and len(data['choices']) > 0:
                    roast = data['choices'][0].get('text', '').strip()
                    if not roast:
                        roast = data['choices'][0].get('message', {}).get('content', '').strip()
                
                # Anthropic/Claude format
                elif 'completion' in data:
                    roast = data['completion'].strip()
                
                # Generic formats
                elif 'response' in data:
                    roast = data['response'].strip()
                elif 'output' in data:
                    roast = data['output'].strip()
                elif 'text' in data:
                    roast = data['text'].strip()
                
                if roast:
                    logger.info(f"Successfully generated AI roast for: {target}")
                    return roast
                else:
                    logger.warning("AI API returned empty response, using fallback")
                    roast_template = random.choice(self.savage_roasts)
                    return roast_template.format(target=target)
            else:
                logger.warning(f"AI API request failed with status {response.status_code}, using fallback")
                roast_template = random.choice(self.savage_roasts)
                return roast_template.format(target=target)
                
        except requests.exceptions.Timeout:
            logger.warning("AI API request timed out, using fallback")
            roast_template = random.choice(self.savage_roasts)
            return roast_template.format(target=target)
        except requests.exceptions.RequestException as e:
            logger.warning(f"AI API request failed: {str(e)}, using fallback")
            roast_template = random.choice(self.savage_roasts)
            return roast_template.format(target=target)
        except Exception as e:
            logger.warning(f"Unexpected error getting AI roast: {str(e)}, using fallback")
            roast_template = random.choice(self.savage_roasts)
            return roast_template.format(target=target)

    @commands.command(name='roast')
    async def roast_command(self, ctx, *, target=None):
        """
        Roast command that generates savage AI-powered roasts
        
        Usage: 
        !roast @user - Roasts the mentioned user
        !roast username - Roasts the specified username  
        !roast - Roasts the command sender
        """
        try:
            # 10% chance to roast itself for comedic variety
            if random.random() < 0.1:
                target_name = "myself (this bot)"
                roast = await self.get_ai_roast(target_name)
                await ctx.send(f"🔥 **Self-Roast Special:** {roast}")
                logger.info("Bot successfully roasted itself")
                return

            # Determine the target
            if target:
                # Check if target contains a mention
                if ctx.message.mentions:
                    mentioned_user = ctx.message.mentions[0]
                    target_name = mentioned_user.display_name
                    mention_tag = mentioned_user.mention
                else:
                    target_name = target
                    mention_tag = None
            else:
                # No target provided, roast the command sender
                target_name = ctx.author.display_name
                mention_tag = ctx.author.mention

            # Add typing indicator for dramatic effect
            async with ctx.typing():
                # Get the brutal roast (AI or built-in)
                roast = await self.get_ai_roast(target_name)
                
                # The get_ai_roast method now always returns a roast (never None)
                # Format the response with optional mention
                if mention_tag and target:
                    response = f"🔥 {mention_tag} {roast}"
                else:
                    response = f"🔥 {roast}"
                
                await ctx.send(response)
                logger.info(f"Successfully roasted {target_name}")
                    
        except Exception as e:
            logger.error(f"Error in roast command: {str(e)}")
            await ctx.send("🔥 Something went wrong while preparing your roast. Even I'm embarrassed by this failure.")

    async def on_command_error(self, ctx, error):
        """Handle command errors gracefully"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🔥 Usage: `!roast <name>` or `!roast @user` or just `!roast` to roast yourself")
        else:
            logger.error(f"Unexpected command error: {str(error)}")
            await ctx.send("🔥 An unexpected error occurred. Even my error handling is better than your life choices.")

    def run_bot(self):
        """Start the bot"""
        try:
            logger.info("Starting Discord bot...")
            if not self.discord_token:
                logger.error("Discord token is not configured")
                raise ValueError("Discord token missing")
            self.run(self.discord_token)
        except discord.LoginFailure:
            logger.error("Failed to login - check your Discord bot token")
            raise
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            raise

def main():
    """Main function to initialize and run the bot"""
    try:
        # Create and run the bot
        bot = RoastBot()
        bot.run_bot()
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()