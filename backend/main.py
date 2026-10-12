from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

from backend.database import SessionLocal, MessageLog


# Create FastAPI application
app = FastAPI(
    title="Real-Time Spam Detection API",
    description="API for detecting spam messages using machine learning",
    version="1.0.0"
)


# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Model paths
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "spam_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl"
)


# Load trained model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# Request format
class MessageRequest(BaseModel):
    message: str


# Home endpoint
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Spam Detection API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict_spam(request: MessageRequest):

    message = request.message

    # Convert message to TF-IDF features
    features = vectorizer.transform([message])

    # Make prediction
    prediction = model.predict(features)[0]

    # Get SVM decision score
    decision_score = model.decision_function(features)[0]

    # Determine system action
    if prediction == "spam":
        action = "BLOCKED"
    else:
        action = "ALLOWED"

    # Save prediction and action to database
    db = SessionLocal()

    try:
        log = MessageLog(
            message=message,
            prediction=prediction,
            confidence_score=abs(float(decision_score)),
            action=action
        )

        db.add(log)
        db.commit()
        db.refresh(log)

    finally:
        db.close()

    return {
        "message": message,
        "prediction": prediction,
        "decision_score": round(float(decision_score), 4),
        "action": action
    }