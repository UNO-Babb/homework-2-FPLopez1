#BusSchedule.py
#Name: Francisc0
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(time):
  """
  Take a time in the format "HH:MM AM and return hour in 24-hour format"
  """
  t = datetime.datetime.strptime(time.strip(), "%I:%M %p")
  return t.hour

def getMinutes(time):
  """
  Given a string in the form "HH:MM AM/PM", return just the minutes portion.
  """
  t = datetime.datetime.strptime(time.strip(), "%I:%M %p")
  return t.minute

def getMinutes(time):
  """
  Given a string in the form "HH:MM AM/PM", return just the minutes portion.
  """
  t = datetime.datetime.strptime(time.strip(), "%I:%M %p")
  return t.minute

def parseTimes(page_text):
  """
  Extracts all times in the form HH:MM AM/PM from the webpage or test file.
  """
  pattern = r'\b(?:[1-9]|1[0-2]):[0-5][0-9]\s?(?:AM|PM)\b'
  times = re.findall(pattern, page_text)
  times = [t.strip().upper() for t in times]
  # Remove duplicates and sort by time
  times = sorted(set(times), key=lambda t: (getHours(t) * 60 + getMinutes(t)))
  return times

def minutesUntil(time, current_time):
  """
  Calculates the number of minutes from current_time (datetime) until given time (string).
  """
  now_minutes = current_time.hour * 60 + current_time.minute
  bus_minutes = getHours(time) * 60 + getMinutes(time)
  diff = bus_minutes - now_minutes
  if diff < 0:
    diff += 24 * 60  # next day
  return diff


def main():
    direction = "EAST"
    stopNumber = "2269"
    routeNumber = "11"

    url = "https://myride.ometro.com/Schedule?stopCode=" + stopNumber + "&routeNumber=" + routeNumber + "&directionName=" + direction
    #c1 = loadURL(url)  # loads the web page
    c1 = loadTestPage()  # loads the test page

    times = parseTimes(c1)

    nowUTC = datetime.datetime.utcnow()
    nowCT = nowUTC - datetime.timedelta(hours=6)
    current = nowCT.strftime("%I:%M %p")

    print("Current Time", current)

    upcoming = []
    for t in times:
        if isLater(t, current):
            upcoming.append(t)

    if len(upcoming) < 2:
        upcoming += times[:2 - len(upcoming)]

    nextBus1 = minutesUntil(upcoming[0], nowCT)
    nextBus2 = minutesUntil(upcoming[1], nowCT)

    print("The next bus will arrive in", nextBus1, "minutes.")
    print("The following bus will arrive in", nextBus2, "minutes.")


main()