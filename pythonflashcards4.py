import random
import time

def read_flashcards(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        flashcards = {}
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                flashcards[i // 2] = (lines[i].strip(), lines[i + 1].strip())
        return flashcards

def display_flashcard(flashcards, index, show_definition):
    term, definition = flashcards[index]
    text = term if not show_definition else definition

    print(text)

def main():
    flashcards = read_flashcards('flashcards.txt')
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
