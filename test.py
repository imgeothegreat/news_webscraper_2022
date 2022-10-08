import csv
import requests
import time
#import nltk
from datetime import date
from bs4 import BeautifulSoup

#global variables
news_list = {}
news_list['NBC'] = {}
news_list['CNN'] = {}

#DATE and TIME

today=date.today()
date_now = today.strftime("%m-%d-%y")

#auto collect news data and add to csv file
def auto_collect_news_data():

    print("Date: " + date_now)
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
        news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']

    print("\nData Collected Succesfully")

    # import to excel

    with open('data.csv', 'a', newline='') as fd:

        fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        for website, link in news_list.items():

            # check if data already exists still on works

            for title in link:
                writer.writerow(
                    {'News Website': website, 'News Title': title, 'Link': link[title],
                     'Date Published': date_now})

    print("Data saved to CSV File Successfully\n")


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

        news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']

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
                writer.writeheader()
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


