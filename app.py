from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # 업로드된 파일을 저장할 경로
midi_folder = 'static/midi/'  # 변환된 MIDI 파일을 저장할 경로

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(midi_folder):
    os.makedirs(midi_folder)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        # 저장할 파일 경로
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)  # 파일 저장

        print(f"File uploaded: {mp3_path}")
        
        # 예시로 MIDI 파일 이름을 반환
        midi_file_name = file.filename.rsplit('.', 1)[0] + '.midi'

        # 실제로 파일 변환하는 코드가 여기에 추가될 수 있습니다.
        
        return render_template('index.html', midi_file=midi_file_name)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(midi_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)