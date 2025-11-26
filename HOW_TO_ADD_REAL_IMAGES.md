# How to Add Real Product Images - Step by Step

## ✅ System is Ready!

I've updated the code to support real product images. Now you just need to add the image URLs.

## Quick Steps

### 1. Find a Product on Myntra

1. Go to https://www.myntra.com
2. Search for "men's t-shirt" (or any product)
3. Click on a product you like
4. Right-click on the product image
5. Select "Copy image address"
6. You'll get a URL like:
   ```
   https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/12345678/2023/1/1/abc123_1.jpg
   ```

### 2. Add to Shopping Data

Open `web/shopping_data.py` and add the `image_url` and `product_url` fields:

```python
MYNTRA_CATALOG = {
    'mens_tshirts': [
        {
            'name': 'Roadster Men Printed Round Neck T-shirt',
            'brand': 'Roadster',
            'price': 399,
            'original': 799,
            'rating': 4.4,
            'reviews': 5600,
            'colors': ['Black', 'Navy', 'White', 'Grey'],
            'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
            
            # ADD THESE TWO LINES:
            'image_url': 'https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/12345678/2023/1/1/abc123_1.jpg',
            'product_url': 'https://www.myntra.com/tshirts/roadster/roadster-men-printed-round-neck-t-shirt/12345678/buy'
        },
        # ... rest of products
    ]
}
```

### 3. Same for Ajio

1. Go to https://www.ajio.com
2. Search and find a product
3. Copy image URL
4. Add to `AJIO_CATALOG` in the same way

### 4. Test It

1. Restart the Flask server (it will auto-reload)
2. Open chatbot
3. Type "Search for t-shirts"
4. You'll see the real images!

## Example: Complete Product Entry

Here's a complete example with real URLs:

```python
{
    'name': 'Roadster Men Printed Round Neck T-shirt',
    'brand': 'Roadster',
    'price': 399,
    'original': 799,
    'rating': 4.4,
    'reviews': 5600,
    'colors': ['Black', 'Navy', 'White', 'Grey'],
    'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
    'image_url': 'https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/productimage.jpg',
    'product_url': 'https://www.myntra.com/tshirts/roadster/product-name/12345678/buy'
},
```

## What Happens Without Real URLs?

- The system uses placeholder URLs
- Products still show with all details (price, rating, etc.)
- Users can click links to see products on Myntra/Ajio

## What Happens With Real URLs?

- Actual product images display in chatbot
- Direct links to specific products
- Better user experience

## Quick Test

After adding URLs, test with:

```bash
python test_shopping_api.py
```

Or in the chatbot:
- "Search for t-shirts"
- "Show trending items"
- "Compare prices"

## Need Help?

If you provide me with:
1. Product names you want
2. Myntra/Ajio product URLs

I can help format them correctly for the shopping_data.py file!

---

**Current Status**: ✅ Code is ready to accept real image URLs
**Next Step**: Add `image_url` and `product_url` to products in `web/shopping_data.py`
