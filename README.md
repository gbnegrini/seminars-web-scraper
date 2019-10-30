# Seminars web scraper

A web scraper tool to extract information about my department's seminars from the institutional website and use it to automatically create Google Calendar events.

## Files
 - app.py: main app.
 - api.py: Google Calendar API code.
 - seminar.py: class for instantiating a Seminar object.
 - scraper.py: scraper code to get the seminars information from department's webpage.
 - requirements.txt: dependencies list.

## Usage
To locallly run the scraper simply execute:
```bash
 $ python app.py
 ```
 
This tool was also deployed to [Heroku](https://biochemistry-seminars.herokuapp.com/) as a worker process to run automatically and to display the calendar.
