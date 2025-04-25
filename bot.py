import discord
from discord.ext import commands
from discord import app_commands, ui
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

GUILD_ID = 1364703542606041128
EARLY_ACCESS_ROLE_ID = 1365053202734645289
EMERGENCY_SERVICES_ROLE_ID = 1365071276103962634
CIVILIAN_ROLE_ID = 1364777004364468234
SESSION_PING_ROLE_ID = 1365032935530696797

class RoleRestrictedButton(ui.Button):
    def __init__(self, label, custom_id, allowed_roles):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.allowed_roles = allowed_roles

    async def callback(self, interaction: discord.Interaction):
        if any(role.id in self.allowed_roles for role in interaction.user.roles):
            await interaction.response.send_message(f"Here is your link: {self.custom_id}", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have permission to access this link.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="session-startup", description="Start a new session", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(reactions_required="Number of reactions required to start the session")
async def session_startup(interaction: discord.Interaction, reactions_required: int):
    embed = discord.Embed(
        title="SFRT | Session Startup",
        description=(
            f"{interaction.user.mention} is now hosting a session! Before continuing, please make sure you have read all of ⁠information.\n"
            "Ensure to register your vehicle before joining the roleplay."
        ),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed.set_image(url="attachment://SFRT.Startup (1).jpg")
    embed.add_field(name="Reaction Requirement", value=f"This message must achieve {reactions_required} reactions for this session to commence.")
    file = discord.File("SFRT.Startup (1).jpg", filename="SFRT.Startup (1).jpg")
    message = await interaction.channel.send(f"<@&{SESSION_PING_ROLE_ID}> @here", embed=embed, file=file)
    await message.add_reaction("✅")
    await interaction.response.send_message("Session startup has been announced!", ephemeral=True)

@bot.tree.command(name="setting-up", description="Announce setup phase", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(countdown="Time until session opens (e.g. 5 minutes)")
async def setting_up(interaction: discord.Interaction, countdown: str):
    await interaction.response.send_message(
        f"{interaction.user.mention} is setting up! Staff, Emergency Services, Content Creators & Boosters may now join within {countdown}",
        ephemeral=False
    )

@bot.tree.command(name="early-access", description="Release early access link", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(link="Roblox session link")
async def early_access(interaction: discord.Interaction, link: str):
    embed = discord.Embed(
        title="SFRT | Early Access",
        description=(
            f"The host {interaction.user.mention} has released Early Access! Emergency Services, Early Access, and Server Boosters may now join using the button below."
        ),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed.set_image(url="attachment://SFRT.EA.jpg")
    view = ui.View()
    view.add_item(RoleRestrictedButton("Join Early Access", link, [EARLY_ACCESS_ROLE_ID, EMERGENCY_SERVICES_ROLE_ID]))
    file = discord.File("SFRT.EA.jpg", filename="SFRT.EA.jpg")
    await interaction.channel.send(f"<@&{EARLY_ACCESS_ROLE_ID}> <@&{EMERGENCY_SERVICES_ROLE_ID}>", embed=embed, view=view, file=file)
    await interaction.response.send_message("Early Access released.", ephemeral=True)

@bot.tree.command(name="session-release", description="Release session to all", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(link="Roblox session link", peacetime_status="On or Off", failroleplay_speeds="Speed limit", drifting="On or Off")
async def session_release(interaction: discord.Interaction, link: str, peacetime_status: str, failroleplay_speeds: int, drifting: str):
    if not all([link, peacetime_status, failroleplay_speeds, drifting]):
        await interaction.response.send_message("All fields are required to release the session.", ephemeral=True)
        return

    embed = discord.Embed(
        title="SFRT | Session Release",
        description=("The session host has now released the link to everyone. Click the button below to join this session!\n\n"
                     f"**Session Host:** {interaction.user.mention}\n"
                     f"**Peacetime Status:** {peacetime_status}\n"
                     f"**Failroleplay Speeds:** {failroleplay_speeds}\n"
                     f"**Drifting Status:** {drifting}"),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed.set_image(url="attachment://SFRT.Release.jpg")
    view = ui.View()
    view.add_item(RoleRestrictedButton("Join Session", link, [CIVILIAN_ROLE_ID]))
    file = discord.File("SFRT.Release.jpg", filename="SFRT.Release.jpg")
    await interaction.channel.send(f"<@&{SESSION_PING_ROLE_ID}> @here", embed=embed, view=view, file=file)
    await interaction.response.send_message("Session released to everyone.", ephemeral=True)

@bot.tree.command(name="conclusion", description="Conclude a roleplay session", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(duration="Total Duration of the session")
async def conclusion(interaction: discord.Interaction, duration: str):
    embed = discord.Embed(
        title="SFRT | Roleplay Concluded",
        description=(f"{interaction.user.mention}'s roleplay session has concluded. Thank you to all who have attended this roleplay.\n"
                     f"**Total Duration:** {duration}"),
        color=discord.Color.from_rgb(255, 255, 255)
    )
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("Session conclusion posted.", ephemeral=True)

bot.run("MTM2NTE1Mjc4MjIwNTcxODYwOA.GtuRO5.cB1oblHvEu_KzpHDKp51sizDuujsXwuQTv6k8Y")
