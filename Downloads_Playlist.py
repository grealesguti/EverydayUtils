from yt_dlp import YoutubeDL
import argparse

def parse_args():
    print('Argument Parser!')
    parser = argparse.ArgumentParser(description='Download YouTube video or audio') 
    parser.add_argument('-url', nargs='?', help='URL of the YouTube video')
    parser.add_argument('--url-list', '-l', help='Text file with list of URLs')
    parser.add_argument('--output', '-o', help='Output file name (default: <title>.mp4)')
    parser.add_argument('--audio', '-a', action='store_true', help='Download audio only', default=False)    
    parser.add_argument('--playlist', '-pl', action='store_true', help='Download full playlist', default=False)    
    parser.add_argument('--resolution', '-r', type=int, help='Maximum video resolution in pixels', default=360)
    parser.add_argument('--outdir', '-od', help='Output directory', default='Downloads')
    parser.add_argument('--subtitles', '-s', action='store_true', help='Download subtitles', default=False)
    parser.add_argument('--processors', '-p', type=int, help='Number of processors', default=1)
    return parser.parse_args()

def download_playlist_mp3(playlist_url, output_dir):
    ydl_opts = {
        'playliststart': 1,
        'playlistend': None,
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def main():
    args = parse_args()
    playlist_url = args.url
    output_dir = 'Downloads/MP3/'
    download_playlist_mp3(playlist_url, output_dir)

if __name__ == '__main__':
    main()
