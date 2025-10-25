# 🔧 AR Try-On Troubleshooting - Clothing Not Showing

## ✅ Quick Fixes (Try These First):

### Fix 1: Hard Refresh Browser
```
Press: Ctrl + Shift + R
```
This clears cache and reloads the updated AR code.

### Fix 2: Open Browser Console
```
Press: F12 (or Ctrl + Shift + I)
Click: "Console" tab
```
Look for error messages or log output.

### Fix 3: Check What's Happening

When you select a cloth, the console should show:
```
✓ Loaded cloth: test_shirt_blue_solid.jpg (600x800)
Drawing cloth at (185, 95), size: 450x380
Using cached cloth: test_shirt_blue_solid.jpg
Drawing image: 600x800 to canvas 450x380 at (185, 95)
✓ Image drawn successfully
```

If you don't see these messages, there's a loading issue.

---

## 🔍 Diagnostic Steps:

### Step 1: Verify Camera is Working
1. Click "▶️ Start Camera"
2. Should see: "Camera Active" (green indicator)
3. Your video feed should appear

**If not working**: Check camera permissions in browser

### Step 2: Verify Keypoints Detected
1. Enable "Show Body Keypoints" checkbox
2. Should see green skeleton on your body
3. Should see labels: L.Shoulder, R.Shoulder, L.Hip, R.Hip

**If not working**: 
- Stand farther from camera
- Ensure full upper body visible
- Better lighting

### Step 3: Select Clothing
1. Scroll down in clothing selector
2. Click ANY clothing item
3. Item should highlight with blue border
4. Status should show: "Trying: [filename]"

**Check console for**:
```
✓ Loaded cloth: [filename]
```

### Step 4: Check Yellow Box
1. With keypoints enabled
2. Should see YELLOW box on screen
3. This shows where cloth WILL be placed
4. Should have text: "Cloth: [size]" and "Pos: [coordinates]"

**If no yellow box**: Keypoints not detected properly

### Step 5: Verify Clothing Renders
**Look for**:
- Clothing image overlaid on video
- Semi-transparent (60% opacity by default)
- Positioned at chest/shoulder area

---

## 🐛 Common Problems & Solutions:

### Problem 1: "No cloth selected"
**Console shows**: `No cloth selected`

**Solution**:
- Click a clothing item in the selector
- Make sure it highlights
- Check status indicator updates

### Problem 2: "Missing landmarks" or "Low visibility landmarks"  
**Console shows**: `Missing landmarks` or `Low visibility landmarks`

**Solution**:
- Stand 4-6 feet from camera
- Face camera directly
- Ensure shoulders and hips visible
- Better lighting
- Remove obstructions

### Problem 3: Image Load Error
**Console shows**: `✗ Failed to load: [filename]`

**Solution**:
- Check Flask server is running
- Verify file exists in `VITON-HD/datasets/test/cloth/`
- Check file permissions
- Try different clothing item

### Problem 4: Clothing Draws Off-Screen
**Yellow box visible but no clothing**

**Solution**:
- Adjust "Vertical Position" slider
- Try negative values: -20, -30, -40
- Click "🎽 Men's Shirt Preset" button
- Check console for position values

### Problem 5: Clothing Too Small or Large
**Clothing renders but wrong size**

**Solution**:
- Adjust "Scale" slider
- Try 90-120% range
- Check "Opacity" is not 0%
- Increase opacity to 70-80%

---

## 🎯 Expected Console Output (Normal Operation):

```javascript
// When selecting clothing:
✓ Loaded cloth: test_shirt_blue_solid.jpg (600x800)

// Every frame (when camera running):
Drawing cloth at (185, 95), size: 450x380
Using cached cloth: test_shirt_blue_solid.jpg
Drawing image: 600x800 to canvas 450x380 at (185, 95)
✓ Image drawn successfully
```

---

## 🔧 Debug Checklist:

Use this checklist to diagnose the issue:

- [ ] Browser console open (F12)
- [ ] Camera started and video visible
- [ ] Green status indicator showing "Camera Active"
- [ ] Keypoints checkbox enabled
- [ ] Green skeleton visible on body
- [ ] Clothing item selected (blue border)
- [ ] Status shows "Trying: [filename]"
- [ ] Yellow box visible on screen
- [ ] Console shows "✓ Loaded cloth"
- [ ] Console shows "Drawing cloth at..."
- [ ] Console shows "✓ Image drawn successfully"

**If all checked ✓ but still no clothing**:
- Increase opacity slider to 100%
- Check yellow box position matches your body
- Try "🎽 Men's Shirt Preset" button

---

## 💡 Pro Tips:

### Best Settings for Testing:
```
Opacity: 70-80% (easier to see)
Scale: 100%
Vertical: -30 (higher up)
Horizontal: 0 (centered)
Show Keypoints: ON (for debugging)
```

### Best Body Position:
```
Distance: 4-6 feet from camera
Pose: Face camera, arms slightly out
Lighting: Bright, even light
Background: Plain, uncluttered
```

### Test with Known Good Files:
```
test_shirt_blue_solid.jpg (generated file)
00006_00.jpg + any cloth (has good keypoints)
00891_00.jpg + any cloth (has good keypoints)
```

---

## 🚀 Quick Reset:

If everything is broken:

```bash
1. Stop camera (⏸️ Stop Camera button)
2. Close browser tab
3. Hard refresh: Ctrl + Shift + R
4. Start camera again
5. Select clothing
6. Click "🎽 Men's Shirt Preset"
```

---

## 📊 What Console Should NOT Show:

**Bad signs**:
```
❌ Failed to load: [filename]
❌ Error drawing image: [error]
❌ Image not loaded or invalid
❌ No cloth selected (continuously)
❌ Missing landmarks (continuously)
```

**If you see these**:
- Check file paths
- Verify Flask server running
- Check camera/pose detection
- Try different browser

---

## 🔍 Advanced Debugging:

### Check Image URL:
In console, type:
```javascript
console.log('/preview/cloth/test_shirt_blue_solid.jpg')
```
Then visit: http://127.0.0.1:5000/preview/cloth/test_shirt_blue_solid.jpg

**Should show**: The clothing image
**If not**: Flask routing or file path issue

### Check Canvas:
```javascript
console.log(canvas.width, canvas.height)
console.log(ctx)
```
Should show canvas dimensions and context object.

### Force Image Load:
```javascript
selectCloth('test_shirt_blue_solid.jpg', document.querySelector('.cloth-item'))
```
Should trigger image loading.

---

## ✅ Success Indicators:

**You'll know it's working when**:
1. ✓ Console shows no errors
2. ✓ Yellow box appears on screen
3. ✓ Clothing image visible on your body
4. ✓ Clothing moves with your body
5. ✓ Can adjust opacity/scale and see changes

---

## 📞 Still Not Working?

**Collect this info**:
1. Browser console output (copy all text)
2. Yellow box position (from yellow text)
3. Which clothing file you selected
4. Screenshot of the issue

**Then check**:
- Flask server terminal for errors
- Browser console for red error messages
- File permissions on clothing images
- Try completely different browser (Chrome vs Edge)

---

## 🎯 Most Common Solution:

**90% of the time, this fixes it**:
```
1. Hard refresh: Ctrl + Shift + R
2. Click "🎽 Men's Shirt Preset"
3. Select test_shirt_blue_solid.jpg
4. Increase Opacity to 80%
```

**If still not working**: Check console output and follow diagnostic steps above!
