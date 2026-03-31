import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# -----------------------------
# Load datasets
# -----------------------------

resume_df = pd.read_excel("dataset/resume_dataset.xlsx")
match_df = pd.read_excel("dataset/candidate_role_match.xlsx")


# -----------------------------
# Get best role for each candidate
# -----------------------------

best_roles = match_df.sort_values("Match_Percentage", ascending=False)\
                     .drop_duplicates("Candidate_Name")

data = pd.merge(resume_df, best_roles[["Candidate_Name","Role"]], on="Candidate_Name")


# -----------------------------
# Feature Engineering
# -----------------------------

data["combined_features"] = (
    data["Skills"].fillna("") + " " +
    data["Tools"].fillna("") + " " +
    data["Education"].fillna("") + " " +
    data["Past_Projects"].fillna("") + " " +
    data["Experience"].fillna("") + " " +
    data["Certification"].fillna("")
)


X_text = data["combined_features"]
y = data["Role"]


# -----------------------------
# Convert text to vectors
# -----------------------------

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_text)


# -----------------------------
# Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -----------------------------
# Train Multiple Models
# -----------------------------

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

best_model = None
best_accuracy = 0


for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)

    print("\nModel:", name)
    print("Accuracy:", acc)

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model


print("\nBest Model Selected with Accuracy:", best_accuracy)


# -----------------------------
# Top-3 Role Predictions
# -----------------------------

prob_matrix = best_model.predict_proba(X)

roles = best_model.classes_

top_roles = []

for probs in prob_matrix:

    role_scores = list(zip(roles, probs*100))

    role_scores.sort(key=lambda x: x[1], reverse=True)

    top3 = role_scores[:3]

    top_roles.append(top3)


results = []

for i, candidate in enumerate(data["Candidate_Name"]):

    r1, r2, r3 = top_roles[i]

    results.append({

        "Candidate_Name": candidate,

        "Top_Role_1": r1[0],
        "Score_1": round(r1[1],2),

        "Top_Role_2": r2[0],
        "Score_2": round(r2[1],2),

        "Top_Role_3": r3[0],
        "Score_3": round(r3[1],2)

    })


result_df = pd.DataFrame(results)


# -----------------------------
# Save results
# -----------------------------

result_df.to_excel("dataset/top3_role_predictions.xlsx", index=False)

print("\nTop 3 role predictions saved successfully!")
import pickle
import os

# create models folder if not exists
os.makedirs("models", exist_ok=True)

# save model
pickle.dump(model, open("models/role_model.pkl","wb"))

# save vectorizer
pickle.dump(vectorizer, open("models/vectorizer.pkl","wb"))

print("Model saved successfully!")