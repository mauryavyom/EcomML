<div align="center">

# 🛍️ E-commerce Website with ML Recommendation System 🚀

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring](https://img.shields.io/badge/Spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

A dynamic e-commerce application built with **Spring Boot** featuring a powerful **Python-based ML recommendation system** to deliver a personalized shopping experience.

</div>

---

## 🎯 Core Features

* **🛒 For Users**: Seamless login/registration, a rich product catalog (filterable by category, subcategory, and brand), a fully functional shopping cart, and smart product recommendations displayed right on the cart page.

* **⚙️ For Admins**: A comprehensive admin panel for full control over products, categories (including subcategories), brands, and user management.

---

## 🛠️ Built With

| Category                | Technology                                     |
| ----------------------- | ---------------------------------------------- |
| **Backend** | `Java`, `Spring Boot`, `Spring Data JPA`       |
| **Frontend** | `HTML`, `Thymeleaf`, `CSS`, `Bootstrap`        |
| **Database** | `MySQL`                                        |
| **Recommendation Engine** | `Python`, `Flask`, `Pandas`, `Scikit-learn` |
| **Build Tool** | `Maven`                                        |

---

## 🧠 Recommendation System Architecture

1.  **➡️ Trigger**: A user visits their shopping cart.
2.  **📡 API Call**: The Spring Boot backend sends the product IDs from the cart to a Python Flask API endpoint (`/recommend`).
3.  **✨ ML Magic**: The Python service uses a **content-based filtering model** to find similar items by comparing their `category`, `subcategory`, and `brand`.
4.  **⬅️ Response**: The model returns a list of recommended product IDs back to the Spring Boot application.
5.  **🖥️ Display**: The recommended products are fetched from the database and beautifully displayed to the user on the cart page.

---

## ✨ Key Project Updates

### 🖥️ Backend Updates
* **`UserController.java`**: Enhanced to call the ML recommendation API from the `/cart` endpoint.
* **`Product.java` Model**: Upgraded with new fields for `brand` and `subcategory` to enrich product data.
* **New Files Added**:
    * `RecommendationResponse.java`: A new class to smoothly handle the JSON response from the ML API.
    * `Subcategory.java`: A new entity to logically manage product subcategories.

### 🎨 Frontend Updates
* **`user/cart.html`**: Redesigned to include an attractive new section for displaying recommended products.
* **Admin Panel**: The "Add/Edit Product" and "Add/Edit Category" pages now have intuitive options to manage **brands** and **subcategories**.
* **Product Pages**: Product detail pages are updated to clearly display brand and subcategory information.

---

## 🚀 Getting Started

### A. ☕ Backend (Java)

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    ```
2.  **Configure Database**:
    Update your database credentials in `src/main/resources/application.properties`.
3.  **Run the Application**:
    ```bash
    mvn spring-boot:run
    ```
    > ✅ The app will be live at `http://localhost:8080`.

### B. 🐍 ML Service (Python)

1.  **Navigate to the ML Directory**:
    ```bash
    cd ml-model
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Service**:
    ```bash
    python app.py
    ```
    > ✅ The recommendation service will be listening at `http://127.0.0.1:5000`.
