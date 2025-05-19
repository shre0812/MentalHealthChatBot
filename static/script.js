document.addEventListener('DOMContentLoaded', function() {
    const welcomeScreen = document.getElementById('welcome-screen');
    const quizContainer = document.getElementById('quiz-container');
    const resultContainer = document.getElementById('result-container');
    const startBtn = document.getElementById('start-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const restartBtn = document.getElementById('restart-btn');
    const questionText = document.getElementById('question-text');
    const questionNumber = document.getElementById('question-number');
    const optionsContainer = document.getElementById('options-container');
    const resultText = document.getElementById('result-text');
    const therapistsContainer = document.getElementById('therapists-container');

    let currentQuestion = 0;
    let answers = [];
    let questions = [];

    // Fetch questions from the backend
    fetch('/get_questions')
        .then(response => response.json())
        .then(data => {
            questions = data;
            answers = new Array(questions.length).fill(null);
        });

    // Start the quiz
    startBtn.addEventListener('click', function() {
        welcomeScreen.style.display = 'none';
        quizContainer.style.display = 'block';
        loadQuestion();
    });

    // Load a question
    function loadQuestion() {
        questionNumber.textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
        questionText.textContent = questions[currentQuestion].question;
        optionsContainer.innerHTML = '';

        questions[currentQuestion].options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.classList.add('option');
            if (answers[currentQuestion] === option) {
                optionElement.classList.add('selected');
            }
            optionElement.textContent = option;
            optionElement.addEventListener('click', function() {
                selectOption(option);
            });
            optionsContainer.appendChild(optionElement);
        });

        // Update button states
        prevBtn.disabled = currentQuestion === 0;
        nextBtn.disabled = answers[currentQuestion] === null;
        submitBtn.disabled = !answers.every(answer => answer !== null);
    }

    // Select an option
    function selectOption(option) {
        answers[currentQuestion] = option;
        const allOptions = document.querySelectorAll('.option');
        allOptions.forEach(opt => {
            opt.classList.remove('selected');
            if (opt.textContent === option) {
                opt.classList.add('selected');
            }
        });
        nextBtn.disabled = false;
        submitBtn.disabled = !answers.every(answer => answer !== null);
    }

    // Previous question
    prevBtn.addEventListener('click', function() {
        if (currentQuestion > 0) {
            currentQuestion--;
            loadQuestion();
        }
    });

    // Next question
    nextBtn.addEventListener('click', function() {
        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            loadQuestion();
        }
    });

    // Submit the quiz
    submitBtn.addEventListener('click', function() {
        fetch('/calculate_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(data => {
            quizContainer.style.display = 'none';
            resultContainer.style.display = 'block';
            
            resultText.textContent = data.text;
            resultText.style.color = data.color;
            
            therapistsContainer.innerHTML = '';
            if (data.show_therapists) {
                const therapistsTitle = document.createElement('h3');
                therapistsTitle.textContent = 'Here are some therapists you can contact: 📞';
                therapistsContainer.appendChild(therapistsTitle);
                
                data.therapists.forEach(therapist => {
                    const therapistElement = document.createElement('div');
                    therapistElement.classList.add('therapist');
                    therapistElement.textContent = therapist;
                    therapistsContainer.appendChild(therapistElement);
                });
            }
        });
    });

    // Restart the quiz
    restartBtn.addEventListener('click', function() {
        currentQuestion = 0;
        answers = new Array(questions.length).fill(null);
        resultContainer.style.display = 'none';
        quizContainer.style.display = 'block';
        loadQuestion();
    });
});