from fuzzywuzzy import fuzz

class user_guessing_controller:
    def __init__(self, user, pokemon_name):

        # Determine the spelling level based on the user's age
        age = user["age"]
        if age < 8:
            self.difficulty = 1
        elif age < 14:
            self.difficulty = 2
        else:
            self.difficulty = 3

        self.pokemon_name = pokemon_name

    def get_user_guess(self):
        guess = input("Enter your guess: ")
        return guess

    # Check if the user's guess is correct
    def check_guess(self, guess):
        # Use fuzzy string matching to compare the guess to the Pokemon name
        similarity = fuzz.ratio(guess.lower(), self.pokemon_name.lower())
        # Determine the threshold based on the user's age group

        # This sounds stupid but it's a cool way to make the game more accessible
        # especially for the age group that is not familiar with Pokemon
        if self.difficulty == 1:
            threshold = 65
        elif self.difficulty == 2:
            threshold = 90
        else:
            threshold = 95

        # If the similarity is above the threshold, consider the guess as correct
        if similarity > threshold:
            return True
        else:
            return False