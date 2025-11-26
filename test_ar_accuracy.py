"""
Test script for AR Try-On accuracy improvements
Tests the enhanced overlay algorithm with various scenarios
"""

import cv2
import numpy as np
import json
import base64
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"

def create_test_keypoints(scenario="normal"):
    """
    Create test keypoints for different scenarios
    
    Scenarios:
    - normal: Person facing camera directly
    - tilted: Person with tilted body
    - side: Person at an angle
    - far: Person far from camera
    - close: Person close to camera
    """
    
    if scenario == "normal":
        # Normal frontal pose
        keypoints = [
            {"x": 0.5, "y": 0.2, "z": 0.0, "visibility": 0.95},  # 0: Nose
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 10,  # 1-10: Other face points
            {"x": 0.4, "y": 0.35, "z": -0.1, "visibility": 0.9},  # 11: Left shoulder
            {"x": 0.6, "y": 0.35, "z": -0.1, "visibility": 0.9},  # 12: Right shoulder
            {"x": 0.35, "y": 0.5, "z": -0.05, "visibility": 0.85},  # 13: Left elbow
            {"x": 0.65, "y": 0.5, "z": -0.05, "visibility": 0.85},  # 14: Right elbow
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 8,  # 15-22: Other points
            {"x": 0.42, "y": 0.65, "z": 0.0, "visibility": 0.88},  # 23: Left hip
            {"x": 0.58, "y": 0.65, "z": 0.0, "visibility": 0.88},  # 24: Right hip
        ]
    
    elif scenario == "tilted":
        # Body tilted to the right
        keypoints = [
            {"x": 0.5, "y": 0.2, "z": 0.0, "visibility": 0.92},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 10,
            {"x": 0.35, "y": 0.32, "z": -0.1, "visibility": 0.88},  # Left shoulder (higher)
            {"x": 0.65, "y": 0.38, "z": -0.1, "visibility": 0.88},  # Right shoulder (lower)
            {"x": 0.3, "y": 0.48, "z": -0.05, "visibility": 0.82},
            {"x": 0.7, "y": 0.52, "z": -0.05, "visibility": 0.82},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 8,
            {"x": 0.38, "y": 0.62, "z": 0.0, "visibility": 0.85},
            {"x": 0.62, "y": 0.68, "z": 0.0, "visibility": 0.85},
        ]
    
    elif scenario == "side":
        # Person at 45-degree angle
        keypoints = [
            {"x": 0.55, "y": 0.2, "z": 0.0, "visibility": 0.9},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 10,
            {"x": 0.45, "y": 0.35, "z": -0.2, "visibility": 0.85},  # Left shoulder (visible)
            {"x": 0.55, "y": 0.35, "z": 0.1, "visibility": 0.7},   # Right shoulder (partially hidden)
            {"x": 0.4, "y": 0.5, "z": -0.15, "visibility": 0.8},
            {"x": 0.6, "y": 0.5, "z": 0.15, "visibility": 0.65},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 8,
            {"x": 0.47, "y": 0.65, "z": -0.1, "visibility": 0.82},
            {"x": 0.53, "y": 0.65, "z": 0.1, "visibility": 0.68},
        ]
    
    elif scenario == "far":
        # Person far from camera (smaller)
        keypoints = [
            {"x": 0.5, "y": 0.3, "z": 0.0, "visibility": 0.88},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 10,
            {"x": 0.45, "y": 0.4, "z": -0.05, "visibility": 0.85},
            {"x": 0.55, "y": 0.4, "z": -0.05, "visibility": 0.85},
            {"x": 0.42, "y": 0.5, "z": -0.03, "visibility": 0.8},
            {"x": 0.58, "y": 0.5, "z": -0.03, "visibility": 0.8},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 8,
            {"x": 0.47, "y": 0.6, "z": 0.0, "visibility": 0.83},
            {"x": 0.53, "y": 0.6, "z": 0.0, "visibility": 0.83},
        ]
    
    elif scenario == "close":
        # Person close to camera (larger)
        keypoints = [
            {"x": 0.5, "y": 0.15, "z": 0.0, "visibility": 0.95},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 10,
            {"x": 0.3, "y": 0.3, "z": -0.15, "visibility": 0.92},
            {"x": 0.7, "y": 0.3, "z": -0.15, "visibility": 0.92},
            {"x": 0.2, "y": 0.5, "z": -0.1, "visibility": 0.88},
            {"x": 0.8, "y": 0.5, "z": -0.1, "visibility": 0.88},
            *[{"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0}] * 8,
            {"x": 0.35, "y": 0.7, "z": 0.0, "visibility": 0.9},
            {"x": 0.65, "y": 0.7, "z": 0.0, "visibility": 0.9},
        ]
    
    else:
        raise ValueError(f"Unknown scenario: {scenario}")
    
    # Pad to 33 keypoints (MediaPipe Pose standard)
    while len(keypoints) < 33:
        keypoints.append({"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.0})
    
    return keypoints[:33]

def create_test_frame(width=640, height=480, color=(100, 150, 200)):
    """Create a test frame with a simple background"""
    frame = np.full((height, width, 3), color, dtype=np.uint8)
    
    # Add some texture
    noise = np.random.randint(-20, 20, (height, width, 3), dtype=np.int16)
    frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add a simple person silhouette
    cv2.ellipse(frame, (width//2, height//2), (width//6, height//3), 
                0, 0, 360, (80, 120, 160), -1)
    
    return frame

def encode_frame(frame):
    """Encode frame to base64"""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def test_ar_overlay_scenarios():
    """Test AR overlay with different scenarios"""
    print("=" * 70)
    print("Testing AR Try-On Accuracy Improvements")
    print("=" * 70)
    
    scenarios = ["normal", "tilted", "side", "far", "close"]
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        print("✅ Server is running\n")
    except:
        print("❌ Error: Flask server is not running")
        print("Please start the server: python web/app.py")
        return
    
    # Get list of available clothes
    try:
        response = requests.get(f"{BASE_URL}/api/get_clothes", timeout=5)
        clothes = response.json().get('clothes', [])
        if not clothes:
            print("❌ No clothing items found")
            return
        test_cloth = clothes[0]
        print(f"📦 Using test cloth: {test_cloth}\n")
    except Exception as e:
        print(f"❌ Error getting clothes: {e}")
        return
    
    results = []
    
    for scenario in scenarios:
        print(f"\n{'='*70}")
        print(f"Testing Scenario: {scenario.upper()}")
        print(f"{'='*70}")
        
        # Create test data
        frame = create_test_frame()
        keypoints = create_test_keypoints(scenario)
        frame_b64 = f"data:image/jpeg;base64,{encode_frame(frame)}"
        
        # Calculate expected metrics
        visible_kps = sum(1 for kp in keypoints if kp['visibility'] > 0.6)
        avg_visibility = np.mean([kp['visibility'] for kp in keypoints if kp['visibility'] > 0])
        
        print(f"\n📊 Input Metrics:")
        print(f"   • Visible keypoints: {visible_kps}/33")
        print(f"   • Average visibility: {avg_visibility:.2f}")
        
        # Test AR overlay
        try:
            response = requests.post(
                f"{BASE_URL}/api/ar/overlay",
                json={
                    "frame": frame_b64,
                    "cloth": test_cloth,
                    "keypoints": keypoints
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Overlay Applied Successfully")
                
                # Decode result frame
                result_b64 = data.get('frame', '').split(',')[1]
                result_bytes = base64.b64decode(result_b64)
                result_array = np.frombuffer(result_bytes, dtype=np.uint8)
                result_frame = cv2.imdecode(result_array, cv2.IMREAD_COLOR)
                
                # Calculate quality metrics
                if result_frame is not None:
                    # Check if overlay was applied (frame changed)
                    diff = cv2.absdiff(frame, result_frame)
                    overlay_applied = np.mean(diff) > 5
                    
                    print(f"   • Overlay detected: {'Yes' if overlay_applied else 'No'}")
                    print(f"   • Frame difference: {np.mean(diff):.2f}")
                    
                    results.append({
                        'scenario': scenario,
                        'success': True,
                        'overlay_applied': overlay_applied,
                        'visible_keypoints': visible_kps,
                        'avg_visibility': avg_visibility,
                        'frame_diff': np.mean(diff)
                    })
                else:
                    print(f"   ❌ Failed to decode result frame")
                    results.append({
                        'scenario': scenario,
                        'success': False,
                        'error': 'Failed to decode frame'
                    })
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text}")
                results.append({
                    'scenario': scenario,
                    'success': False,
                    'error': response.text
                })
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append({
                'scenario': scenario,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}\n")
    
    successful = sum(1 for r in results if r.get('success', False))
    overlays_applied = sum(1 for r in results if r.get('overlay_applied', False))
    
    print(f"📊 Overall Results:")
    print(f"   • Total scenarios tested: {len(scenarios)}")
    print(f"   • Successful requests: {successful}/{len(scenarios)}")
    print(f"   • Overlays applied: {overlays_applied}/{len(scenarios)}")
    print(f"   • Success rate: {(successful/len(scenarios)*100):.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for result in results:
        status = "✅" if result.get('success') else "❌"
        overlay = "🎨" if result.get('overlay_applied') else "⚪"
        print(f"   {status} {overlay} {result['scenario'].upper():10s} - ", end="")
        if result.get('success'):
            print(f"Visibility: {result.get('avg_visibility', 0):.2f}, "
                  f"Diff: {result.get('frame_diff', 0):.2f}")
        else:
            print(f"Error: {result.get('error', 'Unknown')}")
    
    print(f"\n{'='*70}")
    print("✅ Testing Complete!")
    print(f"{'='*70}\n")
    
    print("💡 Next Steps:")
    print("   1. Open http://127.0.0.1:5000/ar_tryon in your browser")
    print("   2. Allow camera access")
    print("   3. Select a clothing item")
    print("   4. Test with different body positions")
    print("   5. Adjust settings in web/ar_config.py for fine-tuning")

if __name__ == "__main__":
    test_ar_overlay_scenarios()
