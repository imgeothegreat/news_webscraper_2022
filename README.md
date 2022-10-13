# Geo Pineda's News Webscraper for News Headlines (NBC and CNN News) Software
- Created by @imgeothegreat
- Collects news Headlines from CNN and NBC News every day. Data collected automatically converted to a CSV File.


## Version 1.0 Now WORKING! Machine learning algorithms and auto back up data on the way. 
- [x] Auto Collect News Data every 24 Hours
- [x] Save to CSV File
- [x] Search by Company, Date (Day,Month,Year,Custom), All
- [x] Save to pdf complete
- [x] Send attached pdf to recepient's email
- [x] Added Duplication Checker
- [ ] Machine learning algo
- [ ] Auto backup data

## Sample CSV File
![image](https://user-images.githubusercontent.com/27014232/194724600-d07f1d42-a93a-4c28-8d47-863ff9cd787d.png)

## Sample PDF File
![image](https://user-images.githubusercontent.com/27014232/195586411-a9439a3f-93f0-47f4-8cff-841a76cf19bf.png)

## Data Collected:
- News Headline
- News Link
- Data Published

CSV File is called data.csv]

## Required Packages for program to work:
- csv
- requests
- time
- datetime
- bs4

## NOTES
Some website links from CNN are from their own websites and they only use /style links with no HTTPS from the beginning. That is why I made a function that
automatically adds an "edition.cnn.com" text before each link for CNN news.

