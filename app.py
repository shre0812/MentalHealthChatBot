from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

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

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        session['answers'] = [None] * len(questions)
        session['current_question_index'] = 0
        return redirect(url_for('questions'))
    else:
        flash('Invalid username or password!')
        return redirect(url_for('index'))

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer:
            session['answers'][session['current_question_index']] = answer
            session['current_question_index'] += 1

        if session['current_question_index'] >= len(questions):
            return redirect(url_for('result'))

    current_question = questions[session['current_question_index']]
    return render_template('questions.html', question=current_question, index=session['current_question_index'])

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('index'))

    score = sum(score_map[ans] for ans in session['answers'] if ans in score_map)
    if score <= 10:
        result_msg = "😊 You're doing great! Keep practicing self-care and stay positive!"
        color = "#2e7d32"  # Green
    elif score <= 20:
        result_msg = "😌 You're doing okay, but some extra support and relaxation could help."
        color = "#fb8c00"  # Orange
    else:
        result_msg = "😟 It seems like you're going through a tough time. Please consider reaching out to a therapist."
        color = "#c2185b"  # Dark Pink

    return render_template('result.html', result_msg=result_msg, color=color)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
