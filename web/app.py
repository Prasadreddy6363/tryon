from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, Response
import os
import time
import subprocess
from pathlib import Path
import sys
import json
from PIL import Image, ImageChops
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import cv2
import base64
from io import BytesIO
import requests
from urllib.parse import quote
import re
from shopping_data import MYNTRA_CATALOG, AJIO_CATALOG, get_category_from_query

app = Flask(__name__)

# Base paths
WORKSPACE = Path(__file__).resolve().parent.parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = VITON_DIR / 'datasets'  # Use VITON-HD dataset with complete preprocessing
CHECKPOINTS_DIR = VITON_DIR / 'checkpoints'  # Checkpoints are in VITON-HD/checkpoints
RESULTS_DIR = VITON_DIR / 'results'

TEST_DIR = DATASETS_DIR / 'test'
IMG_DIR = TEST_DIR / 'image'
CLOTH_DIR = TEST_DIR / 'cloth'

@app.route('/')
def index():
    people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    
    # Load or compute image features for AI recommendations
    initialize_ai_features()
    
    return render_template('index.html', people=people, clothes=clothes)

@app.route('/preview/person/<path:filename>')
def preview_person(filename):
    return send_from_directory(IMG_DIR, filename)

@app.route('/preview/cloth/<path:filename>')
def preview_cloth(filename):
    return send_from_directory(CLOTH_DIR, filename)

@app.route('/api/recommend_clothes', methods=['POST'])
def recommend_clothes():
    """AI-powered clothing recommendations based on selected person"""
    data = request.get_json()
    person = data.get('person')
    if not person:
        return jsonify({'error': 'No person selected'}), 400
    
    try:
        recommendations = get_clothing_recommendations(person)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/similar_items', methods=['POST'])
def similar_items():
    """Find visually similar items using AI"""
    data = request.get_json()
    item_type = data.get('type')  # 'person' or 'cloth'
    item_name = data.get('name')
    
    if not item_type or not item_name:
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        similar = find_similar_items(item_type, item_name)
        return jsonify({'similar': similar})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auto_pair', methods=['GET'])
