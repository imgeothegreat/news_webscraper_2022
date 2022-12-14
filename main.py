import csv
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
import datetime
import pdfkit
from datetime import date
from bs4 import BeautifulSoup
import smtplib
import os
# import time  # this turns grey when I disable the auto collect
import calendar
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

# gui
loading = "Loading Application...."
title_application = "Geo Pineda's Web Scraper Software"

# global variables
news_list = {'NBC': {}, 'CNN': {}}
# for duplicate checker
news_list_final = {'NBC': {}, 'CNN': {}}

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

    print("\nData Collected Successfully")

    # check if csv exists
    exist = 0
    news_list_final = {'NBC': {}, 'CNN': {}}

    if os.path.exists('data.csv'):
        exist = 1
        with open('data.csv', 'r') as data_check:
            # check if news already exist in data.csv
            for website, link_check in news_list.items():

                for title in link_check:

                    reader = csv.reader(data_check)

                    # goes back to the first row again
                    data_check.seek(0)

                    # counter to check if news title already exist in the csv file
                    found = 0
                    for line in reader:

                        if title == line[1]:
                            found = 1
                            break

                    if found != 1:
                        news_list_final[website][title] = news_list[website][title]

        data_check.close()

    # import to excel

    with open('data.csv', 'a', newline='') as fd:

        fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

        writer = csv.DictWriter(fd, fieldnames=fieldnames)

        if exist == 0:

            for website, link_collect in news_list.items():

                # check if data already exists still on works

                for title in link_collect:
                    writer.writerow(
                        {'News Website': website, 'News Title': title, 'Link': link_collect[title],
                         'Date Published': date_now})
        elif exist == 1:

            for website, link_collect in news_list_final.items():

                # check if data already exists still on works

                for title in link_collect:
                    writer.writerow(
                        {'News Website': website, 'News Title': title, 'Link': link_collect[title],
                         'Date Published': date_now})
    fd.close()

    print("Data saved to CSV File Successfully")

    # save to pdf automatically
    # declarations
    data_file = {'NBC': {}, 'CNN': {}}
    company_save = {}

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

    for id_all, info_all in data_file.items():
        company_save['NBC'] = {}
        company_save['CNN'] = {}
        for key_all in info_all:
            company_save[id_all][key_all] = {}
            company_save[id_all][key_all]["Link"] = info_all[key_all]["Link"]
            company_save[id_all][key_all]["Date"] = info_all[key_all]["Date"]

    # import to excel
    with open('company_save.csv', 'a', newline='') as fd:

        fieldnames = ['News Website', 'News Title', 'Link', 'Date Published']

        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        for website, link_csv in company_save.items():
            # check if data already exists still on works

            for title in link_csv:
                writer.writerow(
                    {'News Website': website, 'News Title': title, 'Link': link_csv[title]["Link"],
                     'Date Published': date_now})
    fd.close()

    # save to pdf
    csv_file = pd.read_csv('company_save.csv')
    html_string = csv_file.to_html()
    # configuration
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(html_string, str(date_now) + "_file.pdf", configuration=config)
    os.remove('company_save.csv')
    print("PDF file saved.")

    # send email

    # port and password for SMTP server
    password = 'fgfdfwqkztjdudtx'
    to_address = 'geodominic.pineda@gmail.com'

    # message details
    from_address = "geothemiracle@gmail.com"
    subject = "Sending you News PDF File"
    content = "Attach to this email is the attached News PDF File from python code"
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    # opens pdf file
    filename = str(date_now) + "_file.pdf"
    with open(filename, 'r', errors="ignore") as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # enable security
    server.login(from_address, password)
    server.sendmail(from_address, to_address, msg.as_string())
    print("Email with attached pdf is successfully sent to " + to_address)
    server.quit()


