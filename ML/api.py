import pickle
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

print("--- Loading models and preparing FINAL hybrid application... ---")

# --- 1. Database and Model Loading ---
DB_URI = 'mysql+mysqlconnector://root:vyom123@localhost/ecom_db'
engine = create_engine(DB_URI)

try:
    with open('surprise_model.pkl', 'rb') as f:
        surprise_model = pickle.load(f)
    with open('content_model.pkl', 'rb') as f:
        content_data = pickle.load(f)
    content_product_df = content_data['product_df']
    cosine_sim_matrix = content_data['cosine_sim']
    print("✅ All models loaded successfully.")
except FileNotFoundError as e:
    print(f"❌ ERROR: Model file not found: {e}. Please run the training script first.")
    raise

# --- 2. Static Category and Accessory Mapping ---
# This map uses the SUBCATEGORY names as keys for precise recommendations.
STATIC_CATEGORY_RELATIONS = {
    'Laptops': ['Laptops', 'Laptop Accessories', 'Mouse', 'Keyboard', 'Speakers'],
    'Smartphones': ['Smartphones', 'Smartphone Accessories', 'Headphones & Earbuds', 'Power Banks', 'Smartwatches'],
    'Tablets': ['Tablets', 'Tablet Accessories', 'Headphones & Earbuds'],
    'Speakers': ['Speakers', 'Audio Accessories'],
    'Headphones & Earbuds': ['Headphones & Earbuds', 'Audio Accessories'],
    'Smartwatches': ['Smartwatches', 'Wearable Accessories'],
}

# --- 3. API and Helper Functions ---
app = Flask(__name__)

def fetch_product_details(ids):
    if not ids: return []
    try:
        with engine.connect() as conn:
            id_placeholders = ", ".join([f":id_{i}" for i in range(len(ids))])
            query = text(f"SELECT id, title, price, image, brand FROM product WHERE id IN ({id_placeholders})")
            params = {f"id_{i}": id_val for i, id_val in enumerate(ids)}
            result = conn.execute(query, params)
            details_map = {row.id: {'id': row.id, 'title': row.title, 'price': float(row.price), 'brand': row.brand, 'image': row.image} for row in result}
            return [details_map[id] for id in ids if id in details_map]
    except Exception as e:
        print(f"❌ Database query failed in fetch_product_details: {e}")
        return None

def hybrid_rank(user_id, candidate_ids):
    if not candidate_ids: return []
    collab_scores = {pid: surprise_model.predict(user_id, pid).est for pid in candidate_ids}
    content_scores = {}
    for pid in candidate_ids:
        try:
            idx = content_product_df.index[content_product_df['product_id'] == pid].item()
            content_scores[pid] = np.mean(sorted(cosine_sim_matrix[idx], reverse=True)[:5])
        except ValueError:
            content_scores[pid] = 0.0
    ranked_ids = sorted(
        candidate_ids,
        key=lambda pid: (0.7 * collab_scores.get(pid, 0.0)) + (0.3 * content_scores.get(pid, 0.0)),
        reverse=True
    )
    return ranked_ids

# --- 4. THE DEFINITIVE "CART RECOMMENDATIONS" ENDPOINT ---
@app.route('/recommend/cart', methods=['POST'])
def recommend_for_cart():
    data = request.get_json()
    if not data or 'user_id' not in data or 'product_ids' not in data:
        return jsonify({'error': 'Missing user_id or product_ids in request body'}), 400

    user_id = data['user_id']
    cart_product_ids = data['product_ids']
    print(f"🛒 /recommend/cart request for user_id={user_id}, cart={cart_product_ids}")

    if not cart_product_ids:
        return jsonify({'recommendations': []})
    
    last_product_id = cart_product_ids[-1]
    
    try:
        with engine.connect() as conn:
            # --- THIS IS THE FIX ---
            # Use a JOIN to get the subcategory NAME from the subcategory table
            query = text("""
                SELECT s.name 
                FROM product p
                JOIN subcategory s ON p.subcategory_id = s.id
                WHERE p.id = :id
            """)
            result = conn.execute(query, {"id": last_product_id}).fetchone()
            if not result: return jsonify({'error': 'Product or its subcategory not found'}), 404
            context_subcategory = result[0] # The name is the first column
    except Exception as e:
        print(f"❌ DB error fetching context: {e}")
        return jsonify({'error': 'DB error'}), 500

    related_subcategories = STATIC_CATEGORY_RELATIONS.get(context_subcategory, [context_subcategory])
    
    try:
        with engine.connect() as conn:
            # --- THIS IS THE FIX ---
            # Use a JOIN to filter products by subcategory NAME
            if not related_subcategories:
                candidate_ids = set()
            else:
                subcat_placeholders = ", ".join([f":subcat_{i}" for i in range(len(related_subcategories))])
                query = text(f"""
                    SELECT p.id 
                    FROM product p
                    JOIN subcategory s ON p.subcategory_id = s.id
                    WHERE s.name IN ({subcat_placeholders})
                """)
                params = {f"subcat_{i}": subcat for i, subcat in enumerate(related_subcategories)}
                
                result = conn.execute(query, params)
                candidate_ids = {row[0] for row in result}
    except Exception as e:
        print(f"❌ DB error fetching candidates: {e}")
        return jsonify({'error': 'DB error'}), 500

    candidate_ids = list(candidate_ids - set(cart_product_ids))
    ranked_ids = hybrid_rank(user_id, candidate_ids)[:10]
    recommendations = fetch_product_details(ranked_ids)
    if recommendations is None:
        return jsonify({'error': 'Could not fetch final product details.'}), 500

    return jsonify({'user_id': user_id, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5000)