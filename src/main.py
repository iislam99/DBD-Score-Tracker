#!/usr/bin/env python3

from tracker import DBD_Score_Tracker


def main():
    """Main function to initialize and run game."""
    
    tracker = DBD_Score_Tracker()
    tracker.run()


if __name__ == '__main__':
    main()