import pandas as pd
import pickle
import numpy as np
import random
from surprise import SVD, Dataset, Reader
from surprise.model_selection import GridSearchCV, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, normalize
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack

def train_and_save_models():
    """
    Advanced training pipeline:
    - Optimized Collaborative Filtering (SVD with broader GridSearchCV)
    - Enhanced Content-Based Model with normalized text + balanced features
    - Saves both models to disk with evaluation metrics
    """
    print("=== Starting Advanced Hybrid Model Training ===")

    # --- Ensure Reproducibility ---
    np.random.seed(42)
    random.seed(42)

    # --- 1. Load Data ---
    try:
        df = pd.read_csv('training_data.csv')
        print(f"✅ Loaded {len(df)} rows of training data.")
    except FileNotFoundError:
        print("❌ ERROR: `training_data.csv` not found. Run data population first.")
        return

    df['interaction_score'] = df['interaction_score'].clip(1, 5)

    # --- 2. Collaborative Filtering ---
    print("\n--- Collaborative Filtering Optimization ---")
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'product_id', 'interaction_score']], reader)

    param_grid = {
        'n_factors': [50, 100, 150],
        'n_epochs': [20, 30],
        'reg_all': [0.02, 0.05, 0.1],
        'lr_all': [0.002, 0.005],
        'biased': [True, False]
    }
    gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3, n_jobs=-1)
    gs.fit(data)

    best_params = gs.best_params['rmse']
    print(f"✅ Best SVD Params: {best_params}")

    trainset = data.build_full_trainset()
    algo = SVD(**best_params, random_state=42)
    algo.fit(trainset)

    cv_results = cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=False)
    rmse_score = np.mean(cv_results['test_rmse'])
    print(f"📊 Collaborative Filtering RMSE: {rmse_score:.4f}")

    with open('surprise_model.pkl', 'wb') as f:
        pickle.dump(algo, f)
    print("💾 Saved collaborative model to 'surprise_model.pkl'.")

    # --- 3. Content-Based Filtering ---
    print("\n--- Building Enhanced Content-Based Model ---")
    product_df = df[['product_id', 'category', 'brand', 'subcategory']].drop_duplicates().reset_index(drop=True)

    if 'title' in df.columns:
        title_map = df[['product_id', 'title']].drop_duplicates().set_index('product_id')['title']
        product_df['title'] = product_df['product_id'].map(title_map)
    else:
        product_df['title'] = ''

    if 'description' in df.columns:
        desc_map = df[['product_id', 'description']].drop_duplicates().set_index('product_id')['description']
        product_df['description'] = product_df['product_id'].map(desc_map)
    else:
        product_df['description'] = ''

    # Clean & normalize text
    product_df['soup'] = (
        product_df['title'].fillna('') + ' ' +
        product_df['description'].fillna('') + ' ' +
        product_df['category'].fillna('') + ' ' +
        product_df['brand'].fillna('') + ' ' +
        product_df['subcategory'].fillna('')
    ).str.lower().str.replace(r'\s+', ' ', regex=True)

    # TF-IDF with sublinear scaling
    tfidf = TfidfVectorizer(stop_words='english', sublinear_tf=True)
    tfidf_matrix = tfidf.fit_transform(product_df['soup'])

    # One-hot encode categorical
    ohe = OneHotEncoder(handle_unknown='ignore')
    cat_matrix = ohe.fit_transform(product_df[['category', 'brand', 'subcategory']])

    # Combine & normalize features
    combined_matrix = hstack([tfidf_matrix, cat_matrix])
    combined_matrix = normalize(combined_matrix, norm='l2')

    cosine_sim = cosine_similarity(combined_matrix, combined_matrix)
    print("✅ Content-based similarity matrix computed.")

    with open('content_model.pkl', 'wb') as f:
        pickle.dump({
            'product_df': product_df,
            'cosine_sim': cosine_sim,
            'tfidf': tfidf,
            'ohe': ohe
        }, f)
    print("💾 Saved content-based model to 'content_model.pkl'.")

    print("\n🚀 All models trained, optimized, and saved successfully!")

if __name__ == '__main__':
    train_and_save_models()
