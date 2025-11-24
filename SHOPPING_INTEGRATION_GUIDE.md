# Shopping Integration Guide - Myntra & Ajio

## Overview
The chatbot now includes comprehensive shopping data from Myntra and Ajio, allowing users to search, compare, and discover clothing items directly through the virtual try-on interface.

## Features Added

### 1. **Product Catalog**
- **Myntra**: 40+ products across 7 categories
- **Ajio**: 40+ products across 7 categories
- Categories: T-shirts, Shirts, Jeans, Dresses, Kurtas, Jackets, Shoes

### 2. **Product Information**
Each product includes:
- Product name and brand
- Current price and original price
- Discount percentage
- Customer ratings (out of 5)
- Number of reviews
- Available sizes
- Available colors
- Delivery time
- Stock status
- Direct links to product pages

### 3. **Chatbot Commands**

#### Search for Items
```
"Search for t-shirts"
"Find jeans"
"Show me kurtas"
"I want to buy shoes"
```

#### Compare Prices
```
"Compare t-shirt prices"
"Compare prices for jeans"
"Show price comparison"
```

#### Trending Items
```
"Show trending items"
"What's trending?"
"Latest fashion"
"Popular items"
```

#### Shopping Mode
```
"I want to shop"
"Buy clothes"
"Shopping on Myntra"
"Ajio products"
```

## Product Categories

### Men's Wear
1. **T-Shirts** (8 items each platform)
   - Brands: Roadster, H&M, Nike, Puma, Wrogn, HRX, Levis, Adidas
   - Price Range: ₹349 - ₹1,495

2. **Shirts** (5-6 items each platform)
   - Brands: Roadster, H&M, Levis, Allen Solly, Peter England, Van Heusen
   - Price Range: ₹649 - ₹1,899

3. **Jeans** (5 items each platform)
   - Brands: Levis, Roadster, Wrangler, Flying Machine, Spykar
   - Price Range: ₹999 - ₹2,799

### Women's Wear
4. **Dresses** (5 items each platform)
   - Brands: H&M, Mango, Vero Moda, Forever 21, Only
   - Price Range: ₹1,299 - ₹2,499

5. **Kurtas** (5 items each platform)
   - Brands: Libas, Biba, W, Sangria, Aurelia, Soch, Rangmanch
   - Price Range: ₹899 - ₹1,499

### Unisex
6. **Jackets** (5 items each platform)
   - Brands: Roadster, H&M, Levis, Puma, Nike, Jack & Jones
   - Price Range: ₹1,599 - ₹3,999

7. **Shoes** (5 items each platform)
   - Brands: Nike, Puma, Adidas, Roadster, Red Tape, Reebok
   - Price Range: ₹1,299 - ₹5,995

## API Endpoints

### 1. Search Products
```
POST /api/shopping/search
Body: {
  "query": "t-shirt",
  "category": "clothing",
  "max_results": 5
}
```

### 2. Compare Prices
```
POST /api/shopping/compare
Body: {
  "item_name": "t-shirt"
}
```

### 3. Get Trending Items
```
GET /api/shopping/trending
```

## Response Format

### Search Response
```json
{
  "success": true,
  "query": "t-shirt",
  "results": {
    "myntra": [
      {
        "id": "MYN001",
        "name": "Roadster Men Printed Round Neck T-shirt",
        "brand": "Roadster",
        "price": 399,
        "original_price": 799,
        "discount": 50,
        "rating": 4.4,
        "reviews": 5600,
        "image": "https://assets.myntassets.com/...",
        "url": "https://www.myntra.com/...",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Black", "Navy", "White", "Grey"],
        "category": "clothing",
        "platform": "Myntra",
        "in_stock": true,
        "delivery": "2-3 days"
      }
    ],
    "ajio": [...],
    "summary": {
      "total_items": 10,
      "price_range": {
        "min": 349,
        "max": 1495,
        "avg": 750
      },
      "platforms": 2
    }
  }
}
```

## Chatbot Integration

### Example Conversations

**User**: "I want to buy a t-shirt"
**Bot**: Shows shopping mode message with options to search Myntra & Ajio

**User**: "Search for t-shirts"
**Bot**: Displays 6 t-shirts (3 from Myntra, 3 from Ajio) with:
- Product names and brands
- Prices with discounts
- Ratings and reviews
- Direct links to buy

**User**: "Compare t-shirt prices"
**Bot**: Shows price comparison sorted by lowest to highest price

**User**: "Show trending items"
**Bot**: Displays 5 trending categories with best deals from both platforms

## File Structure

```
web/
├── app.py                    # Main Flask application with shopping routes
├── shopping_data.py          # Comprehensive product catalog
└── templates/
    └── index.html           # Frontend with chatbot integration
```

## Data Management

### Adding New Products
Edit `web/shopping_data.py`:

```python
MYNTRA_CATALOG = {
    'category_name': [
        {
            'name': 'Product Name',
            'brand': 'Brand Name',
            'price': 999,
            'original': 1999,
            'rating': 4.5,
            'reviews': 1000,
            'colors': ['Black', 'White'],
            'sizes': ['S', 'M', 'L', 'XL']
        },
        # Add more products...
    ]
}
```

### Adding New Categories
1. Add category to `MYNTRA_CATALOG` and `AJIO_CATALOG`
2. Update `CATEGORY_MAPPING` in `shopping_data.py`
3. Update chatbot responses in `get_chatbot_response()` function

## Benefits

1. **Seamless Shopping Experience**: Users can search and compare products without leaving the virtual try-on interface
2. **Price Comparison**: Automatically compare prices across Myntra and Ajio
3. **Comprehensive Data**: Detailed product information including ratings, reviews, and availability
4. **Smart Search**: Intelligent category mapping for natural language queries
5. **Trending Insights**: Stay updated with latest fashion trends

## Future Enhancements

1. **Real API Integration**: Connect to actual Myntra and Ajio APIs
2. **Image Integration**: Display actual product images
3. **Virtual Try-On Integration**: Allow users to try on searched products
4. **Wishlist Feature**: Save favorite items
5. **Price Alerts**: Notify users of price drops
6. **Size Recommendations**: AI-powered size suggestions
7. **Style Matching**: Match products with user's body type and preferences

## Testing

### Test the Shopping Features

1. Start the Flask server:
```bash
cd web
python app.py
```

2. Open the chatbot and try these commands:
   - "Search for t-shirts"
   - "Show trending items"
   - "Compare jeans prices"
   - "I want to buy shoes"

3. Verify:
   - Products are displayed correctly
   - Prices and discounts are accurate
   - Links are properly formatted
   - Chatbot suggestions work

## Notes

- All product data is currently simulated for demonstration
- Prices are in Indian Rupees (₹)
- Product images use placeholder URLs
- Links redirect to platform search pages
- Data can be easily replaced with real API responses

## Support

For issues or questions:
1. Check the console for error messages
2. Verify `shopping_data.py` is in the `web/` directory
3. Ensure Flask server is running
4. Check browser console for frontend errors

---

**Last Updated**: November 24, 2025
**Version**: 1.0
**Status**: ✅ Fully Integrated
