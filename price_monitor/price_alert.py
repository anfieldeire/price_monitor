from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

host = 'smtp.gmail.com'
port = 587
username = "user_name"
password = "pass"
from_email = "from_email"


def send_email(self, item, rows, price_diff_percentage, price_drop):
    """ Send the price alert emails to users """
    name = item[2]
    url = rows[0]
    old_price = rows[1]
    title = item[0]
    scraped_price = item[1]
    to_email = item[-1]

    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = "Price alert: {title}".format(title=title)
        the_msg['From'] = from_email
        the_msg['To'] = to_email
        plain_txt = "Text"
        html_txt = """\
        <html>
            <head></head>
            <body>
                <p>Hello {name}, <br/><br/>
                Price alert for item: {title}. </h4><br/><br/>
                The price has dropped from the tracked price: <b>${old_price}</b> to <b>${scraped_price}</b><br/><br/>
                This is a price drop of: <b>{price_drop} %</b><br/><br/>
                Purchase now!!<br/><br/>
                Price tracked from amazon at this url: <b>{url}</b>
            </body>
        </html>""".format(name=name, old_price=old_price, scraped_price=scraped_price, title=title, url=url,
                          price_drop=price_drop)
        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, 'html')
        the_msg.attach(part_1)
        the_msg.attach(part_2)
        email_conn.sendmail(from_email, to_email, the_msg.as_string())
        email_conn.quit()
    except smtplib.SMTPException:
        print("Error sending message")



