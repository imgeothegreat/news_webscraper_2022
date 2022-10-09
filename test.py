import csv
import requests
import time
#import nltk
from datetime import date
from bs4 import BeautifulSoup
from csv import DictReader

#global variables
news_list = {}
news_list['NBC'] = {}
news_list['CNN'] = {}

#DATE and TIME

today=date.today()
date_now = today.strftime("%m-%d-%y")

#auto collect news data and add to csv file
def auto_collect_news_data():

    #SECTION TEXT
    section = ["Coronavirus", "U.S. News", "Politics", "World", "Local", "Business", "Health", "Investigations"
               , "Culture Matters", "Science", 'Sports', "Tech & Media", "Decision 2022", "Video Features",
               "Photos", "Weather", "Select", "Asian America", "NBCBLK", "NBC Latino", "NBC Out"]


    print("Date: " + date_now)
    nbc_url = "https://www.nbcnews.com/world"

    nbc_html = requests.get(nbc_url)

    nbcobj = BeautifulSoup(nbc_html.content, 'lxml')

    # NBCNEWS

    title_list=[]
    link_list=[]

    for link in nbcobj.find_all('h2', {'class': 'tease-card__headline'}):
        news_list['NBC'][link.text] = link.a['href']

    for link in nbcobj.find_all('h3', {'class': 'related-content__headline'}):
        news_list['NBC'][link.text] = link.a['href']

    for link in nbcobj.find_all('div', {'class': 'wide-tease-item__info-wrapper flex-grow-1-m'}):
        text = link.text
        for words in section:
            text = text.removeprefix(words)
            if(len(link.text) != len(text)):
                break;


        title_list.append(text)
        news_list['NBC'][text] = link.a['href']


    for link in nbcobj.find_all('a',{'class':'wide-tease-item__image-wrapper flex-none relative dn dt-m'}):
        link_list.append(link.get('href'))

    for (words, links) in zip(title_list, link_list):
        news_list['NBC'][words] = links

    # CNNNEWS

    cnn_url = "https://edition.cnn.com/world"

    cnn_html = requests.get(cnn_url)

    cnnobj = BeautifulSoup(cnn_html.content, 'lxml')

    for link in cnnobj.find_all('h3', {'class': 'cd__headline'}):

        if link.a['href'][0] == "/":
            news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']
        else:

            news_list['CNN'][link.text] = link.a['href']

    for link in cnnobj.find_all('div', {'class': 'cd__wrapper'}):

        if link.a['href'][0] == "/":
            news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']
        else:

            news_list['CNN'][link.text] = link.a['href']

    print("\nData Collected Succesfully")

    # import to excel

    with open('data.csv', 'a', newline='') as fd:

        fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        for website, link in news_list.items():

            # check if data already exists still on works

            for title in link:
                writer.writerow(
                    {'News Website': website, 'News Title': title, 'Link': link[title],
                     'Date Published': date_now})

    print("Data saved to CSV File Successfully\n")

    #load csv to dictionary

    data_file= {}
    data_file['NBC'] = {}
    data_file['CNN'] = {}
    nbc_rows = 0
    cnn_rows = 0

    with open("data.csv",'r') as data:

        reader = csv.reader(data)

        for line in reader:

            top_level_key = line[0]
            nested_key = line[1]
            link = line[2]
            date_value = line[3]
            data_file[top_level_key][nested_key] = {}
            data_file[top_level_key][nested_key]["Link"] = link
            data_file[top_level_key][nested_key]["Date"] = date_value

            if top_level_key == "NBC":
                nbc_rows+=1

            if top_level_key == "CNN":
                cnn_rows+=1

    print("NBC News Only:")
    print("Number of News Found: " + str(nbc_rows) + "\n")
    for id, info in data_file.items():

        if id == "NBC":
            for key in info:
                print("News Headline: " + key)
                print("News Link: " + info[key]["Link"])
                print("Date Published: " + info[key]["Date"] + "\n")

    print("CNN News Only:")
    print("Number of News Found: " + str(cnn_rows) + "\n")

    for id, info in data_file.items():


        if id == "CNN":
            for key in info:
                print("News Headline: " + key)
                print("News Link: " + info[key]["Link"])
                print("Date Published: " + info[key]["Date"] + "\n")






#collect news data on the web
def collect_data():

    choice=''

    nbc_url = "https://www.nbcnews.com/world"

    nbc_html = requests.get(nbc_url)

    nbcobj = BeautifulSoup(nbc_html.content, 'lxml')

    # NBCNEWS

    for link in nbcobj.find_all('h2', {'class': 'tease-card__headline'}):

        news_list['NBC'][link.text] = link.a['href']

    # CNNNEWS

    cnn_url = "https://edition.cnn.com/world"

    cnn_html = requests.get(cnn_url)

    cnnobj = BeautifulSoup(cnn_html.content, 'lxml')

    for link in cnnobj.find_all('article', {'class': 'cd--large'}):

        if link.a['href'][0] == "/":
            print(link.a['href'][0])
            news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']
        else:
            print(link.a['href'])
            news_list['CNN'][link.text] = link.a['href']

    print("Data Collected Succesfully\n")

    def choices():
        print("**MENU**")
        print("Press [P] to show results")
        print("Press [S] to save in CSV File")
        print("Press [M] to go to Menu")
        choice = input('>')

        if choice == 'p' or choice == 'P':

            for website, link in news_list.items():

                print("\n*** " + website + " News***\n")

                for title in link:
                    print('Headline: ' + title)
                    print('Link: ' + link[title])
                    print('Date Published' + date_now + "\n")
            choices()

        elif choice == 'm' or choice == 'M':
            menu()

        elif choice == 's' or choice == 'S':
            # import to excel

            with open('data.csv', 'a', newline='') as fd:

                fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

                writer = csv.DictWriter(fd, fieldnames=fieldnames)

                for website, link in news_list.items():

                    # check if data already exists still on works

                    for title in link:
                        writer.writerow(
                            {'News Website': website, 'News Title': title, 'Link': link[title],
                             'Date Published': date_now})
            print("Data saved to CSV File Successfully")
            choices()

    choices()


#MENU
def menu():
    print("***MENU***\n")
    print("[C]COLLECT DATA") #option to save to excel
    print("[S]SEARCH DATA") #with filtering based on parameters
    print("[P]SAVE PDF") #saves csv file to pdf file
    print("[E]SEND TO EMAIL") #send the pdf file to inputed email
    print("[T]Terminate Program")

    choice = input('>')

    if  choice == 'C' or choice == 'c':
        collect_data()
    if choice == 't' or choice == 'T':
        print("Exiting Program")
        exit()

#menu()

#automatic collecting news data
if __name__ == '__main__':
    while True:
        auto_collect_news_data()
        time_wait = 24 #hours
        print(f'Waiting {time_wait} hours to collect data again....')
        time.sleep(time_wait * 3600)

#machine learning


#backup data


