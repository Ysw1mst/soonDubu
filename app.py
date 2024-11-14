from flask import Flask, request, render_template, send_from_directory
import os
from convert import separate_and_convert

app = Flask(__name__)

# 업로드된 MP3 파일을 저장할 경로
UPLOAD_FOLDER = 'uploads'
midi_folder = 'static/midi'  # 변환된 MIDI 파일이 저장될 경로

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(midi_folder):
    os.makedirs(midi_folder)

@app.route('/')
def home():
    return render_template('index.html', midi_file=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part in the request")
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        print("No selected file")
        return "No selected file"

    if file:
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)
        print(f"File uploaded: {mp3_path}")

        midi_files = separate_and_convert(mp3_path)  # MP3를 MIDI로 변환
        if midi_files:
            print(f"MIDI conversion completed: {midi_files}")
            midi_file_names = [os.path.basename(midi) for midi in midi_files]
            return render_template('index.html', midi_files=midi_file_names)
        else:
            print("Failed to convert MP3 to MIDI")
            return "Failed to convert MP3 to MIDI"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(midi_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)