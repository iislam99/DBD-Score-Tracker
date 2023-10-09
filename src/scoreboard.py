import numpy as np
import easyocr
import cv2

from killer_list import killerList
from screenshots import generatePlayerScreenshots
import discord_connection as dc


reader = easyocr.Reader(['en'])


def checkWin(path, filename):
    """Check screenshot to see if player won."""

    img_rgb = cv2.imread(f"{path}/{filename}")
    template = cv2.imread("assets/images/escaped.png")

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)

    for _ in zip(*loc[::-1]):
        return True

    return False


def getScreenshotData(path):
    """Extract text from scoreboard screenshots."""

    playerData = []
    for i in range(1, 5):
        imgData = reader.readtext(f"{path}/player{i}.png", detail=0)
        playerData.append(imgData)
    return playerData


def matchPlayer(data, player):
    """Check if the row of data belongs to the given player."""

    for i in range(len(data)):
        if i != len(data) - 1:
            if len(player.username) < len(data[i]):
                shorter = player.username
                longer = data[i]
            else:
                shorter = data[i]
                longer = player.username
            if shorter in longer:
                return True
    return False


def identifyKiller(path):
    """Use screenshot of killer name to identify killer."""
    
    imgData = reader.readtext(f"{path}/killer.png", detail=0)
    print(imgData)
    for i in imgData:
        for killer in killerList:
            if killer in i.lower():
                return killer


def getScoreData(players, teamName, hookUrl, path='assets/images/temp'):
    """Modify player attributes after extracting score data from screenshots."""

    try:
        generatePlayerScreenshots(path)
    except:
        dc.sendError(teamName, hookUrl, "Failed to generate screenshots.")
        return -1
    else:
        try:
            gameData = getScreenshotData(path)
        except:
            dc.sendError(teamName, hookUrl, "Failed to extract data from screenshots.")
            return -1
        else:
            try:
                for p in players:
                    for i, data in enumerate(gameData):
                        if matchPlayer(data, p):
                            p.points += int(''.join(ch for ch in data[-1] if ch.isdigit()))
                            if checkWin(path, f"player{i + 1}_WL.png"):
                                p.wins += 1
                                p.lastGameWon = True
                            else:
                                p.losses += 1
                                p.lastGameWon = False
                            break
            except:
                dc.sendError(teamName, hookUrl, "Failed to update player scores.")
                return -1

    return 0