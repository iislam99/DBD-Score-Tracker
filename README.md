# DBD-Score-Tracker
Score tracker for the Dead by Daylight video game. Scores for your current gaming session are sent to Discord.

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

## How to Use
- Run `src/main.py`
- Answer the questions to set up your team
- Let program run while you play DBD. When a game ends and you reach the scoreboard, press F9 to scan the screen. A sound alert will play when you can move away from the screen. The data from the screen will be sent to your Discord channel. Repeat this for as many games as desired. Press F10 when you are done playing.

## Usage Example

### Set up your team. 
If this is your first time using the tracker, input the requested information of all party members manually.
If you have used this tracker with this party before, use the team name you gave it last time to access player information.
After team information is provided, a welcome message will be sent to Discord with the team's information.

![image](https://user-images.githubusercontent.com/42816266/192924194-885383a5-4916-4d33-a0e2-c92fef4e51d2.png)

![image](https://user-images.githubusercontent.com/42816266/192916173-493ad476-3fa9-4482-927c-862aca7f59f5.png)

### Game 1
Press F9 on the scoreboard screen.

![Game 1 Against the Shape](https://user-images.githubusercontent.com/42816266/192924972-c6adbc41-59c7-41ea-bdd4-f8c8f065dd40.png)

![Bot Message for Game 1](https://user-images.githubusercontent.com/42816266/192924878-e77b7817-f851-45d5-bb96-0fadf4e5f446.png)


### Game 2

Press F9 on the scoreboard screen.

![Game 2 Against the Onryo](https://user-images.githubusercontent.com/42816266/192925146-6c1172d8-647a-4c86-9b11-df1d07bd9e4f.png)

![Bot Message for Game 2](https://user-images.githubusercontent.com/42816266/192924920-326661be-8c1c-4330-b856-4086281ce663.png)

### Final Scores

Press F10 to finish using the tracker and send the final scores to Discord.

![image](https://user-images.githubusercontent.com/42816266/192916227-6929be78-139f-4ad7-85bf-248d10418f5b.png)
