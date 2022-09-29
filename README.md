# DBD-Score-Tracker
Score tracker for the Dead by Daylight video game. Scores are sent to Discord.

**NOTE:** Only works on displays with a resolution of 1920 x 1080. If you want it to work on a different display, you will need to determine the locations of all player information yourself and update `generatePlayerScreenshots()` in `src/scoreboard.py` accordingly.

## Setup
- Install Python 3
- Clone repository
- Navigate to root directory of repository
- Create a Python virtual environment
- Activate virtual environment
- Install all packages in `requirements.txt` using `pip install -r requirements.txt`
- Open `src/discord_connection.py` and set the `HOOK_URL` variable equal to a Discord Webhook link for your Discord channel
- Deactivate virtual environment when you are done using the tracker

## Usage
- Run src/main.py
- Answer the questions to set up your team
- Let program run while you play DBD. When a game ends and you reach the scoreboard, press F9 to scan the screen. A sound alert will play when you can move away from the screen. The data from the screen will be sent to your Discord channel. Repeat this for as many games as desired. Press F10 when you are done playing.

## Usage Example
![image](https://user-images.githubusercontent.com/42816266/192916173-493ad476-3fa9-4482-927c-862aca7f59f5.png)

![image](https://user-images.githubusercontent.com/42816266/192916208-5627aabc-ac3b-4b73-9688-89eba7e983ea.png)

![image](https://user-images.githubusercontent.com/42816266/192916227-6929be78-139f-4ad7-85bf-248d10418f5b.png)
