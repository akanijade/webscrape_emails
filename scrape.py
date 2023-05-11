from email import header
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
# from google.colab import files

# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
# URL='https://google.com/search?q=' + sear
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT} # adding the user agent
# resp = requests.get(URL, headers=headers)
original_url = input("Enter the website url: ") 

unscraped = deque([original_url])  

scraped = set()  

emails = set()  

while len(unscraped):
    url = unscraped.popleft()  
    scraped.add(url)

    parts = urlsplit(url)
        
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
      path = url[:url.rfind('/')+1]
    else:
      path = url

    print("Crawling URL %s" % url)
    try:
        response = requests.get(url, headers=headers)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue

    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
    emails.update(new_emails) 
    print(response.text)


    soup = BeautifulSoup(response.text, 'lxml')

    for anchor in soup.find_all("a"):
      if "href" in anchor.attrs:
        link = anchor.attrs["href"]
      else:
        link = ''

        if link.startswith('/'):
            link = base_url + link
        
        elif not link.startswith('http'):
            link = path + link

        if not link.endswith(".gz"):
          if not link in unscraped and not link in scraped:
              unscraped.append(link)

df = pd.DataFrame(emails, columns=["Email"])
df.to_csv('email.csv', index=False)

# files.download("email.csv")