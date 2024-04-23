# Who's That Pokémon?

## Description

This project is a fun and interactive game called "Who's That Pokémon?". It's a PyQt-based GUI application that challenges players to guess the name of a Pokémon based on its silhouette.

The application uses a QStackedWidget to manage different widgets or "pages". The QStackedWidget provides a stack of widgets, only one of which can be viewed at a time. This is useful for creating wizards or for stacking widgets which occupy the same space in a layout.

The game has two main pages: the main menu and the guess page. The main menu provides options to start the game or exit the application. The guess page displays a silhouette of a Pokémon and provides an input field for the player to enter their guess.

The application also uses a custom style sheet (stylesheet.qss) to customize the appearance of the widgets. This style sheet is loaded at the start of the application and applied to the QApplication instance.
