import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 폴더 설정
UPLOAD_FOLDER = './uploads'
MIDI_FOLDER = './midi'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MIDI_FOLDER, exist_ok=True)

# 설치 완료 여부를 저장할 플래그 파일 경로
FLAG_FILE = "./libraries_installed.txt"

# 설치해야 할 라이브러리 목록
REQUIRED_LIBRARIES = ["demucs", "ffmpeg-python", "transkun", "mido", "Flask"]

# 1. 라이브러리 설치 엔드포인트
@app.route('/install_libraries', methods=['POST'])
def install_libraries():
    if os.path.exists(FLAG_FILE):
        return jsonify({'message': 'Libraries already installed'}), 200

    try:
        for lib in REQUIRED_LIBRARIES:
            subprocess.check_call(["pip", "install", lib])
        # 설치 완료 플래그 파일 생성
        with open(FLAG_FILE, "w") as flag:
            flag.write("Libraries installed")
        return jsonify({'message': 'Libraries installed successfully'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f"Failed to install libraries: {str(e)}"}), 500

# 2. 라이브러리 설치 여부 확인 엔드포인트
@app.route('/check_libraries', methods=['GET'])
def check_libraries():
    if os.path.exists(FLAG_FILE):
        return jsonify({'installed': True}), 200
    return jsonify({'installed': False}), 200

# 3. MP3 업로드 및 MIDI 변환 엔드포인트
@app.route('/upload_mp3', methods=['POST'])
def upload_mp3():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    # MP3 파일 저장
    mp3_file = request.files['file']
    mp3_path = os.path.join(UPLOAD_FOLDER, mp3_file.filename)
    mp3_file.save(mp3_path)

    # sep1.py 실행 (MP3 → MIDI 변환)
    midi_filename = os.path.splitext(mp3_file.filename)[0] + '.midi'
    midi_path = os.path.join(MIDI_FOLDER, midi_filename)
    try:
        subprocess.run(['python3', 'sep1.py', '--input', mp3_path, '--output', midi_path], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error running sep1.py: {str(e)}'}), 500

    # 변환된 MIDI 파일 확인
    if not os.path.exists(midi_path):
        return jsonify({'error': 'MIDI file not generated'}), 500

    # MIDI 데이터 시각화용 노트 데이터 추출
    midi_data = analyze_midi(midi_path)
    return jsonify({'midi_data': midi_data})

# 4. MIDI 파일 다운로드 엔드포인트
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(MIDI_FOLDER, filename, as_attachment=True)

# 5. MIDI 파일 분석 함수
def analyze_midi(midi_path):
    import mido
    midi = mido.MidiFile(midi_path)
    notes = []
    current_time = 0

    for msg in midi:
        if not msg.is_meta:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'time': current_time,
                    'note': msg.note,
                    'velocity': msg.velocity
                })
    return notes

if __name__ == '__main__':
    app.run(debug=True)
