import requests
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

api_key = os.getenv('API_KEY') or os.environ.get('API_KEY')
my_email = os.getenv('EMAIL_ADDRESS') or os.environ.get('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD') or os.environ.get('EMAIL_PASSWORD')
smtp_address = os.getenv('SMTP_ADDRESS') or os.environ.get('SMTP_ADDRESS')
lat = 51.113338
lon = -0.182910
parameters = {
    "lat":lat,
    "lon":lon,
    "exclude": "alerts",
    "appid" : api_key,
    "units" : "metric"
}
URL="https://api.openweathermap.org/data/2.5/weather"
response = requests.get(url=URL, params=parameters)
response.raise_for_status()

data = response.json()
# print(data['weather'][0]['description'])
description = data['weather'][0]['description']
temp = data['main']['temp']
temp_min = data['main']['temp_min']
temp_max = data['main']['temp_max']
# print(data)

if data:
    message = MIMEMultipart()
    message['From'] = my_email
    message['To'] = "olamide.kazeem@yahoo.com"
    message['Subject'] = "Weather Today"

    body = f"Weather Description: {description}\nTemperature: {temp}c\nMin Temperature: {temp_min}c"

    message.attach(MIMEText(body, 'plain'))

    # Send email
    connection = smtplib.SMTP(smtp_address)
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, 
        to_addrs="olamide.kazeem@yahoo.com", 
        msg=message.as_string()
    )
    connection.close()
        
