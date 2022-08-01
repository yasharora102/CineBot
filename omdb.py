import requests
import argparse
import json
import csv

parser = argparse.ArgumentParser(description="Movie Watchlist")
parser.add_argument("--l", required=True, type=int,
                    help="No. of movies to add in list")
parser.add_argument("--api_key", default='YOUR_KEY_GOES_HERE',
                    type=str, help="API Key")

args = parser.parse_args()
yourkey = args.api_key
list_length = args.l
csvheader = ['Title', "Year", 'Released', "imdbRating"]
moviedata = []

with open("movie.csv", 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(csvheader)
    images_saved = 0
    for i in range(list_length):

        movie_name = input("Enter movie name\t")
        api_url = f"http://www.omdbapi.com/?apikey={yourkey}&t={movie_name}"
        request = requests.get(api_url)
        parsed_request = json.loads(request.text)

        if 'Error' in parsed_request:
            print(parsed_request['Error'])

        else:
            listing = [parsed_request["Title"], parsed_request["Year"],
                       parsed_request["Released"], parsed_request["imdbRating"]]
            moviedata.append(listing)
            movie_title = parsed_request["Title"]
            photo_url = parsed_request["Poster"]
            photo_request = requests.get(photo_url)
            photo_path = open(f"{movie_title}.png", "wb")
            photo_path.write(photo_request.content)
            photo_path.close()

    writer.writerows(moviedata)
    f.close()
