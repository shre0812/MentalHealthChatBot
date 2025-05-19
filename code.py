import tkinter as tk
from tkinter import messagebox

therapists = [
    "🌼 Dr. Emily Watson - 8453828624",
    "🌻 MindCare Clinic - 6348652327",
    "🌸 Hope Mental Health - 6378248392",
    "🌺 Wellness Center - 9473027465",
    "🌷 Peaceful Mind Therapy - 0373648839"
]

questions = [
    ("How often do you feel down, depressed, or hopeless? 😔", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you feel little interest or pleasure in doing things? 🎨", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you struggle with sleep (too much or too little)? 😴", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you experience feelings of anxiety or panic? 😰", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you feel tired or have little energy? 🔋", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you have difficulty concentrating? 📚", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you feel bad about yourself — or that you are a failure? 😢", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you feel isolated or lonely? 🧍‍♂️", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Do you experience mood swings? 🌦️", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("Have you lost interest in activities you once enjoyed? 🎶", ["Never", "Rarely", "Sometimes", "Often", "Always"]),

]

score_map = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

class MentalHealthChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("🎀 Mental Health Buddy 🎀")
        self.root.geometry("550x600")
        self.root.configure(bg="#f4f4f4")  # Light background

        self.score = 0
        self.question_index = 0
        self.answers = [None] * len(questions)

        self.title_label = tk.Label(root, text="💬 Welcome to Mental Health Buddy 💬", font=("Bernard MT Condensed", 20, "bold"), bg="#f4f4f4", fg="#d6336c")
        self.title_label.pack(pady=10)

        self.question_label = tk.Label(root, text="", font=("Bradley Hand ITC", 16), wraplength=450, justify="center", bg="#f4f4f4")
        self.question_label.pack(pady=20)

        self.options_var = tk.StringVar()

        self.buttons_frame = tk.Frame(root, bg="#f4f4f4")
        self.buttons_frame.pack()

        self.nav_frame = tk.Frame(root, bg="#f4f4f4")
        self.nav_frame.pack(pady=10)

        self.prev_button = tk.Button(self.nav_frame, text="⬅️ Previous", font=("Arial narrow", 14), command=self.previous_question, bg="#f4f4f4")
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(self.nav_frame, text="Next ➡️", font=("Arial narrow", 14), command=self.next_question, bg="#f4f4f4")
        self.next_button.grid(row=0, column=1, padx=10)

        self.submit_button = tk.Button(root, text="✅ Submit", font=("Arial narrow", 16, "bold"), bg="#f4f4f4", fg="black", command=self.show_result)
        self.submit_button.pack(pady=20)
        self.submit_button.config(state=tk.DISABLED)

        self.update_question()

    def update_question(self):
        self.options_var.set(None)
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        if self.question_index < len(questions):
            q_text, options = questions[self.question_index]
            self.question_label.config(text=q_text)

            for option in options:
                btn = tk.Radiobutton(self.buttons_frame, text=option, font=("Bradley Hand ITC", 14), value=option,
                                     variable=self.options_var, bg="#f4f4f4", fg="#7b1fa2", selectcolor="#f8bbd0",
                                     command=self.option_selected)
                btn.pack(anchor="w", pady=5)

        self.prev_button.config(state=tk.NORMAL if self.question_index > 0 else tk.DISABLED)
        if self.question_index == len(questions) - 1:
            self.next_button.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.NORMAL)
            self.submit_button.config(state=tk.DISABLED)

        # Pre-select if already answered
        if self.answers[self.question_index]:
            self.options_var.set(self.answers[self.question_index])

    def option_selected(self):
        # Enable Next when an option is selected
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        selected = self.options_var.get()
        if not selected:
            messagebox.showwarning("⚠️ Warning", "Please select an option before moving forward!")
            return

        self.answers[self.question_index] = selected
        self.question_index += 1
        self.update_question()

    def previous_question(self):
        self.question_index -= 1
        self.update_question()

    def show_result(self):
        for i, answer in enumerate(self.answers):
            if answer:
                self.score += score_map[answer]

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#f4f4f4")
        result_label = tk.Label(self.root, text="🌟 Your Mental Health Result 🌟", font=("Bernard MT Condensed", 22, "bold"), bg="#f4f4f4", fg="#d6336c")
        result_label.pack(pady=20)

        if self.score <= 10:
            result_text = "😊 You're doing great! Keep practicing self-care and stay positive!"
            color = "#2e7d32"  # Green
        elif self.score <= 20:
            result_text = "😌 You're doing okay, but some extra support and relaxation could help."
            color = "#fb8c00"  # Orange
        else:
            result_text = "😟 It seems like you're going through a tough time. Please consider reaching out to a therapist."
            color = "#c2185b"  # Dark Pink

        final_msg = tk.Label(self.root, text=result_text, font=("Bradley Hand ITC", 16, "bold"), wraplength=450, justify="center", fg=color, bg="#f4f4f4")
        final_msg.pack(pady=20)

        if self.score > 20:
            therapists_label = tk.Label(self.root, text="Here are some therapists you can contact: 📞", font=("Arial narrow", 14), bg="#f4f4f4", fg="#d6336c")
            therapists_label.pack(pady=10)

            for therapist in therapists:
                therapist_label = tk.Label(self.root, text=therapist, font=("Arial narrow", 12), bg="#f4f4f4")
                therapist_label.pack()

        restart_btn = tk.Button(self.root, text="🔄 Restart", font=("Arial narrow", 14), bg="#d6336c", fg="white", command=self.restart)
        restart_btn.pack(pady=20)

    def restart(self):
        self.score = 0
        self.question_index = 0
        self.answers = [None] * len(questions)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.__init__(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthChatbot(root)
    root.mainloop()
