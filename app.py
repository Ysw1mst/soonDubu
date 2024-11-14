from flask import Flask, request, render_template
import os
import glob

app = Flask(__name__)

# 업로드된 MP3 파일을 저장할 경로
UPLOAD_FOLDER = 'uploads'  # 여기에 업로드된 파일이 저장됩니다.
midi_folder = 'static/midi/'  # 변환된 MIDI 파일이 저장될 경로

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(midi_folder):
    os.makedirs(midi_folder)

# MP3 파일을 MIDI로 변환하는 함수 (여기서 실제 변환 작업이 이루어집니다.)
def convert_mp3_to_midi(mp3_path):
    # 변환된 MIDI 파일 이름을 반환합니다.
    file_name = os.path.splitext(os.path.basename(mp3_path))[0]
    midi_file_path = os.path.join(midi_folder, f"{file_name}.midi")
    
    # 실제 변환 코드 (예시로 임시로 파일 경로만 반환)
    # 여기에 transkun 명령어 등 변환 명령을 넣을 수 있습니다.
    
    # 변환 완료 후 MIDI 파일의 경로를 반환
    return midi_file_path  # 변환된 MIDI 파일 경로를 반환합니다.

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
        print(f"Uploaded file saved as: {mp3_path}")  # 업로드된 파일 확인

        midi_file_path = convert_mp3_to_midi(mp3_path)  # MP3를 MIDI로 변환

        if midi_file_path:
            midi_file_name = os.path.basename(midi_file_path)  # MIDI 파일 이름만 추출
            print(f"Converted MIDI file saved as: {midi_file_name}")  # 변환된 파일 확인
            return render_template('index.html', midi_file=midi_file_name)  # MIDI 파일 이름을 템플릿에 전달
        else:
            return "Failed to convert MP3 to MIDI"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)