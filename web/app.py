from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import time
import subprocess
from pathlib import Path
import sys

app = Flask(__name__)

# Base paths
WORKSPACE = Path(__file__).resolve().parent.parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = WORKSPACE / 'datasets'
CHECKPOINTS_DIR = WORKSPACE / 'checkpoints'
RESULTS_DIR = VITON_DIR / 'results'

TEST_DIR = DATASETS_DIR / 'test'
IMG_DIR = TEST_DIR / 'image'
CLOTH_DIR = TEST_DIR / 'cloth'

@app.route('/')
def index():
    people = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.lower().endswith('.jpg')])
    return render_template('index.html', people=people, clothes=clothes)

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

    # Invoke test.py
    cmd = [
        sys.executable, str(VITON_DIR / 'test.py'),
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

    return render_template('result.html', job_name=job_name, image_name=generated[0])

@app.route('/results/<job_name>/<image_name>')
def serve_result(job_name, image_name):
    return send_from_directory(RESULTS_DIR / job_name, image_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
