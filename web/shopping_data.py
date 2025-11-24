"""
Shopping Data for Myntra and Ajio
Comprehensive product catalog for virtual try-on chatbot
"""

# Myntra Product Catalog
MYNTRA_CATALOG = {
    'mens_tshirts': [
        {'name': 'Roadster Men Printed Round Neck T-shirt', 'brand': 'Roadster', 'price': 399, 'original': 799, 'rating': 4.4, 'reviews': 5600, 'colors': ['Black', 'Navy', 'White', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'H&M Men Oversized Fit T-shirt', 'brand': 'H&M', 'price': 699, 'original': 999, 'rating': 4.2, 'reviews': 3400, 'colors': ['Black', 'White', 'Olive'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Nike Men Dri-FIT Training T-shirt', 'brand': 'Nike', 'price': 1495, 'original': 1995, 'rating': 4.6, 'reviews': 4200, 'colors': ['Black', 'Navy', 'Red'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Puma Men Essential Logo T-shirt', 'brand': 'Puma', 'price': 849, 'original': 1299, 'rating': 4.3, 'reviews': 2800, 'colors': ['Black', 'White', 'Blue'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Wrogn Men Graphic Print T-shirt', 'brand': 'Wrogn', 'price': 599, 'original': 1199, 'rating': 4.1, 'reviews': 1900, 'colors': ['Black', 'Navy', 'Maroon'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'HRX Men Active T-shirt', 'brand': 'HRX', 'price': 549, 'original': 999, 'rating': 4.2, 'reviews': 3100, 'colors': ['Black', 'Grey', 'Blue'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Levis Men Graphic T-shirt', 'brand': 'Levis', 'price': 799, 'original': 1299, 'rating': 4.3, 'reviews': 2400, 'colors': ['White', 'Black', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Adidas Men Training T-shirt', 'brand': 'Adidas', 'price': 1199, 'original': 1799, 'rating': 4.5, 'reviews': 3600, 'colors': ['Black', 'Navy', 'White'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'mens_shirts': [
        {'name': 'Roadster Men Slim Fit Casual Shirt', 'brand': 'Roadster', 'price': 699, 'original': 1399, 'rating': 4.3, 'reviews': 2450, 'colors': ['Blue', 'White', 'Pink'], 'sizes': ['38', '40', '42', '44']},
        {'name': 'H&M Men Regular Fit Cotton Shirt', 'brand': 'H&M', 'price': 1299, 'original': 1999, 'rating': 4.1, 'reviews': 1820, 'colors': ['White', 'Blue', 'Black'], 'sizes': ['38', '40', '42', '44']},
        {'name': 'Levis Men Classic Western Shirt', 'brand': 'Levis', 'price': 1899, 'original': 2999, 'rating': 4.5, 'reviews': 3200, 'colors': ['Denim', 'Black', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Allen Solly Men Formal Shirt', 'brand': 'Allen Solly', 'price': 1499, 'original': 2499, 'rating': 4.2, 'reviews': 1650, 'colors': ['White', 'Blue', 'Pink'], 'sizes': ['38', '40', '42', '44', '46']},
        {'name': 'Peter England Men Checked Shirt', 'brand': 'Peter England', 'price': 899, 'original': 1599, 'rating': 4.0, 'reviews': 2100, 'colors': ['Blue', 'Green', 'Red'], 'sizes': ['38', '40', '42', '44']},
        {'name': 'Van Heusen Men Slim Fit Shirt', 'brand': 'Van Heusen', 'price': 1299, 'original': 2199, 'rating': 4.3, 'reviews': 1900, 'colors': ['White', 'Blue', 'Grey'], 'sizes': ['38', '40', '42', '44']},
    ],
    
    'mens_jeans': [
        {'name': 'Levis Men 511 Slim Fit Jeans', 'brand': 'Levis', 'price': 2799, 'original': 3999, 'rating': 4.5, 'reviews': 8900, 'colors': ['Blue', 'Black', 'Grey'], 'sizes': ['28', '30', '32', '34', '36']},
        {'name': 'Roadster Men Skinny Fit Jeans', 'brand': 'Roadster', 'price': 1199, 'original': 1999, 'rating': 4.2, 'reviews': 4500, 'colors': ['Blue', 'Black'], 'sizes': ['28', '30', '32', '34', '36']},
        {'name': 'Wrangler Men Regular Fit Jeans', 'brand': 'Wrangler', 'price': 1899, 'original': 2999, 'rating': 4.4, 'reviews': 3200, 'colors': ['Blue', 'Black', 'Grey'], 'sizes': ['30', '32', '34', '36']},
        {'name': 'Flying Machine Men Tapered Jeans', 'brand': 'Flying Machine', 'price': 1599, 'original': 2499, 'rating': 4.1, 'reviews': 2700, 'colors': ['Blue', 'Black'], 'sizes': ['28', '30', '32', '34']},
        {'name': 'Spykar Men Slim Fit Jeans', 'brand': 'Spykar', 'price': 1799, 'original': 2799, 'rating': 4.3, 'reviews': 2100, 'colors': ['Blue', 'Black', 'Grey'], 'sizes': ['30', '32', '34', '36']},
    ],
    
    'womens_dresses': [
        {'name': 'H&M Women Floral Print Maxi Dress', 'brand': 'H&M', 'price': 1999, 'original': 2999, 'rating': 4.3, 'reviews': 1850, 'colors': ['Floral', 'Black', 'Blue'], 'sizes': ['XS', 'S', 'M', 'L']},
        {'name': 'Mango Women Midi Wrap Dress', 'brand': 'Mango', 'price': 2499, 'original': 3999, 'rating': 4.4, 'reviews': 1200, 'colors': ['Red', 'Black', 'Navy'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Vero Moda Women A-Line Dress', 'brand': 'Vero Moda', 'price': 1799, 'original': 2999, 'rating': 4.2, 'reviews': 2100, 'colors': ['Black', 'Navy', 'Maroon'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Forever 21 Women Bodycon Dress', 'brand': 'Forever 21', 'price': 1299, 'original': 1999, 'rating': 4.0, 'reviews': 1650, 'colors': ['Black', 'Red', 'White'], 'sizes': ['XS', 'S', 'M', 'L']},
        {'name': 'Only Women Casual Shirt Dress', 'brand': 'Only', 'price': 1599, 'original': 2499, 'rating': 4.1, 'reviews': 1400, 'colors': ['Blue', 'White', 'Pink'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'womens_kurtas': [
        {'name': 'Libas Women Printed Straight Kurta', 'brand': 'Libas', 'price': 899, 'original': 1799, 'rating': 4.4, 'reviews': 3200, 'colors': ['Blue', 'Pink', 'Green'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Biba Women Embroidered Anarkali Kurta', 'brand': 'Biba', 'price': 1499, 'original': 2499, 'rating': 4.5, 'reviews': 4100, 'colors': ['Pink', 'Blue', 'Yellow'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'W Women Ethnic Motifs Kurta', 'brand': 'W', 'price': 1199, 'original': 1999, 'rating': 4.2, 'reviews': 2800, 'colors': ['Blue', 'Red', 'Green'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Sangria Women Floral Print Kurta', 'brand': 'Sangria', 'price': 1099, 'original': 1899, 'rating': 4.3, 'reviews': 2400, 'colors': ['Pink', 'Blue', 'White'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Aurelia Women Solid A-Line Kurta', 'brand': 'Aurelia', 'price': 999, 'original': 1699, 'rating': 4.1, 'reviews': 1900, 'colors': ['Blue', 'Pink', 'Yellow'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'jackets': [
        {'name': 'Roadster Men Denim Jacket', 'brand': 'Roadster', 'price': 1799, 'original': 2999, 'rating': 4.3, 'reviews': 2100, 'colors': ['Blue', 'Black'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'H&M Men Bomber Jacket', 'brand': 'H&M', 'price': 2499, 'original': 3999, 'rating': 4.2, 'reviews': 1650, 'colors': ['Black', 'Navy', 'Olive'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Levis Men Trucker Jacket', 'brand': 'Levis', 'price': 3999, 'original': 5999, 'rating': 4.6, 'reviews': 2800, 'colors': ['Denim', 'Black'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Puma Men Padded Jacket', 'brand': 'Puma', 'price': 2999, 'original': 4999, 'rating': 4.4, 'reviews': 1900, 'colors': ['Black', 'Navy', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Nike Men Windrunner Jacket', 'brand': 'Nike', 'price': 3499, 'original': 5499, 'rating': 4.5, 'reviews': 2300, 'colors': ['Black', 'Navy', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'shoes': [
        {'name': 'Nike Men Air Max Sneakers', 'brand': 'Nike', 'price': 5995, 'original': 7995, 'rating': 4.6, 'reviews': 4200, 'colors': ['Black', 'White', 'Blue'], 'sizes': ['7', '8', '9', '10', '11']},
        {'name': 'Puma Men Smash V2 Sneakers', 'brand': 'Puma', 'price': 2499, 'original': 3999, 'rating': 4.3, 'reviews': 3100, 'colors': ['White', 'Black', 'Navy'], 'sizes': ['7', '8', '9', '10', '11']},
        {'name': 'Adidas Men Superstar Shoes', 'brand': 'Adidas', 'price': 4999, 'original': 6999, 'rating': 4.5, 'reviews': 5600, 'colors': ['White', 'Black'], 'sizes': ['7', '8', '9', '10', '11', '12']},
        {'name': 'Roadster Men Casual Shoes', 'brand': 'Roadster', 'price': 1299, 'original': 1999, 'rating': 4.1, 'reviews': 2400, 'colors': ['Black', 'Brown', 'Navy'], 'sizes': ['7', '8', '9', '10']},
        {'name': 'Red Tape Men Formal Shoes', 'brand': 'Red Tape', 'price': 1999, 'original': 3499, 'rating': 4.2, 'reviews': 1800, 'colors': ['Black', 'Brown'], 'sizes': ['7', '8', '9', '10', '11']},
    ],
}

# Ajio Product Catalog
AJIO_CATALOG = {
    'mens_tshirts': [
        {'name': 'DNMX Men Graphic Print T-shirt', 'brand': 'DNMX', 'price': 349, 'original': 699, 'rating': 4.3, 'reviews': 4200, 'colors': ['Black', 'Navy', 'White'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Teamspirit Men Solid T-shirt', 'brand': 'Teamspirit', 'price': 449, 'original': 899, 'rating': 4.1, 'reviews': 3100, 'colors': ['Black', 'White', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Adidas Men Training T-shirt', 'brand': 'Adidas', 'price': 1199, 'original': 1799, 'rating': 4.5, 'reviews': 2800, 'colors': ['Black', 'Navy', 'Red'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Puma Men Essential T-shirt', 'brand': 'Puma', 'price': 799, 'original': 1299, 'rating': 4.2, 'reviews': 2400, 'colors': ['Black', 'White', 'Blue'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'US Polo Men Crew Neck T-shirt', 'brand': 'US Polo', 'price': 699, 'original': 1199, 'rating': 4.0, 'reviews': 1900, 'colors': ['Navy', 'White', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Jack & Jones Men Printed T-shirt', 'brand': 'Jack & Jones', 'price': 899, 'original': 1499, 'rating': 4.3, 'reviews': 2100, 'colors': ['Black', 'Navy', 'White'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'mens_shirts': [
        {'name': 'DNMX Men Slim Fit Casual Shirt', 'brand': 'DNMX', 'price': 649, 'original': 1299, 'rating': 4.2, 'reviews': 1850, 'colors': ['Blue', 'White', 'Black'], 'sizes': ['38', '40', '42', '44']},
        {'name': 'Netplay Men Regular Fit Shirt', 'brand': 'Netplay', 'price': 899, 'original': 1599, 'rating': 4.0, 'reviews': 1200, 'colors': ['White', 'Blue', 'Pink'], 'sizes': ['38', '40', '42', '44']},
        {'name': 'US Polo Men Checked Shirt', 'brand': 'US Polo', 'price': 1399, 'original': 2299, 'rating': 4.3, 'reviews': 2100, 'colors': ['Blue', 'Green', 'Red'], 'sizes': ['38', '40', '42', '44', '46']},
        {'name': 'Jack & Jones Men Denim Shirt', 'brand': 'Jack & Jones', 'price': 1599, 'original': 2499, 'rating': 4.4, 'reviews': 1650, 'colors': ['Denim', 'Black'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Arrow Men Formal Shirt', 'brand': 'Arrow', 'price': 1299, 'original': 2199, 'rating': 4.1, 'reviews': 1900, 'colors': ['White', 'Blue', 'Grey'], 'sizes': ['38', '40', '42', '44']},
    ],
    
    'mens_jeans': [
        {'name': 'DNMX Men Slim Fit Jeans', 'brand': 'DNMX', 'price': 999, 'original': 1799, 'rating': 4.2, 'reviews': 3600, 'colors': ['Blue', 'Black'], 'sizes': ['28', '30', '32', '34', '36']},
        {'name': 'Lee Cooper Men Skinny Jeans', 'brand': 'Lee Cooper', 'price': 1499, 'original': 2499, 'rating': 4.3, 'reviews': 2800, 'colors': ['Blue', 'Black', 'Grey'], 'sizes': ['28', '30', '32', '34']},
        {'name': 'Pepe Jeans Men Regular Fit', 'brand': 'Pepe Jeans', 'price': 1899, 'original': 2999, 'rating': 4.4, 'reviews': 3200, 'colors': ['Blue', 'Black'], 'sizes': ['30', '32', '34', '36']},
        {'name': 'Jack & Jones Men Tapered Jeans', 'brand': 'Jack & Jones', 'price': 1799, 'original': 2799, 'rating': 4.1, 'reviews': 2100, 'colors': ['Blue', 'Black', 'Grey'], 'sizes': ['30', '32', '34', '36']},
        {'name': 'US Polo Men Stretch Jeans', 'brand': 'US Polo', 'price': 1599, 'original': 2399, 'rating': 4.2, 'reviews': 1850, 'colors': ['Blue', 'Black'], 'sizes': ['28', '30', '32', '34', '36']},
    ],
    
    'womens_dresses': [
        {'name': 'Vero Moda Women Floral Dress', 'brand': 'Vero Moda', 'price': 1699, 'original': 2799, 'rating': 4.3, 'reviews': 1650, 'colors': ['Floral', 'Black'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Only Women Midi Dress', 'brand': 'Only', 'price': 1499, 'original': 2499, 'rating': 4.2, 'reviews': 1400, 'colors': ['Black', 'Navy', 'Red'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Marks & Spencer Women A-Line Dress', 'brand': 'M&S', 'price': 1999, 'original': 3299, 'rating': 4.4, 'reviews': 1200, 'colors': ['Black', 'Blue', 'Pink'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Vero Moda Women Wrap Dress', 'brand': 'Vero Moda', 'price': 1799, 'original': 2999, 'rating': 4.1, 'reviews': 1100, 'colors': ['Red', 'Black', 'Navy'], 'sizes': ['S', 'M', 'L']},
        {'name': 'Only Women Casual Dress', 'brand': 'Only', 'price': 1299, 'original': 2199, 'rating': 4.0, 'reviews': 980, 'colors': ['Blue', 'White', 'Pink'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'womens_kurtas': [
        {'name': 'Soch Women Embroidered Kurta', 'brand': 'Soch', 'price': 1199, 'original': 1999, 'rating': 4.4, 'reviews': 2800, 'colors': ['Pink', 'Blue', 'Yellow'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Rangmanch Women Printed Kurta', 'brand': 'Rangmanch', 'price': 899, 'original': 1599, 'rating': 4.2, 'reviews': 2100, 'colors': ['Blue', 'Pink', 'Green'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Avaasa Women Straight Kurta', 'brand': 'Avaasa', 'price': 1099, 'original': 1899, 'rating': 4.3, 'reviews': 1850, 'colors': ['Blue', 'Red', 'White'], 'sizes': ['S', 'M', 'L', 'XL', 'XXL']},
        {'name': 'Soch Women Anarkali Kurta', 'brand': 'Soch', 'price': 1399, 'original': 2299, 'rating': 4.5, 'reviews': 2400, 'colors': ['Pink', 'Blue', 'Yellow'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Rangmanch Women Ethnic Kurta', 'brand': 'Rangmanch', 'price': 999, 'original': 1699, 'rating': 4.1, 'reviews': 1650, 'colors': ['Blue', 'Pink', 'Green'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'jackets': [
        {'name': 'DNMX Men Denim Jacket', 'brand': 'DNMX', 'price': 1599, 'original': 2799, 'rating': 4.2, 'reviews': 1850, 'colors': ['Blue', 'Black'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Jack & Jones Men Bomber Jacket', 'brand': 'Jack & Jones', 'price': 2299, 'original': 3799, 'rating': 4.4, 'reviews': 1400, 'colors': ['Black', 'Navy', 'Olive'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Adidas Men Track Jacket', 'brand': 'Adidas', 'price': 2499, 'original': 3999, 'rating': 4.3, 'reviews': 1650, 'colors': ['Black', 'Navy', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'Puma Men Hooded Jacket', 'brand': 'Puma', 'price': 2199, 'original': 3499, 'rating': 4.1, 'reviews': 1200, 'colors': ['Black', 'Navy', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
        {'name': 'US Polo Men Windcheater', 'brand': 'US Polo', 'price': 1899, 'original': 2999, 'rating': 4.2, 'reviews': 1500, 'colors': ['Black', 'Navy', 'Grey'], 'sizes': ['S', 'M', 'L', 'XL']},
    ],
    
    'shoes': [
        {'name': 'Adidas Men Running Shoes', 'brand': 'Adidas', 'price': 3999, 'original': 5999, 'rating': 4.5, 'reviews': 3200, 'colors': ['Black', 'White', 'Blue'], 'sizes': ['7', '8', '9', '10', '11']},
        {'name': 'Puma Men Casual Sneakers', 'brand': 'Puma', 'price': 2299, 'original': 3799, 'rating': 4.3, 'reviews': 2400, 'colors': ['White', 'Black', 'Navy'], 'sizes': ['7', '8', '9', '10', '11']},
        {'name': 'Reebok Men Training Shoes', 'brand': 'Reebok', 'price': 2999, 'original': 4499, 'rating': 4.4, 'reviews': 2100, 'colors': ['Black', 'Grey', 'Blue'], 'sizes': ['7', '8', '9', '10', '11']},
        {'name': 'Red Tape Men Casual Shoes', 'brand': 'Red Tape', 'price': 1799, 'original': 2999, 'rating': 4.1, 'reviews': 1650, 'colors': ['Black', 'Brown', 'Navy'], 'sizes': ['7', '8', '9', '10']},
        {'name': 'US Polo Men Sneakers', 'brand': 'US Polo', 'price': 1999, 'original': 3299, 'rating': 4.2, 'reviews': 1850, 'colors': ['White', 'Black', 'Navy'], 'sizes': ['7', '8', '9', '10', '11']},
    ],
}

# Category mapping for search queries
CATEGORY_MAPPING = {
    't-shirt': 'mens_tshirts',
    'tshirt': 'mens_tshirts',
    'tee': 'mens_tshirts',
    'shirt': 'mens_shirts',
    'jeans': 'mens_jeans',
    'denim': 'mens_jeans',
    'dress': 'womens_dresses',
    'kurta': 'womens_kurtas',
    'kurti': 'womens_kurtas',
    'jacket': 'jackets',
    'shoes': 'shoes',
    'sneakers': 'shoes',
    'footwear': 'shoes',
}

def get_category_from_query(query):
    """Map search query to product category"""
    query_lower = query.lower()
    
    # Check for direct matches
    for key, category in CATEGORY_MAPPING.items():
        if key in query_lower:
            return category
    
    # Default to t-shirts if no match
    return 'mens_tshirts'
