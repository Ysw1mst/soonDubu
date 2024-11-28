const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');
const convertButton = document.getElementById('convert-button');
const playMidiButton = document.getElementById('play-midi');
const visualization = document.getElementById('visualization');
const downloadButtons = document.querySelectorAll('.small-button');

let uploadedFile = null;
let instrumentFiles = {
    piano: { mp3: '', midi: '' },
    guitar: { mp3: '', midi: '' },
    bass: { mp3: '', midi: '' },
};

// **1. 드래그 앤 드롭 파일 업로드**
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.background = '#eaeaea';
});

dropArea.addEventListener('dragleave', () => {
    dropArea.style.background = '#f9f9f9';
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.background = '#f9f9f9';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadedFile = files[0];
        fileName.textContent = uploadedFile.name;
    }
});

dropArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        uploadedFile = fileInput.files[0];
        fileName.textContent = uploadedFile.name;
    }
});

// **2. Convert to MIDI**
convertButton.addEventListener('click', async () => {
    console.log('Convert button clicked');
    if (!uploadedFile) {
        alert('Please upload a file first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/convert', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Server response:', data);

            // 서버 응답 데이터로 다운로드 버튼 설정
            setupDownloadButtons(data.instrument_files);
            renderVisualization(data.visualization_data || {});
            alert('Conversion successful!');
        } else {
            const errorData = await response.json();
            console.error('Server error:', errorData);
            alert(`Conversion failed: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to send request to server.');
    }
});

// **3. 다운로드 버튼 설정**
function setupDownloadButtons(data) {
    if (!data) {
        console.error('No data received for instrument files.');
        alert('Instrument data is missing. Please try again.');
        return;
    }

    // 안전하게 데이터를 설정
    instrumentFiles.piano = data.piano || { mp3: '', midi: '' };
    instrumentFiles.guitar = data.guitar || { mp3: '', midi: '' };
    instrumentFiles.bass = data.bass || { mp3: '', midi: '' };

    console.log('Instrument files successfully set:', instrumentFiles);

    downloadButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const [type, instrument] = button.id.split('-').slice(1); // "mp3" 또는 "midi"
            const filePath = instrumentFiles[instrument]?.[type];

            console.log(`Download button clicked for ${instrument} (${type}):`, filePath);

            if (filePath) {
                const a = document.createElement('a');
                a.href = `http://127.0.0.1:5000/download/${filePath.split('/').pop()}`;
                a.download = `${instrument}.${type}`;
                a.click();
            } else {
                alert(`No ${type.toUpperCase()} file available for ${instrument}.`);
            }
        });
    });
}

// **4. MIDI 시각화 렌더링**
function renderVisualization(data) {
    visualization.innerHTML = '';

    Object.keys(data).forEach((instrument) => {
        const track = document.createElement('div');
        track.className = 'note-track';
        track.innerHTML = `<h3>${instrument}</h3><div class="note-line"></div>`;
        const noteLine = track.querySelector('.note-line');
        data[instrument].forEach((note) => {
            const noteDiv = document.createElement('div');
            noteDiv.className = 'note';
            noteDiv.style.left = `${note.position}%`;
            noteDiv.style.width = `${note.length}%`;
            noteLine.appendChild(noteDiv);
        });
        visualization.appendChild(track);
    });
}

// **5. Play MIDI**
playMidiButton.addEventListener('click', () => {
    const selectedInstruments = ['piano', 'guitar', 'bass'].filter(
        (inst) => document.getElementById(`${inst}-checkbox`).checked
    );

    if (selectedInstruments.length === 0) {
        alert('Please select at least one instrument to play.');
        return;
    }

    selectedInstruments.forEach((instrument) => {
        const filePath = instrumentFiles[instrument]?.midi;

        if (filePath) {
            fetch(filePath)
                .then((response) => response.arrayBuffer())
                .then((data) => {
                    MIDI.Player.loadArrayBuffer(data);
                    MIDI.Player.start();
                });
        }
    });
});
