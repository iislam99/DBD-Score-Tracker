from playsound import playsound
from PIL import ImageGrab

import numpy as np
import easyocr
import cv2
import os

from killer_list import killerList
import discord_connection as dc


reader = easyocr.Reader(['en'])


def checkWin(path, filename):
    """Check screenshot to see if player won."""

    escaped = 0
    img_rgb = cv2.imread(f"{path}/{filename}")
    template = cv2.imread("assets/images/escaped.png")

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)

    for _ in zip(*loc[::-1]):
        escaped = 1
        break

    return escaped


def generatePlayerScreenshots(path):
    """Generate screenshots isolating player information from scoreboard screen."""

    x_min1 = 185
    x_max1 = 870
    x_min2 = 900
    x_max2 = 950

    # Create screenshot directory if does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Screenshot of entire screen
    screen = ImageGrab.grab(bbox=None)
    screen.save(f"{path}/score.png")
    playsound(f'{os.getcwd()}/assets/sound/alert.mp3')     # Lets user know they can change their screen now

    # Screenshots of player scores from initial screenshot
    img = cv2.imread(f"{path}/score.png")
    nameScoreCrop = img[270:370, x_min1:x_max1]
    winLossCrop = img[300:370, x_min2:x_max2]
    cv2.imwrite(f"{path}/player1.png", nameScoreCrop)
    cv2.imwrite(f"{path}/player1_WL.png", winLossCrop)

    nameScoreCrop = img[390:490, x_min1:x_max1]
    winLossCrop = img[420:490, x_min2:x_max2]
    cv2.imwrite(f"{path}/player2.png", nameScoreCrop)
    cv2.imwrite(f"{path}/player2_WL.png", winLossCrop)

    nameScoreCrop = img[500:600, x_min1:x_max1]
    winLossCrop = img[530:600, x_min2:x_max2]
    cv2.imwrite(f"{path}/player3.png", nameScoreCrop)
    cv2.imwrite(f"{path}/player3_WL.png", winLossCrop)

    nameScoreCrop = img[620:720, x_min1:x_max1]
    winLossCrop = img[650:720, x_min2:x_max2]
    cv2.imwrite(f"{path}/player4.png", nameScoreCrop)
    cv2.imwrite(f"{path}/player4_WL.png", winLossCrop)

    # Screenshot of killer name
    killerCrop = img[740:770, x_min1:x_max1]
    cv2.imwrite(f"{path}/killer.png", killerCrop)


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



def getScoreData(players, teamName, path='assets/images/temp'):
    """Modify player attributes after extracting score data from screenshots."""

    try:
        generatePlayerScreenshots(path)
    except:
        dc.sendError(teamName, "Failed to generate screenshots.")
        return -1
    else:
        try:
            gameData = getScreenshotData(path)
        except:
            dc.sendError(teamName, "Failed to extract data from screenshots.")
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
                dc.sendError(teamName, "Failed to update player scores.")
                return -1

    return 0