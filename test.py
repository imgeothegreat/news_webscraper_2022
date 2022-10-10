import csv
import requests
# import nltk
import datetime
import pandas as pd
import pdfkit
import os
from datetime import date
from bs4 import BeautifulSoup

# global variables
news_list = {'NBC': {}, 'CNN': {}}

# DATE and TIME

today = date.today()
date_now = today.strftime("%m-%d-%y")


# auto collect news data and add to csv file
def auto_collect_news_data():
    # SECTION TEXT
    section = ["Coronavirus", "U.S. News", "Politics", "World", "Local", "Business", "Health", "Investigations",
               "Culture Matters", "Science", 'Sports', "Tech & Media", "Decision 2022", "Video Features",
               "Photos", "Weather", "Select", "Asian America", "NBCBLK", "NBC Latino", "NBC Out"]

    print("Date: " + date_now)
    nbc_url = "https://www.nbcnews.com/world"

    nbc_html = requests.get(nbc_url)

    nbcobj = BeautifulSoup(nbc_html.content, 'lxml')

    # NBC NEWS

    title_list = []
    link_list = []

    for link in nbcobj.find_all('h2', {'class': 'tease-card__headline'}):
        news_list['NBC'][link.text] = link.a['href']

    for link in nbcobj.find_all('h3', {'class': 'related-content__headline'}):
        news_list['NBC'][link.text] = link.a['href']

    for link in nbcobj.find_all('div', {'class': 'wide-tease-item__info-wrapper flex-grow-1-m'}):
        text = link.text
        for words in section:
            text = text.removeprefix(words)
            if len(link.text) != len(text):
                break

        title_list.append(text)
        news_list['NBC'][text] = link.a['href']

    for link in nbcobj.find_all('a', {'class': 'wide-tease-item__image-wrapper flex-none relative dn dt-m'}):
        link_list.append(link.get('href'))

    for (words, links) in zip(title_list, link_list):
        news_list['NBC'][words] = links

    # CNN NEWS

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


# collect news data on the web
def collect_data():
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

            news_list['CNN'][link.text] = "https://edition.cnn.com" + link.a['href']
        else:

            news_list['CNN'][link.text] = link.a['href']

    print("Data Collected Succesfully\n")

    def choices():
        print("**MENU**")
        print("Press [P] to show results")
        print("Press [S] to save in CSV File")
        print("Press [M] to go to Menu")
        choice_collect = input('>')

        if choice_collect == 'p' or choice_collect == 'P':

            for website, link_collect in news_list.items():

                print("\n*** " + website + " News***\n")

                for title in link_collect:
                    print('Headline: ' + title)
                    print('Link: ' + link_collect[title])
                    print('Date Published' + date_now + "\n")
            choices()

        elif choice_collect == 'm' or choice_collect == 'M':
            menu()

        elif choice_collect == 's' or choice_collect == 'S':
            # import to excel

            with open('data.csv', 'a', newline='') as fd:

                fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

                writer = csv.DictWriter(fd, fieldnames=fieldnames)

                for website, link_collect in news_list.items():

                    # check if data already exists still on works

                    for title in link_collect:
                        writer.writerow(
                            {'News Website': website, 'News Title': title, 'Link': link_collect[title],
                             'Date Published': date_now})
            print("Data saved to CSV File Successfully")
            choices()

    choices()


