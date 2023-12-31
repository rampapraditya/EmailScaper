from cgitb import reset
from collections import  deque
import re

from bs4 import BeautifulSoup
import requests
import urllib.parse

user_url = str(input('[+] Masukkan url : '))
limit = int(input('[+] Limit : '))

urls = deque([user_url])

print(urls)

scraped_urls = set()
emails = set()
count = 0

try:

    while True:
        count += 1
        if count > limit:
            break

        if urls :
            url = urls.popleft()
            scraped_urls.add(url)
            parts = urllib.parse.urlsplit(url)
            base_url = f'{parts.scheme}://{parts.netloc}'
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            print(f'{count} memproses {url}')

            try:
                response = requests.get(url)

                new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[A-Z\.]+', response.text, re.I))
                emails.update(new_emails)
    
                soup = BeautifulSoup(response.text, 'html.parser')
                for anchor in soup.find_all('a'):
                    link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = path + link
    
                    if not link in urls and not link in scraped_urls:
                        urls.append(link)
                    
            except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                pass

           

        else:
            print("Empty deque");



except KeyboardInterrupt:
    print('[-] Closing!')

print('\n Proses selesai')
print(f'{len(emails)} email ditemukan \n')
for mail in emails:
    print(' ' + mail)
print('\n')
