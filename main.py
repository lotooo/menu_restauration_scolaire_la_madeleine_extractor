#!/usr/bin/env python
import caldav
import dateparser
import os
import requests
import pdfplumber
from datetime import timedelta,datetime
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile

calendar_url = "https://%s:%s@%s" % (
    os.environ.get('WEBDAV_USER'),
    os.environ.get('WEBDAV_PASS'),
    os.environ.get('WEBDAV_URL')
)

root_page = 'https://www.ville-lamadeleine.fr/au-quotidien/enfance-ecole/restauration-scolaire'

vcal_date_format = "%Y%m%dT%H%M%S"
client = caldav.DAVClient(calendar_url)
principal = client.principal()
calendar = principal.calendar(os.environ.get('WEBDAV_CAL'))

reqs = requests.get(root_page)
soup = BeautifulSoup(reqs.text, 'html.parser')

for link in soup.find_all('a'):
    target = link.get('href')
    if not target:
      continue
    if not 'pdf' in target or 'tarif' in target or 'node' in target:
      continue
    filename = target.split('/')[-1]
    f = NamedTemporaryFile(delete=True)
    print(f"Downloading {target} to {f.name}")
    start = dateparser.parse('-'.join(filename.split('-')[0:2]))
    if start.weekday() != 0:
      start = start - timedelta(days=start.weekday())
    r = requests.get(target)
    f.write(r.content)
    pdf = pdfplumber.open(f.name)
    page = pdf.pages[0]
    menu = page.extract_table()
    week_num = 0
    for line in menu:
      if line[0] is None or 'Semaine' not in line[0]:
        continue
      week_start = start+timedelta(days=7)*week_num
      week_end = start+timedelta(days=7)*week_num + timedelta(days=4)
      print(f"Extracting menu from {week_start.date()} to {week_end.date()}")
      week_menu = { d: m for d,m in enumerate(line[1:]) }
      for d,m in enumerate(line[1:]):
        day = week_start + timedelta(days=d)
        formated_day_menu = m.replace('\n', ' - ')
        event_id = str(day.date())
        event_start = day.replace(hour=11, minute=30)
        event_end = day.replace(hour=13, minute=30)
        vcal = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:{event_id}
DTSTAMP:{datetime.now().strftime(vcal_date_format)}
DTSTART:{event_start.strftime(vcal_date_format)}
DTEND:{event_end.strftime(vcal_date_format)}
SUMMARY:Menu
DESCRIPTION:{formated_day_menu}
END:VEVENT
END:VCALENDAR
        """
        print(vcal)
        e = calendar.add_event(vcal)

      week_num += 1
    pdf.close()
