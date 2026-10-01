import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. ─── FLASK HEARTBEAT WEB SERVER (KEEPS BOT AWAKE) ──────────────────
app = Flask('')

@app.route('/')
def home():
    return "Bot is online and running 24/7!"

def run_webserver():
    # Runs the background web server on port 8080
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_webserver)
    t.start()

# 2. ─── DISCORD BOT CONFIGURATION ─────────────────────────────────────
intents = discord.Intents.default()
intents.voice_states = True  # Triggers when a user joins or leaves a VC
bot = commands.Bot(command_prefix="!", intents=intents)

# Localized Voice and Text Chat pairings
CHANNEL_MAP = {
    1555025161076609065: 1555025003420979220,  # lord-farm-1 vc : lord-farm-1 text
    1555029628425469992: 1555029151025729626,  # lord-farm-2 vc : lord-farm-2 text
    1555029948685881394: 1555029830335201330,  # lord-farm-3 vc : lord-farm-3 text
    1555030506884702239: 1555030441159954482,  # lord-farm-4 vc : lord-farm-4 text
    1555031442059304971: 1555031216024059924,  # lord-farm-5 vc : lord-farm-5 text
}

@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user.name}! 24/7 Mode Active.")

@bot.event
async def on_voice_state_update(member, before, after):
    # Detects strictly when a user fully exits a voice room
    if before.channel is not None and after.channel is None:
        vc_id = before.channel.id
        
        # Route to the matching farm chat room
        if vc_id in CHANNEL_MAP:
            target_chat_id = CHANNEL_MAP[vc_id]
            log_channel = bot.get_channel(target_chat_id)
            
            if log_channel:
                # Recreates the exact orange-striped embed structure
                embed = discord.Embed(
                    title="Member Left Voice Channel", 
                    description=f"{member.mention} left the voice channel.",
                    color=discord.Color.from_rgb(230, 126, 34)  # Orange color accent
                )
                embed.set_footer(text="rave - Lord Farming System")
                
                # Sends both the text tag notification and the matching system card
                await log_channel.send(content=f"{member.mention} left the voice channel.", embed=embed)

# Launch the background heartbeat web server before booting the bot
keep_alive()

# Pulls your private token key securely from Render's environment settings
bot.run(os.environ['DISCORD_TOKEN'])
