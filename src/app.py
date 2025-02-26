from tkinter import Tk, Frame, Label, Button, StringVar, CENTER, Entry
import json
import os
import random
from flashcard import Flashcard  # Import Flashcard class

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flashcard Quiz App")
        self.master.configure(bg="#FFFAF0")  # Light cream background
        self.master.geometry("600x400")  # Set fixed window size
        self.master.resizable(False, False)  # Disable resizing

        self.flashcards = self.load_flashcards()
        self.current_index = 0
        self.quiz_mode = False

        self.top_frame = Frame(self.master, bg="#FFFAF0")
        self.top_frame.pack(pady=10)

        self.toggle_quiz_button = Button(self.top_frame, text="Toggle Quiz Mode", command=self.toggle_quiz_mode, bg="#FFB6C1", fg="white", font=("Helvetica", 12, "bold"), highlightbackground="#FF69B4", highlightthickness=2)
        self.toggle_quiz_button.pack()

        self.card_frame = Frame(self.master, bg="#FFFAF0")
        self.card_frame.pack(pady=20, padx=20, expand=True)

        self.question_var = StringVar()
        self.answer_var = StringVar()
        self.is_flipped = False

        self.question_label = Label(self.card_frame, textvariable=self.question_var, font=("Helvetica", 24), wraplength=400, bg="#FFFAF0", fg="#FF69B4", justify=CENTER)
        self.question_label.pack(pady=10)
        self.question_label.bind("<Button-1>", self.flip_card)

        self.answer_entry = Entry(self.card_frame, font=("Helvetica", 18))
        self.answer_entry.pack(pady=10)
        self.answer_entry.pack_forget()  # Hide initially

        self.check_button = Button(self.card_frame, text="Check Answer", command=self.check_answer, bg="#FFB6C1", fg="white", font=("Helvetica", 12, "bold"), highlightbackground="#FF69B4", highlightthickness=2)
        self.check_button.pack(pady=10)
        self.check_button.pack_forget()  # Hide initially

        self.unknown_button = Button(self.card_frame, text="Mark as Unknown", command=self.mark_unknown, bg="#FF6347", fg="white", font=("Helvetica", 12, "bold"), highlightbackground="#FF4500", highlightthickness=2)
        self.unknown_button.pack(pady=10)

        button_style = {"bg": "#FFB6C1", "fg": "white", "font": ("Helvetica", 12, "bold"), "highlightbackground": "#FF69B4", "highlightthickness": 2}

        self.nav_frame = Frame(self.master, bg="#FFFAF0")
        self.nav_frame.pack(pady=10)

        self.prev_button = Button(self.nav_frame, text="Previous", command=self.prev_card, **button_style)
        self.prev_button.pack(side="left", padx=20)

        self.next_button = Button(self.nav_frame, text="Next", command=self.next_card, **button_style)
        self.next_button.pack(side="left", padx=20)

        self.action_frame = Frame(self.master, bg="#FFFAF0")
        self.action_frame.pack(pady=10)

        self.shuffle_button = Button(self.action_frame, text="Shuffle", command=self.shuffle_flashcards, **button_style)
        self.shuffle_button.pack(side="left", padx=20)

        self.known_button = Button(self.action_frame, text="Mark as Known", command=self.mark_known, **button_style)
        self.known_button.pack(side="left", padx=20)

        self.show_question()

    def load_flashcards(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'flashcards.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Flashcard(item['question'], item['answer']) for item in data]

    def show_question(self):
        self.is_flipped = False
        self.question_var.set(self.flashcards[self.current_index].get_question())
        self.answer_var.set(self.flashcards[self.current_index].get_answer())
        self.answer_entry.delete(0, 'end')

    def flip_card(self, event=None):
        if self.is_flipped:
            self.question_var.set(self.flashcards[self.current_index].get_question())
        else:
            self.question_var.set(self.flashcards[self.current_index].get_answer())
        self.is_flipped = not self.is_flipped

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.flashcards[self.current_index].get_answer().strip().lower()
        if user_answer == correct_answer:
            self.question_var.set("Correct!")
        else:
            self.question_var.set(f"Incorrect! The correct answer is: {self.flashcards[self.current_index].get_answer()}")

    def next_card(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.current_index = 0
            self.show_question()

    def prev_card(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()
        else:
            self.current_index = len(self.flashcards) - 1
            self.show_question()

    def shuffle_flashcards(self):
        random.shuffle(self.flashcards)
        self.current_index = 0
        self.show_question()

    def toggle_quiz_mode(self):
        self.quiz_mode = not self.quiz_mode
        if self.quiz_mode:
            self.answer_entry.pack(pady=10)
            self.check_button.pack(pady=10)
        else:
            self.answer_entry.pack_forget()
            self.check_button.pack_forget()

    def mark_known(self):
        self.flashcards[self.current_index].mark_known()
        self.next_card()

    def mark_unknown(self):
        self.flashcards[self.current_index].mark_unknown()
        self.next_card()

if __name__ == "__main__":
    root = Tk()
    app = FlashcardApp(root)
    root.mainloop()