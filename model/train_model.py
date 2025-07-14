import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Load dataset
df = pd.read_csv("../data/leads_dataset.csv")

# Feature engineering
# Convert age groups and family backgrounds to numeric
age_map = {
    "18-25": 0,
    "26-35": 1,
    "36-50": 2,
    "51+": 3
}

family_map = {
    "Single": 0,
    "Married": 1,
    "Married with Kids": 2
}

df["age_group_num"] = df["age_group"].map(age_map)
df["family_background_num"] = df["family_background"].map(family_map)

# Select features and target
features = ["credit_score", "age_group_num", "family_background_num", "income"]
X = df[features]
y = df["intent"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["credit_score", "income"]),
        ("cat", "passthrough", ["age_group_num", "family_background_num"]),
    ]
)

# Create model pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    ))
])

# Train model
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("\nModel Evaluation:")
print(classification_report(y_test, y_pred))
print(f"\nROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Save model
joblib.dump(model, "lead_scoring_model.pkl")
print("\nModel saved as lead_scoring_model.pkl")