# collect news data on the web
def collect_data():
    # SECTION TEXT
    section = ["Coronavirus", "U.S. News", "Politics", "World", "Local", "Business", "Health", "Investigations",
               "Culture Matters", "Science", 'Sports', "Tech & Media", "Decision 2022", "Video Features",
               "Photos", "Weather", "Select", "Asian America", "NBCBLK", "NBC Latino", "NBC Out"]

    nbc_url = "https://www.nbcnews.com/world"

    nbc_html = requests.get(nbc_url)

    nbcobj = BeautifulSoup(nbc_html.content, 'lxml')

    # NBC_NEWS

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

    # CNN_NEWS

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

    print("Data Collected Successfully\n")

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

            # check if csv exists
            exist = 0
            news_list_final = {'NBC': {}, 'CNN': {}}
            news_id = 0

            if os.path.exists('data.csv'):
                exist = 1
                with open('data.csv', 'r') as data_check:
                    # check if news already exist in data.csv

                    reader = csv.reader(data_check)

                    # counts news id
                    for line in reader:
                        news_id += 1
                    news_id -= 1
                    for website, link_check in news_list.items():

                        for title in link_check:

                            # goes back to the first row again
                            data_check.seek(0)

                            # counter to check if news title already exist in the csv file
                            found = 0

                            # goes back to the first row again
                            data_check.seek(0)

                            for line in reader:
                                if title == line[2]:
                                    found = 1
                                    break

                            if found != 1:
                                news_list_final[website][title] = news_list[website][title]

                data_check.close()

            # import to excel

            with open('data.csv', 'a', newline='') as fd:

                fieldnames = ['News ID', 'Website', 'News Title', 'Link', 'Date Published']

                writer = csv.DictWriter(fd, fieldnames=fieldnames)

                if exist == 0:
                    writer.writeheader()

                    for website, link_collect in news_list.items():

                        # check if data already exists still on works

                        for title in link_collect:
                            # adds 1 counter for the news id
                            news_id += 1

                            writer.writerow(
                                {'Website': website, 'News ID': news_id, 'News Title': title,
                                 'Link': link_collect[title],
                                 'Date Published': date_now})

                elif exist == 1:

                    for website, link_collect in news_list_final.items():

                        # check if data already exists still on works

                        for title in link_collect:
                            # adds 1 counter for the news id
                            news_id += 1
                            writer.writerow(
                                {'Website': website, 'News ID': news_id, 'News Title': title,
                                 'Link': link_collect[title],
                                 'Date Published': date_now})

            fd.close()
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
            next(reader)

            for line in reader:
                news_id = line[0]  # id
                top_level_key = line[1]  # website
                nested_key = line[2]  # news headline
                link = line[3]  # link
                date_value = line[4]  # date
                data_file[top_level_key][nested_key] = {}
                data_file[top_level_key][nested_key]["News ID"] = news_id
                data_file[top_level_key][nested_key]["Link"] = link
                data_file[top_level_key][nested_key]["Date"] = date_value

                if top_level_key == "NBC":
                    nbc_rows += 1

                if top_level_key == "CNN":
                    cnn_rows += 1

        data.close()
        # add the total number of rows for the csv file
        total_rows = nbc_rows + cnn_rows

        def print_news(info_news, key_news):
            print("News ID: " + info_news[key_news]["News ID"])
            print("News Headline: " + key_news)
            print("News Link: " + info_news[key_news]["Link"])
            print("Date Published: " + info_news[key_news]["Date"] + "\n")

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
                            print_news(info, key)
            elif news == 'c' or news == 'C':
                print("CNN News Only:")
                print("Number of News Found: " + str(cnn_rows) + "\n")

                for id_search, info in data_file.items():

                    if id_search == "CNN":
                        for key in info:
                            print_news(info, key)
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
                                print_news(info, key)

                elif choice_year == 'b' or choice_year == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) < int(year):
                                print_news(info, key)
                elif choice_year == 'a' or choice_year == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) > int(year):
                                print_news(info, key)

            # month search
            elif search == 'm' or search == 'M':

                print("Enter Month:")
                month = input('>')

                # loop for month digit to month word
                month_word = calendar.month_name[int(month)]

                print("[Y]Show All " + month_word + " news")
                print("[B]Show Before " + month_word + " news")
                print("[A]Show After " + month_word + " news")
                choice_month = input('>')

                if choice_month == 'y' or choice_month == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][:2] == str(month):
                                print_news(info, key)

                elif choice_month == 'b' or choice_month == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) < int(month):
                                print_news(info, key)
                elif choice_month == 'a' or choice_month == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) > int(month):
                                print_news(info, key)

            # day search

            elif search == 'd' or search == 'D':

                print("Enter Day:")
                day = input('>')

                print("[Y]Show All " + day + " day news")
                print("[B]Show Before " + day + " day news")
                print("[A]Show After " + day + " day news")

                choice_day = input('>')

                if choice_day == 'y' or choice_day == 'Y':
                    for id_search, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][3:5] == str(day):
                                print_news(info, key)

                elif choice_day == 'b' or choice_day == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) < int(day):
                                print_news(info, key)
                elif choice_day == 'a' or choice_day == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) > int(day):
                                print_news(info, key)

                choices()

            # custom search
            elif search == 'c' or search == 'C':
                print("Enter Day:")
                day = input('>')
                print("Enter Month:")
                month = input('>')
                print("Enter year:")
                year = input('>')
                print("[Y]Show All " + month + " " + day + " " + year + " news")
                print("[B]Show Before " + month + " " + day + " " + year + " news")
                print("[A]Show After " + month + " " + day + " " + year + " news")
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
                                print_news(info, key)

                elif choice_custom == 'b' or choice_custom == 'B':
                    for id_search, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date < custom_date:
                                print_news(info, key)
                elif choice_custom == 'a' or choice_custom == 'A':
                    for id_search, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date > custom_date:
                                print_news(info, key)

            choices()

        elif choice_search == 'a' or choice_search == 'A':

            print("All News File:\n")
            print("Results Found:" + str(total_rows))

            for id_2, info in data_file.items():
                print("News Company: " + id_2 + "\n")
                for key in info:
                    print_news(info, key)

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
            news_id = line[0]  # id
            top_level_key = line[1]  # website
            nested_key = line[2]  # news headline
            link = line[3]  # link
            date_value = line[4]  # date
            data_file[top_level_key][nested_key] = {}
            data_file[top_level_key][nested_key]["News ID"] = news_id
            data_file[top_level_key][nested_key]["Link"] = link
            data_file[top_level_key][nested_key]["Date"] = date_value

    data.close()

    def choices():

        def save_to_csv(csv_save, type_file):
            with open('company_save.csv', 'a', newline='') as fd:

                fieldnames = ['News ID', 'News Website', 'News Title', 'Link', 'Date Published']

                writer = csv.DictWriter(fd, fieldnames=fieldnames)
                writer.writeheader()
                for website, link_csv in csv_save.items():
                    # check if data already exists still on works

                    for title in link_csv:
                        writer.writerow(
                            {'News ID': link_csv[title]["News ID"], 'News Website': website, 'News Title': title,
                             'Link': link_csv[title]["Link"],
                             'Date Published': date_now})

                print("Data saved to CSV File Successfully")
            fd.close()
            save_to_pdf(type_file)

        def save_to_pdf(type_file):

            csv_file = pd.read_csv('company_save.csv')
            html_string = csv_file.to_html()
            # configuration
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

            # renames file based on type of file being saved
            filename = ""

            if type_file == "cnn":
                filename = "CNN News File_" + str(date_now) + "_file.pdf"
                pdfkit.from_string(html_string, filename, configuration=config)
            elif type_file == "nbc":
                filename = "NBC News File_" + str(date_now) + "_file.pdf"
                pdfkit.from_string(html_string, filename, configuration=config)
            elif type_file == "date":
                filename = "Date File_" + str(date_now) + "_file.pdf"
                pdfkit.from_string(html_string, filename, configuration=config)
            elif type_file == "all":
                filename = "All News Data_" + str(date_now) + "_file.pdf"
                pdfkit.from_string(html_string, filename, configuration=config)

            os.remove('company_save.csv')
            print(filename + " file saved successfully.")
            choices()

        def save_all():
            for id_all, info_all in data_file.items():
                company_save['NBC'] = {}
                company_save['CNN'] = {}
                for key_all in info_all:
                    company_save[id_all][key_all] = {}
                    company_save[id_all][key_all]["News ID"] = info_all[key_all]["News ID"]
                    company_save[id_all][key_all]["Link"] = info_all[key_all]["Link"]
                    company_save[id_all][key_all]["Date"] = info_all[key_all]["Date"]
            # import to excel
            save_to_csv(company_save, "all")
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

            def save_company(save_info, save_key):
                company_save['CNN'][save_key] = {}
                company_save['CNN'][save_key]["News ID"] = save_info[save_key]["News ID"]
                company_save['CNN'][save_key]["Link"] = save_info[save_key]["Link"]
                company_save['CNN'][save_key]["Date"] = save_info[save_key]["Date"]

            # CNN save
            if news_save == 'c' or news_save == 'C':
                company_save['CNN'] = {}
                # save to csv
                for id_save, info in data_file.items():

                    if id_save == "CNN":
                        for key in info:
                            save_company(info, key)

                # import to excel
                save_to_csv(company_save, "cnn")

            # NBC save
            elif news_save == 'n' or news_save == 'N':
                company_save['NBC'] = {}
                # save to csv
                for id_save, info in data_file.items():

                    if id_save == "NBC":
                        for key in info:
                            save_company(info, key)

                # import to excel
                save_to_csv(company_save, "nbc")

            choices()

        # save by date
        elif choice_save == 'd' or choice_save == 'D':

            print("**Save by Date**")
            print("Save [D] by Day Search")
            print("Save [M] by Month Search")
            print("Save [Y] by Year Search")
            print("Save [C] by Custom Search")

            save = input('>')

            def save_date(date_info, date_key):
                company_save[id_date][date_key] = {}
                company_save['CNN'][date_key]["News ID"] = date_info[date_key]["News ID"]
                company_save[id_date][date_key]["Link"] = date_info[date_key]["Link"]
                company_save[id_date][date_key]["Date"] = date_info[date_key]["Date"]

            # year search
            if save == 'y' or save == 'Y':

                print("Enter Year:")
                year = input('>')
                print("[Y]Show All " + year + " news")
                print("[B]Show Before" + year + " news")
                print("[A]Show After" + year + " news")
                save_year = input('>')

                # turns year into 2 digits
                year = year[2:]

                if save_year == 'y' or save_year == 'Y':
                    for id_date, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][6:] == str(year):
                                save_date(info, key)

                    # import to excel
                    save_to_csv(company_save, "date")

                elif save_year == 'b' or save_year == 'B':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) < int(year):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")
                elif save_year == 'a' or save_year == 'A':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][6:]) > int(year):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

            # month search
            elif save == 'm' or save == 'M':

                print("Enter Month:")
                month = input('>')
                print("[Y]Show All " + month + " news")
                print("[B]Show Before " + month + " news")
                print("[A]Show After " + month + " news")
                choice_month = input('>')

                if choice_month == 'y' or choice_month == 'Y':
                    for id_date, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][:2] == str(month):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

                elif choice_month == 'b' or choice_month == 'B':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) < int(month):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")
                elif choice_month == 'a' or choice_month == 'A':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][:2]) > int(month):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

            # day search

            elif save == 'd' or save == 'D':

                print("Enter Day:")
                day = input('>')

                print("[Y]Show All " + day + " news")
                print("[B]Show Before " + day + " news")
                print("[A]Show After " + day + " news")

                choice_day = input('>')

                if choice_day == 'y' or choice_day == 'Y':
                    for id_date, info in data_file.items():

                        for key in info:
                            if info[key]["Date"][3:5] == str(day):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

                elif choice_day == 'b' or choice_day == 'B':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) < int(day):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")
                elif choice_day == 'a' or choice_day == 'A':
                    for id_date, info in data_file.items():

                        for key in info:
                            if int(info[key]["Date"][3:5]) > int(day):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

                choices()

            # custom search
            elif save == 'c' or save == 'C':
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
                    for id_date, info in data_file.items():

                        for key in info:
                            if info[key]["Date"] == str(custom_day):
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

                elif choice_custom == 'b' or choice_custom == 'B':
                    for id_date, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date < custom_date:
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")
                elif choice_custom == 'a' or choice_custom == 'A':
                    for id_date, info in data_file.items():

                        for key in info:
                            year = info[key]["Date"][6:]
                            month = info[key]["Date"][:2]
                            day = info[key]["Date"][3:5]
                            news_date = datetime.datetime(2000 + int(year), int(month), int(day))
                            if news_date > custom_date:
                                save_date(info, key)
                    # import to excel
                    save_to_csv(company_save, "date")

            choices()

        # save by all
        elif choice_save == 'a' or choice_save == 'A':
            save_all()

        # go to menu
        elif choice_save == 'm' or choice_save == 'M':
            menu()

    choices()


