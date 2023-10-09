from PIL import ImageGrab
from playsound import playsound

import os
import cv2

def getScreenshotCoordinates(displayRes, currDisplay):
    """Use display information to identify location of player data in screenshots."""

    dataLocation = {
        1080: {
            'name_score_x_min': 185 + (1920 * (currDisplay - 1)),
            'name_score_x_max': 870 + (1920 * (currDisplay - 1)),
            'win_loss_x_min': 900 + (1920 * (currDisplay - 1)),
            'win_loss_x_max': 950 + (1920 * (currDisplay - 1)),

            'p1_name_y_min': 270,
            'p1_name_y_max': 370,
            'p1_win_loss_y_min': 300,
            'p1_win_loss_y_max': 370,

            'p2_name_y_min': 390,
            'p2_name_y_max': 490,
            'p2_win_loss_y_min': 420,
            'p2_win_loss_y_max': 490,

            'p3_name_y_min': 500,
            'p3_name_y_max': 600,
            'p3_win_loss_y_min': 530,
            'p3_win_loss_y_max': 600,

            'p4_name_y_min': 620,
            'p4_name_y_max': 720,
            'p4_win_loss_y_min': 650,
            'p4_win_loss_y_max': 720,

            'killer_y_min': 740,
            'killer_y_max': 770
        },
        1440: {
            'name_score_x_min': 235 + (2560 * (currDisplay - 1)),
            'name_score_x_max': 1180 + (2560 * (currDisplay - 1)),
            'win_loss_x_min': 1185 + (2560 * (currDisplay - 1)),
            'win_loss_x_max': 1290 + (2560 * (currDisplay - 1)),

            'p1_name_y_min': 350,
            'p1_name_y_max': 500,
            'p1_win_loss_y_min': 400,
            'p1_win_loss_y_max': 500,

            'p2_name_y_min': 500,
            'p2_name_y_max': 650,
            'p2_win_loss_y_min': 550,
            'p2_win_loss_y_max': 650,

            'p3_name_y_min': 650,
            'p3_name_y_max': 800,
            'p3_win_loss_y_min': 700,
            'p3_win_loss_y_max': 800,

            'p4_name_y_min': 800,
            'p4_name_y_max': 950,
            'p4_win_loss_y_min': 850,
            'p4_win_loss_y_max': 950,

            'killer_y_min': 950,
            'killer_y_max': 1030
        }
    }

    return dataLocation[displayRes]


def generatePlayerScreenshots(path):
    """Generate screenshots isolating player information from scoreboard screen."""

    displayRes = 1440
    currDisplay = 2
    # displayRes = os.getenv('display_res')
    # currDisplay = os.getenv('curr_display')
    pos = getScreenshotCoordinates(displayRes, currDisplay)

    x_min1 = 185
    x_max1 = 870
    x_min2 = 900
    x_max2 = 950

    # Create screenshot directory if does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Screenshot of entire screen
    screen = ImageGrab.grab(bbox=None, all_screens=True)
    screen.save(f"{path}/score.png")
    playsound(f'{os.getcwd()}/assets/sound/alert.mp3')     # Lets user know they can change their screen now

    # Screenshots of player scores from initial screenshot
    img = cv2.imread(f"{path}/score.png")
    x_min1 = pos['name_score_x_min']
    x_max1 = pos['name_score_x_max']
    x_min2 = pos['win_loss_x_min']
    x_max2 = pos['win_loss_x_max']

    for i in range (1, 5):
        y_min1 = pos[f'p{i}_name_y_min']
        y_max1 = pos[f'p{i}_name_y_max']
        y_min2 = pos[f'p{i}_win_loss_y_min']
        y_max2 = pos[f'p{i}_win_loss_y_max']

        nameScoreCrop = img[y_min1:y_max1, x_min1:x_max1]
        winLossCrop = img[y_min2:y_max2, x_min2:x_max2]
        cv2.imwrite(f"{path}/player{i}.png", nameScoreCrop)
        cv2.imwrite(f"{path}/player{i}_WL.png", winLossCrop)

    # Screenshot of killer name
    y_min = pos['killer_y_min']
    y_max = pos['killer_y_max']
    
    killerCrop = img[y_min:y_max, x_min1:x_max1]
    cv2.imwrite(f"{path}/killer.png", killerCrop)

    # # Screenshots of player scores from initial screenshot
    # img = cv2.imread(f"{path}/score.png")
    # nameScoreCrop = img[270:370, x_min1:x_max1]
    # winLossCrop = img[300:370, x_min2:x_max2]
    # cv2.imwrite(f"{path}/player1.png", nameScoreCrop)
    # cv2.imwrite(f"{path}/player1_WL.png", winLossCrop)

    # nameScoreCrop = img[390:490, x_min1:x_max1]
    # winLossCrop = img[420:490, x_min2:x_max2]
    # cv2.imwrite(f"{path}/player2.png", nameScoreCrop)
    # cv2.imwrite(f"{path}/player2_WL.png", winLossCrop)

    # nameScoreCrop = img[500:600, x_min1:x_max1]
    # winLossCrop = img[530:600, x_min2:x_max2]
    # cv2.imwrite(f"{path}/player3.png", nameScoreCrop)
    # cv2.imwrite(f"{path}/player3_WL.png", winLossCrop)

    # nameScoreCrop = img[620:720, x_min1:x_max1]
    # winLossCrop = img[650:720, x_min2:x_max2]
    # cv2.imwrite(f"{path}/player4.png", nameScoreCrop)
    # cv2.imwrite(f"{path}/player4_WL.png", winLossCrop)

    # # Screenshot of killer name
    # killerCrop = img[740:770, x_min1:x_max1]
    # cv2.imwrite(f"{path}/killer.png", killerCrop)