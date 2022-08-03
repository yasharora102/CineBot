import requests
import json
import csv

yourkey = 'YOUR_KEY_GOES_HERE'

def create_dataset(lst):
    csvheader = ['Title', "Year", 'Released', "imdbRating"]
    moviedata = []

    with open("dataset.csv", 'w', encoding='UTF8') as f:
        print("Creating dataset...")
        print("Total Items: ", len(lst))

        writer = csv.writer(f)
        writer.writerow(csvheader)
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
                writer.writerows(moviedata)
                moviedata.clear()
                print("Item: ", count+1)
                count += 1

        print("Dataset created successfully!")
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

# function call
create_dataset(get_data())
