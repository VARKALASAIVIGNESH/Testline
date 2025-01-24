
# Quiz App with Machine Learning and Line Chart Visualization

## Repository
**GitHub Link**: [Quiz App Repository](https://github.com/VARKALASAIVIGNESH/Testline)

## Description
This project is a Flask-based web application designed for interactive quizzes, personalized feedback, and historical score tracking using visualizations. It also incorporates machine learning to provide recommendations for improvement based on past performance.

##Output images
![{231C1D4A-879A-4C17-87D8-A1F820156AD7}](https://github.com/user-attachments/assets/74d557f1-ac28-4b65-9609-e1382c70f1d7)
![{B4EB7374-F5DD-46E0-84A8-10D95D917ACB}](https://github.com/user-attachments/assets/95d54771-1f1d-458e-9e4a-5122e578a9a1)
![{D48C0F34-20C7-4BFF-A619-BC6E6C17FE60}](https://github.com/user-attachments/assets/731bd9e3-7de0-455b-8d1d-90f55547cd5f)


## Features
- **Quiz Functionality**: Users can take quizzes on various topics and immediately view their results.
- **Performance Feedback**: Displays metrics like accuracy, score, and mistakes made.
- **Historical Comparison**: Compares current performance with historical data.
- **Interactive Line Chart**: Uses Chart.js to render a line chart of historical scores (final scores).
- **Machine Learning Recommendations**: Provides feedback based on predictions from a pre-trained model.

## Technologies Used
- **Flask**: Backend framework to build the web app.
- **NumPy**: For numerical operations.
- **Scikit-learn**: Implements machine learning functionality (Random Forest model).
- **Chart.js**: JavaScript library for interactive line charts.
- **HTML/CSS**: Frontend design and layout.
- **JSON**: Data storage for quizzes and historical records.

---

## Installation Guide

### Prerequisites
- **Python 3.8+**: Make sure Python is installed on your system.
- **Pip**: Comes bundled with Python, used for installing dependencies.
- A virtual environment is recommended to manage dependencies.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/VARKALASAIVIGNESH/Testline.git
   cd Testline
   ```

2. Create and activate a virtual environment:
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open the application in your browser:
   ```
   http://127.0.0.1:5000/
   ```

---

## Project Structure

```
Testline/
│
├── app.py               # Flask application
├── requirements.txt     # Dependencies for the project
├── /templates
│   ├── index.html       # Home page
│   └── results.html     # Results page with historical score visualization
├── /static
│   └── style.css        # CSS for page styling
├── historical_data.json # JSON containing past quiz performance data
├── quiz_data.json       # JSON with quiz questions and details
├── submission_data.json # JSON storing user submission data
├── ml_model.pkl         # Pre-trained machine learning model
└── README.md            # Documentation for the repository
```

---

## JSON File Details

- **`quiz_data.json`**: Contains quiz questions and metadata such as topic, total score, and correct answers.
- **`submission_data.json`**: Records users' quiz submissions, including accuracy, mistakes, and scores.
- **`historical_data.json`**: Stores historical quiz results used for generating trends and comparisons.

### Example JSON Formats

#### `quiz_data.json`
```json
{
  "quiz": {
    "topic": "Math",
    "total_score": 100,
    "score": 85,
    "questions": [
      {"question_id": 1, "question_text": "2 + 2 = ?", "correct_answer": "4"}
    ]
  }
}
```

#### `submission_data.json`
```json
{
  "correct_answers": 8,
  "incorrect_answers": 2,
  "total_questions": 10,
  "final_score": 85
}
```

#### `historical_data.json`
```json
[
  {"quiz": {"topic": "Math", "score": 80}},
  {"quiz": {"topic": "Science", "score": 90}}
]
```

---

## Features Breakdown

### 1. **Home Page**
Navigate to the home page to start quizzes or view historical results.

### 2. **Results Page**
After completing a quiz, view:
- Accuracy, final score, and performance level.
- Historical score comparison visualized as a line chart.
- Recommendations for improvement based on mistakes and machine learning predictions.

### 3. **Historical Line Chart**
Utilizes `Chart.js` to display a line chart of historical quiz performance. Each data point represents the score of a past quiz.

---

## License
This project is open-source and available under the **MIT License**.

---

## Contributions
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

---

## Contact
For questions or feedback, please reach out via GitHub or [email](vickeyvignesh775@gmail.com).

---

Enjoy using the Quiz App! 🎉


---
