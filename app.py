from flask import Flask, request, render_template, redirect, url_for
import os
from convert import separate_and_convert  # convert.py의 변환 함수

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
MIDI_FOLDER = 'static/midi/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(MIDI_FOLDER):
    os.makedirs(MIDI_FOLDER)

@app.route('/')
def home():
    return render_template('index.html', midi_file=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)  # MP3 파일 저장

        # MP3를 MIDI로 변환
        midi_files = separate_and_convert(mp3_path)
        
        if midi_files:
            midi_file_name = os.path.basename(midi_files[0])  # 변환된 첫 번째 MIDI 파일 이름
            return render_template('index.html', midi_file=midi_file_name)
        else:
            return "Failed to convert MP3 to MIDI"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)