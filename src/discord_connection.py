from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime

from scoreboard import identifyKiller


def welcomeMessage(players, teamName, start, hookUrl):
    """Send welcome message to Discord."""
   
    hook = DiscordWebhook(url=hookUrl)

    embed = DiscordEmbed(
        title=teamName,
        description="""
            Welcome to the Dead by Daylight score tracker!
            Your scores for your current gaming session are now being tracked.
        """,
        color="00ECFF"
    )

    with open("assets/images/wallpaper.jpg", "rb") as f:
        hook.add_file(file=f.read(), filename='wallpaper.jpg')
    embed.set_image("attachment://wallpaper.jpg")

    for p in players:
        embed.add_embed_field(
            name=p.name,
            value=f"""
                > Wins: `{p.wins}`
                > Losses: `{p.losses}`
                > BP: `{p.points}`
            """,
            inline=False
        )

    embed.set_footer(text=f"Session started at {start.strftime('%H:%M:%S')} on {start.strftime('%Y-%m-%d')}.")
    hook.add_embed(embed)
    hook.execute()


def finalScores(players, teamName, start, hookUrl):
    """Send final scores to Discord."""
    
    hook = DiscordWebhook(url=hookUrl)
    players.sort(key=lambda p: (p.wins, p.points), reverse=True)
    
    embed = DiscordEmbed(
        title=teamName,
        description="Here are your final scores!",
        color="0FFF50"
    )
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/001/448/736/ab7.png")
    
    for p in players:
        embed.add_embed_field(
            name=p.name,
            value=f"""
                > Wins: `{p.wins}`
                > Losses: `{p.losses}`
                > BP: `{p.points}`
            """,
            inline=False
        )

    end = datetime.now()
    elapsed = end - start
    hours = elapsed.seconds // 3600
    minutes = elapsed.seconds // 60 % 60
    seconds = elapsed.seconds % 60
    embed.set_footer(text=f"Total gaming time - {hours}:{minutes}:{seconds}")
    
    hook.add_embed(embed)
    hook.execute()


def sendGameData(players, teamName, hookUrl):
    """Send updated game data to Discord."""

    hook = DiscordWebhook(url=hookUrl)
    players.sort(key=lambda p: (p.wins, p.points), reverse=True)
    killer = identifyKiller("assets/images/temp")
    killerName = 'The ' + killer.title()
    
    # Converting spaces into underscores for file name
    if ' ' in killer:    
        killer = ''.join([c if c != ' ' else '_' for c in killer])
    
    embed = DiscordEmbed(
        title=teamName,
        description=f"Scores after facing {killerName}.",
        color="7F00FF"
    )
    
    with open(f"assets/images/killers/{killer}.png", "rb") as f:
        hook.add_file(file=f.read(), filename=f"{killer}.png")
    embed.set_thumbnail(url=f"attachment://{killer}.png")

    for p in players:
        if p.lastGameWon:
            value = f"""
                > Wins: `{p.wins}`:small_red_triangle:
                > Losses: `{p.losses}`
                > BP: `{p.points}`
            """
        else:
            value = f"""
                > Wins: `{p.wins}`
                > Losses: `{p.losses}`:small_red_triangle:
                > BP: `{p.points}`
            """
        
        embed.add_embed_field(
            name=p.name,
            value=value,
            inline=False
        )

    now = datetime.now()
    embed.set_footer(text=f"Game finished at {now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}.")

    hook.add_embed(embed)
    hook.execute()


def sendError(teamName, hookUrl, message="An error has occurred."):
    """Send error message to Discord."""
    
    hook = DiscordWebhook(url=hookUrl)

    embed = DiscordEmbed(
        title=teamName,
        description=f"**ERROR:** {message}\n*Player scores not updated.*",
        color="FF0000"
    )

    now = datetime.now()
    embed.set_footer(text=f"Error occurred at {now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}.")

    hook.add_embed(embed)
    hook.execute()