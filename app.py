from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from convert import separate_and_convert

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
        print("No file part")
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return redirect(url_for('home'))

    if file:
        mp3_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp3_path)
        print(f"Received file: {file.filename}")
        
        midi_files = separate_and_convert(mp3_path)
        midi_file_names = [os.path.basename(midi) for midi in midi_files]
        
        return render_template('index.html', uploaded_file=file.filename, midi_files=midi_file_names)

@app.route('/download')
def download():
    midi_files = os.listdir(MIDI_FOLDER)
    if midi_files:
        midi_file_path = os.path.join(MIDI_FOLDER, midi_files[0])
        return send_from_directory(MIDI_FOLDER, midi_files[0], as_attachment=True)
    else:
        return "No MIDI files available for download."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)