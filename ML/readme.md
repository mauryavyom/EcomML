# 🛍️ E-commerce Hybrid Recommendation System

This project implements a hybrid recommendation system for an e-commerce platform. It combines collaborative and content-based filtering techniques to provide personalized product suggestions. The system is composed of three main scripts for data loading, model training, and serving recommendations via a Flask API.

---

## 📜 Table of Contents
- [Project Overview](#project-overview)
- [How It Works](#how-it-works)
  - [1. `load_data.py`](#1-load_datapy)
  - [2. `train_model.py`](#2-train_modelpy)
  - [3. `api.py`](#3-apipy)
- [API Endpoint](#api-endpoint)
- [Getting Started](#getting-started)
- [Contact](#contact)

---

## 🎯 Project Overview

The goal of this recommendation system is to enhance user experience by suggesting relevant products. It analyzes user behavior (cart/order history) and product attributes (title, category, brand) to generate high-quality recommendations.

The workflow is divided into three stages:
1.  **Data Population & Preprocessing**: Populating a MySQL database with realistic e-commerce data and generating a training dataset.
2.  **Model Training**: Training a collaborative filtering model (SVD) and a content-based filtering model (Cosine Similarity) on the generated data.
3.  **API Deployment**: Serving the recommendations through a Flask API that combines the strengths of both models.

---

## ⚙️ How It Works

The project is built around three core Python scripts. They must be run in the specified order.

### 1. `load_data.py`
This script sets up the environment by populating the `ecom_db` MySQL database with sample e-commerce data. It handles foreign key constraints to ensure data integrity across categories, subcategories, and products.

**Key Actions:**
- **Database Population**:
    - Inserts categories and subcategories.
    - Inserts over 1,000 products with realistic details and pricing.
    - Inserts 20,000 sample users.
    - Generates 100,000 transactions for cart and order history to simulate purchase patterns.
- **Data Export**:
    - After populating the database, it generates a `training_data.csv` file. This file contains user-product interaction scores and product features required for model training.

### 2. `train_model.py`
This script trains and saves the two recommendation models that power the system.

**Models Trained:**
1.  **Collaborative Filtering (SVD)**:
    - Uses the `surprise` library to implement Singular Value Decomposition (SVD).
    - `GridSearchCV` is used to find the optimal hyperparameters.
    - The model's performance is evaluated using cross-validation RMSE.
2.  **Content-Based Filtering**:
    - Uses TF-IDF vectorization for product titles and descriptions.
    - Applies one-hot encoding for categorical features like category, brand, and subcategory.
    - Combines and normalizes all features to compute a cosine similarity matrix between products.

**Outputs:**
- `surprise_model.pkl`: The trained collaborative filtering SVD model.
- `content_model.pkl`: A file containing the product feature matrix, cosine similarity matrix, and fitted vectorizers for the content-based model.

### 3. `api.py`
This script deploys a Flask API to serve hybrid recommendations in real-time.

**Features:**
- **Hybrid Approach**: Generates a final recommendation score by blending collaborative filtering predictions (70%) and content-based similarity (30%).
- **Database Connection**: Connects to the `ecom_db` MySQL database to fetch live product and category information.
- **Context-Awareness**: Uses a static mapping of related subcategories to provide more contextually relevant suggestions.

---

## 🔌 API Endpoint

### `POST /recommend/cart`
Generates personalized product recommendations based on the items in a user's cart.

-   **Input**:
    -   `user_id`: The ID of the user.
    -   `product_ids`: A list of product IDs currently in the user's cart.

-   **Process**:
    1.  Identifies the subcategories of the products in the cart.
    2.  Finds related subcategories to broaden the pool of candidate products.
    3.  Ranks the candidate products using the hybrid scoring model.
    4.  Returns the top-ranked products.

-   **Output Example**:
    ```json
    {
      "user_id": 123,
      "recommendations": [
        {
          "id": 45,
          "title": "Wireless Mouse",
          "price": 799.0,
          "brand": "Logitech",
          "image": "mouse.jpg"
        },
        {
          "id": 102,
          "title": "Mechanical Keyboard",
          "price": 2499.0,
          "brand": "Corsair",
          "image": "keyboard.jpg"
        }
      ]
    }
    ```

---

## 🚀 Getting Started

To run this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Install dependencies:**

    This project uses a local wheel file for `scikit-surprise` to avoid common installation issues.

    First, install the package from the `wheels` directory:
    ```bash
    # For Windows
    pip install wheels\*.whl

    # For macOS/Linux
    pip install wheels/*.whl
    ```

    Next, install the remaining packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your MySQL database:**
    -   Create a database named `ecom_db`.
    -   Update the database credentials in `load_data.py` and `api.py`.
4.  **Run the scripts in order:**
    ```bash
    # 1. Populate the database and create training data
    python load_data.py

    # 2. Train the recommendation models
    python train_model.py

    # 3. Start the API server
    python api.py
    ```

---

## 📞 Contact
For more details, please contact:
- **Vyom Maurya**