# Send_To_Email
def send_email():
    print("Enter receiver email address")
    to_address = input('>')

    # port and password for SMTP server
    password = 'fgfdfwqkztjdudtx'

    # message details
    from_address = "geothemiracle@gmail.com"
    subject = "Sending you News PDF File"
    content = "Attach to this email is the attached News PDF File from python code"
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    # opens pdf file
    filename = str(date_now) + "_file.pdf"
    with open(filename, 'r', errors="ignore") as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # enable security
    server.login(from_address, password)
    server.sendmail(from_address, to_address, msg.as_string())
    print("Email with attached pdf is successfully sent to " + to_address)
    server.quit()
    f.close()

    # menu()

# machine learning

# gcloud backup data


def backup():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    # get file list for overwrite
    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format('1igD-KW2bSIXTbMyPOJzLMQnt--GPin6K')}).GetList()

    upload_file_list = ['data.csv', 'main.py']

    for upload_file in upload_file_list:

        gfile = drive.CreateFile({'parents': [{'id': '1igD-KW2bSIXTbMyPOJzLMQnt--GPin6K'}]})
        # Read file and set it as the content of this instance.
        for file in file_list:
            if file["title"] == upload_file:
                file.Delete()
                gfile.SetContentFile(upload_file)
                gfile.Upload()  # Upload the file.
            else:
                gfile.SetContentFile(upload_file)
                gfile.Upload()  # Upload the file.

    print("Files Uploaded to Gdrive Folder Successfully\n")

    # If Files doesnt exist
    menu()


