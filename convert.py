import nbformat
from nbconvert import ExecutePreprocessor
from flask import Flask, request, send_file, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MIDI_FOLDER'] = 'midi_outputs'

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MIDI_FOLDER'], exist_ok=True)

def run_notebook(input_mp3_path):
    with open("Music_Sep.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': './'}})

    # MIDI 파일 생성 후 경로 리턴
    midi_file_path = os.path.join(app.config['MIDI_FOLDER'], "output.mid")
    return midi_file_path

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'mp3_file' not in request.files:
        return "No file provided", 400
    
    mp3_file = request.files['mp3_file']
    mp3_path = os.path.join(app.config['UPLOAD_FOLDER'], mp3_file.filename)
    mp3_file.save(mp3_path)

    # Music_Sep.ipynb 파일을 실행하고 MIDI 파일을 생성
    midi_file_path = run_notebook(mp3_path)
    
    # MIDI 파일 다운로드 링크 제공
    return send_file(midi_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)