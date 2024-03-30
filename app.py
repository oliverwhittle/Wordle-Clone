import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Wordle Clone")

# Set up the clock
clock = pygame.time.Clock()

# Set up the colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (108,169,101)
YELLOW = (200,182,83)
GREY = (120,124,127)
DARK_GREY = (18,18,19)

BACKGROUND_COLOUR = WHITE
TEXT_COLOUR = BLACK
GRID_COLOUR = BLACK

# Set up the font
font = pygame.font.Font(None, 36)

# Cap the frame rate
clock.tick(60)

# Set up background
screen.fill(BACKGROUND_COLOUR)

# Draw the grid
cell_width = 75
cell_height = 75
grid_width = 5
grid_height = 6

# Set the border width
border_width = 2

#Set the word of the day (must be 5 letters long)
def get_random_word(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip().lower()

todays_word = get_random_word('words.txt').upper()

# Function to compare two words and return an array of comparisons
def compare_words(word1, word2):
    comparison_array = []

    # Create a copy of word2 to modify during comparisons
    remaining_letters = list(word2)

    # First pass: find and mark the correct letters in the correct position (Green)
    for i, (letter1, letter2) in enumerate(zip(word1, word2)):
        if letter1 == letter2:
            comparison_array.append('Green')
            # Remove matched letters from remaining_letters
            remaining_letters.remove(letter1)
        else:
            comparison_array.append(None)  # Placeholder for letters not yet evaluated

    # Second pass: find and mark the correct letters in the incorrect position (Yellow)
    for i, letter1 in enumerate(word1):
        if comparison_array[i] is None and letter1 in remaining_letters:
            comparison_array[i] = "Yellow"
            remaining_letters.remove(letter1)

    # Third pass: mark letters not present in word2 (Grey)
    for i, letter1 in enumerate(word1):
        if comparison_array[i] is None:
            comparison_array[i] = "Grey"

    return comparison_array

# Calculate the starting position of the grid
grid_start_x = (screen.get_width() - (grid_width * cell_width)) // 2
grid_start_y = (screen.get_height() - (grid_height * cell_height)) // 2 - 150 # 150 is an offset to make room for the keyboard

# Draw the grid
for row in range(grid_height):
    for col in range(grid_width):
        x = grid_start_x + col * cell_width
        y = grid_start_y + row * cell_height
        pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)

# Set up the QWERTY keyboard
qwerty_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

keyboard_width = len(qwerty_layout[0]) * cell_width
keyboard_height = len(qwerty_layout) * cell_height

keyboard_start_x = (screen.get_width() - keyboard_width) // 2
keyboard_start_y = (screen.get_height() - keyboard_height) // 2 + 250

