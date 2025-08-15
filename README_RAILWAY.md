# 🤖 Hail Mary AI Roast Bot - Railway Deployment Guide

## Railway Free Tier Setup

### Step 1: Prepare Your Repository
1. Copy all files from this Replit to a new GitHub repository
2. Include these essential files:
   - `bot_simple.py` (main bot code)
   - `railway.json` (Railway configuration)
   - `Procfile` (process configuration)
   - `nixpacks.toml` (build configuration)
   - `runtime.txt` (Python version)

### Step 2: Railway Deployment
1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account and select your bot repository
4. Railway will automatically detect it's a Python project

### Step 3: Environment Variables
Add these in Railway's Variables tab:
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Step 4: Railway Free Tier Limits
- **$5 monthly credit** (should be plenty for a Discord bot)
- **512MB RAM** (sufficient for this bot)
- **1GB storage** (more than enough)
- **100GB network** (very generous)
- **No sleep mode** (bot stays online 24/7)

### Step 5: Bot Setup
1. Make sure your Discord bot has these permissions:
   - Send Messages
   - Use Slash Commands
   - Add Reactions
   - Read Message History
   - Embed Links

2. Invite your bot to servers with this permission integer: `2147534912`

### Step 6: Deploy
1. Railway automatically deploys when you push to GitHub
2. Check the deployment logs for any issues
3. Your bot should come online within 1-2 minutes

## Commands Available
- **22 total commands** with AI-powered responses
- **Roasting features**: battle, challenge, verse, compare, truth, roastme, therapy, fortune
- **General fun**: story, joke, advice, riddle
- **Utilities**: poll, flip, dice, choose

## Monitoring
- Railway provides logs and metrics in the dashboard
- Bot automatically restarts if it crashes
- Memory and CPU usage are monitored

## Free Tier Tips
- Your bot should use ~50-100MB RAM (well under the 512MB limit)
- Network usage will be minimal for a Discord bot
- $5/month credit should last the full month easily
- Railway doesn't put free apps to sleep like some other platforms

## Support
If you need help:
1. Check Railway logs for errors
2. Verify environment variables are set correctly
3. Ensure Discord bot token has proper permissions
4. Test locally first if issues persist