import streamlit as st
import pandas as pd
import os

# Set page title and icon
st.set_page_config(page_title="Sapphire Online Store", page_icon="👗", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
/* Custom header */
.header {
    background-color: #6C5B7B;
    color: white;
    padding: 20px;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Custom footer */
.footer {
    background-color: #6C5B7B;
    color: white;
    padding: 10px;
    text-align: center;
    font-size: 14px;
    border-radius: 10px;
    margin-top: 20px;
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background-color: #F8B195;
    padding: 10px;
    border-radius: 10px;
}

/* Product card styling */
.card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: white;
}

.card img {
    border-radius: 10px;
}

.card h3 {
    color: #6C5B7B;
    font-size: 24px;
    margin-bottom: 10px;
}

.card p {
    color: #555;
    font-size: 16px;
    margin-bottom: 5px;
}

/* Button styling */
.stButton button {
    background-color: #6C5B7B;
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #4A3F55;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    collection = pd.read_csv("sapphire_collection_extended.csv")
    products = pd.read_csv("sapphire_products.csv")
    return collection, products

collection, products = load_data()

# Initialize session state for cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Function to add items to cart
def add_to_cart(product_name, price):
    st.session_state.cart.append({"Product": product_name, "Price": price})
    st.success(f"Added {product_name} to cart!")

# Custom header
st.markdown('<div class="header">Sapphire Online Store</div>', unsafe_allow_html=True)

# Sidebar for navigation and filters
st.sidebar.title("Navigation & Filters")
options = st.sidebar.radio("Go to",["Home", "Collection", "Products", "Cart"])

# Search bar
search_query = st.sidebar.text_input("Search by product name")

# Filter by category
categories = collection["Category"].unique()
selected_category = st.sidebar.selectbox("Filter by category", ["All"] + list(categories))

# Sort by price
sort_option = st.sidebar.selectbox("Sort by price", ["None", "Low to High", "High to Low"])

# Home Page
if options == "Home":
    st.markdown('<p class="big-font">Explore our latest collection of clothing and accessories.</p>', unsafe_allow_html=True)
    
    if os.path.exists("static/product_1.jpg"):
        st.image("static/product_32.jpg", width=800, use_container_width=True)
    else:
        st.error("Image not found: static/product_1.jpg")

# Collection Page
elif options == "Collection":
    st.title("Sapphire Collection")
    st.write("Browse through our exclusive collection.")
    
    # Apply filters and search
    filtered_collection = collection.copy()
    if search_query:
        filtered_collection = filtered_collection[filtered_collection["Name"].str.contains(search_query, case=False)]
    if selected_category != "All":
        filtered_collection = filtered_collection[filtered_collection["Category"] == selected_category]
    if sort_option == "Low to High":
        filtered_collection = filtered_collection.sort_values(by="Price", ascending=True)
    elif sort_option == "High to Low":
        filtered_collection = filtered_collection.sort_values(by="Price", ascending=False)
    
    # Display collection items in cards
    for index, row in filtered_collection.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                image_path = f"product_{index+1}.jpg"
                if os.path.exists(image_path):
                    st.image(image_path, width=200)
                else:
                    st.error(f"Image not found: {image_path}")
            with col2:
                st.markdown(f'<h3>{row["Name"]}</h3>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Price:</strong> ₹{row["Price"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Stock:</strong> {row["Stock"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Category:</strong> {row["Category"]}</p>', unsafe_allow_html=True)
                if st.button(f"Add to Cart - {row['Name']}", key=f"add_{index}"):
                    add_to_cart(row["Name"], row["Price"])
            st.markdown('</div>', unsafe_allow_html=True)

# Products Page
elif options == "Products":
    st.title("All Products")
    st.write("Check out all our products.")
    
    # Apply filters and search
    filtered_products = products.copy()
    if search_query:
        filtered_products = filtered_products[filtered_products["Name"].str.contains(search_query, case=False)]
    if sort_option == "Low to High":
        filtered_products = filtered_products.sort_values(by="Price", ascending=True)
    elif sort_option == "High to Low":
        filtered_products = filtered_products.sort_values(by="Price", ascending=False)
    
    # Display all products in cards
    for index, row in filtered_products.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                if os.path.exists(row["Image"]):
                    st.image(row["Image"], width=200)
                else:
                    st.error(f"Image not found: {row['Image']}")
            with col2:
                st.markdown(f'<h3>{row["Name"]}</h3>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Price:</strong> ₹{row["Price"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Stock:</strong> {row["Stock"]}</p>', unsafe_allow_html=True)
                if st.button(f"Add to Cart - {row['Name']}", key=f"add_{index}"):
                    add_to_cart(row["Name"], row["Price"])
            st.markdown('</div>', unsafe_allow_html=True)

# Cart Page
elif options == "Cart":
    st.title("Your Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        st.write("Here are the items in your cart:")
        for item in st.session_state.cart:
            st.markdown(f'<div class="card"><p><strong>{item["Product"]}</strong> - ₹{item["Price"]}</p></div>', unsafe_allow_html=True)
        total_price = sum(item["Price"] for item in st.session_state.cart)
        st.write(f"**Total Price:** ₹{total_price}")
        if st.button("Checkout"):
            st.session_state.cart = []
            st.success("Thank you for your purchase! Your cart is now empty.")

# Custom footer
st.markdown("""
<div class="footer">
    <p>© 2023 Sapphire Online Store. All rights reserved.</p>
    <p>Follow us: 
        <a href="https://facebook.com" target="_blank">Facebook</a> | 
        <a href="https://instagram.com" target="_blank">Instagram</a> | 
        <a href="https://twitter.com" target="_blank">Twitter</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Created by Nayab Dilbar, Rabail Sarwar and Co.")