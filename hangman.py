import pygame
import time
import sys
import random

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman: The Hound of the Baskervilles")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images
hangman_images = [pygame.image.load(f'C:\\Users\\91990\\Desktop\\intermediate coding\\python\\hangman{i}.jpg') for i in range(7)]
hound_image = pygame.image.load('C:\\Users\\91990\\Desktop\\intermediate coding\\python\\hound.jpg')  # Image of the hound for loss animation
sir_henry_image = pygame.image.load('C:\\Users\\91990\\Desktop\\intermediate coding\\python\\henry.jpg')

# Fonts
font = pygame.font.Font(None, 40)
hint_font = pygame.font.Font(None, 30)

# Words and story stages
story_stages = [
    ("LEGEND", "The curse of the Baskervilles is an ancient legend."),
    ("MOOR", "The moor is eerie, filled with fog and hidden dangers."),
    ("HOUND", "A giant spectral hound is said to haunt the Baskervilles."),
]

# Game variables
stage = 0
word, story_text = story_stages[stage]
guessed = set()
wrong_guesses = 0
max_attempts = 6
ai_help_enabled = False  # AI only helps when the player is struggling

def draw_screen():
    screen.fill(WHITE)
    
    # Draw hangman
    screen.blit(hangman_images[wrong_guesses], (50, 100))
    
    # Draw guessed word
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])
    text_surface = font.render(display_word, True, BLACK)
    screen.blit(text_surface, (300, 200))
    
    # Show story text
    story_surface = hint_font.render(story_text, True, BLUE)
    screen.blit(story_surface, (50, 50))
    
    pygame.display.update()

def iddfs_reveal():
    """Iterative Deepening DFS to reveal letters step by step."""
    for depth in range(1, len(word) + 1):
        dfs_reveal(word, depth)
        time.sleep(1)  # Adds delay for a suspenseful reveal

def dfs_reveal(word, depth, current_depth=0):
    """Recursive DFS letter reveal based on depth."""
    if current_depth == depth:
        return
    guessed.add(word[current_depth])
    draw_screen()
    dfs_reveal(word, depth, current_depth + 1)

def rbfs():
    """Recursive Best-First Search (RBFS) to suggest the most common missing letter."""
    letter_freq = {'E': 13, 'T': 9, 'A': 8, 'O': 7, 'I': 7, 'N': 7, 'S': 6, 'H': 6}
    missing_letters = [l for l in word if l not in guessed]
    
    if missing_letters:
        best_letter = max(missing_letters, key=lambda x: letter_freq.get(x, 0))
        return best_letter
    return None

def fade_to_next_stage():
    """Fades to the next stage once the player completes the current word."""
    global stage, word, story_text, guessed, wrong_guesses, ai_help_enabled
    if stage < len(story_stages) - 1:
        for alpha in range(255, 0, -5):
            screen.fill((alpha, alpha, alpha))
            pygame.display.update()
            time.sleep(0.02)
        stage += 1
        word, story_text = story_stages[stage]
        guessed = set()
        wrong_guesses = 0
        ai_help_enabled = False
    else:
        game_over("You solved the mystery!")

def hound_chase_animation():
    """Animates the hound chasing Sir Henry when the player loses."""
    x_sir_henry, y_sir_henry = 600, 400
    x_hound, y_hound = 50, 400
    
    for _ in range(30):  # Animate for a short duration
        screen.fill(WHITE)
        screen.blit(sir_henry_image, (x_sir_henry, y_sir_henry))
        screen.blit(hound_image, (x_hound, y_hound))
        pygame.display.update()
        time.sleep(0.1)
        x_hound += 15  # Moves the hound towards Sir Henry

def game_over(message):
    """Ends the game with a loss message and hound animation."""
    hound_chase_animation()
    screen.fill(WHITE)
    text_surface = font.render(message, True, RED)
    screen.blit(text_surface, (WIDTH//2 - 100, HEIGHT//2))
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Main game loop
running = True
while running:
    draw_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                letter = event.unicode.upper()
                if letter in word and letter not in guessed:
                    guessed.add(letter)
                else:
                    wrong_guesses += 1
                
                if all(l in guessed for l in word):
                    fade_to_next_stage()
                elif wrong_guesses >= max_attempts:
                    game_over("You lost! The hound got you!")

    # AI Assistance using RBFS (only if player struggles)
    if wrong_guesses >= 3 and not ai_help_enabled:
        ai_help_enabled = True
        time.sleep(1)
        ai_letter = rbfs()
        if ai_letter:
            guessed.add(ai_letter)
            draw_screen()
            time.sleep(1)

pygame.quit()
