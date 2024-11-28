# !python3 -m pip install -U demucs
# !pip install ffmpeg-python
# !pip3 install transkun
# !pip install mido

# Music Seperate(음원 분리)
import demucs.separate
import shlex
import os
import glob
import mido

demucs.separate.main(shlex.split('--mp3 -n htdemucs_6s -d cuda "./bal.mp3"'))
# MIDI 파일 저장 경로
midi_folder = './sep_midi/'
if not os.path.exists(midi_folder):
    os.makedirs(midi_folder)

# 음악 파일 경로(음원 분리 된 mp3파일이 있는 경로)
music_folder = './separated/htdemucs_6s/'

# 폴더 내 모든 mp3 파일 찾기
mp3_files = glob.glob(os.path.join(music_folder, '**/*.mp3'), recursive=True)

# 각 악기에 맞는 MIDI 프로그램 번호 설정 (General MIDI 기준)
instrument_programs = {
    'piano': 0,    # 0: Acoustic Grand Piano
    'guitar': 24,  # 24: Acoustic Guitar (nylon)
    'bass': 32     # 32: Acoustic Bass
}

# MIDI 파일에서 악기 변경 함수
def change_instrument(midi_file_path, program_number):
    # MIDI 파일 열기
    mid = mido.MidiFile(midi_file_path)

    # 각 트랙의 메시지 수정
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'program_change':
                # 기존 프로그램 번호를 새로운 프로그램 번호로 변경
                msg.program = program_number

    # 수정된 MIDI 파일 저장
    mid.save(midi_file_path)

# 각 mp3 파일마다 transkun 명령어 실행 전 파일 이름 확인
for mp3_file in mp3_files:
    file_name = os.path.splitext(os.path.basename(mp3_file))[0]
    midi_file_path = os.path.join(midi_folder, file_name + ".midi")

    # 기본 악기는 피아노로 설정
    instrument = 'piano'
    program_number = instrument_programs[instrument]

    # 파일 이름에 'piano', 'guitar', 'bass'가 포함되어 있는지 확인하여 악기 설정
    if 'piano' in mp3_file.lower():
        instrument = 'piano'
        program_number = instrument_programs[instrument]
    elif 'guitar' in mp3_file.lower():
        instrument = 'guitar'
        program_number = instrument_programs[instrument]
    elif 'bass' in mp3_file.lower():
        instrument = 'bass'
        program_number = instrument_programs[instrument]
    else:
        # 해당 악기가 없으면 변환 건너뜀
        print(f'Skipping {mp3_file} (no matching instrument)')
        continue

    # transkun 명령어로 MIDI 파일 생성
    command = f'transkun "{mp3_file}" "{midi_file_path}" --device cuda'
    print(f"Executing: {command}")
    os.system(command)

    # transkun으로 변환된 파일이 존재하는지 확인
    if not os.path.exists(midi_file_path):
        print(f'Failed to generate MIDI file for {mp3_file}')
        continue

    # transkun으로 생성된 MIDI 파일에서 악기 번호 변환
    change_instrument(midi_file_path, program_number)
    print(f'Instrument changed to {instrument} for {midi_file_path}')
