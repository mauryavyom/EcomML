<div align="center">

🛍️ E-commerce Website with ML Recommendation System 🚀
</div>

🎯 1. Overview & Features
This project is a dynamic e-commerce application built with Spring Boot and features a powerful Python-based ML recommendation system to deliver a personalized shopping experience.

🛒 User Features: Seamless user login/registration, a rich product catalog (filterable by category, subcategory, and brand), a fully functional shopping cart, and smart product recommendations displayed right on the cart page.

⚙️ Admin Features: A comprehensive admin panel for full control over products, categories (including subcategories), brands, and user management.

🛠️ 2. Technology Stack
Category

Technology

Backend

Java, Spring Boot, Spring Data JPA

Frontend

HTML, Thymeleaf, CSS, Bootstrap

Database

MySQL

Recommendation Engine

Python, Flask, Pandas, Surprise

Build Tool

Maven

🧠 3. How the Recommendation System Works
Trigger: A user visits their shopping cart.

API Call: The Spring Boot backend sends the product IDs from the cart to a Python Flask API endpoint (/recommend).

ML Magic: The Python service uses a content-based filtering model to find similar items by comparing their category, subcategory, and brand.

Response: The model returns a list of recommended product IDs back to the Spring Boot application.

Display: The recommended products are fetched from the database and beautifully displayed to the user on the cart page.

✨ 4. Summary of Recent Changes
Backend Updates
UserController.java: Enhanced to call the ML recommendation API from the /cart endpoint.

Product.java Model: Upgraded with new fields for brand and subcategory to enrich product data.

New Files Added:

RecommendationResponse.java: A new class to smoothly handle the JSON response from the ML API.

Subcategory.java: A new entity to logically manage product subcategories.

Frontend Updates
user/cart.html: Redesigned to include an attractive new section for displaying recommended products.

Admin Panel: The "Add/Edit Product" and "Add/Edit Category" pages now have intuitive options to manage brands and subcategories.

Product Pages: Product detail pages are updated to clearly display brand and subcategory information.

🚀 5. Quick Setup
A. Backend (Java)
Clone the Repository:

git clone <your-repo-url>

Configure Database:
Update your database credentials in src/main/resources/application.properties.

Run the Application:

mvn spring-boot:run

The app will be live at http://localhost:8080.

B. ML Service (Python)
Navigate to the ML Directory:

cd ml-model

Install Dependencies:

pip install -r requirements.txt

Run the Service:

python app.py

The recommendation service will be listening at http://127.0.0.1:5000.
