NEEDS TO BE CLEAR AND CONCISE!!!

# DC-Roulette

## Introduction

Let's enjoy a game of roulette inside of Discord!
This game runs on a Discord bot, which is written in Python and leverages an SQLite database to store user data.

## How to Invite the Bot to Your Server
Invite link: https://discord.com/api/oauth2/authorize?client_id=1093214162605318254&permissions=34359740416&scope=bot
- Paste this invite link into your browser
- Login to your Discord account
- Choose your server
- Select the needed permissions (Send messages; Create public threads)
- Confirm you are human
- As long as the bot is being hosted by me, you can start interacting with it! (If you'd like to try it out and it's down - just reach out to me, I'll spin it back up!)

## How to Run the Bot by Yourself
- Setup a new bot on Discord:
    - In Discord settings, go to "Advanced" and turn on "Developer mode".
    - Click on "Discord API" link.
    - Click on "make an app" link in the description.
    - In the Developer portal, in "Applications" menu, click "New Application" button.
    - Name the bot and "Save changes".
    - Go to the "Bot" menu and generate a token using "Add Bot". Copy the token, store it somewhere safe.
    - Click on "OAuth2", "URL Generator", check the box "bot", check the permissions "Send messages" and "Create public threads", and then click on "Copy". This will be the invite link for the bot.
    - Follow **How to invite the Bot to Your Server** guide with this invite link.
- Have Python 3.10.11 installed
- After cloning this repository, go to the project root and run `pip install -r requirements.txt` to install Python dependencies
- Setup the app environment:
    - Make a new `.env` file at the project root.
    - Add your bot's token as a `TOKEN` var to the `.env` file.
    - There are several more configurations you can setup in there (though they're optional):
        - `DB_NAME` - Points to an SQLite .db file
        - `DATETIME_FORMAT` - Used in DB to format datetime columns
        - `GAME_NAME` - The name by which the Bot will call the game
        - `ROUND_DURATION_S` - Duration of betting rounds in seconds
- At the root of the project, use terminal command `python run.py` to start the bot.

## How to Play
- In Discord chat, type command `/roulette` to call up a main menu prompt. From there you can access three actions:
    - `Register`: Adds you to the player ranks - Awards you 100 coins which you can blow away betting and registers your Discord user in the database.
    - `Read rules`: Shows detailed rules of how to play the game.
    - `List Commands`: Lists all commands the bot can process
- Once you are registered you can check your coins with the command `/my_coins`.
- Now, about placing bets. Players can place bets on a specific number (0-36) or color (red or black). This is what you should know about it beforehand:
    - Once someone places a bet, a 2 minute timer will start ticking down. Anyone can place as many bets as they want in that time.
    - Then, the roulette spins and generates a random outcome. It will be a number and a color.
    - Red roulette numbers are: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
    - Black roulette numbers are: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
    - 0 is green
    - For correctly guessed color winnings are 2 times the bet sum
    - For correctly guessed number winnings are 36 times the bet sum
    - If you run out coins, you can register from the `/roulette` command once again.
- If you'd like to bid on a color, use command `/bet color (value) (bet_amount)`. Instead of `(value)` type in `red` or `black`, and replace `bet_amount` with the amount of coins you'd like to bet.
- If you'd like to bid on a number, use the command `/bet number (value) (bet_amount)`. In place of `(value)` type in a number from `0` to `36`, replace `bet_amount` with the amount of coins you'd like to bet.
- While the timer is ticking, you can check your active bets with command `/my_bets`.
- Have fun on your path to becoming the next Discord roulette millionnaire! :P
