import tkinter as tk
from tkinter import messagebox

# Data for the app
users = {
    "user1": "password1",
    "user2": "password2",
}

questions = [
    ("1. How often do you feel down, depressed, or hopeless? 😔", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("2. Do you feel little interest or pleasure in doing things? 🎨", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("3. Do you struggle with sleep (too much or too little)? 😴", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("4. Do you experience feelings of anxiety or panic? 😰", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("5. Do you feel tired or have little energy? 🔋", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("6. Do you have difficulty concentrating? 📚", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("7. Do you feel bad about yourself — or that you are a failure? 😢", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("8. Do you feel isolated or lonely? 🧍‍♂️", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("9. Do you experience mood swings? 🌦️", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("10. Have you lost interest in activities you once enjoyed? 🎶", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
]

score_map = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

class MentalHealthChatbotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎀 Mental Health Buddy 🎀")
        self.geometry("600x450")
        self.resizable(False, False)
        self.configure(bg="#f0e6f7")  # pastel background

        # Data: answers stored by index (None means unanswered)
        self.answers = [None]*len(questions)
        self.current_question_index = 0

        # Setup frames container
        self.frames = {}

        # Setup all frames (pages)
        for F in (LoginPage, QuestionPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def login_successful(self):
        self.current_question_index = 0
        self.answers = [None]*len(questions)
        self.frames["QuestionPage"].load_question(self.current_question_index)
        self.show_frame("QuestionPage")

    def submit_answers(self):
        # Check all questions answered:
        if None in self.answers:
            messagebox.showwarning("⚠️ Warning", "Please answer all questions before submitting.")
            return

        # Calculate score
        score = sum(score_map[ans] for ans in self.answers if ans in score_map)

        if score <= 10:
            result_msg = "😊 You're doing great! Keep practicing self-care and stay positive!"
            color = "#2e7d32"  # Green
        elif score <= 20:
            result_msg = "😌 You're doing okay, but some extra support and relaxation could help."
            color = "#fb8c00"  # Orange
        else:
            result_msg = "😟 It seems like you're going through a tough time. Please consider reaching out to a therapist."
            color = "#c2185b"  # Dark Pink

        self.frames["ResultPage"].show_result(result_msg, color, score)
        self.show_frame("ResultPage")

    def restart(self):
        self.answers = [None]*len(questions)
        self.current_question_index = 0
        self.frames["QuestionPage"].load_question(self.current_question_index)
        self.show_frame("QuestionPage")

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#d8b4f2")  # purple pastel bg

        tk.Label(self, text="Welcome to Mental Health Buddy 💬", font=("Helvetica", 18, "bold"),
                 bg="#d8b4f2", fg="#45046e").pack(pady=30)

        tk.Label(self, text="Login", font=("Arial", 14, "bold"),
                 bg="#d8b4f2", fg="#2c0735").pack(pady=10)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        username_label = tk.Label(self, text="Username:", bg="#d8b4f2", fg="#2c0735", font=("Arial", 12))
        username_label.pack(pady=(10, 0))
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Password:", bg="#d8b4f2", fg="#2c0735", font=("Arial", 12))
        password_label.pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        login_btn = tk.Button(self, text="Login", bg="#7b36c3", fg="white", font=("Arial", 12, "bold"),
                              command=self.check_login)
        login_btn.pack(pady=20)

    def check_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        if users.get(username) == password:
            self.controller.login_successful()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

class QuestionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0e6f7")

        self.question_label = tk.Label(self, text="", font=("Arial", 16, "bold"),
                                       wraplength=550, justify="center", bg="#f0e6f7", fg="#5a1d96")
        self.question_label.pack(pady=(30, 20))

        self.answer_var = tk.StringVar()

        self.options_frame = tk.Frame(self, bg="#f0e6f7")
        self.options_frame.pack()

        nav_frame = tk.Frame(self, bg="#f0e6f7")
        nav_frame.pack(pady=30)

        self.prev_button = tk.Button(nav_frame, text="⬅️ Previous", font=("Arial", 14, "bold"),
                                     bg="#a08ad6", fg="white", command=self.previous_question)
        self.prev_button.grid(row=0, column=0, padx=25)

        self.next_button = tk.Button(nav_frame, text="Next ➡️", font=("Arial", 14, "bold"),
                                     bg="#7b36c3", fg="white", command=self.next_question)
        self.next_button.grid(row=0, column=1, padx=25)

        self.submit_button = tk.Button(self, text="✅ Submit", font=("Arial", 16, "bold"),
                                       bg="#c72c6c", fg="white", command=self.submit_answers)
        self.submit_button.pack(pady=(0,30))

    def load_question(self, q_index):
        q_text, options = questions[q_index]
        self.question_label.config(text=q_text)
        self.answer_var.set(self.controller.answers[q_index] if self.controller.answers[q_index] else "")

        # Clear old radiobuttons
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for option in options:
            rb = tk.Radiobutton(self.options_frame, text=option, variable=self.answer_var, value=option,
                                font=("Arial", 14), bg="#f0e6f7", fg="#3a0ca3", selectcolor="#e0c3fc",
                                activebackground="#d4bff9", cursor="hand2", command=self.option_selected)
            rb.pack(anchor="w", pady=4)

        self.update_buttons()

    def option_selected(self):
        self.controller.answers[self.controller.current_question_index] = self.answer_var.get()
        self.update_buttons()

    def update_buttons(self):
        i = self.controller.current_question_index
        # Previous enabled if not first question
        self.prev_button.config(state=tk.NORMAL if i > 0 else tk.DISABLED)

        # Next enabled only if current question is answered and not last question
        if self.answer_var.get() and i < len(questions)-1:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

        # Submit enabled only if last question and answered
        if i == len(questions)-1 and self.answer_var.get():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def next_question(self):
        if not self.answer_var.get():
            messagebox.showwarning("⚠️ Warning", "Please select an option before moving forward!")
            return

        self.controller.answers[self.controller.current_question_index] = self.answer_var.get()
        self.controller.current_question_index += 1
        self.load_question(self.controller.current_question_index)

    def previous_question(self):
        self.controller.current_question_index -= 1
        self.load_question(self.controller.current_question_index)

    def submit_answers(self):
        if not self.answer_var.get():
            messagebox.showwarning("⚠️ Warning", "Please select an option before submitting!")
            return

        self.controller.answers[self.controller.current_question_index] = self.answer_var.get()
        self.controller.submit_answers()

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0e6f7")

        self.result_label = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#f0e6f7")
        self.result_label.pack(pady=30)

        self.detail_label = tk.Label(self, text="", font=("Arial", 14), wraplength=580, justify="center", bg="#f0e6f7")
        self.detail_label.pack(pady=20)

        self.therapists_frame = tk.Frame(self, bg="#f0e6f7")
        self.therapists_frame.pack(pady=10)

        self.restart_button = tk.Button(self, text="🔄 Restart", font=("Arial", 14, "bold"),
                                        bg="#b40d57", fg="white", command=self.controller.restart)
        self.restart_button.pack(pady=20)

    def show_result(self, message, color, score):
        self.result_label.config(text="🌟 Your Mental Health Result 🌟", fg=color)
        self.detail_label.config(text=message, fg=color)

        # Clear previous therapist listings
        for widget in self.therapists_frame.winfo_children():
            widget.destroy()

        if score > 20:
            tk.Label(self.therapists_frame, text="Here are some therapists you can contact: 📞",
                     font=("Arial", 14, "bold"), bg="#f0e6f7", fg="#7b1fa2").pack(pady=5)

            therapists = [
                "🌼 Dr. Emily Watson - 8453828624",
                "🌻 MindCare Clinic - 6348652327",
                "🌸 Hope Mental Health - 6378248392",
                "🌺 Wellness Center - 9473027465",
                "🌷 Peaceful Mind Therapy - 0373648839"
            ]
            for therapist in therapists:
                tk.Label(self.therapists_frame, text=therapist, font=("Arial", 12), bg="#f0e6f7").pack(anchor="w")

if __name__ == "__main__":
    app = MentalHealthChatbotApp()
    app.mainloop()

