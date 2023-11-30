import random
import time
import re

def read_flashcards(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        flashcards = {}
        current_term = None

        for line in lines:
            # Check if the line starts with a number followed by a period using regex
            if re.match(r'^\d+\. ', line.strip()):
                if current_term is not None:
                    flashcards[len(flashcards)] = (current_term, current_definition)
                current_term = line.strip()
                current_definition = ""
            elif current_term is not None:
                # If current_term is set, it means we are reading a definition
                current_definition += line.strip()

        # Add the last flashcard after the loop
        if current_term is not None:
            flashcards[len(flashcards)] = (current_term, current_definition)

        return flashcards



def display_flashcard(flashcards, index, show_definition):
    term, definition = flashcards[index]
    text = term if not show_definition else definition

    print("\n" + text + "\n")

def main():
    filename = input("Enter the name of the text document (e.g., flashcards.txt): ")
    
    try:
        flashcards = read_flashcards(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    num_flashcards = len(flashcards)
    index = 0

    running = True
    show_definition = False
    automatic_play = False
    shuffle_mode = False
    flashcard_keys = list(flashcards.keys())

    show_duration = 2
    automatic_play_interval = show_duration
    last_auto_play_time = time.time()

    while running:
        for event in input("Press W/A/S/D/R/F to navigate or 'q' to quit: "):
            if event.lower() == 'q':
                running = False

            if event.lower() == 'a':
                index = (index - 1) % num_flashcards
                show_definition = False
            elif event.lower() == 'd':
                index = (index + 1) % num_flashcards
                show_definition = False
            elif event.lower() == 'w' or event.lower() == 's':
                show_definition = not show_definition
            elif event.lower() == 'r':
                shuffle_mode = not shuffle_mode
                if shuffle_mode:
                    random.shuffle(flashcard_keys)
                    index = 0
            elif event.lower() == 'f':
                automatic_play = not automatic_play
                last_auto_play_time = time.time() if automatic_play else 0

        if automatic_play and time.time() - last_auto_play_time > automatic_play_interval:
            last_auto_play_time = time.time()
            if automatic_play:
                show_definition = not show_definition
                if show_definition:
                    automatic_play_interval = show_duration
                else:
                    index = (index + 1) % num_flashcards
                    automatic_play_interval = show_duration

        current_index = flashcard_keys[index] if shuffle_mode else index
        display_flashcard(flashcards, current_index, show_definition)

if __name__ == "__main__":
    main()
