import os
import glob
import mido
import subprocess

# MIDI 파일 저장 경로
midi_folder = 'static/midi/'
music_folder = 'uploads/separated/'  # 음원 분리된 mp3 파일이 저장될 폴더

# 각 악기에 맞는 MIDI 프로그램 번호 설정 (General MIDI 기준)
instrument_programs = {
    'piano': 0,    # Acoustic Grand Piano
    'guitar': 24,  # Acoustic Guitar (nylon)
    'bass': 32     # Acoustic Bass
}

# 음원 분리 및 MIDI 변환 함수
def separate_and_convert(mp3_path):
    # 1. 음원 분리 수행 (Demucs 사용)
    demucs_command = f"demucs -n htdemucs_6s --mp3 \"{mp3_path}\" -o {music_folder}"
    subprocess.run(demucs_command, shell=True, check=True)

    # 2. 변환된 음원 파일들을 찾아 MIDI로 변환
    separated_folder = os.path.join(music_folder, "htdemucs_6s")
    mp3_files = glob.glob(os.path.join(separated_folder, '**/*.mp3'), recursive=True)

    midi_files = []
    for mp3_file in mp3_files:
        file_name = os.path.splitext(os.path.basename(mp3_file))[0]
        midi_file_path = os.path.join(midi_folder, f"{file_name}.midi")
        
        # 악기 설정
        instrument = 'piano'  # 기본 악기
        program_number = instrument_programs[instrument]
        if 'guitar' in mp3_file.lower():
            instrument = 'guitar'
            program_number = instrument_programs[instrument]
        elif 'bass' in mp3_file.lower():
            instrument = 'bass'
            program_number = instrument_programs[instrument]

        # transkun을 사용하여 MIDI 파일 생성
        transkun_command = f"transkun \"{mp3_file}\" \"{midi_file_path}\" --device cuda"
        subprocess.run(transkun_command, shell=True, check=True)

        # 악기 변경
        if os.path.exists(midi_file_path):
            change_instrument(midi_file_path, program_number)
            midi_files.append(midi_file_path)

    return midi_files

# MIDI 파일에서 악기 변경 함수
def change_instrument(midi_file_path, program_number):
    mid = mido.MidiFile(midi_file_path)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'program_change':
                msg.program = program_number
    mid.save(midi_file_path)