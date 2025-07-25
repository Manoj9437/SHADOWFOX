import tkinter as tk
from tkinter import messagebox
import random

# Modified word pool with new words for each difficulty
WORD_POOL = {
    "EASY": [
        "APPLE", "BALL", "CAT", "DOLL", "EASY", "FORK", "GIFT", "HAT", "ICE", "JUMP",
        "KING", "LAMP", "MOON", "NEST", "OPEN", "PEAR", "QUICK", "RAIN", "SUN", "TOY",
        "VAN", "WIND", "YARN", "ZEBRA", "ZERO", "FROG", "DOG", "CUP", "BIRD", "STAR"
    ],
    "MEDIUM": [
        "PYRAMID", "GARDEN", "ORCHARD", "TRAVEL", "FARMING", "DOCTOR", "BRIDGE", "FLOWER", "RAINFOREST", "MOUNTAIN",
        "KEYBOARD", "BICYCLE", "PICTURE", "FURNACE", "JOURNAL", "LIBRARY", "WEATHER", "HISTORY", "SCIENCE", "EXPLORE",
        "FOREST", "RIVER", "CASTLE", "MONKEY", "PENCIL", "DESERT", "VOLCANO", "ZEBRA", "SCHOOL", "TRAFFIC"
    ],
    "HARD": [
        "PROGRAMMING", "ALGORITHM", "DIFFICULTY", "ENIGMATIC", "ZEPHYR", "QUASAR", "JUXTAPOSE", "KALEIDOSCOPE",
        "MNEMONIC", "PHOENIX", "RHAPSODY", "SYNCHRONIZE", "XENOPHOBIA", "WHISPERING", "CRYPTOGRAPHY", "PARADOXICAL",
        "ABYSS", "VORTEX", "SYZYGY", "FLUMMOX", "HYPOTHESIS", "JUBILANT", "OBFUSCATE", "QUINTESSENCE", "SERENDIPITY",
        "TRANQUILITY", "UBIQUITOUS", "VICARIOUS", "WINSOME", "YIELDING"
    ]
}

DIFFICULTY_PARAMS = {
    "EASY": {
        "max_attempts": 10,
        "hint_uses": 2,
        "hint_letters": 1,
        "starting_reveal": 1
    },
    "MEDIUM": {
        "max_attempts": 7,
        "hint_uses": 2,
        "hint_letters": 1,
        "starting_reveal": (1, 2)
    },
    "HARD": {
        "max_attempts": 5,
        "hint_uses": 1,
        "hint_letters": 1,
        "starting_reveal": (2, 3)
    }
}

