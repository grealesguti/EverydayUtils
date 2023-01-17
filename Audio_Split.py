import argparse
import os
from pydub import AudioSegment

# TO USE
# python Audio_Split.py -i ToSplit/MushokuVol7.mp3 -cn MushokuVol7

def test_mp3_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    if not file_path.endswith('.mp3'):
        print(f"Error: File {file_path} is not an MP3 file.")
        return False
    print("MP3 file EXISTS.")
    return True

def split_on_silence(input_file, chunk_name, min_silence_len, min_silence_chunk_len, output_dir):
    # Open the audio file
    print("Opening the file.")
    audio = AudioSegment.from_file(input_file, format="mp3")
    print("Opened file.")

    # Split the audio file into chunks based on silence
    chunks = pydub.silence.split_on_silence(audio, min_silence_len=500, silence_thresh=-16)

    # Initialize a list to store the final chunks
    final_chunks = []

    # Iterate over the chunks and merge any that are shorter than the minimum chunk length
    chunk_start = 0
    while chunk_start < len(chunks):
        # Initialize a new chunk
        merged_chunk = pydub.AudioSegment.empty()

        # Merge chunks until the minimum chunk length is reached
        while (len(merged_chunk) < min_chunk_length * 1000) and (chunk_start < len(chunks)):
            merged_chunk += chunks[chunk_start]
            chunk_start += 1

        # Add the merged chunk to the list of final chunks
        final_chunks.append(merged_chunk)
            
    # Save the chunks to separate files
    for i, chunk in enumerate(final_chunks):
        chunk.export(os.path.join(output_dir, f"{chunk_name}_{i}.mp3"), format="mp3")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_file",'-i', help="Input MP3 file")
    parser.add_argument("-chunk_name",'-cn', help="Name of the output chunk files")
    parser.add_argument("--min_silence_len",'-msl', type=int, default=1000, help="Minimum length of silence to detect")
    parser.add_argument("--min_silence_chunk_len",'-mscl', type=int, default=20*1000*60, help="Minimum length of the resulting chunks of audio")
    parser.add_argument("--output_dir", default="AudioChunks/", help="Output directory for the chunk files")
    return parser.parse_args()

def main():
    args = parse_args()
    print("Parsed Arguments.")
    test_mp3_file(args.input_file)
    split_on_silence(args.input_file, args.chunk_name, args.min_silence_len, args.min_silence_chunk_len, args.output_dir)

if __name__ == "__main__":
    main()
    print("END.")