# search news data on data.csv file
def search_data():

    def choices():
        print("**MENU**")
        print("Press [C] Search by Company")
        print("Press [D] Search by Date")
        print("Press [A] Search by All")
        print("Press [M] Go to Menu")
        choice_search = input(">")

        # load csv to dictionary

        data_file = {'NBC': {}, 'CNN': {}}
        nbc_rows = 0
        cnn_rows = 0

        with open("data.csv", 'r') as data:

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
                    nbc_rows += 1

                if top_level_key == "CNN":
                    cnn_rows += 1

        # add the total number of rows for the csv file
        total_rows = nbc_rows + cnn_rows

        print("true")
        print(choice_search)
        # choices
        if choice_search == 'c' or choice_search == 'C':

            print("Press [N] for NBC News")
            print("Press [C] for CNN News")

            news = input('>')

            if news == 'n' or news == 'N':
                print("NBC News Only:")
                print("Number of News Found: " + str(nbc_rows) + "\n")
                for id_search, info in data_file.items():

                    if id_search == "NBC":
                        for key in info:
                            print("News Headline: " + key)
                            print("News Link: " + info[key]["Link"])
                            print("Date Published: " + info[key]["Date"] + "\n")
            elif news == 'c' or news == 'C':
                print("CNN News Only:")
                print("Number of News Found: " + str(cnn_rows) + "\n")

                for id_search, info in data_file.items():

                    if id_search == "CNN":
                        for key in info:
                            print("News Headline: " + key)
                            print("News Link: " + info[key]["Link"])
                            print("Date Published: " + info[key]["Date"] + "\n")
            choices()

        elif choice_search == 'd' or choice_search == 'D':

            print("Press [D] by Day Search")
            print("Press [M] by Month Search")
            print("Press [Y] by Year Search")
            print("Press [C] by Custom Search")

            search = input('>')

            # year search
            if search == 'y' or search == 'Y':

                print("Enter Year:")
                year = input('>')
                print("[Y] Show All " + year + " news")
                print("[B]Show Before" + year + " news")
                print("[A]Show After" + year + " news")
                choice_year = input('>')

                # turns year into 2 digits
                year = year[2:]

                if choice_year == 'y' or choice_year == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][6:] == year:
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_year == 'b' or choice_year == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) < int(year):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_year == 'a' or choice_year == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) > int(year):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            # month search
            elif search == 'm' or search == 'M':

                print("Enter Month:")
                month = input('>')
                print("[Y]Show All " + month + " news")
                print("[B]Show Before " + month + " news")
                print("[A]Show After " + month + " news")
                choice_month = input('>')

                if choice_month == 'y' or choice_month == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][:2] == str(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_month == 'b' or choice_month == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) < int(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_month == 'a' or choice_month == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) > int(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            # day search

            elif search == 'd' or search == 'D':

                print("Enter Day:")
                day = input('>')

                print("[Y]Show All " + day + " news")
                print("[B]Show Before " + day + " news")
                print("[A]Show After " + day + " news")

                choice_day = input('>')

                if choice_day == 'y' or choice_day == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][3:5] == str(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_day == 'b' or choice_day == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) < int(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_day == 'a' or choice_day == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) > int(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                choices()

            # custom search
            elif search == 'c' or search == 'C':
                print("Enter Day:")
                day = input('>')
                print("Enter Month:")
                month = input('>')
                print("Enter year:")
                year = input('>')
                print("[Y]Show All " + day + " " + month + " " + year + " news")
                print("[B]Show Before " + day + " " + month + " " + year + " news")
                print("[A]Show After " + day + " " + month + " " + year + " news")
                choice_custom = input('>')

                # turns year into 2 digits
                year = year[2:]
                custom_day = str(month + "-" + day + "-" + year)

                # turns string date into datetime format
                custom_date = datetime.datetime(int(year), int(month), int(day))

                if choice_custom == 'y' or choice_custom == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"] == str(custom_day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_custom == 'b' or choice_custom == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date < custom_date:
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_custom == 'a' or choice_custom == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date > custom_date:
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            choices()

        elif choice_search == 'a' or choice_search == 'A':

            print("All News File:\n")
            print("Results Found:" + str(total_rows))

            for id_2, info in data_file.items():
                print("News Company: " + id_2 + "\n")
                for key in info:
                    print("News Headline: " + key)
                    print("News Link: " + info[key]["Link"])
                    print("Date Published: " + info[key]["Date"] + "\n")

            choices()

        elif choice_search == 'm' or choice_search == 'M':
            menu()

    choices()


# saves csv file to pdf
def pdf():
    # declarations
    data_file = {'NBC': {}, 'CNN': {}}

    # csv to dictionary
    with open("data.csv", 'r') as data:

        reader = csv.reader(data)

        for line in reader:
            top_level_key = line[0]
            nested_key = line[1]
            link = line[2]
            date_value = line[3]
            data_file[top_level_key][nested_key] = {}
            data_file[top_level_key][nested_key]["Link"] = link
            data_file[top_level_key][nested_key]["Date"] = date_value

    def choices():

        def save_to_csv(csv_save):
            with open('company_save.csv', 'a', newline='') as fd:

                fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

                writer = csv.DictWriter(fd, fieldnames=fieldnames)

                for website, link_csv in csv_save.items():
                    # check if data already exists still on works

                    for title in link_csv:
                        writer.writerow(
                            {'News Website': website, 'News Title': title, 'Link': link_csv[title],
                             'Date Published': date_now})
                print("Data saved to CSV File Successfully")
            save_to_pdf()

        def save_to_pdf():

            csv_file = pd.read_csv('company_save.csv')
            html_string = csv_file.to_html()
            # configuration
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdfkit.from_string(html_string, str(date_now) + "_file.pdf", configuration=config)
            os.remove('company_save.csv')
            print("PDF file saved.")
            choices()

        print("**MENU**")
        print("Press [C] Save by Company")
        print("Press [D] Save by Date")
        print("Press [A] Save All")
        print("Press [M] Go to Menu")
        choice_save = input(">")

        # saves csv to pdf

        company_save = {}

        # save by company
        if choice_save == 'c' or choice_save == 'C':
            print("**Company**")
            print("Press [C] CNN News")
            print("Press [N] NBC News")
            news_save = input(">")

            # CNN save
            if news_save == 'c' or news_save == 'C':
                company_save['CNN'] = {}
                # save to csv
                for id_save, info in data_file.items():

                    if id_save == "CNN":
                        for key in info:
                            company_save['CNN'][key] = {}
                            company_save['CNN'][key]["Link"] = info[key]["Link"]
                            company_save['CNN'][key]["Date"] = info[key]["Date"]

                # import to excel
                save_to_csv(company_save)

            # NBC save
            elif news_save == 'n' or news_save == 'N':
                company_save['NBC'] = {}
                # save to csv
                for id_save, info in data_file.items():

                    if id_save == "NBC":
                        for key in info:
                            company_save['NBC'][key] = {}
                            company_save['NBC'][key]["Link"] = info[key]["Link"]
                            company_save['NBC'][key]["Date"] = info[key]["Date"]

                # import to excel
                save_to_csv(company_save)

        # save by date
        elif choice_save == 'd' or choice_save == 'D':

            print("**Save by Date**")
            print("Save [D] by Day Search")
            print("Save [M] by Month Search")
            print("Save [Y] by Year Search")
            print("Save [C] by Custom Search")

            save = input('>')

            # year search
            if save == 'y' or save == 'Y':

                print("Enter Year:")
                year = input('>')
                print("[Y] Show All " + year + " news")
                print("[B]Show Before" + year + " news")
                print("[A]Show After" + year + " news")
                choice_year = input('>')

                # turns year into 2 digits
                year = year[2:]

                if choice_year == 'y' or choice_year == 'Y':
                    for id, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][6:] == year:
                                company_save = info[key]["Date"] = link.a['href']
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_year == 'b' or choice_year == 'B':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) < int(year):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_year == 'a' or choice_year == 'A':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) > int(year):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            # month search
            elif search == 'm' or search == 'M':

                choice_month = ''

                print("Enter Month:")
                month = input('>')
                print("[Y]Show All " + month + " news")
                print("[B]Show Before " + month + " news")
                print("[A]Show After " + month + " news")
                choice_month = input('>')

                if choice_month == 'y' or choice_month == 'Y':
                    for id, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][:2] == str(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_month == 'b' or choice_month == 'B':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) < int(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_month == 'a' or choice_month == 'A':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) > int(month):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            # day search

            elif search == 'd' or search == 'D':

                print("Enter Day:")
                day = input('>')

                print("[Y]Show All " + day + " news")
                print("[B]Show Before " + day + " news")
                print("[A]Show After " + day + " news")

                choice_day = input('>')

                if choice_day == 'y' or choice_day == 'Y':
                    for id, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][3:5] == str(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_day == 'b' or choice_day == 'B':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) < int(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_day == 'a' or choice_day == 'A':
                    for id, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) > int(day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                choices()

            # custom search
            elif search == 'c' or search == 'C':
                print("Enter Day:")
                day = input('>')
                print("Enter Month:")
                month = input('>')
                print("Enter year:")
                year = input('>')
                print("[Y]Show All " + day + " " + month + " " + year + " news")
                print("[B]Show Before " + day + " " + month + " " + year + " news")
                print("[A]Show After " + day + " " + month + " " + year + " news")
                choice_custom = input('>')

                # turns year into 2 digits
                year = year[2:]
                custom_day = str(month + "-" + day + "-" + year)

                # turns string date into datetime format
                custom_date = datetime.datetime(int(year), int(month), int(day))

                if choice_custom == 'y' or choice_custom == 'Y':
                    for id, info in data_file.items():

                        for key in info:
                            if info[key]["Date"] == str(custom_day):
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

                elif choice_custom == 'b' or choice_custom == 'B':
                    for id, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date < custom_date:
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")
                elif choice_custom == 'a' or choice_custom == 'A':
                    for id, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date > custom_date:
                                print("News Headline: " + key)
                                print("News Link: " + info[key]["Link"])
                                print("Date Published: " + info[key]["Date"] + "\n")

            choices()

    choices()


# MENU
def menu():
    print("***MENU***\n")
    print("[C]COLLECT DATA")  # option to save to excel
    print("[S]SEARCH DATA")  # with filtering based on parameters
    print("[P]SAVE PDF")  # saves csv file to pdf file
    print("[E]SEND TO EMAIL")  # send the pdf file to inputed email
    print("[T]Terminate Program")

    choice = input('>')

    if choice == 'C' or choice == 'c':
        collect_data()
    elif choice == 'S' or choice == 's':
        search_data()
    elif choice == 'p' or choice == 'P':
        pdf()
    elif choice == 't' or choice == 'T':
        print("Exiting Program")
        exit()


menu()

# automatic collecting news data
# if __name__ == '__main__':
# while True:
# auto_collect_news_data()
# time_wait = 24 #hours
# print(f'Waiting {time_wait} hours to collect data again....')
# time.sleep(time_wait * 3600)

# machine learning


# backup data
