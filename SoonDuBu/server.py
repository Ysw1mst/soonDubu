from flask import Flask, request, jsonify, send_file
import os
import subprocess
import shlex

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# **Convert Endpoint**
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    midi_output = os.path.join(OUTPUT_FOLDER, file.filename.replace('.mp3', '.midi'))
    piano_mp3 = os.path.join(OUTPUT_FOLDER, 'piano.mp3')
    guitar_mp3 = os.path.join(OUTPUT_FOLDER, 'guitar.mp3')
    bass_mp3 = os.path.join(OUTPUT_FOLDER, 'bass.mp3')

    try:
        input_path = shlex.quote(file_path)
        output_path = shlex.quote(midi_output)

        # Run the sep.py script
        subprocess.run(
            ['python', 'sep.py', '--input', input_path, '--output', output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        return jsonify({
            'midi_url': midi_output,
            'instrument_files': {
                'piano': {'mp3': piano_mp3, 'midi': midi_output},
                'guitar': {'mp3': guitar_mp3, 'midi': midi_output},
                'bass': {'mp3': bass_mp3, 'midi': midi_output},
            },
            'visualization_data': {
                'piano': [{'position': 10, 'length': 20}],
                'guitar': [{'position': 30, 'length': 40}],
                'bass': [{'position': 50, 'length': 60}],
            }
        })
    except Exception as e:
        print("Error during conversion:", e)
        return jsonify({'error': str(e)}), 500

# **File Download Endpoint**
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    print(f"Received download request for: {filename}")
    print(f"Resolved file path: {file_path}")

    if os.path.exists(file_path):
        print(f"File found: {file_path}. Sending to client.")
        return send_file(file_path, as_attachment=True)
    else:
        print(f"File not found: {file_path}")
        return jsonify({'error': 'File not found'}), 404

# Serve static files
@app.route('/')
def index():
    return send_file('main.html')

@app.route('/style.css')
def serve_css():
    return send_file('style.css')

@app.route('/script.js')
def serve_js():
    return send_file('script.js')

if __name__ == '__main__':
    app.run(port=5000)
