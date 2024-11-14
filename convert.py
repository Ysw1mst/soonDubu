import os
import glob
import mido

midi_folder = 'static/midi'
music_folder = 'uploads/separated'

# 각 악기에 맞는 MIDI 프로그램 번호 설정
instrument_programs = {
    'piano': 0,    # Acoustic Grand Piano
    'guitar': 24,  # Acoustic Guitar (nylon)
    'bass': 32     # Acoustic Bass
}

# 음원 분리 및 MIDI 변환 함수
def separate_and_convert(mp3_path):
    print(f"Starting separation and conversion for: {mp3_path}")
    
    # 1. 음원 분리 수행
    demucs_command = f"demucs -n htdemucs_6s --mp3 \"{mp3_path}\" -o {music_folder}"
    os.system(demucs_command)
    print("Separation complete, starting MIDI conversion...")

    separated_folder = os.path.join(music_folder, "htdemucs_6s")
    mp3_files = glob.glob(os.path.join(separated_folder, '**/*.mp3'), recursive=True)

    midi_files = []
    for mp3_file in mp3_files:
        file_name = os.path.splitext(os.path.basename(mp3_file))[0]
        midi_file_path = os.path.join(midi_folder, f"{file_name}.midi")
        
        instrument = 'piano'
        program_number = instrument_programs[instrument]
        if 'guitar' in mp3_file.lower():
            instrument = 'guitar'
            program_number = instrument_programs[instrument]
        elif 'bass' in mp3_file.lower():
            instrument = 'bass'
            program_number = instrument_programs[instrument]

        transkun_command = f"transkun \"{mp3_file}\" \"{midi_file_path}\" --device cuda"
        print(f"Converting {mp3_file} to MIDI at {midi_file_path} using {instrument} (program {program_number})")
        os.system(transkun_command)

        if os.path.exists(midi_file_path):
            change_instrument(midi_file_path, program_number)
            midi_files.append(midi_file_path)
            print(f"Conversion successful: {midi_file_path}")
        else:
            print(f"Conversion failed for: {mp3_file}")

    print(f"All conversions completed. MIDI files: {midi_files}")
    return midi_files

# MIDI 파일에서 악기 변경 함수
def change_instrument(midi_file_path, program_number):
    mid = mido.MidiFile(midi_file_path)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'program_change':
                msg.program = program_number
    mid.save(midi_file_path)
    print(f"Instrument changed to program {program_number} for {midi_file_path}")