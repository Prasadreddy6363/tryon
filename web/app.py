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
        </ul>
        <p style="color: #d9534f; font-weight: bold;">⚠️ Showing mock result (original person image only) - actual virtual try-on not available</p>
        <p><a href="/">← Back</a></p>
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

    # Invoke test.py
    cmd = [
        sys.executable, str(test_script),
        '--name', job_name,
        '--dataset_dir', str(DATASETS_DIR),
        '--checkpoint_dir', str(CHECKPOINTS_DIR),
        '--save_dir', str(RESULTS_DIR)
    ]
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
        
        if not all([kp.get('visibility', 0) > 0.5 for kp in [left_shoulder, right_shoulder, left_hip, right_hip]]):
            return frame
        
        # Calculate bounding box for torso
        frame_h, frame_w = frame.shape[:2]
        
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
            if kp.get('visibility', 0) > 0.5:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
