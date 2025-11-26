# How to Add Real Product Images from Myntra & Ajio

## Current Status
The shopping integration currently uses placeholder image URLs. To add real product images, follow this guide.

## Method 1: Manual Image URLs (Recommended)

### Step 1: Find Product Images

**For Myntra:**
1. Go to https://www.myntra.com
2. Search for a product (e.g., "men's t-shirt")
3. Right-click on product image → "Copy image address"
4. The URL will look like: `https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/...`

**For Ajio:**
1. Go to https://www.ajio.com
2. Search for a product
3. Right-click on product image → "Copy image address"
4. The URL will look like: `https://assets.ajio.com/medias/...`

### Step 2: Update Shopping Data

Edit `web/shopping_data.py` and replace placeholder URLs:

```python
# Example for Myntra
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
            # ADD REAL IMAGE URL HERE:
            'image_url': 'https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/...'
        },
        # ... more products
    ]
}
```

### Step 3: Update App.py to Use Image URLs

The `get_myntra_data()` and `get_ajio_data()` functions in `web/app.py` need to be updated to use the `image_url` field:

```python
def get_myntra_data(query, category="clothing", max_results=5):
    # ... existing code ...
    
    for i, item in enumerate(items[:max_results]):
        myntra_items.append({
            # ... existing fields ...
            'image': item.get('image_url', f'https://assets.myntassets.com/placeholder.jpg'),
            # ... rest of fields ...
        })
```

## Method 2: Use Product IDs (Better)

Instead of full URLs, store product IDs and construct URLs:

```python
MYNTRA_CATALOG = {
    'mens_tshirts': [
        {
            'name': 'Roadster Men Printed Round Neck T-shirt',
            'brand': 'Roadster',
            'product_id': '1234567',  # Myntra product ID
            'price': 399,
            # ... other fields
        }
    ]
}

# Then in get_myntra_data():
'image': f'https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/{item["product_id"]}/1.jpg',
'url': f'https://www.myntra.com/{item["product_id"]}'
```

## Method 3: Web Scraping (Advanced)

### Requirements
```bash
pip install requests beautifulsoup4 selenium
```

### Create Scraper Script

I can create a script that:
1. Searches Myntra/Ajio for products
2. Extracts product details (name, price, image, etc.)
3. Updates the shopping_data.py file

**Note**: Web scraping may violate terms of service. Use official APIs if available.

## Method 4: Use Official APIs (Best Practice)

### Myntra API
- Check if Myntra offers an affiliate or partner API
- Register for API access
- Use official endpoints

### Ajio API
- Check Reliance Retail's developer portal
- Apply for API access
- Use authenticated requests

## Quick Fix: Display Product Links

For now, you can add direct product links so users can see images on the actual websites:

```python
# In chatbot response, add clickable links:
message += f"🔗 [View on Myntra]({item['url']})\n"
message += f"🔗 [View on Ajio]({item['url']})\n"
```

## Example: Adding One Real Product

Let's say you found a Roadster t-shirt on Myntra:

1. **Product URL**: `https://www.myntra.com/tshirts/roadster/roadster-men-printed-round-neck-t-shirt/1234567/buy`
2. **Image URL**: `https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/1234567/2023/1/1/abc123_1.jpg`

Update in `web/shopping_data.py`:

```python
{
    'name': 'Roadster Men Printed Round Neck T-shirt',
    'brand': 'Roadster',
    'price': 399,
    'original': 799,
    'rating': 4.4,
    'reviews': 5600,
    'image_url': 'https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/1234567/2023/1/1/abc123_1.jpg',
    'product_url': 'https://www.myntra.com/tshirts/roadster/roadster-men-printed-round-neck-t-shirt/1234567/buy',
    'colors': ['Black', 'Navy', 'White'],
    'sizes': ['S', 'M', 'L', 'XL', 'XXL']
}
```

## Frontend Display

To display images in the chatbot, update `web/templates/index.html`:

```javascript
// In the chatbot message rendering:
if (item.image) {
    content += `<img src="${item.image}" style="max-width: 100px; border-radius: 8px;" />`;
}
```

## Legal Considerations

⚠️ **Important**:
- Respect copyright and trademark laws
- Don't hotlink images without permission
- Consider downloading and hosting images yourself
- Use official APIs when available
- Add proper attribution

## Alternative: Use Generic Fashion Images

You can use free stock images from:
- Unsplash (https://unsplash.com)
- Pexels (https://pexels.com)
- Pixabay (https://pixabay.com)

Search for "men's t-shirt", "jeans", etc., and use those URLs.

## Next Steps

1. **Choose a method** from above
2. **Collect image URLs** for your products
3. **Update shopping_data.py** with real URLs
4. **Test** the chatbot to see images
5. **Optimize** image loading and caching

---

**Need Help?**
- Let me know which method you prefer
- Provide sample image URLs and I'll integrate them
- I can create a scraper script if needed (with disclaimers)
