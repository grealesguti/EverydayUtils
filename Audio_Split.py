import argparse
import os
from pydub import AudioSegment

def split_on_silence(input_file, chunk_name, min_silence_len, min_silence_chunk_len, output_dir):
    # Open the audio file
    audio = AudioSegment.from_file(input_file, format="mp3")

    # Split the audio file at moments of silence
    chunks = audio.split_on_silence(
        # Minimum length of silence to detect
        min_silence_len=min_silence_len,
        # Minimum length of the resulting chunks of audio
        min_silence_chunk_len=min_silence_chunk_len,
    )

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the chunks to separate files
    for i, chunk in enumerate(chunks):
        chunk.export(os.path.join(output_dir, f"{chunk_name}_{i}.mp3"), format="mp3")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input MP3 file")
    parser.add_argument("chunk_name", help="Name of the output chunk files")
    parser.add_argument("--min_silence_len", type=int, default=1000, help="Minimum length of silence to detect")
    parser.add_argument("--min_silence_chunk_len", type=int, default=2000, help="Minimum length of the resulting chunks of audio")
    parser.add_argument("--output_dir", default=".", help="Output directory for the chunk files")
    return parser.parse_args()

def main():
    args = parse_args()
    split_on_silence(args.input_file, args.chunk_name, args.min_silence_len, args.min_silence_chunk_len, args.output_dir)

if __name__ == "__main__":
    main()