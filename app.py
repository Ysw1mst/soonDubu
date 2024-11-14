from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from convert import separate_and_convert  # separate_and_convert 함수가 convert.py에 있다고 가정

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
MIDI_FOLDER = 'static/midi'

# 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MIDI_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', uploaded_file=None, midi_files=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    if file:
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)

        midi_files = separate_and_convert(mp3_path)  # 변환된 MIDI 파일 리스트 반환
        midi_file_names = [os.path.basename(midi) for midi in midi_files]
        
        return render_template('index.html', uploaded_file=file.filename, midi_files=midi_file_names)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(MIDI_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)