import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

def generate_synthetic_data():
    """Generates a synthetic tabular dataset of prior criminal records."""
    data = [
        {"id": "CR001", "name": "Raju Bhai", "crime_type": "Theft", "mo": "Breaks locks using a crowbar", "traits": "Tall, scar on left cheek", "status": "Wanted"},
        {"id": "CR002", "name": "Kalia", "crime_type": "Extortion", "mo": "Threatens victims over phone calls", "traits": "Heavy build, deep voice", "status": "Incarcerated"},
        {"id": "CR003", "name": "Babu Rao", "crime_type": "Fraud", "mo": "Creates fake property documents", "traits": "Wears thick glasses", "status": "Out on bail"},
        {"id": "CR004", "name": "Munna", "crime_type": "Assault", "mo": "Uses a baseball bat in street fights", "traits": "Tattoos on both arms", "status": "Wanted"},
        {"id": "CR005", "name": "Circuit", "crime_type": "Smuggling", "mo": "Hides contraband in electronic goods", "traits": "Speaks fast, short height", "status": "Wanted"},
        {"id": "CR006", "name": "Gogo", "crime_type": "Robbery", "mo": "Snatching gold chains on a bike", "traits": "Wears a black cape", "status": "Wanted"},
        {"id": "CR007", "name": "Teja", "crime_type": "Murder", "mo": "Poisoning victims", "traits": "Bald, mark on head", "status": "Incarcerated"},
    ]
    df = pd.DataFrame(data)
    # Save to CSV for the offline dataset requirement
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "criminal_records.csv")
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    df.to_csv(dataset_path, index=False)
    print(f"Synthetic dataset saved to {dataset_path}")
    return df

def train_model():
    """Trains the Custom ML Retriever (KNN) using Feature Engineering."""
    print("Loading tabular dataset...")
    df = generate_synthetic_data()

    print("Performing Feature Engineering (Encoding MO, Crime Type, Traits)...")
    # Combine relevant features into a single text block for TF-IDF vectorization
    # In a more complex scenario, we could use OneHotEncoding for Crime Type and TF-IDF for MO/Traits separately,
    # but combining them works well for a unified NearestNeighbors retriever.
    df['combined_features'] = df['crime_type'] + " " + df['mo'] + " " + df['traits']

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['combined_features'])

    print("Training ML Model (KNN / Nearest Neighbors)...")
    # Using NearestNeighbors to retrieve the closest matching criminal profiles based on features
    model = NearestNeighbors(n_neighbors=3, metric='cosine')
    model.fit(X)

    # Save trained weights and vectorizer (For Faculty Requirement: "Loads Trained Weights")
    models_dir = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "criminal_knn_model.pkl")
    vectorizer_path = os.path.join(models_dir, "criminal_vectorizer.pkl")
    data_path = os.path.join(models_dir, "criminal_data.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(df, data_path) # Save dataframe so the retriever can return the matched record details

    print(f"Trained model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
    print("Offline ML Training Phase complete.")

if __name__ == "__main__":
    train_model()
