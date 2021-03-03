from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re


def search_email(user_url):
    urls = deque([user_url])

    scraped_urls = set()
    emails = set()
    email_found = False
    count = 0
    try:
        while len(urls) and not email_found:
            count +=1
            if count == 100:
                break
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)

            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            print("[%d] Processing %s" % (count, url))

            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
            except Exception as e:
                continue
            #
            new_emails = set(re.findall(r"[a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+",response.text,re.I))
            emails.update(new_emails)
        
        
            soup =  BeautifulSoup(response.text , features='html.parser')

            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in urls and not link in scraped_urls:
                     if link.startswith(user_url) and not link.endswith('.pdf') and 'contact' in link.lower():
                         urls.append(link)
            for mail in new_emails:
                if(".co" in mail):
                    print(mail)
                    email_found = True

    except KeyboardInterrupt:
        print('[-] Closing')
    
    print('Emails Found')
    for mail in emails:
        print(mail)
    return emails
if __name__ == '__main__':
    user_url = str(input('[+] Enter Url: '))
    search_email(user_url)



