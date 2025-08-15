import pandas as pd
import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

print("Starting final database population script, with foreign key fix...")

# --- Database Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vyom123',
    'database': 'ecom_db'
}

# --- Helper function for BATCHED SQL insertion ---
def insert_df_in_batches(conn, df, table_name, batch_size=50000):
    print(f"Starting batched insertion for `{table_name}`...")
    cursor = conn.cursor()
    cols = ", ".join([f"`{c}`" for c in df.columns])
    placeholders = ", ".join(["%s"] * len(df.columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
    
    total_inserted = 0
    try:
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            data_to_insert = [tuple(row) for row in batch.itertuples(index=False)]
            cursor.executemany(query, data_to_insert)
            conn.commit()
            total_inserted += cursor.rowcount
            print(f"  ...inserted batch {i // batch_size + 1}, total rows: {total_inserted}")
        print(f"✅ Successfully finished batched insertion for `{table_name}`. Total rows: {total_inserted}.")
        return True
    except Error as e:
        print(f"❌ Error during batched insertion for `{table_name}`: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

# --- Data Structure Definitions ---
category_mapping = { "Smartphones": ("Electronics & Appliances", "Smartphones"), "Laptops": ("Electronics & Appliances", "Laptops"), "Smartphone Accessories": ("Electronics & Appliances", "Smartphone Accessories"), "Laptop Accessories": ("Electronics & Appliances", "Laptop Accessories"), "Tablets": ("Electronics & Appliances", "Tablets"), "Tablet Accessories": ("Electronics & Appliances", "Tablet Accessories"), "Power Banks": ("Electronics & Appliances", "Power Banks"), "Audio": ("Electronics & Appliances", "Headphones & Earbuds"), "Wearables": ("Electronics & Appliances", "Smartwatches"), "Audio Accessories": ("Electronics & Appliances", "Audio Accessories"), "Wearable Accessories": ("Electronics & Appliances", "Wearable Accessories"), "Speakers": ("Electronics & Appliances", "Speakers"), "Men's Clothing": ("Fashion & Clothing", "Men's Clothing"), "Women's Clothing": ("Fashion & Clothing", "Women's Clothing"), "Footwear": ("Fashion & Clothing", "Footwear"), "Large Appliances": ("Electronics & Appliances", "Large Appliances"), "Small Appliances": ("Electronics & Appliances", "Small Appliances"), "Cookware": ("Home & Kitchen", "Cookware"), "Makeup": ("Beauty, Health & Personal Care", "Makeup"), "Skincare": ("Beauty, Health & Personal Care", "Skincare"), "Gym Equipment": ("Sports & Outdoors", "Gym Equipment"), "Outdoor Gear": ("Sports & Outdoors", "Outdoor Gear"), "Snacks": ("Grocery & Food", "Snacks"), "Beverages": ("Grocery & Food", "Beverages"), "Toys": ("Toys, Baby & Kids", "Toys"), "Baby Care": ("Toys, Baby & Kids", "Baby Care"), "Books": ("Books, Stationery & Hobbies", "Books"), "Stationery": ("Books, Stationery & Hobbies", "Stationery")}
products_data = [ {'id': 1, 'name': 'iPhone 15 Pro Max', 'subcategory': 'Smartphones', 'brand': 'Apple'}, {'id': 2, 'name': 'Samsung Galaxy S24 Ultra', 'subcategory': 'Smartphones', 'brand': 'Samsung'}, {'id': 3, 'name': 'Google Pixel 9 Pro', 'subcategory': 'Smartphones', 'brand': 'Google'}, {'id': 4, 'name': 'MacBook Pro M4', 'subcategory': 'Laptops', 'brand': 'Apple'}, {'id': 5, 'name': 'Dell XPS 17', 'subcategory': 'Laptops', 'brand': 'Dell'}, {'id': 6, 'name': 'ASUS ROG Zephyrus G16', 'subcategory': 'Laptops', 'brand': 'ASUS'}, {'id': 7, 'name': 'Apple Silicone Case', 'subcategory': 'Smartphone Accessories', 'brand': 'Apple'}, {'id': 8, 'name': 'Spigen Tough Armor Case', 'subcategory': 'Smartphone Accessories', 'brand': 'Spigen'}, {'id': 9, 'name': 'Anker 100W GaN Charger', 'subcategory': 'Smartphone Accessories', 'brand': 'Anker'}, {'id': 10, 'name': 'Samsung S Pen Pro', 'subcategory': 'Smartphone Accessories', 'brand': 'Samsung'}, {'id': 11, 'name': 'Mosiso Laptop Sleeve', 'subcategory': 'Laptop Accessories', 'brand': 'Mosiso'}, {'id': 12, 'name': 'Logitech MX Master 3S Mouse', 'subcategory': 'Laptop Accessories', 'brand': 'Logitech'}, {'id': 13, 'name': 'Razer BlackWidow V4 Keyboard', 'subcategory': 'Laptop Accessories', 'brand': 'Razer'}, {'id': 14, 'name': 'HyperX Cloud III Headset', 'subcategory': 'Laptop Accessories', 'brand': 'HyperX'}, {'id': 15, 'name': 'iPad Pro M4', 'subcategory': 'Tablets', 'brand': 'Apple'}, {'id': 16, 'name': 'Samsung Galaxy Tab S9', 'subcategory': 'Tablets', 'brand': 'Samsung'}, {'id': 17, 'name': 'Apple Pencil Pro', 'subcategory': 'Tablet Accessories', 'brand': 'Apple'}, {'id': 18, 'name': 'Logitech Combo Touch Keyboard Case', 'subcategory': 'Tablet Accessories', 'brand': 'Logitech'}, {'id': 19, 'name': 'Anker PowerCore 24K Power Bank', 'subcategory': 'Power Banks', 'brand': 'Anker'}, {'id': 20, 'name': 'Belkin 3-in-1 MagSafe Charger', 'subcategory': 'Smartphone Accessories', 'brand': 'Belkin'}, {'id': 21, 'name': 'Sony WH-1000XM5 Headphones', 'subcategory': 'Audio', 'brand': 'Sony'}, {'id': 22, 'name': 'Apple AirPods Pro 3', 'subcategory': 'Audio', 'brand': 'Apple'}, {'id': 23, 'name': 'Bose QuietComfort Ultra Earbuds', 'subcategory': 'Audio', 'brand': 'Bose'}, {'id': 24, 'name': 'Apple Watch Ultra 2', 'subcategory': 'Wearables', 'brand': 'Apple'}, {'id': 25, 'name': 'Samsung Galaxy Watch 6', 'subcategory': 'Wearables', 'brand': 'Samsung'}, {'id': 26, 'name': 'Replacement Earpads for Sony XM5', 'subcategory': 'Audio Accessories', 'brand': 'Generic'}, {'id': 27, 'name': 'Sport Loop Straps for Apple Watch', 'subcategory': 'Wearable Accessories', 'brand': 'Apple'}, {'id': 28, 'name': 'Charging Dock Station for Watch', 'subcategory': 'Wearable Accessories', 'brand': 'Generic'}, {'id': 29, 'name': 'JBL Flip 6 Bluetooth Speaker', 'subcategory': 'Speakers', 'brand': 'JBL'}, {'id': 30, 'name': 'Sonos Era 300 Speaker', 'subcategory': 'Speakers', 'brand': 'Sonos'}]
product_name_templates = { "Men's Clothing": ["Casual Shirt", "Formal Shirt", "Denim Jeans", "Polo T-Shirt", "Hoodie"], "Women's Clothing": ["Evening Dress", "Cotton Kurti", "Maxi Dress", "Saree", "Crop Top"], "Footwear": ["Running Shoes", "Sneakers", "Sandals", "Formal Shoes", "Slippers"], "Large Appliances": ["Double Door Refrigerator", "Front Load Washing Machine", "Microwave Oven", "Air Conditioner"], "Small Appliances": ["Mixer Grinder", "Electric Kettle", "Hand Blender", "Toaster"], "Cookware": ["Non-Stick Frying Pan", "Pressure Cooker", "Stainless Steel Pot", "Wok"], "Makeup": ["Lipstick", "Foundation", "Mascara", "Compact Powder"], "Skincare": ["Face Wash", "Moisturizer", "Sunscreen", "Night Cream"], "Gym Equipment": ["Treadmill", "Dumbbell Set", "Exercise Bike", "Yoga Mat"], "Outdoor Gear": ["Camping Tent", "Hiking Backpack", "Sleeping Bag", "Portable Stove"], "Snacks": ["Potato Chips", "Instant Noodles", "Chocolate Bar", "Trail Mix"], "Beverages": ["Orange Juice", "Cola Drink", "Iced Tea", "Energy Drink"], "Toys": ["Building Blocks", "Remote Control Car", "Doll Set", "Puzzle Game"], "Baby Care": ["Baby Lotion", "Diaper Pack", "Baby Shampoo", "Baby Wipes"], "Books": ["Fiction Novel", "Science Textbook", "Children's Storybook", "Self-Help Guide"], "Stationery": ["Notebook", "Gel Pen", "Sketch Markers", "Fountain Pen"]}
categories_brands = { "Men's Clothing": ["Levi's", "Raymond", "Nike", "Adidas"], "Women's Clothing": ["Zara", "Biba", "Michael Kors", "Swarovski"], "Footwear": ["Nike", "Adidas", "Puma", "Reebok"], "Large Appliances": ["LG", "Samsung", "Bosch", "Whirlpool"], "Small Appliances": ["Philips", "Wonderchef", "Prestige", "Bajaj"], "Cookware": ["Prestige", "Hawkins", "Vinod", "Cello"], "Makeup": ["Maybelline", "MAC", "L'Oreal", "Lakme"], "Skincare": ["Neutrogena", "Nivea", "Cetaphil", "Himalaya"], "Gym Equipment": ["PowerMax", "Decathlon", "Cultsport", "Fitkit"], "Outdoor Gear": ["Coleman", "Quechua", "Wildcraft", "The North Face"], "Snacks": ["Lay's", "Maggi", "Kurkure", "Bingo"], "Beverages": ["Tropicana", "Coca-Cola", "Pepsi", "Real"], "Toys": ["LEGO", "Hot Wheels", "Barbie", "Nerf"], "Baby Care": ["Pampers", "Johnson's", "Himalaya", "Mee Mee"], "Books": ["Penguin", "HarperCollins", "Rupa", "Scholastic"], "Stationery": ["Classmate", "Parker", "Faber-Castell", "Pilot"]}

# --- Main Database Insertion Logic ---
try:
    conn = mysql.connector.connect(**db_config)
    print("\n✅ Successfully connected to MySQL database.")
    
    # --- Generate and Insert Categories ---
    main_categories = sorted(list({v[0] for v in category_mapping.values()}))
    category_df = pd.DataFrame({'name': main_categories, 'is_active': 1, 'image_name': [f"https://placehold.co/400x300?text={name.replace(' ', '+')}" for name in main_categories]})
    if not insert_df_in_batches(conn, category_df, 'category'):
         raise Exception("Failed to insert categories, stopping script.")
    
    # --- Generate and Insert Subcategories ---
    db_categories_df = pd.read_sql("SELECT id, name FROM category", conn)
    cat_name_to_id = db_categories_df.set_index('name')['id'].to_dict()
    subcategory_data = [{'name': sub, 'category_id': cat_name_to_id[main]} for sub, (main, _) in category_mapping.items() if main in cat_name_to_id]
    subcategory_df = pd.DataFrame(subcategory_data).drop_duplicates()
    if not insert_df_in_batches(conn, subcategory_df, 'subcategory'):
         raise Exception("Failed to insert subcategories, stopping script.")

    # --- Generate and Insert Products ---
    db_subcategories_df = pd.read_sql("SELECT id, name FROM subcategory", conn)
    subcat_name_to_id = db_subcategories_df.set_index('name')['id'].to_dict()

    # Use 'subcategory_name' as a temporary key
    for p in products_data:
        p['subcategory_name'] = p.pop('subcategory')
        
    current_id = len(products_data) + 1
    while len(products_data) < 1000:
        subcat_name = random.choice(list(categories_brands.keys()))
        brand = random.choice(categories_brands[subcat_name])
        product_type = random.choice(product_name_templates[subcat_name])
        products_data.append({'id': current_id, 'name': f"{brand} {product_type}", 'subcategory_name': subcat_name, 'brand': brand})
        current_id += 1
    
    product_df = pd.DataFrame(products_data)
    product_df.rename(columns={'name': 'title'}, inplace=True)
    product_df['subcategory_id'] = product_df['subcategory_name'].map(subcat_name_to_id)
    
    # ---- THIS IS THE FIRST PART OF THE FIX ----
    # Drop rows with invalid subcategories BEFORE doing anything else
    product_df.dropna(subset=['subcategory_id'], inplace=True)
    product_df['subcategory_id'] = product_df['subcategory_id'].astype(int)
    
    # Now that the DataFrame is clean, we can proceed
    product_df['category'] = product_df['subcategory_name'].map({k: v[0] for k, v in category_mapping.items()})
    product_df['subcategory'] = product_df['subcategory_name']
    product_df['description'] = product_df['title'] + ' - ' + product_df['brand']
    product_df['price'] = [round(random.uniform(10.0, 3000.0), 2) for _ in range(len(product_df))]
    product_df['stock'] = [random.randint(10, 200) for _ in range(len(product_df))]
    product_df['image'] = product_df.apply(lambda row: f"https://placehold.co/600x400?text={row['title'].replace(' ', '+')[:20]}", axis=1)
    product_df['is_active'] = 1
    product_df['discount'] = [random.randint(0, 40) for _ in range(len(product_df))]
    product_df['discount_priced'] = round(product_df['price'] * (1 - product_df['discount'] / 100), 2)
    
    product_df_for_db = product_df[['id', 'title', 'description', 'price', 'discount_priced', 'discount', 'stock', 'image', 'category', 'brand', 'is_active', 'subcategory_id']]
    
    if not insert_df_in_batches(conn, product_df_for_db, 'product'):
        raise Exception("Failed to insert products, stopping script.")

    # --- Generate Users, Cart, and Order Data ---
    NUM_USERS = 20000
    users_data = [{'id': i, 'name': f'User {i}', 'email': f'user{i}@example.com', 'password': 'password123'} for i in range(1, NUM_USERS + 1)]
    users_df = pd.DataFrame(users_data)
    if not insert_df_in_batches(conn, users_df, 'user_dtls'): raise Exception("Failed to insert users, stopping script.")
    
    print("\nGenerating realistic purchase and cart history...")
    purchase_patterns = { 1: [7, 9, 20, 22], 2: [8, 9, 10, 25], 3: [8, 9, 19], 4: [11, 12, 13, 14], 5: [11, 12, 14], 6: [12, 13, 14], 15: [17, 18], 16: [10, 18], 21: [26], 24: [27, 28], 25: [28]}
    NUM_TRANSACTIONS = 100000
    
    # ---- THIS IS THE SECOND PART OF THE FIX ----
    # Create the price map and valid ID list from the FINAL, CLEANED product_df
    valid_product_ids = product_df['id'].tolist()
    product_price_map = product_df.set_index('id')['price'].to_dict()
    
    valid_user_ids = users_df['id'].tolist()
    cart_data = []
    order_data = []
    for i in range(NUM_TRANSACTIONS):
        if (i + 1) % 25000 == 0: print(f"  Generated {i + 1}/{NUM_TRANSACTIONS} transaction records...")
        user_id = random.choice(valid_user_ids)
        
        def create_order_entry(uid, pid):
            quantity = random.randint(1, 3)
            price = product_price_map.get(pid, 0) * quantity
            return {'order_date': datetime.now() - timedelta(days=random.randint(0, 730)), 'payment_type': random.choice(['COD', 'CARD', 'UPI']), 'price': price, 'quantity': quantity, 'status': 'DELIVERED', 'product_id': pid, 'user_id': uid}
            
        # The logic now uses the guaranteed-to-exist product IDs
        if random.random() < 0.7 and purchase_patterns:
            primary_product_id = random.choice(list(purchase_patterns.keys()))
            if primary_product_id in valid_product_ids:
                order_data.append(create_order_entry(user_id, primary_product_id))
                if random.random() < 0.8: cart_data.append({'user_id': user_id, 'product_id': primary_product_id, 'quantity': 1})
                for related_id in purchase_patterns.get(primary_product_id, []):
                    if related_id in valid_product_ids and random.random() < 0.5:
                        order_data.append(create_order_entry(user_id, related_id))
                        if random.random() < 0.8: cart_data.append({'user_id': user_id, 'product_id': related_id, 'quantity': 1})
        else:
            product_id = random.choice(valid_product_ids)
            order_data.append(create_order_entry(user_id, product_id))
            if random.random() < 0.8: cart_data.append({'user_id': user_id, 'product_id': product_id, 'quantity': 1})
            
    cart_df = pd.DataFrame(cart_data).drop_duplicates()
    order_df = pd.DataFrame(order_data).drop_duplicates()
    if not insert_df_in_batches(conn, cart_df, 'cart'): raise Exception("Failed to insert cart data, stopping script.")
    if not insert_df_in_batches(conn, order_df, 'product_order'): raise Exception("Failed to insert order data, stopping script.")

except Exception as e:
    print(f"❌ A critical error occurred: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("\n🔌 Database connection closed. Process finished.")

# --- Create the CSV file for model training ---
print("\n--- Creating CSV file for model training... ---")
cart_df['interaction_score'] = 2.0
order_df['interaction_score'] = 5.0
order_interactions = order_df[['user_id', 'product_id', 'interaction_score']]
cart_interactions = cart_df[['user_id', 'product_id', 'interaction_score']]
combined_interactions = pd.concat([cart_interactions, order_interactions])
final_interactions = combined_interactions.groupby(['user_id', 'product_id'])['interaction_score'].max().reset_index()

product_features_df = product_df[['id', 'category', 'subcategory', 'brand']].rename(columns={'id': 'product_id'})
training_df = pd.merge(final_interactions, product_features_df, on='product_id')

training_df.to_csv('training_data.csv', index=False)
print("✅ Successfully saved `training_data.csv`.")