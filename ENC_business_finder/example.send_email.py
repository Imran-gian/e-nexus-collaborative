import smtplib, ssl
from email.message import EmailMessage


def send_email(EMAILs,BNAME,COUNTRY):
    
    for EMAIL in EMAILs:
        try:
            print("EMAIL:::", EMAIL)
            if(EMAIL in "email"):
                continue
            smtpserver = smtplib.SMTP("smtp.mail.yahoo.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            SENDER = 'bluefishgeneral@yahoo.com'
            smtpserver.login(SENDER, 'EXAMPLE_YAHOO_MAIL_APP_PASS')
    
            msg = EmailMessage()
            msg.set_content( '''Hello '''+str(BNAME)+''',
    A startup in Canada wants to partner with you. They develop technology that allows it's users to listen to english television shows instantly without subtitles in Hindi and 14 other languages. Please, let me know if you'd be interested in being an official reseller of this product and the startup and I would love to get in touch with you.

Sincerely,

- Adil''')
            msg['From'] = SENDER
            msg['To'] = EMAIL
            msg['Subject'] = 'North American Company Partnership'
            smtpserver.send_message(msg)
            smtpserver.quit()
        except:
            print("NOT A REAL EMAIL ERROR")
            continue
if __name__ == '__main__':
    send_email("garadadil@gmail.com", "BNAME", "COUNTRY")
    '''A large group of high-tech startups backed by high-tech startup incubators and startup hubs across Canada would like to partner with you to distribute their products in '''+str("COUNTRY")+'''. These are pre-revenue startups, and they can supply their products cost-free to you. Just long as you are willing to try and sell them to your customers. Let me know if you would be interested in this. Thank you!'''
