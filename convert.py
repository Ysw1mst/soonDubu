import os
import glob
import mido

# MIDI 파일 저장 경로
MIDI_FOLDER = 'static/midi/'
MUSIC_FOLDER = 'uploads/separated/'

instrument_programs = {
    'piano': 0,
    'guitar': 24,
    'bass': 32
}

def separate_and_convert(mp3_path):
    demucs_command = f"demucs -n htdemucs_6s --mp3 \"{mp3_path}\" -o {MUSIC_FOLDER}"
    os.system(demucs_command)

    separated_folder = os.path.join(MUSIC_FOLDER, "htdemucs_6s")
    mp3_files = glob.glob(os.path.join(separated_folder, '**/*.mp3'), recursive=True)

    midi_files = []
    for mp3_file in mp3_files:
        file_name = os.path.splitext(os.path.basename(mp3_file))[0]
        midi_file_path = os.path.join(MIDI_FOLDER, f"{file_name}.midi")

        instrument = 'piano'
        program_number = instrument_programs[instrument]
        if 'guitar' in mp3_file.lower():
            instrument = 'guitar'
            program_number = instrument_programs[instrument]
        elif 'bass' in mp3_file.lower():
            instrument = 'bass'
            program_number = instrument_programs[instrument]

        transkun_command = f"transkun \"{mp3_file}\" \"{midi_file_path}\" --device cuda"
        os.system(transkun_command)

        if os.path.exists(midi_file_path):
            change_instrument(midi_file_path, program_number)
            midi_files.append(midi_file_path)

    return midi_files

def change_instrument(midi_file_path, program_number):
    mid = mido.MidiFile(midi_file_path)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'program_change':
                msg.program = program_number
    mid.save(midi_file_path)