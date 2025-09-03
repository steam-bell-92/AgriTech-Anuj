# src/train.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from utils import encode_features

# Load dataset
df = pd.read_csv('../data/fertilizer_dataset.csv')

# Encode categorical variables
df = encode_features(df)

# Features and target
X = df.drop(['Fertilizer Name'], axis=1)
y = df['Fertilizer Name']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
# src/train.py (update)

from utils import encode_features, soil_encoder, crop_encoder, fertilizer_encoder
import joblib

# existing training code ...

# Save model and encoders
joblib.dump(clf, '../saved_model/fertilizer_model.pkl')
joblib.dump(soil_encoder, '../saved_model/soil_encoder.pkl')
joblib.dump(crop_encoder, '../saved_model/crop_encoder.pkl')
joblib.dump(fertilizer_encoder, '../saved_model/fertilizer_encoder.pkl')

print("[INFO] Model and encoders saved successfully.")

# Save model
joblib.dump(clf, '../saved_model/fertilizer_model.pkl')
print("[INFO] Model trained and saved successfully.")
