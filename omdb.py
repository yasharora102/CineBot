import requests
# import argparse
import json
import csv

# we can add these filters but I thought they will increase the workload as they don't have a purpose here.

# parser = argparse.ArgumentParser(description="Movie Watchlist")
# parser.add_argument("--l", required=True, type=int,
#                     help="No. of movies to add in list")
# parser.add_argument("--api_key", default='',
#                     type=str, help="API Key")
# args = parser.parse_args()
# yourkey = args.api_key
# list_length = args.l

yourkey = 'Your_Key_Goes_Here'
def create_dataset(lst):
    csvheader = ['Title', "Year", 'Released', "imdbRating"]
    moviedata = []

    with open("dataset.csv", 'w', encoding='UTF8') as f:
        print("Creating dataset...")
        print("Total Items: ", len(lst))
        
        writer = csv.writer(f)
        writer.writerow(csvheader)
        images_saved = 0
        count = 0       
        for movie_name in lst:
            
            api_url = f"http://www.omdbapi.com/?apikey={yourkey}&t={movie_name}"
            request = requests.get(api_url)
            parsed_request = json.loads(request.text)

            if 'Error' in parsed_request:
                print(parsed_request['Error'])

            else:
                # code for making a list of movies
                listing = [parsed_request["Title"], parsed_request["Year"],
                           parsed_request["Released"], parsed_request["imdbRating"]]
                moviedata.append(listing)
                print("Item: ", count+1)
                count += 1
            #since we are not saving the images, we can comment this out. 
            # code for saving the images

                # movie_title = parsed_request["Title"]
                # photo_url = parsed_request["Poster"]
                # photo_request = requests.get(photo_url)
                # photo_path = open(f"{movie_title}.png", "wb")
                # photo_path.write(photo_request.content)
                # photo_path.close()
        print("Dataset created successfully!")        
        writer.writerows(moviedata)
        f.close()

# function for extracting the data from the txt file
def get_data():
    lst = []
    with open("data.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            lst.append(line)
    return lst

create_dataset(get_data())
