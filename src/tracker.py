import os
import re
from datetime import datetime
from pynput import keyboard

from discord_connection import sendGameData, welcomeMessage, finalScores
from scoreboard import getScoreData
from player import Player


class DBD_Score_Tracker:
    """Initializes tracker and waits for command to update player scores."""

    def __init__(self):
        self._players = []
        self._teamName = ""
        self._sessionStart = datetime.now()
        self._lastScores = []
        self._hookUrl = ""

        if not os.path.exists("assets/teams"):
            os.mkdir("assets/teams")
    

    def initPlayers(self):
        """Initialize players manually or with a text file."""
        
        while True:
            resp = input("\nInput players manually or read from a file (M/F)? ").lower()
            
            if resp == 'm':
                while True:
                    numPlayers = input("\nHow many players are there (1-4)? ")
                    pattern = r'^[1-4]$'
                    if re.match(pattern, numPlayers):
                        numPlayers = int(numPlayers)
                        break
                    else:
                        print("Invalid input. Input a number from 1-4.")

                for i in range(numPlayers):
                    p = Player()
                    
                    while True:
                        p.name = input(f"\nWhat is Player {i + 1}'s name? ")
                        if p.name == '':
                            print("Invalid name.")
                        else:
                            break
                    
                    while True:
                        p.username = input(f"What is {p.name}'s DBD username? ")
                        if p.username == '':
                            print("Invalid username.")
                        else:
                            break
                    
                    self._players.append(p)
                
                self._teamName = input("\nWhat would you like to name this team? ")

                while True:
                    self._hookUrl = input("\nPlease input the Discord Webhook URL for the Discord server channel you want to receive score updates:\n")
                    pattern = r'^https://discord.com/api/webhooks/\d+/[A-Za-z0-9_-]+$'
                    if re.match(pattern, self._hookUrl):
                        break
                    else:
                        print("Invalid URL provided.")
                
                with open (f"assets/teams/{self._teamName}.txt", 'w') as f:
                    for p in self._players:
                        f.write(f"{p.name}={p.username}\n")
                    f.write(f"DISCORD_WEBHOOK={self._hookUrl}\n")
                print(f"\nUse team name '{self._teamName}' to access this team next time.")

                break
            elif resp == 'f':
                try:
                    self._teamName = input("\nWhat is the team name? ")
                    with open (f"assets/teams/{self._teamName}.txt", 'r') as file:
                        f = file.read().splitlines()
                        for line in f:
                            line.rstrip('\n')
                            key, val = line.split('=')
                            if key is not 'DISCORD_WEBHOOK':
                                self._players.append(Player(key, val))
                            else:
                                self._hookUrl = val
                    break
                except:
                    print("File not found.")
            else:
                print("Invalid input. Press M or F, then hit enter.")
        
        self._lastScores = self._players
        print("\nPlayers Identified")
        print("-------------------")
        for p in self._players:
            print(p.name, '-', p.username)
        
        welcomeMessage(self._players, self._teamName, self._sessionStart, self._hookUrl)


    def on_release(self, key):
        """Processes keyboard inputs and executes commands accordingly."""

        if key == keyboard.Key.f9:
            # Get data from screenshots and send it to Discord
            if getScoreData(self._players, self._teamName, self._hookUrl) == 0:
                sendGameData(self._players, self._teamName, self._hookUrl)
                self._lastScores = self._players
            else:
                self._players = self._lastScores
        
        if key == keyboard.Key.f10:
            # End key listener
            finalScores(self._players, self._teamName, self._sessionStart, self._hookUrl)
            return False


    def run(self):
        """Initializes tracker data and listens for command to scan screen."""

        self.initPlayers()
        
        # Wait for scoreboard screenshot key
        with keyboard.Listener(on_release=self.on_release) as listener:
            try:
                listener.join()
                print("\nProgram completed execution.")
            except Exception as e:
                print(f"ERROR: {e}")
