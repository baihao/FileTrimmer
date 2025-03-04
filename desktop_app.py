from flask import Flask, render_template, jsonify, request
import os
import subprocess
import json
import webview
import sys
import os

# Add this near the top of your file
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_files():
    data = request.json
    input_dir = data['inputDir']
    cache_dir = data['cacheDir']
    cache_path = os.path.join(cache_dir, 'file_cache.json')
    
    try:
        subprocess.run([
            sys.executable,
            os.path.join(base_dir, "compare_word_files.py"),
            "--dir", input_dir,
            "--cache", cache_path,
            "--similarity", "0.7"
        ], check=True)
        
        with open(cache_path, 'r') as f:
            groups = json.load(f)
            
        return jsonify({
            'success': True,
            'groups': groups
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    window = webview.create_window('File Trimmer', app)
    webview.start()