# sql

# MENU


def menu():
    choice_list = ['C', 'c', 's', 'S', 'e', 'E', 't', 'T']

    print("Geo Pineda's Web Scraper Software for News Headlines (NBC and CNN News)")
    print("***MENU***\n")
    print("[C]COLLECT DATA")  # option to save to excel
    print("[S]SEARCH DATA")  # with filtering based on parameters
    print("[P]SAVE PDF")  # saves csv file to pdf file
    print("[E]SEND TO EMAIL")  # send the pdf file to inputted email
    print("[B]BACK UP FILES")
    print("[T]Terminate Program")

    choice = input('>')

    if choice == 'C' or choice == 'c':
        collect_data()
    elif choice == 'S' or choice == 's':
        search_data()
    elif choice == 'p' or choice == 'P':
        pdf()
    elif choice == 'e' or choice == 'E':
        send_email()
    elif choice == 'b' or choice == 'B':
        backup()
    elif choice == 't' or choice == 'T':
        print("Exiting Program")
        exit()

    for letter in choice_list:
        if choice != letter:
            print("Wrong input, please enter again.")
            menu()


menu()

# automatic collecting news data
"""
if __name__ == '__main__':
    while True:
        auto_collect_news_data()
        time_wait = 24  # hours
        print(f'Waiting {time_wait} hours to collect data again....')
        time.sleep(time_wait * 3600)
"""
