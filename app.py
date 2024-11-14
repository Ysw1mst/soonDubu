from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from convert import convert_mp3_to_midi

app = Flask(__name__)

# 업로드된 MP3 파일을 저장할 경로
UPLOAD_FOLDER = 'uploads'
MIDI_FOLDER = 'static/midi'  # 변환된 MIDI 파일이 저장될 경로

# 폴더가 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MIDI_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', midi_file=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('home'))

    if file:
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)  # MP3 파일 저장

        midi_file_path = convert_mp3_to_midi(mp3_path)  # MP3를 MIDI로 변환

        if midi_file_path:
            midi_file_name = os.path.basename(midi_file_path)
            return render_template('index.html', midi_file=midi_file_name)  # 변환된 MIDI 파일 이름을 템플릿에 전달
        else:
            return "Failed to convert MP3 to MIDI"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(MIDI_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)