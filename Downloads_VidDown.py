"""
Requirements
mamba install yt-dlp
mamba install ffmpeg
"""
import argparse
import youtube_dl
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor


print('Modules loaded')

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
    parser.add_argument('--subtitles', '-s', action='store_true', help='Download subtitles (IF THERE ARE)', default=False)
    parser.add_argument('--processors', '-p', type=int, help='Number of processors (NOT WORKING)', default=1)
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

def download_playlist(playlist_url, output_dir, max_res, subtitles):
    ydl_opts = {
        'format': f'bestvideo[height<={max_res}]+bestaudio/best[height<={max_res}]',     
        'playliststart': 1,
        'playlistend': None,
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ignoreerrors': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def download_video(url, output, max_res, subtitles):
    ydl_opts = {
        'format': f'bestvideo[height<={max_res}]+bestaudio/best[height<={max_res}]',        
        'merge_output_format': 'mp4',
        'outtmpl': output,
        'max_download_rate': 1000000,        
    }
    if subtitles:
        ydl_opts['writesubtitles'] = True
        ydl_opts['allsubtitles'] = True
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            print('Entries:'+info['entries'])
            ydl.download_all(info['entries'])
        else:
            ydl.download([url])

def download_audio(url, output):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            print('Entries: '+info['entries'])
            ydl.download_all(info['entries'])
        else:
            ydl.download([url])
            
def download_audio_parallel(urls, output_files, num_processors):
    with ThreadPoolExecutor(max_workers=num_processors) as executor:
        executor.map(download_audio, urls, output_files)

        
print("MAIN START")
args = parse_args()
url = args.url
url_list = args.url_list
resolution = args.resolution
if url:
        print('URL: '+url)
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(args.url, download=False)
            title = info['title']
            print('TITLE: '+title)
        if args.output is None:
            if args.audio:
                output = f'{args.outdir}/MP3/{title}.mp3'                
            else:
                output = f'{args.outdir}/MP4/{title}.mp4'
        else:
            output = args.output
        # Download single video
        if args.audio:
            if args.playlist:
                download_playlist_mp3(url,f'{args.outdir}/MP3/')
            else:
                download_audio(url, output)
        elif args.playlist:
                        download_playlist(url, args.outdir, resolution, args.subtitles)
        else:
                        download_video(url, output, resolution, args.subtitles)
elif url_list:
        # Read list of URLs from file and download all videos
        with open(url_list, 'r') as f:
            for line in f:
                url = line.strip()
                print('URL: '+url)
                with youtube_dl.YoutubeDL() as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info['title']
                    print('TITLE: '+title)
                if args.output is None:
                    if args.audio:
                        output = f'{args.outdir}/MP3/{title}.mp3'
                    else:
                        output = f'{args.outdir}/MP4/{title}.mp4'
                if args.audio:
                            download_audio(url, output)
                elif args.playlist:
                            download_playlist(url, args.outdir, resolution, args.subtitles)
                else:
                            download_video(url, output, resolution, args.subtitles)
else:
        print('Error: No URL or URL list specified')

