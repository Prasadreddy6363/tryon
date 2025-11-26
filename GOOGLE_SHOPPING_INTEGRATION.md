# Google Shopping Integration

## ✅ Feature Added

The chatbot now includes direct links to Google Shopping for browsing more Myntra and Ajio products!

## How It Works

### 1. General Shopping Query
When users ask general shopping questions:
- "I want to shop"
- "Show me shopping options"
- "Myntra and Ajio"

**Response includes:**
```
🔗 View All Myntra & Ajio Products on Google Shopping
https://www.google.com/search?udm=28&q=myntra+and+ajio
```

### 2. Specific Product Search
When users search for specific items:
- "Search for t-shirts"
- "Find jeans"
- "Show me shoes"

**Response includes:**
- Our curated product list (6 items)
- Prices, ratings, discounts
- **Plus** a Google Shopping link at the bottom:
```
🔍 Want more options?
Browse all t-shirts on Google Shopping
https://www.google.com/search?udm=28&q=t-shirt+myntra+ajio
```

## Benefits

✅ **More Options** - Users can browse thousands of products  
✅ **Real Images** - Google Shopping shows actual product photos  
✅ **Live Prices** - Current prices from Myntra and Ajio  
✅ **Direct Links** - Click to go straight to product pages  
✅ **Comparison** - See products from both platforms side-by-side  

## Example Conversations

### Example 1: General Shopping
```
User: "I want to shop"

Bot: 🛍️ Shopping Assistant Ready!
     
     I can help you:
     • Search items on Myntra & Ajio
     • Compare prices across platforms
     • Show trending fashion items
     
     Browse More:
     🔗 View All Myntra & Ajio Products on Google Shopping
     
     What would you like to shop for today?
```

### Example 2: Specific Search
```
User: "Search for t-shirts"

Bot: 🛍️ Found 6 t-shirt items across 2 platforms!
     
     💰 Price Range: ₹349 - ₹1,495
     
     🏪 Myntra (3 items):
     • Roadster Men T-shirt - ₹399 (50% off) ⭐4.4
     • H&M Oversized T-shirt - ₹699 (30% off) ⭐4.2
     • Nike Dri-FIT T-shirt - ₹1,495 (25% off) ⭐4.6
     
     🏪 Ajio (3 items):
     • DNMX Graphic T-shirt - ₹349 (50% off) ⭐4.3
     • Teamspirit Solid T-shirt - ₹449 (50% off) ⭐4.1
     • Adidas Training T-shirt - ₹1,199 (33% off) ⭐4.5
     
     🔍 Want more options?
     Browse all t-shirts on Google Shopping
```

## Technical Details

### URL Format

**General Shopping:**
```
https://www.google.com/search?udm=28&q=myntra+and+ajio
```

**Specific Product:**
```
https://www.google.com/search?udm=28&q={product}+myntra+ajio
```

Parameters:
- `udm=28` - Google Shopping mode
- `q` - Search query

### Code Implementation

**Location:** `web/app.py`

**Functions Modified:**
1. `get_chatbot_response()` - Added link to general shopping response
2. `format_shopping_results()` - Added link to search results

**Example Code:**
```python
# In format_shopping_results()
google_shopping_url = f"https://www.google.com/search?udm=28&q={quote(query)}+myntra+ajio"
message += f"🔍 **Want more options?**\n"
message += f"[Browse all {query}s on Google Shopping]({google_shopping_url})\n"
```

## User Experience

### Before
- Users saw 6 products (3 Myntra + 3 Ajio)
- Limited to our catalog
- No way to see more options

### After
- Users see 6 curated products
- **Plus** link to browse thousands more
- Direct access to Google Shopping
- Can see real product images
- Can compare across all sellers

## Testing

### Test Commands
```bash
# Open chatbot
http://127.0.0.1:5000

# Try these:
1. "I want to shop"
2. "Search for t-shirts"
3. "Find jeans"
4. "Show me shoes"
```

### Expected Results
- ✅ General query shows main Google Shopping link
- ✅ Specific search shows product-specific link
- ✅ Links open in new tab
- ✅ Google Shopping displays Myntra & Ajio products

## Future Enhancements

### Possible Improvements
1. **Deep Links** - Link directly to Myntra/Ajio product pages
2. **Price Tracking** - Show if prices have dropped
3. **Availability** - Show which sizes are in stock
4. **Reviews** - Display customer reviews
5. **Similar Items** - Show related products

### API Integration
For even better results, consider:
- Myntra Affiliate API
- Ajio Partner Program
- Google Shopping API
- Real-time price updates

## Notes

⚠️ **Important:**
- Google Shopping links are external
- Prices may vary from our catalog
- Product availability depends on Myntra/Ajio
- Links open in user's browser

✅ **Advantages:**
- No API keys needed
- Always up-to-date
- Shows real product images
- Free to use

## Support

### If Links Don't Work
1. Check internet connection
2. Verify Google Shopping is accessible
3. Try different search terms
4. Clear browser cache

### If Products Don't Show
1. Myntra/Ajio may be out of stock
2. Try broader search terms
3. Check spelling
4. Try alternative keywords

---

**Status:** ✅ Fully Integrated  
**Version:** 1.0  
**Last Updated:** November 25, 2025  
**Tested:** ✅ Working