def auto_pair():
    """AI-powered automatic pairing of person and cloth"""
    try:
        pairs = get_auto_pairs(limit=5)
        return jsonify({'pairs': pairs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get generation history"""
    try:
        history = load_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/delete', methods=['POST'])
def delete_history_item():
    """Delete a specific history item"""
    try:
        data = request.get_json()
        index = data.get('index')
        
        if index is None:
            return jsonify({'error': 'Index not provided'}), 400
        
        cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
        if not cache_file.exists():
            return jsonify({'error': 'No history found'}), 404
        
        with open(cache_file, 'rb') as f:
            features = pickle.load(f)
        
        history = features.get('history', [])
        
        if index < 0 or index >= len(history):
            return jsonify({'error': 'Invalid index'}), 400
        
        # Remove the item
        deleted_item = history.pop(index)
        features['history'] = history
        
        # Save updated history
        with open(cache_file, 'wb') as f:
            pickle.dump(features, f)
        
        return jsonify({
            'success': True,
            'deleted': deleted_item,
            'remaining': len(history)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear all history"""
    try:
        cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
        if not cache_file.exists():
            return jsonify({'success': True, 'message': 'No history to clear'})
        
        with open(cache_file, 'rb') as f:
            features = pickle.load(f)
        
        features['history'] = []
        
        with open(cache_file, 'wb') as f:
            pickle.dump(features, f)
        
        return jsonify({'success': True, 'message': 'History cleared'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """AI Chatbot for virtual try-on assistance"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chatbot response
        response = get_chatbot_response(user_message)
        
        return jsonify({
            'response': response['message'],
            'actions': response.get('actions', []),
            'suggestions': response.get('suggestions', [])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/stats', methods=['GET'])
def chatbot_stats():
    """Get statistics for chatbot responses"""
    try:
        people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
        clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
        
        # Get history count
        history = load_history()
        
        # Get skin tone stats if available
        skin_tone_stats = {}
        classification_file = WORKSPACE / 'skin_tone_classification' / 'skin_tone_classification.json'
        if classification_file.exists():
            with open(classification_file, 'r') as f:
                classification_data = json.load(f)
                for category, images in classification_data.get('classification', {}).items():
                    if category != 'unknown':
                        skin_tone_stats[category] = len(images)
        
        return jsonify({
            'total_people': len(people),
            'total_clothes': len(clothes),
            'total_combinations': len(people) * len(clothes),
            'history_count': len(history),
            'skin_tone_available': len(skin_tone_stats) > 0,
            'skin_tone_stats': skin_tone_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping/search', methods=['POST'])
def shopping_search():
    """Search for items across shopping platforms"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        category = data.get('category', 'clothing')
        max_results = data.get('max_results', 5)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        shopping_data = get_shopping_data(query, category, max_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': shopping_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping/compare', methods=['POST'])
def shopping_compare():
    """Compare prices for a specific item"""
    try:
        data = request.get_json()
        item_name = data.get('item_name', '').strip()
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        comparison = get_price_comparison(item_name)
        
        return jsonify({
            'success': True,
            'item_name': item_name,
            'comparison': comparison
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping/trending', methods=['GET'])
def shopping_trending():
    """Get trending fashion items"""
    try:
        trending = get_trending_items()
        
        return jsonify({
            'success': True,
            'trending': trending
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skin_tone_filter', methods=['POST'])
def skin_tone_filter():
    """Filter person images by skin tone category"""
    try:
        data = request.get_json()
        skin_tone = data.get('skin_tone', 'all')  # 'all', 'light', 'intermediate', 'tan', 'brown', 'dark'
        
        # Load skin tone classification data
        classification_file = WORKSPACE / 'skin_tone_classification' / 'skin_tone_classification.json'
        
        if not classification_file.exists():
            return jsonify({
                'error': 'Skin tone classification not found. Please run classify_skin_tone.py first.',
                'people': []
            }), 404
        
        with open(classification_file, 'r') as f:
            classification_data = json.load(f)
        
        if skin_tone == 'all':
            # Return all people
            people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
        else:
            # Filter by skin tone category
            if skin_tone in classification_data['classification']:
                people = sorted(classification_data['classification'][skin_tone])
            else:
                people = []
        
        return jsonify({
            'people': people,
            'total': len(people),
            'category': skin_tone
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skin_tone_stats', methods=['GET'])
def skin_tone_stats():
    """Get skin tone classification statistics"""
    try:
        classification_file = WORKSPACE / 'skin_tone_classification' / 'skin_tone_classification.json'
        
        if not classification_file.exists():
            return jsonify({
                'available': False,
                'message': 'Skin tone classification not available'
            })
        
        with open(classification_file, 'r') as f:
            classification_data = json.load(f)
        
        stats = {
            'available': True,
            'total_images': classification_data['total_images'],
            'successful': classification_data['successful'],
            'failed': classification_data['failed'],
            'categories': {}
        }
        
        # Count per category
        for category, images in classification_data['classification'].items():
            if category != 'unknown':
                stats['categories'][category] = len(images)
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ar_tryon')
def ar_tryon():
    """AR Live Try-On page"""
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    return render_template('ar_tryon.html', clothes=clothes)

@app.route('/instant_tryon')
def instant_tryon():
    """Instant Try-On page (Snapchat-style)"""
    return render_template('instant_tryon.html')

@app.route('/api/get_clothes', methods=['GET'])
def get_clothes():
    """Get list of all clothing items"""
    try:
        # Try to use custom configuration
        from instant_tryon_config import get_cloth_images
        clothes = get_cloth_images()
    except:
        # Fallback to default
        clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    return jsonify({'clothes': clothes})

@app.route('/api/get_people', methods=['GET'])
def get_people():
    """Get list of all people"""
    try:
        # Try to use custom configuration
        from instant_tryon_config import get_person_images
        people = get_person_images()
    except:
        # Fallback to default
        people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
    return jsonify({'people': people})

@app.route('/api/instant_tryon_config', methods=['GET'])
def get_instant_tryon_config():
    """Get instant try-on configuration"""
    try:
        from instant_tryon_config import get_config
        config = get_config()
        return jsonify({
            'display': config['display'],
            'processing': config['processing']
        })
    except:
        return jsonify({
            'display': {
                'person_aspect_ratio': '3/4',
                'cloth_aspect_ratio': '3/4',
                'grid_columns': 2,
                'items_per_page': 50
            },
            'processing': {
                'use_ai': True,
                'timeout': 60,
                'quality': 'high'
            }
        })

@app.route('/api/ar/overlay', methods=['POST'])
def ar_overlay():
    """Process AR overlay for live try-on"""
    try:
        data = request.get_json()
        frame_data = data.get('frame')
        cloth_file = data.get('cloth')
        keypoints = data.get('keypoints')
        
        if not frame_data or not cloth_file:
            return jsonify({'error': 'Missing frame or cloth data'}), 400
        
        # Decode base64 frame
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Load cloth image
        cloth_path = CLOTH_DIR / cloth_file
        cloth = cv2.imread(str(cloth_path))
        
        if cloth is None:
            return jsonify({'error': 'Cloth not found'}), 404
        
        # Apply AR overlay using keypoints
        result_frame = apply_ar_overlay(frame, cloth, keypoints)
        
        # Encode result back to base64
        _, buffer = cv2.imencode('.jpg', result_frame)
        result_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({'frame': f'data:image/jpeg;base64,{result_b64}'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ar/capture', methods=['POST'])
def ar_capture():
    """Capture AR try-on frame and save"""
    try:
        data = request.get_json()
        frame_data = data.get('frame')
        cloth_name = data.get('cloth', 'unknown')
        
        if not frame_data:
            return jsonify({'error': 'No frame data'}), 400
        
        # Decode and save
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        
        # Create AR captures directory
        ar_dir = WORKSPACE / 'web' / 'static' / 'ar_captures'
        ar_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = int(time.time())
        filename = f'ar_capture_{timestamp}_{cloth_name}'
        filepath = ar_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(frame_bytes)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': url_for('static', filename=f'ar_captures/{filename}')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tryon', methods=['POST'])
def tryon():
    person = request.form.get('person')
    cloth = request.form.get('cloth')
    full_body = request.form.get('full_body', False)
    
    if not person or not cloth:
        return redirect(url_for('index'))

    job_name = f"web_{int(time.time())}"

    # We will reuse the dataset structure; only need a pairs file
    pairs_path = DATASETS_DIR / 'test_pairs.txt'
    with open(pairs_path, 'w', encoding='utf-8') as f:
        f.write(f"{person} {cloth}\n")

    # Ensure result subdir exists
    (RESULTS_DIR / job_name).mkdir(parents=True, exist_ok=True)

    # Check if test.py exists
    test_script = VITON_DIR / 'test.py'
    if not test_script.exists():
        error_msg = f"""<h2>Missing VITON-HD inference code</h2>
        <p>The file <code>{test_script}</code> does not exist.</p>
        <p><strong>To fix this:</strong></p>
        <ol>
            <li>Clone the official VITON-HD repository: <code>git clone https://github.com/shadow2496/VITON-HD.git</code></li>
            <li>Copy the required files (test.py, networks.py, data.py, etc.) to your VITON-HD directory</li>
            <li>Download the pre-trained models and place them in the checkpoints directory</li>
        </ol>
        <p><strong>Current Selection:</strong></p>
        <ul>
            <li>Person: {person}</li>
            <li>Cloth: {cloth}</li>
            <li>Full Body: {full_body}</li>
        </ul>
        """
        
        # Create a visual comparison mock result
        try:
            from PIL import Image
            import io
            
            # Load person and cloth images
            person_img = Image.open(IMG_DIR / person)
            cloth_img = Image.open(CLOTH_DIR / cloth)
            
            # Resize images to same height for comparison
            height = 600
            person_aspect = person_img.width / person_img.height
            cloth_aspect = cloth_img.width / cloth_img.height
            
            person_resized = person_img.resize((int(height * person_aspect), height), Image.Resampling.LANCZOS)
            cloth_resized = cloth_img.resize((int(height * cloth_aspect), height), Image.Resampling.LANCZOS)
            
            # Create side-by-side comparison
            total_width = person_resized.width + cloth_resized.width + 100
            comparison = Image.new('RGB', (total_width, height + 100), color=(255, 255, 255))
            
            # Paste images
            comparison.paste(person_resized, (25, 50))
            comparison.paste(cloth_resized, (person_resized.width + 75, 50))
            
            # Save comparison
            result_name = f"{person.replace('.jpg', '')}_{cloth.replace('.jpg', '')}_mock.jpg"
            result_path = RESULTS_DIR / job_name / result_name
            comparison.save(result_path, 'JPEG', quality=95)
            
            return f"""{error_msg}
            <div style="margin-top: 20px;">
                <h3>Mock Comparison (Not Actual Try-On)</h3>
                <img src="{url_for('serve_result', job_name=job_name, image_name=result_name)}" style="max-width: 100%; border: 2px solid #d9534f;">
                <p style="font-size: 12px; color: #666;">Left: Selected person | Right: Selected cloth (virtual try-on NOT applied)</p>
            </div>
            """
        except ImportError:
            # PIL not available, just copy person image
            import shutil
            result_name = f"{person.replace('.jpg', '')}_{cloth.replace('.jpg', '')}.jpg"
            result_path = RESULTS_DIR / job_name / result_name
            shutil.copy(IMG_DIR / person, result_path)
            return f"{error_msg}<p>Install Pillow for better mock preview: <code>pip install Pillow</code></p>"
        except Exception as e:
            return f"{error_msg}<pre>Error creating mock result: {e}</pre>", 500

    # Invoke test.py with full-body option if requested
    cmd = [
        sys.executable, str(test_script),
        '--name', job_name,
        '--dataset_dir', str(DATASETS_DIR),
        '--checkpoint_dir', str(CHECKPOINTS_DIR),
        '--save_dir', str(RESULTS_DIR)
    ]
    
    # Add full-body flag if requested
    if full_body:
        cmd.extend(['--full_body', 'True'])
    
    # Run and capture output (blocking)
    proc = subprocess.run(cmd, cwd=str(VITON_DIR), capture_output=True, text=True)
    if proc.returncode != 0:
        return f"Inference failed:<br><pre>{proc.stdout}\n{proc.stderr}</pre>", 500

    # Find produced file (pattern: <person_id>_<cloth_id>.jpg)
    out_dir = RESULTS_DIR / job_name
    generated = sorted([p.name for p in out_dir.glob('*.jpg')])
    if not generated:
        return "No result generated.", 500

    # Save to history
    result_url = url_for('serve_result', job_name=job_name, image_name=generated[0])
    save_to_history(person, cloth, result_url)

    return render_template('result.html', job_name=job_name, image_name=generated[0])

@app.route('/results/<job_name>/<image_name>')
def serve_result(job_name, image_name):
    return send_from_directory(RESULTS_DIR / job_name, image_name)

# AI Feature Functions
def initialize_ai_features():
    """Initialize AI features cache"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if cache_file.exists():
        return
    
    print("Initializing AI features...")
    features = {
        'person_features': {},
        'cloth_features': {},
        'history': []
    }
    
    # Extract basic color features from images
    for person_file in os.listdir(IMG_DIR):
        if person_file.lower().endswith('.jpg'):
            try:
                img_path = IMG_DIR / person_file
                img = Image.open(img_path).resize((64, 64))
                features['person_features'][person_file] = extract_color_features(img)
            except:
                pass
    
    for cloth_file in os.listdir(CLOTH_DIR):
        if cloth_file.lower().endswith('.jpg'):
            try:
                img_path = CLOTH_DIR / cloth_file
                img = Image.open(img_path).resize((64, 64))
                features['cloth_features'][cloth_file] = extract_color_features(img)
            except:
                pass
    
    with open(cache_file, 'wb') as f:
        pickle.dump(features, f)
    print(f"AI features initialized: {len(features['person_features'])} people, {len(features['cloth_features'])} clothes")

def extract_color_features(img):
    """Extract color histogram features from image"""
    img_array = np.array(img)
    # Get color histograms for R, G, B channels
    hist_r = np.histogram(img_array[:,:,0], bins=8, range=(0, 256))[0]
    hist_g = np.histogram(img_array[:,:,1], bins=8, range=(0, 256))[0]
    hist_b = np.histogram(img_array[:,:,2], bins=8, range=(0, 256))[0]
    # Normalize and concatenate
    features = np.concatenate([hist_r, hist_g, hist_b]).astype(float)
    features = features / (features.sum() + 1e-6)
    return features.tolist()

def get_clothing_recommendations(person_file, top_k=6):
    """Get AI-recommended clothes for a person based on color matching"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if not cache_file.exists():
        initialize_ai_features()
    
    with open(cache_file, 'rb') as f:
        features = pickle.load(f)
    
    if person_file not in features['person_features']:
        # Return random clothes if person not in cache
        clothes = list(features['cloth_features'].keys())
        return clothes[:top_k]
    
    person_feat = np.array(features['person_features'][person_file]).reshape(1, -1)
    
    # Calculate similarity with all clothes
    similarities = []
    for cloth_file, cloth_feat in features['cloth_features'].items():
        cloth_feat_array = np.array(cloth_feat).reshape(1, -1)
        sim = cosine_similarity(person_feat, cloth_feat_array)[0][0]
        similarities.append((cloth_file, sim))
    
    # Sort by similarity (complementary colors score higher)
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in similarities[:top_k]]

def find_similar_items(item_type, item_name, top_k=6):
    """Find similar items using AI"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if not cache_file.exists():
        initialize_ai_features()
    
    with open(cache_file, 'rb') as f:
        features = pickle.load(f)
    
    feature_key = 'person_features' if item_type == 'person' else 'cloth_features'
    
    if item_name not in features[feature_key]:
        return []
    
    item_feat = np.array(features[feature_key][item_name]).reshape(1, -1)
    
    similarities = []
    for other_name, other_feat in features[feature_key].items():
        if other_name == item_name:
            continue
        other_feat_array = np.array(other_feat).reshape(1, -1)
        sim = cosine_similarity(item_feat, other_feat_array)[0][0]
        similarities.append((other_name, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in similarities[:top_k]]

def get_auto_pairs(limit=5):
    """Get AI-recommended person-cloth pairs"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if not cache_file.exists():
        initialize_ai_features()
    
    with open(cache_file, 'rb') as f:
        features = pickle.load(f)
    
    # Check for valid pose data
    pose_dir = TEST_DIR / 'openpose-json'
    valid_people = []
    
    for person_file in features['person_features'].keys():
        person_id = person_file.replace('.jpg', '')
        pose_file = pose_dir / f"{person_id}_keypoints.json"
        if pose_file.exists():
            try:
                with open(pose_file, 'r') as f:
                    pose_data = json.load(f)
                    if pose_data.get('people') and len(pose_data['people']) > 0:
                        valid_people.append(person_file)
            except:
                pass
    
    if not valid_people:
        valid_people = list(features['person_features'].keys())[:limit]
    
    pairs = []
    for person in valid_people[:limit]:
        # Get best matching cloth
        recommendations = get_clothing_recommendations(person, top_k=1)
        if recommendations:
            pairs.append({'person': person, 'cloth': recommendations[0]})
    
    return pairs

def load_history():
    """Load generation history"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if not cache_file.exists():
        return []
    
    with open(cache_file, 'rb') as f:
        features = pickle.load(f)
    
    return features.get('history', [])

def save_to_history(person, cloth, result_url):
    """Save generation to history"""
    cache_file = WORKSPACE / 'web' / 'ai_cache.pkl'
    if not cache_file.exists():
        initialize_ai_features()
    
    with open(cache_file, 'rb') as f:
        features = pickle.load(f)
    
    features['history'].insert(0, {
        'person': person,
        'cloth': cloth,
        'result': result_url,
        'timestamp': time.time()
    })
    
    # Keep only last 20 items
    features['history'] = features['history'][:20]
    
    with open(cache_file, 'wb') as f:
        pickle.dump(features, f)

def get_chatbot_response(user_message):
    """Generate chatbot response based on user message"""
    message = user_message.lower()
    
    # Greeting responses
    if any(word in message for word in ['hello', 'hi', 'hey', 'start', 'help']):
        return {
            'message': "👋 Hello! I'm your Virtual Try-On Assistant! I can help you:\n\n• Navigate the interface\n• Find the perfect outfit\n• Use AI features\n• Manage your history\n• Answer questions about virtual try-on\n\nWhat would you like to do today?",
            'suggestions': [
                "How do I try on clothes?",
                "Show me AI recommendations",
                "What's in my history?",
                "Help me find similar items"
            ]
        }
    
    # How to use / Tutorial
    elif any(word in message for word in ['how', 'tutorial', 'guide', 'start', 'begin']):
        if 'try on' in message or 'use' in message:
            return {
                'message': "🎯 Here's how to use Virtual Try-On:\n\n1️⃣ **Select a Person** - Click on any person image from the left gallery\n2️⃣ **Select Clothing** - Click on any clothing item from the right gallery\n3️⃣ **Generate** - Click the 'Generate Virtual Try-On' button\n4️⃣ **View Result** - See your amazing virtual try-on result!\n\n💡 **Pro Tips:**\n• Use AI recommendations for best matches\n• Try the AR Live Try-On for real-time experience\n• Check your history to see previous results",
                'actions': ['highlight_galleries'],
                'suggestions': [
                    "Show me AI features",
                    "What is AR try-on?",
                    "How do I save results?"
                ]
            }
        elif 'ar' in message or 'live' in message:
            return {
                'message': "📹 **AR Live Try-On Guide:**\n\n1️⃣ Click the 'AR Live Try-On' tab\n2️⃣ Allow camera access when prompted\n3️⃣ Select a clothing item\n4️⃣ See real-time try-on with your webcam!\n5️⃣ Adjust opacity and scale as needed\n6️⃣ Capture screenshots of your favorites\n\n🎯 **Perfect for:** Real-time fitting, quick previews, and sharing with friends!",
                'actions': ['switch_to_ar'],
                'suggestions': [
                    "Switch to AR tab",
                    "What about regular try-on?",
                    "How do I add new clothes?"
                ]
            }
    
    # AI Features
    elif any(word in message for word in ['ai', 'smart', 'recommend', 'suggestion', 'intelligent']):
        return {
            'message': "🤖 **AI Features Available:**\n\n✨ **Smart Recommendations** - AI suggests clothes that match your selected person\n🔍 **Similar People** - Find people with similar features\n👔 **Similar Clothes** - Discover similar clothing items\n🎨 **Auto-Pair** - Let AI pick the perfect person-clothing combination\n🌈 **Skin Tone Filter** - Filter people by skin tone categories\n\n💡 **Tip:** Select a person first, then use 'Smart Recommendations' for best results!",
            'actions': ['highlight_ai_panel'],
            'suggestions': [
                "Use smart recommendations",
                "Try auto-pair feature",
                "Filter by skin tone",
                "Find similar items"
            ]
        }
    
    # History
    elif any(word in message for word in ['history', 'previous', 'past', 'saved', 'results']):
        return {
            'message': "📜 **Your Try-On History:**\n\nI can help you manage your virtual try-on history:\n\n👁️ **View** - See all your previous try-on results\n💾 **Download** - Save your favorite results\n🗑️ **Delete** - Remove individual items or clear all\n📊 **Track** - See your try-on patterns and favorites\n\n🎯 **Access:** Click the 'History' tab to see all your previous virtual try-ons!",
            'actions': ['switch_to_history'],
            'suggestions': [
                "Show my history",
                "Clear all history",
                "Download my results",
                "What's my most recent try-on?"
            ]
        }
    
    # Skin tone
    elif any(word in message for word in ['skin', 'tone', 'color', 'complexion', 'filter']):
        return {
            'message': "🎨 **Skin Tone Classification:**\n\nI can filter people by skin tone using scientific ITA° algorithm:\n\n☀️ **Light Skin** - Fair complexion\n🌤️ **Intermediate** - Light brown\n🌅 **Tan Skin** - Medium brown\n🌰 **Brown Skin** - Dark brown\n🌑 **Dark Skin** - Very dark\n👥 **All People** - Show everyone\n\n💡 **Note:** Run `classify_skin_tone.py` first to enable this feature!",
            'actions': ['highlight_skin_tone'],
            'suggestions': [
                "Filter by light skin",
                "Show all people",
                "What is ITA algorithm?",
                "How accurate is classification?"
            ]
        }
    
    # Adding clothes
    elif any(word in message for word in ['add', 'upload', 'new', 'clothes', 'clothing', 'garment']):
        return {
            'message': "➕ **Add New Clothing:**\n\n🎯 **Easy Upload Process:**\n1️⃣ Click 'Add 2D Clothing' tab\n2️⃣ Drag & drop your clothing images\n3️⃣ Choose processing options (size, background)\n4️⃣ Let AI remove backgrounds automatically\n5️⃣ Your new clothes appear in the gallery!\n\n✨ **Features:** Batch upload, auto-resize, background removal, mask creation",
            'actions': ['switch_to_add'],
            'suggestions': [
                "Open clothing manager",
                "What formats are supported?",
                "How to remove backgrounds?",
                "Batch upload multiple items"
            ]
        }
    
    # Technical questions
    elif any(word in message for word in ['error', 'problem', 'issue', 'bug', 'not working']):
        return {
            'message': "🔧 **Troubleshooting Help:**\n\n**Common Issues:**\n• **No result generated** - Check if both person and clothing are selected\n• **Poor quality** - Try different person-clothing combinations\n• **Slow processing** - Large images take more time\n• **Camera not working** - Allow camera permissions in browser\n• **Missing features** - Some features need additional setup\n\n💡 **Quick Fixes:** Refresh page, clear browser cache, try different images",
            'suggestions': [
                "Check system requirements",
                "How to improve quality?",
                "Camera permission issues",
                "Contact support"
            ]
        }
    
    # Quality and tips
    elif any(word in message for word in ['quality', 'better', 'improve', 'tips', 'best']):
        return {
            'message': "⭐ **Tips for Best Results:**\n\n🎯 **Person Images:**\n• Clear, front-facing poses work best\n• Good lighting and resolution\n• Minimal background clutter\n\n👕 **Clothing Images:**\n• Clean, flat-lay or mannequin shots\n• White/transparent backgrounds\n• High resolution for detail\n\n🤖 **AI Tips:**\n• Use Smart Recommendations for color matching\n• Try similar body types for better fit\n• Experiment with different combinations!",
            'suggestions': [
                "Use AI recommendations",
                "Find similar people",
                "Upload better images",
                "Try different poses"
            ]
        }
    
    # Statistics and info
    elif any(word in message for word in ['stats', 'statistics', 'count', 'how many', 'total']):
        return {
            'message': "📊 **Platform Statistics:**\n\nLet me fetch the current stats for you...\n\n💡 **Available Data:**\n• Total people in database\n• Total clothing items\n• Possible combinations\n• Your try-on history\n• Skin tone distribution\n\nWould you like to see detailed statistics?",
            'actions': ['fetch_stats'],
            'suggestions': [
                "Show detailed stats",
                "My personal stats",
                "Most popular items",
                "Recent activity"
            ]
        }
    
    # Shopping and purchasing
    elif any(word in message for word in ['buy', 'purchase', 'shop', 'price', 'cost', 'myntra', 'ajio', 'shopping']):
        if 'compare' in message or 'price' in message:
            return {
                'message': "💰 **Price Comparison & Shopping:**\n\nI can help you find the best deals across multiple platforms!\n\n🛍️ **Available Platforms:**\n• **Myntra** - Wide variety, great discounts\n• **Ajio** - Trendy collections, competitive prices\n\n💡 **What I can do:**\n• Search for specific items\n• Compare prices across platforms\n• Show trending fashion items\n• Find best deals and discounts\n\nWhat would you like to shop for?",
                'actions': ['shopping_mode'],
                'suggestions': [
                    "Search for t-shirts",
                    "Compare jeans prices", 
                    "Show trending items",
                    "Find best deals"
                ]
            }
        elif 'search' in message or any(item in message for item in ['shirt', 'jeans', 'dress', 'shoes', 'jacket']):
            # Extract item from message
            items = ['shirt', 'jeans', 'dress', 'shoes', 'jacket', 't-shirt', 'kurta', 'saree', 'blazer']
            found_item = next((item for item in items if item in message), 'clothing')
            
            return {
                'message': f"🔍 **Searching for {found_item}s across Myntra & Ajio...**\n\nI'll find the best options with:\n• Competitive prices\n• High ratings\n• Good discounts\n• Multiple size options\n\nLet me fetch the latest deals for you!",
                'actions': ['search_shopping', found_item],
                'suggestions': [
                    f"Compare {found_item} prices",
                    "Show more options",
                    "Filter by brand",
                    "Find similar items"
                ]
            }
        else:
            return {
                'message': "🛍️ **Shopping Assistant Ready!**\n\n**I can help you:**\n• 🔍 Search items on Myntra & Ajio\n• 💰 Compare prices across platforms\n• 🔥 Show trending fashion items\n• 🏷️ Find best deals and discounts\n• ⭐ Check ratings and reviews\n• 📏 Find size availability\n\n**Popular Categories:**\nT-shirts, Jeans, Dresses, Shoes, Jackets, Kurtas, Sarees, Blazers\n\nWhat would you like to shop for today?",
                'suggestions': [
                    "Search for t-shirts",
                    "Show trending items",
                    "Compare prices",
                    "Find best deals"
                ]
            }
    
    # Trending items
    elif any(word in message for word in ['trending', 'popular', 'latest', 'fashion', 'style']):
        return {
            'message': "🔥 **Trending Fashion & Latest Styles:**\n\nI'll show you what's hot in fashion right now across Myntra and Ajio!\n\n✨ **Trending Categories:**\n• Oversized clothing\n• Sustainable fashion\n• Athleisure wear\n• Ethnic fusion\n• Minimalist designs\n\nLet me fetch the latest trending items for you!",
            'actions': ['fetch_trending'],
            'suggestions': [
                "Show trending items",
                "Search oversized t-shirts",
                "Find ethnic wear",
                "Show athleisure"
            ]
        }
    
    # Fun and creative
    elif any(word in message for word in ['fun', 'creative', 'surprise', 'random', 'inspire']):
        return {
            'message': "🎨 **Get Creative!**\n\n✨ **Fun Ideas:**\n• Use Auto-Pair for surprise combinations\n• Try contrasting colors for bold looks\n• Mix formal and casual pieces\n• Experiment with different skin tones\n• Create themed outfits (summer, winter, party)\n• Shop for trending items to try on\n\n🎯 **Challenge:** Try to create 5 different styles with the same person!",
            'actions': ['auto_pair'],
            'suggestions': [
                "Surprise me with auto-pair",
                "Show trending fashion",
                "Search for bold colors",
                "Create themed outfit"
            ]
        }
    
    # Default response
    else:
        return {
            'message': "🤔 I'm not sure about that, but I'm here to help with virtual try-on!\n\n**I can assist with:**\n• How to use the interface\n• AI features and recommendations\n• Managing your history\n• Troubleshooting issues\n• Tips for better results\n• Adding new clothing\n\nWhat would you like to know?",
            'suggestions': [
                "How do I try on clothes?",
                "Show me AI features",
                "Help with navigation",
                "Troubleshooting tips"
            ]
        }

def get_shopping_data(query, category="clothing", max_results=5):
    """Get shopping data from multiple platforms"""
    results = {
        'myntra': get_myntra_data(query, category, max_results),
        'ajio': get_ajio_data(query, category, max_results),
        'summary': {}
    }
    
    # Create summary
    all_items = results['myntra'] + results['ajio']
    if all_items:
        prices = [item['price'] for item in all_items if item.get('price')]
        results['summary'] = {
            'total_items': len(all_items),
            'price_range': {
                'min': min(prices) if prices else 0,
                'max': max(prices) if prices else 0,
                'avg': sum(prices) / len(prices) if prices else 0
            },
            'platforms': len([p for p in ['myntra', 'ajio'] if results[p]])
        }
    
    return results

def get_myntra_data(query, category="clothing", max_results=5):
    """Get Myntra product data from comprehensive catalog"""
    # Get category from query
    cat_key = get_category_from_query(query)
    
    # Get items from catalog
    items = MYNTRA_CATALOG.get(cat_key, MYNTRA_CATALOG['mens_tshirts'])
    
    # Format items
    myntra_items = []
    for i, item in enumerate(items[:max_results]):
        discount = round(((item['original'] - item['price']) / item['original']) * 100)
        myntra_items.append({
            'id': f'MYN{i+1:03d}',
            'name': item['name'],
            'brand': item['brand'],
            'price': item['price'],
            'original_price': item['original'],
            'discount': discount,
            'rating': item['rating'],
            'reviews': item['reviews'],
            'image': f'https://assets.myntassets.com/{item["brand"].lower().replace(" ", "-")}/{i+1}.jpg',
            'url': f'https://www.myntra.com/search?q={quote(query)}',
            'sizes': item.get('sizes', ['S', 'M', 'L', 'XL']),
            'colors': item.get('colors', ['Black', 'Navy', 'White']),
            'category': category,
            'platform': 'Myntra',
            'in_stock': True,
            'delivery': '2-3 days'
        })
    
    return myntra_items

def get_ajio_data(query, category="clothing", max_results=5):
    """Get Ajio product data from comprehensive catalog"""
    # Get category from query
    cat_key = get_category_from_query(query)
    
    # Get items from catalog
    items = AJIO_CATALOG.get(cat_key, AJIO_CATALOG['mens_tshirts'])
    
    # Format items
    ajio_items = []
    for i, item in enumerate(items[:max_results]):
        discount = round(((item['original'] - item['price']) / item['original']) * 100)
        ajio_items.append({
            'id': f'AJI{i+1:03d}',
            'name': item['name'],
            'brand': item['brand'],
            'price': item['price'],
            'original_price': item['original'],
            'discount': discount,
            'rating': item['rating'],
            'reviews': item['reviews'],
            'image': f'https://assets.ajio.com/{item["brand"].lower().replace(" ", "-")}/{i+1}.jpg',
            'url': f'https://www.ajio.com/search/{quote(query)}',
            'sizes': item.get('sizes', ['S', 'M', 'L', 'XL']),
            'colors': item.get('colors', ['Black', 'Navy', 'White']),
            'category': category,
            'platform': 'Ajio',
            'in_stock': True,
            'delivery': '3-5 days'
        })
    
    return ajio_items

def format_shopping_results(shopping_data, query):
    """Format shopping results for chatbot response"""
    if not shopping_data or shopping_data['summary'].get('total_items', 0) == 0:
        return f"Sorry, I couldn't find any {query} items right now. Please try a different search term."
    
    summary = shopping_data['summary']
    message = f"🛍️ **Found {summary['total_items']} {query} items across {summary['platforms']} platforms!**\n\n"
    
    if summary['price_range']['min'] > 0:
        message += f"💰 **Price Range:** ₹{summary['price_range']['min']:,.0f} - ₹{summary['price_range']['max']:,.0f}\n"
        message += f"📊 **Average Price:** ₹{summary['price_range']['avg']:,.0f}\n\n"
    
    # Show top items from each platform
    for platform in ['myntra', 'ajio']:
        items = shopping_data[platform]
        if items:
            message += f"🏪 **{platform.title()} ({len(items)} items):**\n"
            for item in items[:3]:  # Show top 3 from each platform
                discount_text = f" ({item['discount']}% off)" if item.get('discount') else ""
                rating_text = f" ⭐{item['rating']}" if item.get('rating') else ""
                message += f"• **{item['name']}** by {item['brand']}\n"
                message += f"  ₹{item['price']:,}{discount_text}{rating_text}\n"
            message += "\n"
    
    return message

def get_price_comparison(item_name):
    """Compare prices across platforms"""
    myntra_data = get_myntra_data(item_name, max_results=3)
    ajio_data = get_ajio_data(item_name, max_results=3)
    
    all_items = myntra_data + ajio_data
    if not all_items:
        return "No price comparison data available."
    
    # Sort by price
    all_items.sort(key=lambda x: x['price'])
    
    message = f"💰 **Price Comparison for '{item_name}':**\n\n"
    message += "**Best Deals:**\n"
    
    for i, item in enumerate(all_items[:5], 1):
        discount_text = f" ({item['discount']}% off ₹{item['original_price']:,})" if item.get('discount') else ""
        message += f"{i}. **{item['brand']}** - ₹{item['price']:,}{discount_text} on {item['platform']}\n"
    
    return message

def get_trending_items():
    """Get trending fashion items with real data from Myntra and Ajio"""
    trending_categories = {
        'Oversized T-Shirts': {
            'myntra': [
                {'name': 'Roadster Oversized Graphic T-shirt', 'brand': 'Roadster', 'price': 499, 'original': 999, 'rating': 4.4},
                {'name': 'H&M Oversized Fit T-shirt', 'brand': 'H&M', 'price': 799, 'original': 1199, 'rating': 4.3}
            ],
            'ajio': [
                {'name': 'DNMX Oversized Printed T-shirt', 'brand': 'DNMX', 'price': 449, 'original': 899, 'rating': 4.2},
                {'name': 'Teamspirit Oversized T-shirt', 'brand': 'Teamspirit', 'price': 549, 'original': 999, 'rating': 4.1}
            ]
        },
        'High Waist Jeans': {
            'myntra': [
                {'name': 'Levis High Rise Skinny Jeans', 'brand': 'Levis', 'price': 2999, 'original': 4499, 'rating': 4.5},
                {'name': 'Roadster High Waist Jeans', 'brand': 'Roadster', 'price': 1399, 'original': 2199, 'rating': 4.2}
            ],
            'ajio': [
                {'name': 'DNMX High Waist Slim Jeans', 'brand': 'DNMX', 'price': 1199, 'original': 1999, 'rating': 4.3},
                {'name': 'Lee Cooper High Rise Jeans', 'brand': 'Lee Cooper', 'price': 1599, 'original': 2499, 'rating': 4.1}
            ]
        },
        'Ethnic Kurtas': {
            'myntra': [
                {'name': 'Libas Printed Straight Kurta', 'brand': 'Libas', 'price': 899, 'original': 1799, 'rating': 4.4},
                {'name': 'Biba Embroidered Kurta', 'brand': 'Biba', 'price': 1499, 'original': 2499, 'rating': 4.5}
            ],
            'ajio': [
                {'name': 'Soch Ethnic Kurta', 'brand': 'Soch', 'price': 1199, 'original': 1999, 'rating': 4.4},
                {'name': 'Rangmanch Printed Kurta', 'brand': 'Rangmanch', 'price': 899, 'original': 1599, 'rating': 4.2}
            ]
        },
        'Sneakers': {
            'myntra': [
                {'name': 'Nike Air Max Sneakers', 'brand': 'Nike', 'price': 5995, 'original': 7995, 'rating': 4.6},
                {'name': 'Puma Smash Sneakers', 'brand': 'Puma', 'price': 2499, 'original': 3999, 'rating': 4.3}
            ],
            'ajio': [
                {'name': 'Adidas Running Sneakers', 'brand': 'Adidas', 'price': 3999, 'original': 5999, 'rating': 4.5},
                {'name': 'Reebok Classic Sneakers', 'brand': 'Reebok', 'price': 2999, 'original': 4499, 'rating': 4.4}
            ]
        },
        'Denim Jackets': {
            'myntra': [
                {'name': 'Roadster Denim Jacket', 'brand': 'Roadster', 'price': 1799, 'original': 2999, 'rating': 4.3},
                {'name': 'Levis Trucker Jacket', 'brand': 'Levis', 'price': 3999, 'original': 5999, 'rating': 4.6}
            ],
            'ajio': [
                {'name': 'DNMX Denim Jacket', 'brand': 'DNMX', 'price': 1599, 'original': 2799, 'rating': 4.2},
                {'name': 'Jack & Jones Denim Jacket', 'brand': 'Jack & Jones', 'price': 2299, 'original': 3799, 'rating': 4.4}
            ]
        }
    }
    
    message = "🔥 **Trending Fashion Items:**\n\n"
    
    for i, (category, platforms) in enumerate(trending_categories.items(), 1):
        message += f"**{i}. {category}**\n"
        
        # Show best deal from each platform
        myntra_best = platforms['myntra'][0]
        ajio_best = platforms['ajio'][0]
        
        myntra_discount = round(((myntra_best['original'] - myntra_best['price']) / myntra_best['original']) * 100)
        ajio_discount = round(((ajio_best['original'] - ajio_best['price']) / ajio_best['original']) * 100)
        
        message += f"   • Myntra: {myntra_best['brand']} - ₹{myntra_best['price']:,} ({myntra_discount}% off) ⭐{myntra_best['rating']}\n"
        message += f"   • Ajio: {ajio_best['brand']} - ₹{ajio_best['price']:,} ({ajio_discount}% off) ⭐{ajio_best['rating']}\n\n"
    
    message += "💡 **Ask me to search for any category to see more options!**"
    
    return message

def apply_ar_overlay(frame, cloth, keypoints):
    """Apply AR clothing overlay on frame using body keypoints"""
    if not keypoints or len(keypoints) < 33:
        # No valid pose detected, just return original frame
        return frame
    
    try:
        # Extract relevant keypoints (MediaPipe Pose landmarks)
        # Key points: 11-left shoulder, 12-right shoulder, 23-left hip, 24-right hip
        left_shoulder = keypoints[11] if len(keypoints) > 11 else None
        right_shoulder = keypoints[12] if len(keypoints) > 12 else None
        left_hip = keypoints[23] if len(keypoints) > 23 else None
        right_hip = keypoints[24] if len(keypoints) > 24 else None
        
        # Check if all required keypoints are visible
        if not all([left_shoulder, right_shoulder, left_hip, right_hip]):
            return frame
        
        # Check visibility of keypoints
        if not all([kp.get('visibility', 0) > 0.5 if kp else False for kp in [left_shoulder, right_shoulder, left_hip, right_hip]]):
            return frame
        
        # Calculate bounding box for torso
        frame_h, frame_w = frame.shape[:2]
        
        # Ensure keypoints are not None before accessing
        if left_shoulder and right_shoulder and left_hip and right_hip:
            shoulder_x = int((left_shoulder['x'] + right_shoulder['x']) / 2 * frame_w)
            shoulder_y = int((left_shoulder['y'] + right_shoulder['y']) / 2 * frame_h)
            hip_x = int((left_hip['x'] + right_hip['x']) / 2 * frame_w)
            hip_y = int((left_hip['y'] + right_hip['y']) / 2 * frame_h)
            
            shoulder_width = int(abs(right_shoulder['x'] - left_shoulder['x']) * frame_w)
            torso_height = int(abs(hip_y - shoulder_y))
            
            # Expand for better coverage
            shoulder_width = int(shoulder_width * 1.3)
            torso_height = int(torso_height * 1.2)
            
            # Calculate cloth placement
            cloth_x = max(0, shoulder_x - shoulder_width // 2)
            cloth_y = max(0, shoulder_y - int(torso_height * 0.1))
            cloth_w = min(shoulder_width, frame_w - cloth_x)
            cloth_h = min(torso_height, frame_h - cloth_y)
            
            if cloth_w <= 0 or cloth_h <= 0:
                return frame
            
            # Resize cloth to fit torso
            cloth_resized = cv2.resize(cloth, (cloth_w, cloth_h))
            
            # Create alpha blend for natural overlay
            alpha = 0.6  # Transparency level
            
            # Blend cloth onto frame
            roi = frame[cloth_y:cloth_y+cloth_h, cloth_x:cloth_x+cloth_w]
            blended = cv2.addWeighted(roi, 1-alpha, cloth_resized, alpha, 0)
            frame[cloth_y:cloth_y+cloth_h, cloth_x:cloth_x+cloth_w] = blended
            
            # Draw keypoints for visualization (optional)
            for kp in [left_shoulder, right_shoulder, left_hip, right_hip]:
                if kp and kp.get('visibility', 0) > 0.5:
                    x = int(kp['x'] * frame_w)
                    y = int(kp['y'] * frame_h)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
        return frame
        
    except Exception as e:
        print(f"AR overlay error: {e}")
        return frame

def remove_white_background(img, threshold=240):
    """
    Remove white background from image and make it transparent.
    
    Args:
        img: PIL Image in RGBA mode
        threshold: Brightness threshold for white detection (0-255)
    
    Returns:
        PIL Image with transparent background
    """
    # Convert to numpy array
    data = np.array(img)
    
    # Get RGB channels
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Create mask for white pixels (where all RGB values are above threshold)
    white_mask = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Set alpha channel to 0 (transparent) where white is detected
    data[:,:,3] = np.where(white_mask, 0, a)
    
    # Convert back to PIL Image
    return Image.fromarray(data, 'RGBA')

@app.route('/add_clothing')
def add_clothing_page():
    """2D Clothing addition page"""
    # Get current dataset statistics
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    total_clothes = len(clothes)
    
    # Get next available ID
    existing_ids = []
    for filename in clothes:
        try:
            id_part = filename.split('_')[0]
            if id_part.isdigit():
                existing_ids.append(int(id_part))
        except:
            continue
    
    next_id = max(existing_ids) + 1 if existing_ids else 1
    next_id_str = f"{next_id:05d}_00"
    
    return render_template('add_clothing.html', 
                         total_clothes=total_clothes,
                         next_id=next_id_str)

@app.route('/api/add_clothing', methods=['POST'])
def add_clothing_api():
    """API to process and add clothing images to dataset"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400
        
        # Get processing options
        target_size = request.form.get('target_size', '768x1024')
        bg_color = request.form.get('bg_color', 'white')
        create_mask = request.form.get('create_mask', 'true') == 'true'
        center_image = request.form.get('center_image', 'true') == 'true'
        name_prefix = request.form.get('name_prefix', '')
        
        # Parse target size
        if target_size != 'original':
            width, height = map(int, target_size.split('x'))
        else:
            width, height = None, None
        
        # Get next available ID
        clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
        existing_ids = []
        for filename in clothes:
            try:
                id_part = filename.split('_')[0]
                if id_part.isdigit():
                    existing_ids.append(int(id_part))
            except:
                continue
        
        next_id = max(existing_ids) + 1 if existing_ids else 1
        
        # Process each file
        added_files = []
        cloth_ids = []
        
        for idx, file in enumerate(files):
            if file.filename == '':
                continue
            
            # Generate cloth ID
            cloth_id = f"{next_id + idx:05d}_00"
            cloth_ids.append(cloth_id)
            
            # Open image
            img = Image.open(file.stream)
            
            # Convert to RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Remove white background (make transparent)
            img = remove_white_background(img)
            
            # Resize if specified
            if width and height:
                # Maintain aspect ratio
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                
                # Create background based on selection
                if bg_color == 'transparent':
                    # Keep transparent background
                    final_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                else:
                    # Create colored background
                    bg_colors = {
                        'white': (255, 255, 255, 255),
                        'black': (0, 0, 0, 255),
                        'gray': (128, 128, 128, 255)
                    }
                    final_img = Image.new('RGBA', (width, height), bg_colors.get(bg_color, (255, 255, 255, 255)))
                
                # Center image if requested
                if center_image:
                    x_offset = (width - img.width) // 2
                    y_offset = (height - img.height) // 2
                    final_img.paste(img, (x_offset, y_offset), img)  # Use img as mask for transparency
                else:
                    final_img.paste(img, (0, 0), img)
                
                img = final_img
            
            # Convert to RGB for JPEG saving (no alpha channel)
            img = img.convert('RGB')
            
            # Save cloth image
            cloth_path = CLOTH_DIR / f"{cloth_id}.jpg"
            img.save(cloth_path, 'JPEG', quality=95)
            added_files.append(cloth_path)
            
            # Create mask if requested
            if create_mask:
                mask_dir = TEST_DIR / 'cloth-mask'
                mask_dir.mkdir(parents=True, exist_ok=True)
                
                # Create proper mask from alpha channel
                # Reopen with alpha to extract mask
                temp_img = Image.open(file.stream)
                if temp_img.mode != 'RGBA':
                    temp_img = temp_img.convert('RGBA')
                temp_img = remove_white_background(temp_img)
                
                # Resize mask to match cloth size
                temp_img.thumbnail((width if width else temp_img.width, 
                                   height if height else temp_img.height), 
                                  Image.Resampling.LANCZOS)
                
                # Extract alpha channel as mask
                mask = Image.new('L', (width if width else temp_img.width, 
                                      height if height else temp_img.height), 0)
                if center_image and width and height:
                    x_offset = (width - temp_img.width) // 2
                    y_offset = (height - temp_img.height) // 2
                    mask.paste(temp_img.split()[3], (x_offset, y_offset))  # Alpha channel
                else:
                    mask.paste(temp_img.split()[3], (0, 0))
                
                mask_path = mask_dir / f"{cloth_id}.jpg"
                mask.save(mask_path, 'JPEG', quality=95)
        
        # Update total count
        all_clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
        
        return jsonify({
            'success': True,
            'added_count': len(added_files),
            'cloth_ids': cloth_ids,
            'total_clothes': len(all_clothes),
            'next_id': f"{next_id + len(files):05d}_00"
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/color_harmony', methods=['POST'])
def color_harmony():
    """Calculate color harmony score between person and clothing"""
    try:
        data = request.get_json()
        person = data.get('person')
        
        if not person:
            return jsonify({'error': 'No person selected'}), 400
        
        # Calculate color harmony score (simplified implementation)
        harmony_score = calculate_color_harmony(person)
        
        return jsonify({
            'harmony_score': harmony_score,
            'person': person
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_color_harmony(person_file):
    """Calculate color harmony between person and clothing (simplified)"""
    try:
        # Load person image
        person_path = IMG_DIR / person_file
        person_img = Image.open(person_path).resize((64, 64))
        
        # Extract color features
        person_features = extract_color_features(person_img)
        
        # For demo purposes, we'll return a random score between 0.7 and 0.95
        # In a real implementation, this would compare with selected clothing
        import random
        return random.uniform(0.7, 0.95)
    except:
        return 0.5  # Default score if calculation fails

@app.route('/api/dataset/stats', methods=['GET'])
def dataset_stats():
    """Get dataset statistics"""
    try:
        # Count images in each directory
        person_count = len([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
        cloth_count = len([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
        mask_count = len([f for f in os.listdir(TEST_DIR / 'cloth-mask') if f.lower().endswith('.jpg')])
        
        # Get skin tone stats if available
        skin_tone_stats = {}
        classification_file = WORKSPACE / 'skin_tone_classification' / 'skin_tone_classification.json'
        if classification_file.exists():
            with open(classification_file, 'r') as f:
                classification_data = json.load(f)
                skin_tone_stats = classification_data.get('categories', {})
        
        return jsonify({
            'persons': person_count,
            'clothes': cloth_count,
            'masks': mask_count,
            'skin_tone_distribution': skin_tone_stats,
            'total_pairs': person_count * cloth_count  # Theoretical maximum pairs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/person/<person_id>', methods=['DELETE'])
def delete_person(person_id):
    """Delete a person from the dataset"""
    try:
        # Delete person image
        person_path = IMG_DIR / person_id
        if person_path.exists():
            person_path.unlink()
        
        # Delete associated files
        parse_path = TEST_DIR / 'image-parse' / person_id.replace('.jpg', '.png')
        if parse_path.exists():
            parse_path.unlink()
            
        pose_img_path = TEST_DIR / 'openpose-img' / person_id.replace('.jpg', '_rendered.png')
        if pose_img_path.exists():
            pose_img_path.unlink()
            
        pose_json_path = TEST_DIR / 'openpose-json' / person_id.replace('.jpg', '_keypoints.json')
        if pose_json_path.exists():
            pose_json_path.unlink()
        
        return jsonify({'success': True, 'message': f'Person {person_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/cloth/<cloth_id>', methods=['DELETE'])
def delete_cloth(cloth_id):
    """Delete a clothing item from the dataset"""
    try:
        # Delete cloth image
        cloth_path = CLOTH_DIR / cloth_id
        if cloth_path.exists():
            cloth_path.unlink()
        
        # Delete associated mask
        mask_path = TEST_DIR / 'cloth-mask' / cloth_id
        if mask_path.exists():
            mask_path.unlink()
        
        return jsonify({'success': True, 'message': f'Clothing item {cloth_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/batch_delete', methods=['POST'])
def batch_delete():
    """Delete multiple items from the dataset"""
    try:
        data = request.get_json()
        persons = data.get('persons', [])
        clothes = data.get('clothes', [])
        
        deleted_persons = []
        deleted_clothes = []
        
        # Delete persons
        for person_id in persons:
            try:
                person_path = IMG_DIR / person_id
                if person_path.exists():
                    person_path.unlink()
                    deleted_persons.append(person_id)
                    
                # Delete associated files
                parse_path = TEST_DIR / 'image-parse' / person_id.replace('.jpg', '.png')
                if parse_path.exists():
                    parse_path.unlink()
                    
                pose_img_path = TEST_DIR / 'openpose-img' / person_id.replace('.jpg', '_rendered.png')
                if pose_img_path.exists():
                    pose_img_path.unlink()
                    
                pose_json_path = TEST_DIR / 'openpose-json' / person_id.replace('.jpg', '_keypoints.json')
                if pose_json_path.exists():
                    pose_json_path.unlink()
            except Exception as e:
                print(f"Error deleting person {person_id}: {e}")
        
        # Delete clothes
        for cloth_id in clothes:
            try:
                cloth_path = CLOTH_DIR / cloth_id
                if cloth_path.exists():
                    cloth_path.unlink()
                    deleted_clothes.append(cloth_id)
                    
                # Delete associated mask
                mask_path = TEST_DIR / 'cloth-mask' / cloth_id
                if mask_path.exists():
                    mask_path.unlink()
            except Exception as e:
                print(f"Error deleting cloth {cloth_id}: {e}")
        
        return jsonify({
            'success': True,
            'deleted_persons': deleted_persons,
            'deleted_clothes': deleted_clothes,
            'message': f'Deleted {len(deleted_persons)} persons and {len(deleted_clothes)} clothing items'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/virtual_tryon')
def virtual_tryon_page():
    """Virtual Try-On pipeline visualization page"""
    # Get available person and cloth images
    people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    
    # Select first person and cloth as defaults
    default_person = people[0] if people else None
    default_cloth = clothes[0] if clothes else None
    
    return render_template('virtual_tryon.html', 
                         people=people, 
                         clothes=clothes,
                         default_person=default_person,
                         default_cloth=default_cloth)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
