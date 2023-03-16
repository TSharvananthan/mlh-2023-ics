from bs4 import BeautifulSoup
from ics import Calendar, Event
from requests import get

calendar = Calendar()

url = "https://mlh.io/seasons/2023/events"
soup = BeautifulSoup(get(url).content, "lxml")
events = soup.find_all("div", {"class": "event"})

for event in events:
    name = event \
        .find("a", {"class": "event-link"})["title"]
    
    begin = event \
        .find("meta", {"itemprop": "startDate"})["content"]
    
    end = event \
        .find("meta", {"itemprop": "endDate"})["content"]
    
    location = event \
        .find("div", {"class": "event-location"}) \
        .get_text() \
        .strip() \
        .replace("\n          ", " ")
    
    url = event \
        .find("a", {"class": "event-link"})["href"]
    
    event = Event(name=name, begin=begin, end=end, location=location, url=url)
    calendar.events.add(event)

with open(f'hackathons.ics', 'w') as f:
    f.writelines(calendar.serialize_iter())