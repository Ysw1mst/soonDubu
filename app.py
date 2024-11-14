from flask import Flask, request, render_template, send_file
import os
from convert import separate_and_convert

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
MIDI_FOLDER = 'static/midi'

# 업로드 폴더가 없으면 생성
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
        file.save(mp3_path)

        # MP3 파일을 분리 및 MIDI로 변환
        midi_files = separate_and_convert(mp3_path)

        # 변환된 첫 번째 MIDI 파일을 사용하여 다운로드 링크를 생성
        if midi_files:
            midi_file_path = midi_files[0]  # 첫 번째 MIDI 파일
            midi_file_name = os.path.basename(midi_file_path)
            return render_template('index.html', midi_file=midi_file_name)
        else:
            return "Failed to convert MP3 to MIDI"

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(MIDI_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)