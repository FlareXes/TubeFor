from platform import system as system_os
import argparse
from os import system, environ
from googleapiclient.discovery import build


class Youtube:
    def __init__(self, query, count):
        self.query = query
        self.api_key = environ.get("YOUTUBE_API")
        self.response: dict
        self.count = count

    def search(self) -> None:
        service = build('youtube', 'v3', developerKey=self.api_key)
        request = service.search().list(q=self.query, part="snippet",
                                        maxResults=self.count, type="video")
        response = request.execute()
        self.response = response
        service.close()

    def print_response(self) -> None:
        print("\nTotal Requested Result: ", self.count)
        print("Total Response Results: ", len(self.response["items"]))
        print("\n-------------------------------------------------\n")

        for stats in self.response["items"]:
            video_id = stats["id"]["videoId"]
            video_url = f"https://youtube.com/watch?v={video_id}"
            title = stats["snippet"]["title"]
            thumbnail = stats["snippet"]["thumbnails"]["high"]["url"]
            channel = stats["snippet"]["channelTitle"]
            print(title)
            print(video_url)
            print(thumbnail)
            print(channel)
            print("\n-------------------------------------------------\n")


if __name__ == "__main__":
    argp = argparse.ArgumentParser(
        usage="youfor.py -q QUERY -c [COUNT] -o [OUTPUT]")
    argp.add_argument("-q", "--query", required=True)
    argp.add_argument("-c", "--count", default=10)

    parser = argp.parse_args()
    query = parser.query
    count = parser.count

    if system_os() == 'Linux':
        system('clear')
    elif system_os() == 'Windows':
        system('cls')

    youtube = Youtube(query=query, count=count)
    youtube.search()
    youtube.print_response()
