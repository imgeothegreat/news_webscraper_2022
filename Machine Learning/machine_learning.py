import csv
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense
from sklearn.metrics import accuracy_score

# json to dictionary


def half_data():
    data_file = {}
    rows = 0

    data = [json.loads(line)
            for line in open('news.json', 'r', encoding='utf8')]

    # count for the number of lines in the reader
    count_line = 0

    for line in data:
        rows += 1

    for line in data:
        count_line += 1
        rows_fourth = rows / 8

        data_file[str(line['headline'])] = {}
        data_file[str(line['headline'])]["link"] = str(line['link'])
        data_file[str(line['headline'])]["category"] = str(line['category'])
        data_file[str(line['headline'])]["short_description"] = str(line['short_description'])
        data_file[str(line['headline'])]["authors"] = str(line['authors'])
        data_file[str(line['headline'])]["date"] = str(line['date'])

        if count_line == round(rows_fourth):
            break

    with open('data.csv', 'w', newline='', encoding='utf-8') as fd:

        fieldnames = ['headline', 'link', 'category', 'short_description', 'authors', 'date']

        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()

        for headline, info in data_file.items():
            title = headline
            writer.writerow(
                {'headline': title, 'link': info['link'], 'category': info['category'],
                 'short_description': info['short_description'], 'authors': info['authors'],
                 'date': info['date']})

    fd.close()
    print("Data.csv file created successfully")


# half_data()

def train_data():

    data = pd.read_csv('data.csv')
    x = pd.get_dummies(data.drop(['category', 'headline'], axis=1))
    y = data['category'].apply(lambda x: 1 if x == 'Yes' else 0)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2)

    def menu():

        print("**MENU**")
        print("[T] for Train Data")
        print("[Q] quit")

        choice = input(">")

        if choice == 't' or choice == 'T':
            train()
        elif choice == 'q' or choice == 'Q':
            exit()

    def train():
        x_train.head()
        y_train.head()
        print("Training success")

        model = Sequential()
        model.add(Dense(units=32, activation='relu', input_dim=len(x_train.columns)))
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=1, activation='sigmoid'))

        model.compile(loss="binary_crossentropy", optimizer="sgd", metrics='accuracy')

        print("Model compile complete")

        model.fit(x_train, y_train, epochs=200, batch_size=32)

        print("Model fit complete")

        def predict():

            y_hat = model.predict(x_test)
            y_hat = [0 if val < 0.5 else 1 for val in y_hat]

            print("Accuracy Score:")
            print(accuracy_score(y_test, y_hat))
            menu_train()

        def reload():
            model = load_model('tfmodel')
            print("reload model successfully")
            menu_train()

        def save():
            model.save('tfmodel')
            print("Model save successfully")
            menu_train()

        def menu_train():
            print("**MENU**")
            print("[P] predict")
            print("[S] save")
            print("[R] reload Model")
            print("[M] main menu")

            choice = input(">")

            if choice == 'p' or choice == 'P':
                predict()
            elif choice == 'r' or choice == 'R':
                reload()
            elif choice == 's' or choice == 'S':
                save()
            elif choice == 'm' or choice == 'M':
                menu()

        menu_train()

    # calls menu choices

    menu()

# calls main function


train_data()
