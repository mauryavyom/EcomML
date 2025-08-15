E-commerce Website with ML Recommendation System
1. Overview & Features
This is a Spring Boot e-commerce application with a Python-based ML recommendation system.

User Features: User login/registration, product catalog (with category, subcategory, and brand), shopping cart, and personalized product recommendations on the cart page.

Admin Features: Full management of products, categories (with subcategories), brands, and users.

2. Technology Stack
Backend: Java, Spring Boot, Spring Data JPA

Frontend: HTML, Thymeleaf, CSS, Bootstrap

Database: MySQL 

Recommendation Engine: Python, Flask, Pandas,Surprise

Build Tool: Maven

3. How the Recommendation System Works
When a user visits their cart, the Spring Boot backend calls a Python Flask API (/recommend).

The API is sent the product IDs from the user's cart.

The Python service uses a content-based model (comparing category, subcategory, brand) to find similar items.

A list of recommended product IDs is returned to the Spring Boot app.

The recommended products are then displayed on the cart page.

4. Summary of Recent Changes
Backend Updates
UserController.java: Updated to call the ML recommendation API from the /cart endpoint.

Product.java Model: Added new fields for brand and subcategory.

New Files Added:

RecommendationResponse.java: To handle the JSON response from the ML API.

Subcategory.java: New entity to manage product subcategories.

Frontend Updates
user/cart.html: A new section was added to display the recommended products.

Admin Panel: The "Add/Edit Product" and "Add/Edit Category" pages now have options to manage brands and subcategories.

Product Pages: Product detail pages now display brand and subcategory information.

5. Quick Setup
A. Backend (Java)
Clone: git clone <your-repo-url>

Configure: Update database details in src/main/resources/application.properties.

Run: mvn spring-boot:run. The app will be on http://localhost:8080.

B. ML Service (Python)
Navigate: cd ml-model

Install: pip install -r requirements.txt

Run: python app.py. The service will be on http://127.0.0.1:5000.
