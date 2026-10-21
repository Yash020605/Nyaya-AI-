import os
import joblib
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_and_export_models():
    project_root = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(project_root, "data", "raw", "criminal_records_dataset.csv")
    models_dir = os.path.join(project_root, "backend", "app", "ml_models")
    os.makedirs(models_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Run generate_criminal_records.py first.")
        
    logger.info(f"Loading criminal dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded {len(df)} rows.")

    # 1. Feature Engineering
    # Features representing suspect traits, modus operandi, and crime context
    categorical_features = [
        "primary_crime_type", "weapon_used", "gang_affiliation",
        "state", "build", "complexion"
    ]
    numeric_features = ["age", "height_cm", "prior_convictions", "active_warrants"]
    
    X = df[categorical_features + numeric_features]
    y = df["risk_level"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
            ("num", StandardScaler(), numeric_features)
        ]
    )
    
    # 2. Train-Test Split for Supervised Model (Random Forest & SVM for Risk/Profile Prediction)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Fit preprocessor
    logger.info("Fitting feature preprocessor...")
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)
    
    # Model A: Random Forest Classifier (Multi-class Risk Level & MO Patterning)
    logger.info("Training Random Forest Classifier...")
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_train_transformed, y_train)
    rf_pred = rf_clf.predict(X_test_transformed)
    logger.info(f"Random Forest Accuracy: {accuracy_score(y_test, rf_pred):.4f}")
    
    # Model B: Support Vector Machine (SVM)
    logger.info("Training SVM Classifier...")
    svm_clf = SVC(probability=True, random_state=42)
    svm_clf.fit(X_train_transformed, y_train)
    svm_pred = svm_clf.predict(X_test_transformed)
    logger.info(f"SVM Accuracy: {accuracy_score(y_test, svm_pred):.4f}")

    # Model C: K-Nearest Neighbors (KNN) for Suspect Similarity Matching
    # Used directly by the Custom Trained ML Retriever to find top-K matching criminal profiles!
    logger.info("Training KNN Nearest Neighbors for Suspect Profile Matching...")
    X_all_transformed = preprocessor.transform(X)
    knn_retriever = NearestNeighbors(n_neighbors=5, metric="cosine")
    knn_retriever.fit(X_all_transformed)

    # 3. Save Trained Weights & Metadata
    logger.info(f"Saving model artifacts to {models_dir}...")
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessor.joblib"))
    joblib.dump(rf_clf, os.path.join(models_dir, "random_forest_risk_model.joblib"))
    joblib.dump(svm_clf, os.path.join(models_dir, "svm_classifier.joblib"))
    joblib.dump(knn_retriever, os.path.join(models_dir, "knn_suspect_retriever.joblib"))
    
    # Save dataframe index mapping for KNN lookups with complete profile metadata
    df["criminal_id"] = df["record_id"]
    export_cols = [
        "criminal_id", "record_id", "name", "alias", "age", "gender", "primary_crime_type",
        "modus_operandi", "weapon_used", "gang_affiliation", "state", "district",
        "prior_convictions", "active_warrants", "risk_level"
    ]
    available_cols = [c for c in export_cols if c in df.columns]
    df[available_cols].to_json(
        os.path.join(models_dir, "criminal_id_index.json"), orient="records", indent=2
    )

    logger.info("Offline ML Training Phase Completed Successfully!")
    print(f"Artifacts saved to {models_dir}:")
    print(" - preprocessor.joblib")
    print(" - random_forest_risk_model.joblib")
    print(" - svm_classifier.joblib")
    print(" - knn_suspect_retriever.joblib")
    print(" - criminal_id_index.json")

if __name__ == "__main__":
    train_and_export_models()
