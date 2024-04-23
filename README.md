## Who's That Pokémon Project
This project is a fun, interactive console-based game inspired by the "Who's That Pokémon?" segment from the Pokémon TV series.

## Overview
In the game, players are shown an obscured image of a Pokémon and must guess the Pokémon's name. The game includes the ability to select a generation to guess from and multiple difficulty levels determined from age to enhance the gameplay experience.

## How It Works
The game uses ASCII art to display the obscured Pokémon images in the console. The ASCII art is generated from actual Pokémon images, fetched from the PokeAPI, using the ascii_magic library.

The game also uses the rich library to enhance the console display with rich text and beautiful formatting. This includes color and style formatting, as well as advanced features like tables, markdown, and syntax highlighting.

All pokemon game data is fetched from the PokeAPI and this is all handled in the PokeAPI controller.

The user data, including usernames, passwords and highscores is all stored in the database and managed through the db controller. The log_in.py file handles user authentication. Users can create an account with a username, password, and date of birth. The authenticate method in this file prompts the user to enter their username and password, and checks if the entered credentials are correct.

## How to Play
To play the game, run the main.py file from your terminal. If you're a new user, you'll be prompted to create an account. Once you're logged in, you can start guessing Pokémon!