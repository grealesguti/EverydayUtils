import argparse
from yt_dlp import YoutubeDL

def extract_playlist_urls(playlist_url):
    ydl_opts = {
        'playliststart': 1,
        'playlistend': None,
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=True)
        print(playlist_info.keys())
        print(playlist_info['formats'])

        playlist_items = playlist_info['entries']
        urls = [item['webpage_url'] for item in playlist_items]

    return urls

def parse_args():
    parser = argparse.ArgumentParser(description='Extract YouTube playlist URLs')
    parser.add_argument('playlist_url', help='URL of the YouTube playlist')
    parser.add_argument('--output_file', '-o', help='Output file name', default='urls.txt')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    playlist_url = args.playlist_url
    output_file = args.output_file
    urls = extract_playlist_urls(playlist_url)

    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

if __name__ == '__main__':
    main()
