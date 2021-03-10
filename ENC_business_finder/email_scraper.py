from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

'''
Send get emails from the websites' contact form. This is probably the most important function.

How: look for the contact form via url name ("contact" in the title), then scrape it.

params:
- user_url: Just the website url.
'''
def search_email(user_url):
    # init vars
    urls = deque([user_url])

    scraped_urls = set()
    emails = set()
    email_found = False
    count = 0
    try:
        # Look for an email on the website and every sub page while no email is found yet.
        while len(urls) and not email_found:
            # Parse the NEXT url to evaluate. Then add it to a blacklist.
            count +=1
            if count == 100:
                break
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)

            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            print("[%d] Processing %s" % (count, url))
            
            # Attempt to scrape the URL. Simulate a browser.
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
            except Exception as e:
                continue
            # Do a regular expression search for all possible emails and add all found to the list.
            new_emails = set(re.findall(r"[a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+",response.text,re.I))
            emails.update(new_emails)
        
        
            soup =  BeautifulSoup(response.text , features='html.parser')
            # Filter out the next url and add current email found to the list of found emails.
            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in urls and not link in scraped_urls:
                     if link.startswith(user_url) and not link.endswith('.pdf') and (link in user_url or 'contact' in link.lower()):
                         urls.append(link)
            for mail in new_emails:
                if(".co" in mail):
                    print(mail)
                    email_found = True

    except KeyboardInterrupt:
        print('[-] Closing')
    # display all of the emails found in the terminal, then return them to the main program.
    print('Emails Found')
    for mail in emails:
        print(mail)
    return emails
if __name__ == '__main__':
    user_url = str(input('[+] Enter Url: '))
    search_email(user_url)



