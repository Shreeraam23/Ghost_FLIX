from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder ka path
UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Max file size (optional) — 500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')  # Tumhara HTML file templates folder me hona chahiye

@app.route('/upload-files', methods=['POST'])
def upload_files():
    if 'docs' not in request.files:
        return jsonify({'error': 'No files found'}), 400

    files = request.files.getlist('docs')
    saved_files = []

    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        # Agar subfolders preserve karne hain to:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        saved_files.append(filename)

    return jsonify({
        'message': 'Files uploaded successfully',
        'count': len(saved_files)
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
