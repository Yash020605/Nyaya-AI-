import os
import json
import logging
import joblib
import pandas as pd
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class CustomMLRetriever:
    """
    Custom Trained ML Retriever as specified in the Nyaya AI architecture diagram:
    Loads trained offline ML weights (KNN / Random Forest) and matches suspect traits/MO
    extracted from the FIR against the historical criminal records dataset.
    """
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")
        self.preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
        self.knn_path = os.path.join(models_dir, "knn_suspect_retriever.joblib")
        self.rf_path = os.path.join(models_dir, "random_forest_risk_model.joblib")
        self.index_path = os.path.join(models_dir, "criminal_id_index.json")

        self.is_loaded = False
        self._load_models()

    def _load_models(self):
        try:
            if (os.path.exists(self.preprocessor_path) and 
                os.path.exists(self.knn_path) and 
                os.path.exists(self.rf_path) and 
                os.path.exists(self.index_path)):
                
                self.preprocessor = joblib.load(self.preprocessor_path)
                self.knn_model = joblib.load(self.knn_path)
                self.rf_model = joblib.load(self.rf_path)
                
                with open(self.index_path, "r", encoding="utf-8") as f:
                    self.criminal_index = json.load(f)
                    
                self.is_loaded = True
                logger.info("Custom ML Retriever models and index successfully loaded into memory.")
            else:
                logger.warning("ML model weight files not found. Run scripts/train_criminal_ml.py first.")
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")
            self.is_loaded = False

    def predict_and_match(
        self,
        primary_crime_type: str = "Theft / Burglary",
        weapon_used: str = "None",
        gang_affiliation: str = "Independent",
        state: str = "Delhi",
        build: str = "Medium",
        complexion: str = "Wheatish",
        age: int = 30,
        height_cm: int = 170,
        prior_convictions: int = 1,
        active_warrants: int = 0,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Takes suspect features and crime context, predicts the risk classification,
        and retrieves top-K matching criminal records from the tabular dataset using KNN.
        """
        if not self.is_loaded:
            return {"error": "ML models are not loaded.", "matched_suspects": []}

        # Build query DataFrame matching the training schema
        query_data = {
            "primary_crime_type": [primary_crime_type],
            "weapon_used": [weapon_used],
            "gang_affiliation": [gang_affiliation],
            "state": [state],
            "build": [build],
            "complexion": [complexion],
            "age": [age],
            "height_cm": [height_cm],
            "prior_convictions": [prior_convictions],
            "active_warrants": [active_warrants]
        }
        df_query = pd.DataFrame(query_data)

        try:
            # Transform features
            query_vector = self.preprocessor.transform(df_query)

            # 1. Predict predicted recidivism / risk category using Random Forest
            predicted_risk = self.rf_model.predict(query_vector)[0]
            risk_probs = self.rf_model.predict_proba(query_vector)[0]
            risk_confidence = float(max(risk_probs))

            # 2. Retrieve Nearest Matching Criminal Profiles using KNN
            distances, indices = self.knn_model.kneighbors(query_vector, n_neighbors=top_k)

            matches = []
            for dist, idx in zip(distances[0], indices[0]):
                profile = self.criminal_index[idx].copy()
                similarity_score = round(float(1.0 - dist), 4) # Cosine similarity
                profile["similarity_score"] = similarity_score
                profile["criminal_id"] = profile.get("criminal_id") or profile.get("record_id", f"CR-{idx+1:04d}")
                matches.append(profile)

            return {
                "predicted_risk_level": predicted_risk,
                "confidence": round(risk_confidence, 4),
                "matched_suspects": matches
            }
        except Exception as e:
            logger.error(f"Error executing ML retriever inference: {e}")
            return {"error": str(e), "matched_suspects": []}

# Singleton instance for route integration
custom_ml_retriever = CustomMLRetriever()
