from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)

# 업로드된 파일을 저장할 경로 설정
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '파일이 없습니다.'
    file = request.files['file']
    if file.filename == '':
        return '파일 이름이 없습니다.'
    if file and file.filename.endswith('.mp3'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # 여기서 Music_Sep.ipynb의 MIDI 변환 코드를 호출해야 함
        # 예를 들어, subprocess를 사용해 해당 스크립트를 실행할 수 있습니다.

        return redirect(url_for('home'))
    else:
        return 'MP3 파일만 업로드할 수 있습니다.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)