class HangmanApp:
    def __init__(self, root):
        self.root = root
        root.title("Hangman Game")
        root.geometry("700x650")
        root.configure(bg="#f0f0f0")

        self.secret_word = ""
        self.visible_word = []
        self.guessed_chars = set()
        self.guessed_full_words = set()
        self.remaining_tries = 0
        self.total_tries = 0
        self.available_hints = 0
        self.chars_per_hint = 0
        self.difficulty_level = tk.StringVar(value="EASY")

        self._create_widgets()
        self._initialize_game()

    def _create_widgets(self):
        tk.Label(self.root, text="HANGMAN", font=("Arial", 36, "bold"), bg="#f0f0f0", fg="#4CAF50").pack(pady=10)

        diff_frame = tk.Frame(self.root, bg="#f0f0f0")
        diff_frame.pack(pady=5)
        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 12), bg="#f0f0f0", fg="#333333").pack(side=tk.LEFT)

        for label, val in [("Easy", "EASY"), ("Medium", "MEDIUM"), ("Hard", "HARD")]:
            rb = tk.Radiobutton(
                diff_frame, text=label, variable=self.difficulty_level, value=val,
                command=self._initialize_game,
                font=("Arial", 10), bg="#f0f0f0", fg="#333333", selectcolor="#d4edda", indicatoron=0,
                borderwidth=2, width=8, relief=tk.RAISED
            )
            rb.pack(side=tk.LEFT, padx=5)

        self.hangman_canvas = tk.Canvas(self.root, width=250, height=250, bg="white", bd=2, relief=tk.SUNKEN)
        self.hangman_canvas.pack(pady=10)

        self.word_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.word_var, font=("Courier", 32, "bold"), bg="#f0f0f0", fg="#0056b3").pack(pady=10)

        self.tries_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.tries_var, font=("Arial", 14), bg="#f0f0f0", fg="#c0392b").pack()

        self.hints_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.hints_var, font=("Arial", 14), bg="#f0f0f0", fg="#2980b9").pack()

        self.guessed_letters_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.guessed_letters_var, font=("Arial", 12), bg="#f0f0f0", fg="#555555", wraplength=600).pack()

        self.guessed_words_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.guessed_words_var, font=("Arial", 12), bg="#f0f0f0", fg="#555555", wraplength=600).pack()

        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=15)

        self.entry_guess = tk.Entry(input_frame, width=15, font=("Arial", 16), justify="center")
        self.entry_guess.pack(side=tk.LEFT, padx=5)
        self.entry_guess.bind("<Return>", self._process_guess_event)

        self.btn_guess = tk.Button(
            input_frame, text="Guess", command=self._process_guess, font=("Arial", 14),
            bg="#2ecc71", fg="white", activebackground="#27ae60", relief=tk.RAISED, bd=2
        )
        self.btn_guess.pack(side=tk.LEFT, padx=5)

        self.btn_hint = tk.Button(
            input_frame, text="Hint", command=self._reveal_hint, font=("Arial", 14),
            bg="#3498db", fg="white", activebackground="#2980b9", relief=tk.RAISED, bd=2
        )
        self.btn_hint.pack(side=tk.LEFT, padx=5)

        self.btn_new_game = tk.Button(
            self.root, text="New Game", command=self._initialize_game,
            font=("Arial", 14), bg="#e67e22", fg="white", activebackground="#d35400",
            relief=tk.RAISED, bd=2
        )
        self.btn_new_game.pack(pady=10)

    def _select_word_and_params(self, difficulty):
        params = DIFFICULTY_PARAMS[difficulty]
        picked_word = random.choice(WORD_POOL[difficulty]).upper()
        visible = ["_" for _ in picked_word]
        guessed_chars = set()

        reveal = params["starting_reveal"]
        if isinstance(reveal, tuple):
            reveal = random.randint(reveal[0], reveal[1])

        unique_letters = list(set(picked_word))
        reveal_count = min(reveal, len(unique_letters))
        if reveal_count > 0:
            letters_to_show = random.sample(unique_letters, reveal_count)
            for reveal_char in letters_to_show:
                for i, ch in enumerate(picked_word):
                    if ch == reveal_char:
                        visible[i] = ch
                guessed_chars.add(reveal_char)

        return (picked_word, params["max_attempts"], params["hint_uses"],
                params["hint_letters"], visible, guessed_chars)

    def _initialize_game(self):
        level = self.difficulty_level.get()
        self.secret_word, self.total_tries, self.available_hints, \
        self.chars_per_hint, self.visible_word, self.guessed_chars = self._select_word_and_params(level)

        self.remaining_tries = self.total_tries
        self.guessed_full_words = set()

        self._refresh_ui()
        self._draw_hangman()
        self.entry_guess.delete(0, tk.END)
        self.entry_guess.config(state=tk.NORMAL)
        self.btn_guess.config(state=tk.NORMAL)
        self.btn_hint.config(state=tk.NORMAL if self.available_hints > 0 else tk.DISABLED)
        self.entry_guess.focus_set()

    def _refresh_ui(self):
        self.word_var.set(" ".join(self.visible_word))
        self.tries_var.set(f"Tries Left: {self.remaining_tries} / {self.total_tries}")
        self.hints_var.set(f"Hints Left: {self.available_hints}")
        self.guessed_letters_var.set(f"Guessed Letters: {', '.join(sorted(self.guessed_chars))}")
        self.guessed_words_var.set(f"Guessed Words: {', '.join(sorted(self.guessed_full_words))}")

    def _draw_hangman(self):
        self.hangman_canvas.delete("all")
        wrong_guesses = self.total_tries - self.remaining_tries

        self.hangman_canvas.create_line(50, 240, 150, 240, width=2)   # Base
        self.hangman_canvas.create_line(100, 240, 100, 40, width=2)   # Pole
        self.hangman_canvas.create_line(100, 40, 200, 40, width=2)    # Beam
        self.hangman_canvas.create_line(200, 40, 200, 70, width=2)    # Rope

        max_parts = 6

        if wrong_guesses > 0:  # Head
            self.hangman_canvas.create_oval(180, 70, 220, 110, outline="black", width=2)
        if wrong_guesses > (1 * self.total_tries / max_parts):  # Body
            self.hangman_canvas.create_line(200, 110, 200, 170, width=2)
        if wrong_guesses > (2 * self.total_tries / max_parts):  # Left Arm
            self.hangman_canvas.create_line(200, 130, 170, 150, width=2)
        if wrong_guesses > (3 * self.total_tries / max_parts):  # Right Arm
            self.hangman_canvas.create_line(200, 130, 230, 150, width=2)
        if wrong_guesses > (4 * self.total_tries / max_parts):  # Left Leg
            self.hangman_canvas.create_line(200, 170, 170, 210, width=2)
        if wrong_guesses > (5 * self.total_tries / max_parts):  # Right Leg
            self.hangman_canvas.create_line(200, 170, 230, 210, width=2)

    def _process_guess_event(self, event):
        self._process_guess()

    def _process_guess(self):
        attempt = self.entry_guess.get().upper().strip()
        self.entry_guess.delete(0, tk.END)

        if not attempt:
            messagebox.showwarning("Wrong Input", "Please input a letter or word.")
            return

        if not attempt.isalpha():
            messagebox.showwarning("Wrong Input", "Only alphabetic characters allowed.")
            return

        if len(attempt) == 1:
            if attempt in self.guessed_chars:
                messagebox.showinfo("Repeated", f"You already guessed '{attempt}'.")
                return
            if attempt in self.secret_word:
                self.guessed_chars.add(attempt)
                for idx, ch in enumerate(self.secret_word):
                    if ch == attempt:
                        self.visible_word[idx] = ch
            else:
                self.guessed_chars.add(attempt)
                self.remaining_tries -= 1

        elif len(attempt) == len(self.secret_word):
            if attempt in self.guessed_full_words:
                messagebox.showinfo("Repeated", f"You already tried the word '{attempt}'.")
                return
            if attempt == self.secret_word:
                self.visible_word = list(self.secret_word)
            else:
                self.guessed_full_words.add(attempt)
                self.remaining_tries -= 1
        else:
            messagebox.showwarning("Wrong Input", "Guess a single letter or the complete word.")

        self._refresh_ui()
        self._draw_hangman()
        self._check_end_condition()

    def _reveal_hint(self):
        if self.available_hints <= 0:
            messagebox.showinfo("Hints Over", "You have no hints left.")
            return

        unrevealed = [ch for i, ch in enumerate(self.secret_word) if self.visible_word[i] == "_"]

        if not unrevealed:
            messagebox.showinfo("All Revealed", "You have revealed most of the word.")
            return

        count_to_reveal = min(len(set(unrevealed)), self.chars_per_hint)
        hint_letters = random.sample(list(set(unrevealed)), count_to_reveal)

        for letter in hint_letters:
            if letter not in self.guessed_chars:
                self.guessed_chars.add(letter)
                for i, ch in enumerate(self.secret_word):
                    if ch == letter:
                        self.visible_word[i] = ch

        self.available_hints -= 1
        if self.available_hints == 0:
            self.btn_hint.config(state=tk.DISABLED)

        self._refresh_ui()
        self._check_end_condition()

    def _check_end_condition(self):
        if "_" not in self.visible_word:
            messagebox.showinfo("Victory!", f"You won! The word was: {self.secret_word}")
            self._lock_controls()
        elif self.remaining_tries <= 0:
            messagebox.showinfo("Defeat", f"No tries left. The word was: {self.secret_word}")
            self._lock_controls()

    def _lock_controls(self):
        self.entry_guess.config(state=tk.DISABLED)
        self.btn_guess.config(state=tk.DISABLED)
        self.btn_hint.config(state=tk.DISABLED)

if __name__ == "__main__":
    app_window = tk.Tk()
    HangmanApp(app_window)
    app_window.mainloop()
