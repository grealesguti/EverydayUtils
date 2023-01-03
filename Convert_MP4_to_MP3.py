import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

def extract_audio(video_file, audio_file):
    command = ['ffmpeg', '-i', video_file, '-vn', '-acodec', 'copy', audio_file]
    subprocess.run(command)

def extract_audio_parallel(video_files, audio_files, num_processors):
    with ThreadPoolExecutor(max_workers=num_processors) as executor:
        executor.map(extract_audio, video_files, audio_files)

def parse_args():
    parser = argparse.ArgumentParser(description='Extract audio from video files in parallel')
    parser.add_argument('input_files', nargs='*', help='Input video files')
    parser.add_argument('--input_dir', '-d', help='Input directory')
    parser.add_argument('output_dir', help='Output directory')
    parser.add_argument('--processors', '-p', type=int, help='Number of processors', default=1)
    args = parser.parse_args()
    
    video_files = []
    if args.input_files:
        video_files = args.input_files
    elif args.input_dir:
        for root, dirs, files in os.walk(args.input_dir):
            video_files.extend([f'{root}/{f}' for f in files if f.endswith('.mp4')])
    
    audio_files = [f.replace('.mp4', '.mp3') for f in video_files]
    audio_files = [f'{args.output_dir}/{f}' for f in audio_files]
    
    extract_audio_parallel(video_files, audio_files, args.processors)

if __name__ == '__main__':
    parse_args()
