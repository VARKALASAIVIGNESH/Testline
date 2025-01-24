import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load quiz and historical data
def load_data():
    try:
        with open("quiz_data.json", "r") as f:
            quiz_data = json.load(f)
        with open("historical_data.json", "r") as f:
            historical_data = json.load(f)
        return quiz_data, historical_data
    except FileNotFoundError:
        print("JSON files not found!")
        return {}, []

# Preprocess the data to extract features and labels
def preprocess_data(quiz_data, historical_data):
    le = LabelEncoder()
    
    # Extract topics from historical data
    topics = [quiz['quiz']['topic'] for quiz in historical_data if 'quiz' in quiz and 'topic' in quiz['quiz']]
    le.fit(topics)
    
    # Process features (X) and labels (y)
    X = []
    y = []
    
    for quiz in historical_data:
        if 'quiz' not in quiz:
            continue  # Skip any entries that don't have a 'quiz' key

        # Get historical data for the topic
        current_topic = quiz['quiz'].get('topic', 'Unknown')  # Default to 'Unknown' if topic is missing
        score = quiz.get('score', 0)  # Default to 0 if score is missing
        total_questions = quiz['quiz'].get('total_questions', 0)  # Total number of questions (used as total score)

        # Use 'final_score' if available, otherwise use score
        final_score = quiz.get('final_score', score)

        # Convert final_score to float if it's a string (could be a string representing a number)
        try:
            final_score = float(final_score)
        except ValueError:
            final_score = 0.0  # If conversion fails, default to 0

        # Calculate historical average score for the topic
        topic_scores = [q['score'] for q in historical_data if 'quiz' in q and q['quiz'].get('topic') == current_topic]
        historical_avg = np.mean(topic_scores) if topic_scores else 0
        
        # Encode the topic as a numerical value
        current_topic_encoded = le.transform([current_topic])[0] if current_topic in le.classes_ else -1
        
        # Feature vector [encoded_topic, score, total_score, historical_avg]
        feature_vector = [current_topic_encoded, score, total_questions, historical_avg]
        X.append(feature_vector)
        
        # Define the label: 1 for good performance (final_score >= 75% of total score), else 0
        if total_questions > 0:
            label = 1 if (final_score / total_questions) >= 0.75 else 0
        else:
            label = 0  # If there are no questions, consider it as a non-good performance
        
        y.append(label)
    
    return np.array(X), np.array(y), le

# Train the model
def train_model():
    quiz_data, historical_data = load_data()
    
    if not historical_data:
        print("No historical data available for training.")
        return
    
    X, y, label_encoder = preprocess_data(quiz_data, historical_data)
    
    # Create and train the RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Save the model and label encoder to disk
    with open("ml_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)
    
    print("Model training completed and saved to 'ml_model.pkl'")

# Run the training process
if __name__ == "__main__":
    train_model()