# Draw the QWERTY keyboard
for row_index, row in enumerate(qwerty_layout):
    for col_index, char in enumerate(row):
        # Apply an offset to the second and third rows
        if row_index == 1:  # Second row
            key_x = keyboard_start_x + col_index * cell_width + cell_width // 2
        elif row_index == 2:  # Third row
            key_x = keyboard_start_x + col_index * cell_width + cell_width
        else:
            key_x = keyboard_start_x + col_index * cell_width
        key_y = keyboard_start_y + row_index * cell_height
        pygame.draw.rect(screen, GRID_COLOUR, (key_x, key_y, cell_width, cell_height), border_width)
        text = font.render(char, True, TEXT_COLOUR)
        text_rect = text.get_rect(center=(key_x + cell_width // 2, key_y + cell_height // 2))
        screen.blit(text, text_rect)

# Initialize row and column
row = 0
col = 0

# Initialize key log
key_log = [None] * grid_width

# Create a dictionary to store guessed letters and their colours
guessed_letters = {}

# Game state variable
game_won = False
game_lost = False

# Update display
pygame.display.update()

# Run game loop
running = True

# Track if a word has been entered
word_entered = False  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard input
        if event.type == pygame.KEYDOWN and event.unicode.isalpha() and (game_won == False and game_lost == False) and event.key != pygame.K_RETURN:
            # Get the key that was pressed
            key = pygame.key.name(event.key).upper()
            key_log[col] = str(key)

            # Set the text of the grid cell to the key pressed
            text = font.render(str(key), True, TEXT_COLOUR)

            # Calculate the position of the grid cell based on the current row and column
            x = grid_start_x + col * cell_width
            y = grid_start_y + row * cell_height

            # Draw the updated grid cell
            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))

            # Increment the current cell by 1
            col += 1

            # Update the display
            pygame.display.update()

            # Check if the word player has input exists in the dictionary
            if col >= grid_width:
                word_entered = True  # Set word_entered to True after the user has entered a word
        
        # Handle backspace key input
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if col > 0:
                col -= 1
                key_log[col] = None
                # Clear the cell
                x = grid_start_x + col * cell_width
                y = grid_start_y + row * cell_height
                pygame.draw.rect(screen, BACKGROUND_COLOUR, (x, y, cell_width, cell_height))
                pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                pygame.display.update()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if word_entered:
                if "".join(key_log) not in open('words.txt').read().upper():
                    # Clear the key log
                    for i in range(grid_width):
                        if key_log[i] is not None:
                            key_log[i] = None          

                    # Redraw the grid
                    for col in range(grid_width):
                        x = grid_start_x + col * cell_width
                        y = grid_start_y + row * cell_height
                        pygame.draw.rect(screen, BACKGROUND_COLOUR, (x, y, cell_width, cell_height))
                        pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                    
                    # Reset the column and row
                    col = 0

                else:
                    # Check if the collected keys equal todays_word
                    position_array = compare_words("".join(key_log), todays_word)
                    # Check if the player has won
                    if all(position_array[i] == "Green" for i in range(len(position_array))):
                        # Set the winning row
                        winning_row = row
                        # Colour the cells in the selected row
                        for col in range(grid_width):
                            x = grid_start_x + col * cell_width
                            y = grid_start_y + winning_row * cell_height
                            text = font.render(key_log[col], True, TEXT_COLOUR)
                            pygame.draw.rect(screen, GREEN, (x, y, cell_width, cell_height))
                            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))
                        game_won = True
                    else:
                        # Colour the cells in the selected row
                        for col in range(grid_width):
                            x = grid_start_x + col * cell_width
                            y = grid_start_y + row * cell_height
                            text = font.render(key_log[col], True, TEXT_COLOUR)
                            if position_array[col] == "Green":
                                pygame.draw.rect(screen, GREEN, (x, y, cell_width, cell_height))
                            elif position_array[col] == "Yellow":
                                pygame.draw.rect(screen, YELLOW, (x, y, cell_width, cell_height))
                            elif position_array[col] == "Grey":
                                pygame.draw.rect(screen, GREY, (x, y, cell_width, cell_height))
                            #Redraw the border
                            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))
                    
                    # Update guessed_letters dictionary with the guessed letters and their colours
                    for i, letter in enumerate(key_log):
                        if letter not in guessed_letters:
                            guessed_letters[letter] = position_array[i]
                        elif letter in guessed_letters:
                            if guessed_letters[letter] == "Grey" and position_array[i] != "Grey":
                                guessed_letters[letter] = position_array[i]
                            elif guessed_letters[letter] == "Yellow" and position_array[i] == "Green":
                                guessed_letters[letter] = position_array[i]
                    
                    # Redraw the keyboard with updated colours
                    for row_index, keyboard_row in enumerate(qwerty_layout):
                        for col_index, char in enumerate(keyboard_row):
                            # Apply an offset to the second and third rows
                            if row_index == 1:  # Second row
                                key_x = keyboard_start_x + col_index * cell_width + cell_width // 2
                            elif row_index == 2:  # Third row
                                key_x = keyboard_start_x + col_index * cell_width + cell_width
                            else:
                                key_x = keyboard_start_x + col_index * cell_width
                            key_y = keyboard_start_y + row_index * cell_height
                            # Determine the colour for the current key based on comparison result
                            if char in guessed_letters:
                                if guessed_letters[char] == "Green":
                                    colour = GREEN
                                elif guessed_letters[char] == "Yellow":
                                    colour = YELLOW
                                elif guessed_letters[char] == "Grey":   
                                    colour = GREY
                            else:
                                colour = BACKGROUND_COLOUR  # Default colour
                            pygame.draw.rect(screen, colour, (key_x, key_y, cell_width, cell_height))
                            pygame.draw.rect(screen, GRID_COLOUR, (key_x, key_y, cell_width, cell_height), border_width)
                            text = font.render(char, True, TEXT_COLOUR)
                            text_rect = text.get_rect(center=(key_x + cell_width // 2, key_y + cell_height // 2))
                            screen.blit(text, text_rect)

                    # Reset the row and column
                    col = 0
                    row += 1
                    # Check if the player has lost
                    if row >= grid_height and game_won == False:
                        game_lost = True
                        # Display the word and end the game
                        screen.fill(BACKGROUND_COLOUR)
                        text = font.render("You lost! The word was: " + todays_word, True, TEXT_COLOUR)
                        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        break
                    elif game_won == True:
                        # Display the word and end the game
                        screen.fill(BACKGROUND_COLOUR)
                        text = font.render("You won! The word was: " + todays_word, True, TEXT_COLOUR)
                        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        break

            # Update the display
            pygame.display.update()

# quit pygame
pygame.quit()

