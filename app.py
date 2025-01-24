from flask import Flask, render_template, request
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

app = Flask(__name__)

# Load JSON data
def load_data():
    try:
        with open("quiz_data.json", "r") as f:
            quiz_data = json.load(f)
        with open("submission_data.json", "r") as f:
            submission_data = json.load(f)
        with open("historical_data.json", "r") as f:
            historical_data = json.load(f)
        return quiz_data, submission_data, historical_data
    except FileNotFoundError:
        return {}, {}, {}

# Load the ML model
def load_ml_model():
    try:
        with open("ml_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None

# Preprocess data for ML
def preprocess_data(quiz_data, historical_data):
    le = LabelEncoder()
    topics = [quiz['quiz']['topic'] for quiz in historical_data]
    le.fit(topics)

    current_topic = quiz_data.get('quiz', {}).get('topic', '')
    current_topic_encoded = le.transform([current_topic])[0] if current_topic in le.classes_ else -1

    total_score = quiz_data.get('quiz', {}).get('total_score', 0)
    current_score = quiz_data.get('quiz', {}).get('score', 0)
    topic_scores = [q['quiz']['score'] for q in historical_data if q['quiz']['topic'] == current_topic]
    historical_average = np.mean(topic_scores) if topic_scores else 0

    return np.array([current_topic_encoded, total_score, current_score, historical_average]).reshape(1, -1)

# Predict with ML
def predict_with_ml(quiz_data, historical_data, ml_model):
    if ml_model is None:
        return "No model available. Train a model to provide predictions."

    features = preprocess_data(quiz_data, historical_data)
    prediction = ml_model.predict(features)[0]

    return "You're doing well!" if prediction == 1 else "Review your weak areas."

# Analyze mistakes
def analyze_mistakes(submission_data, historical_data):
    mistakes = {}
    
    # Analyze each question in the submission data
    for question_id, selected_option in submission_data.get('response_map', {}).items():
        # Find the question's topic
        topic = ""
        for quiz_entry in historical_data:
            # Check if 'quiz' and 'questions' exist in the entry
            if 'quiz' in quiz_entry and 'questions' in quiz_entry['quiz']:
                for question in quiz_entry['quiz']['questions']:
                    if question['question_id'] == question_id:
                        topic = question['topic']  # Get the topic of the current question
                        break

        if topic:  # Ensure that topic exists
            if topic not in mistakes:
                mistakes[topic] = 1  # Increment mistakes for the topic
            else:
                mistakes[topic] += 1

    return mistakes

def generate_feedback(quiz_data, submission_data, historical_data):
    print("Quiz Data:", quiz_data)
    print("Submission Data:", submission_data)
    print("Historical Data:", historical_data)

    # Extract relevant data from submission_data
    correct_answers = submission_data.get('correct_answers', 0)
    incorrect_answers = submission_data.get('incorrect_answers', 0)
    total_questions = submission_data.get('total_questions', 0)
    final_score = float(submission_data.get('final_score', 0))
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    initial_mistake_count = submission_data.get('initial_mistake_count', 0)
    mistakes_corrected = submission_data.get('mistakes_corrected', 0)

    # Calculate score
    performance_level = "Good" if accuracy >= 75 else "Needs Improvement"

    # Historical performance feedback
    historical_scores = [entry['quiz']['score'] for entry in historical_data if 'quiz' in entry and 'score' in entry['quiz']]
    avg_historical_score = np.mean(historical_scores) if historical_scores else 0

    performance_feedback = {
        "accuracy": accuracy,
        "final_score": final_score,
        "score": final_score,
        "mistakes": initial_mistake_count - mistakes_corrected,
        "performance_level": performance_level,
        "historical_average_score": avg_historical_score,
    }

    if final_score < avg_historical_score:
        performance_feedback["historical_comparison"] = "Your score is lower than your usual performance. Consider revisiting topics you find difficult."
    else:
        performance_feedback["historical_comparison"] = "You're performing better than your historical average! Keep it up."

    # Mistakes analysis and recommendations
    recommendations = []
    if initial_mistake_count > 0:
        recommendations.append(f"You made {initial_mistake_count} mistakes initially, but corrected {mistakes_corrected}. Keep focusing on those areas.")
    if incorrect_answers > 0:
        recommendations.append(f"You got {incorrect_answers} answers incorrect. Revise the topics where you had difficulty.")

    # Additional feedback based on performance
    if accuracy < 50:
        recommendations.append("Focus on improving your accuracy. Consider reviewing the most difficult topics.")
    elif accuracy >= 50 and accuracy < 75:
        recommendations.append("You're making progress, but there are still areas to improve. Keep practicing.")
    else:
        recommendations.append("Great job! Continue reviewing to stay sharp.")

    # Machine Learning-based feedback
    ml_model = load_ml_model()
    ml_feedback = predict_with_ml(quiz_data, historical_data, ml_model)
    recommendations.append(ml_feedback)

    return performance_feedback, recommendations

# Routes
@app.route('/')
def home():
    return render_template('index.html', message="Welcome to the Quiz App!")

@app.route('/results')
def results():
    quiz_data, submission_data, historical_data = load_data()
    ml_model = load_ml_model()

    # Get performance feedback and recommendations
    performance_feedback, recommendations = generate_feedback(quiz_data, submission_data, historical_data)

    # Historical scores for graphing
    historical_scores = [entry['quiz']['score'] for entry in historical_data if 'quiz' in entry and 'score' in entry['quiz']]

    return render_template('results.html', performance=performance_feedback, recommendations=recommendations, historical_scores=historical_scores)

if __name__ == '__main__':
    app.run(debug=True)
