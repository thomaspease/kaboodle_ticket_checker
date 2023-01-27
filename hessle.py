from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib as smtp
from email.message import EmailMessage
import time
from datetime import datetime
import threading


EMAIL_FROM = "residentadvisoralerts@gmail.com"
EMAIL_TO = ''
PASSWORD = ""
START_URL = ''
CHECK_FREQ = 60.0

class Scraper:
  def __init__(self, start_url=None,headless=True):
    options = Options()
    options.headless = headless
    self.driver = webdriver.Chrome(options = options)
    self.start_url = start_url

class Email:
  def send_email_with_url(self, url):
    msg = EmailMessage()
    msg.set_content(f'There is currently a ticket available for this event: {url}')

    msg['Subject'] = 'Ticket alert!'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    # Send the message via our own SMTP server.
    server = smtp.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_FROM, PASSWORD)
    server.send_message(msg)
    server.quit()

def check():
  threading.Timer(CHECK_FREQ, check).start()
  now = datetime.now()
  print(f'Checking. The time is now {now.strftime("%H:%M:%S")}')
  start_url = START_URL

  scraper = Scraper(start_url)
  scraper.driver.get(scraper.start_url)

  time.sleep(3)
  buttons = scraper.driver.find_elements(By.XPATH, '//*[@class="label label-danger"]')
  text = [x.text for x in buttons]

  try:
    buttonsoos = scraper.driver.find_elements(By.XPATH, '//*[@class="label label-warning"]')
  except:
    pass

  scraper.driver.quit()

  print(f'Buttons currently showing {text}')

  if text == ['Sold Out', 'Sold Out']:
    print('Passed!')
    pass
  elif buttonsoos:
    print('Out of stock!')
    pass
  else:
    buyscraper = Scraper(START_URL, headless=False)
    buyscraper.driver.get(buyscraper.start_url)
    # email = Email()
    # email.send_email_with_url(start_url)
    # print('Emailed!')

if __name__ == "__main__":
  check()