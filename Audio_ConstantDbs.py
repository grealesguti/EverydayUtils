import pydub

def equalize_mp3(input_file, target_dBFS):
    # Load the MP3 file
    audio = pydub.AudioSegment.from_mp3(input_file)

    # Calculate the change in volume required to reach the target
    change_in_dBFS = target_dBFS - audio.dBFS

    # Boost the volume by the required amount
    equalized_audio = audio + change_in_dBFS

    return equalized_audio
