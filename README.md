# news_webscraper_2022
- Created by @imgeothegreat
- Collects news Headlines from CNN and NBC News every day. Data collected automatically converted to a CSV File.


## Still have missing features but the program already works. 
- [x] Auto Collect News Data every 24 Hours
- [x] Save to CSV File
- [ ] Still missing save to pdf 
- [ ] send email, 
- [ ] machine learning algo
- [ ] auto backup data

## Sample CSV File
![image](https://user-images.githubusercontent.com/27014232/194724600-d07f1d42-a93a-4c28-8d47-863ff9cd787d.png)

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

