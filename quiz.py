#Python program for basic quiz using tkinter
import tkinter as tk
import random

#Creation of Initial introductory window
class WelcomeWindow:
    def __init__(self):
        self.welcome_root = tk.Tk()
        self.welcome_root.title("Welcome to the Quiz")
        self.welcome_root.geometry("400x300")
        self.welcome_root.configure(bg="white")

        self.welcome_label = tk.Label(self.welcome_root, text="Welcome to the Quiz!", font=("Castellar", 16,"bold"), bg="white")
        self.welcome_label.pack(pady=20)

        self.name_label = tk.Label(self.welcome_root, text="Enter your name:", font=("Arial", 12), bg="white")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.welcome_root, font=("", 10), width=30)
        self.name_entry.pack(pady=10)

        self.submit_button = tk.Button(self.welcome_root, text="Submit",bg="gold", command=self.start_quiz)
        self.submit_button.pack()

        self.welcome_root.mainloop()

    def start_quiz(self):
        participant_name = self.name_entry.get()
        self.welcome_root.destroy()  # Close the welcome window
        root = tk.Tk()
        app = QuizApp(root, participant_name)
        root.mainloop()

#Main Quiz code
class QuizApp:
    def __init__(self, root, participant_name):
        self.root = root
        self.root.title("Basic Quiz Game")
        self.root.geometry("600x400")  # Adjusted to accommodate the left panel
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.participant_name = participant_name

#easy to change questions
        self.questions = [
            {
                "question": "Which place have the monument called Arc de Triomphe?",
                "options": ["Paris", "Berlin", "Rome", "Madrid"],
                "answer": "Paris"
            },
            {
                "question": "What is the national flower of Japan?",
                "options": ["Orchid", "Sakura", "Daisy", "Rose"],
                "answer": "Sakura"
            },
            {
                "question": "What is the largest ocean in the world?",
                "options": ["Atlantic Ocean", "Pacific Ocean", "Indian Ocean", "Arctic Ocean"],
                "answer": "Pacific Ocean"
            },
            {
                "question": "Which planet has the most moons?",
                "options": ["Mars", "Earth", "Saturn", "Venus"],
                "answer": "Saturn"
            },
            {
                "question": "When was Netflix founded?",
                "options": ["1997", "2001", "2018", "2006"],
                "answer": "1997"
            }
        ]

        self.current_question = 0
        self.score = 0
        self.total_questions = len(self.questions)
        self.right_answers = 0

        self.setup_ui()
#code to display total number of questions
    def setup_ui(self):
        self.left_panel = tk.Frame(self.root, bg="lightgray", width=100)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.question_labels = []
        for i in range(self.total_questions):
            question_num = "Q" + str(i + 1)
            question_label = tk.Label(self.left_panel, text=question_num, font=("Arial", 10), bg="white", borderwidth=1, relief="solid", padx=5)
            question_label.pack(anchor=tk.W)
            self.question_labels.append(question_label)

        self.right_panel = tk.Frame(self.root, bg="white")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.question_label = tk.Label(self.right_panel, text="", font=("Arial", 12, "bold"), bg="white")
        self.question_label.pack(pady=20)
#color changing buttons
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.right_panel, text="", width=30, bg="sky blue", command=lambda idx=i: self.check_answer(idx))
            btn.bind("<Enter>", lambda event, btn=btn: btn.config(bg="light green"))
            btn.bind("<Leave>", lambda event, btn=btn: btn.config(bg="sky blue"))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.feedback_label = tk.Label(self.right_panel, text="", font=("Arial", 10), bg="white")
        self.feedback_label.pack(pady=10)

        self.score_label = tk.Label(self.right_panel, text="Score: 0/0", font=("Arial", 10), bg="white")
        self.score_label.pack(pady=5)

        self.display_question()

    def display_question(self):
        if self.current_question < self.total_questions:
            question_data = self.questions[self.current_question]

            self.question_label.config(text=question_data['question'])

            for i in range(4):
                self.option_buttons[i].config(text=question_data['options'][i])

            for idx, label in enumerate(self.question_labels):
                label.config(bg="white")
            self.question_labels[self.current_question].config(bg="lightblue")

            if self.current_question < self.total_questions - 1:
                if not hasattr(self, 'skip_button'):
                    self.skip_button = tk.Button(self.right_panel, text="Skip", command=self.skip_question, bg="lightcoral")
                    self.skip_button.pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            self.show_result("Quiz Completed!")

    def check_answer(self, selected_option):
        question_data = self.questions[self.current_question]

        chosen_answer = question_data['options'][selected_option]
        correct_answer = question_data['answer']

        if chosen_answer == correct_answer:
            self.score += 1
            self.right_answers += 1
            feedback = "Correct!"
        else:
            feedback = f"Wrong! Correct answer: {correct_answer}"

        self.current_question += 1
        self.display_question()
        
        self.feedback_label.config(text=feedback)
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
#results page
    def show_result(self, feedback):
        self.change_background_color()

        success_rate = (self.right_answers / self.total_questions) * 100
        result_message = ""

        if success_rate >= 70:
            result_message = "★★★\n Excellent"
        elif 50 <= success_rate < 70:
            result_message = "★★\n Good Job"
        elif 40 <= success_rate < 50:
            result_message = "★\n Can do better!!"
        elif success_rate < 40:
            result_message = "Better luck next time"
        elif success_rate == 0:
            result_message = " Sorry you Failed "

        self.clear_quiz()
        result_text = f"Final Score: {self.right_answers}/{self.total_questions}\n"
        result_text += f"{feedback}\n"

        result_text += f"{result_message if result_message else 'No badge'}"
        self.result_label = tk.Label(self.right_panel, text=result_text, font=("Arial", 12), bg="white")
        self.result_label.pack(expand=True, pady=20)

        self.go_home_button = tk.Button(self.right_panel, text="Go to Home",bg="paleturquoise", command=self.return_to_home)
        self.go_home_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.display_thank_you()
#end note
    def display_thank_you(self):
        thank_you_window = tk.Toplevel(self.root)
        thank_you_window.title("Thank You!")
        thank_you_window.geometry("400x300")
        thank_you_window.configure(bg="white")

        thank_you_label = tk.Label(thank_you_window, text=f"Thank you, {self.participant_name},\n for participating in the quiz!", font=("Arial", 12,"bold"), bg="white")
        thank_you_label.pack(pady=100)
        
    def change_background_color(self):
        colors = ['white']
        self.root.config(bg=random.choice(colors))
        self.root.after(10000, self.change_background_color)

    def clear_quiz(self):
        self.question_label.pack_forget()
        self.feedback_label.pack_forget()
        self.score_label.pack_forget()

        for btn in self.option_buttons:
            btn.pack_forget()

        if hasattr(self, 'skip_button'):
            self.skip_button.pack_forget()
#function to skip a question
    def skip_question(self):
        if self.current_question < self.total_questions - 1:
            self.current_question += 1
            self.display_question()
        else:
            self.show_result("No more questions to skip.")

    def return_to_home(self):
        self.root.destroy()  # Close the quiz window
        WelcomeWindow()  # Re-open the welcome window

# Starting the application
if __name__ == "__main__":
    WelcomeWindow()
