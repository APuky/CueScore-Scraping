# CueScoreScraping

//WORK IN PROGRESS --> AN ALTERNATIVE TO WHATSAPP

//BEAUTIFULSOUP4 and SELENIUM are required

CueScore scraper using Python requests, BeautifulSoup4 and Selenium

The purpose of this repo is to learn basics of web scraping and Selenium on a real life example.

It is meant to be used for Ironman pool matches, which can take up to 6 hours with a race to 30 frames.
Since CueScore only shows the end result after the match is over, I figured it would be nice to see some more data without having to watch the matches in entirety.

This code fetches data from CueScore every 20 seconds and sends messages over WhatsApp if certain conditions are met.
In a race to 30 frames, it's nice to see how many lead changes can occur (if any), and track both the longest streaks and largest leads for both players.

Unfortunately, WhatsApp sometimes send messages that cannot be read, so the data is also printed to the console.
