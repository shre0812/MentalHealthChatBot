from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

therapists = [
    "🌼 Dr. Emily Watson - 8453828624",
    "🌻 MindCare Clinic - 6348652327",
    "🌸 Hope Mental Health - 6378248392",
    "🌺 Wellness Center - 9473027465",
    "🌷 Peaceful Mind Therapy - 0373648839"
]

questions = [
    {"question": "How often do you feel down, depressed, or hopeless? 😔", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you feel little interest or pleasure in doing things? 🎨", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you struggle with sleep (too much or too little)? 😴", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you experience feelings of anxiety or panic? 😰", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you feel tired or have little energy? 🔋", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you have difficulty concentrating? 📚", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you feel bad about yourself — or that you are a failure? 😢", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you feel isolated or lonely? 🧍‍♂️", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Do you experience mood swings? 🌦️", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"question": "Have you lost interest in activities you once enjoyed? 🎶", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]}
]

score_map = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_questions')
def get_questions():
    return jsonify(questions)

@app.route('/calculate_score', methods=['POST'])
def calculate_score():
    answers = request.json.get('answers', [])
    score = 0
    
    for answer in answers:
        if answer in score_map:
            score += score_map[answer]
    
    result = {}
    if score <= 10:
        result['text'] = "😊 You're doing great! Keep practicing self-care and stay positive!"
        result['color'] = "#2e7d32"
        result['show_therapists'] = False
    elif score <= 20:
        result['text'] = "😌 You're doing okay, but some extra support and relaxation could help."
        result['color'] = "#fb8c00"
        result['show_therapists'] = False
    else:
        result['text'] = "😟 It seems like you're going through a tough time. Please consider reaching out to a therapist."
        result['color'] = "#c2185b"
        result['show_therapists'] = True
    
    result['therapists'] = therapists
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)