import os
import telebot
import requests
import json
import csv

yourkey = os.getenv("yourkey")
bot_id = os.getenv("bot_id")

bot = telebot.TeleBot(bot_id)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    global file_created
    file_created = False

    bot.reply_to(
        message, 'Hello there! I am a bot that will show movie information for you and export it in a CSV file.\n\n')


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nHave a good time')
    os.remove('movie.csv')
    moviedata.clear()


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/movie MOVIE_NAME\" command to get the details of a particular movie. For eg: \"/movie The Shawshank Redemption\"\n\n2.0. You can use \"/export\" command to export all the movie data in CSV format.\n\n3.0. You can use \"/stop\" or the command \"/bye\" to stop the bot.')


moviedata = []


@bot.message_handler(func=lambda message: botRunning, commands=['movie'])
def getMovie(message):
    bot.reply_to(message, 'Getting movie info...')
    text_data = message.text
    movie_name_data = text_data.replace('/movie ', '')
    print(movie_name_data)

    lst = []
    if ',' in movie_name_data:
        lst = movie_name_data.split(',')
    else:
        lst.append(movie_name_data)
    print(lst)

    with open("movie.csv", 'w', encoding='UTF8') as f:
        file_created = True
        writer = csv.writer(f)
        csvheader = ['Title', "Year", 'Released', "imdbRating"]
        writer.writerow(csvheader)

        for i in lst:
            movie_name = str(i)
            api_url = f"http://www.omdbapi.com/?apikey={yourkey}&t={movie_name}"
            request = requests.get(api_url)
            parsed_request = json.loads(request.text)

            if 'Error' in parsed_request:
                print(parsed_request['Error'])
                reply = 'Movie not found!, Please try again'
                bot.send_message(message.chat.id, reply)

            else:
                # code for movies
                listing = [parsed_request["Title"], parsed_request["Year"],
                           parsed_request["Released"], parsed_request["imdbRating"]]
                moviedata.append(listing)

                # code for the images
                movie_title = parsed_request["Title"]
                photo_url = parsed_request["Poster"]
                photo_request = requests.get(photo_url)

                reply = "Movie found!"
                caption = "Movie Name: " + parsed_request["Title"] + "\n" + "Year: " + parsed_request["Year"] + "\n" + \
                    "Released: " + \
                    parsed_request["Released"] + "\n" + \
                    "imdbRating: " + parsed_request["imdbRating"]
                bot.send_message(message.chat.id, reply)
                bot.send_photo(message.chat.id, photo_url, caption=caption)

        writer.writerows(moviedata)


@bot.message_handler(func=lambda message: botRunning, commands=['export'])
def getList(message):
    if file_created:
        bot.reply_to(message, 'Generating file...')
        bot.reply_to(message, 'File generated!')
        bot.send_document(message.chat.id, open('movie.csv', 'rb'))
    else:
        bot.reply_to(message, 'No file to export!')


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
