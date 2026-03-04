import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1️⃣ Create Sample Spam Dataset (Normally you load CSV)
data = {
    "text": [
        "Win money now!!!",
        "Hello how are you",
        "Limited offer claim prize",
        "Meeting at 5pm",
        "Free vacation click now",
        "Project discussion tomorrow",
        "Congratulations you won lottery",
        "Let’s have lunch"
    ],
    "label": [1,0,1,0,1,0,1,0]  # 1 = Spam, 0 = Not Spam
}

df = pd.DataFrame(data)

# 2️⃣ Split Data
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

# 3️⃣ Convert Text to Numbers (TF-IDF)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# 4️⃣ Define Models
models = {
    "Logistic Regression": LogisticRegression(),
    "Naive Bayes": MultinomialNB(),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier()
}

# 5️⃣ Train + Evaluate
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    results[name] = acc
    print(f"{name} Accuracy: {acc:.4f}")

# 6️⃣ Select Best Model
best_model_name = max(results, key=results.get)
print("\nBest Model:", best_model_name)

best_model = models[best_model_name]

# 7️⃣ Real-Time Prediction Function
def predict_spam(text):
    text_vector = vectorizer.transform([text])
    prediction = best_model.predict(text_vector)[0]
    return "Spam" if prediction == 1 else "Not Spam"

# 8️⃣ Try Live Prediction
print("\nLive Prediction:")
print(predict_spam("Congratulations! You won free money"))