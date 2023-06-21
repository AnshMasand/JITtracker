import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
import os


url = 'https://www.supplier.com'

response = requests.get(url)

# Parse the HTML content of the page with Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the inventory items
items = soup.find_all('div', class_='inventory-item')

# Create a list to store the scraped data
data = []


for item in items:
    name = item.find('h2').text
    price = item.find('p', class_='price').text
    data.append((name, price))

# Convert the list to a DataFrame
df = pd.DataFrame(data, columns=['Name', 'Price'])

# Load the previously scraped data
if os.path.exists('previous_data.csv'):
    previous_data = pd.read_csv('previous_data.csv')
else:
    previous_data = pd.DataFrame(columns=['Name', 'Price'])

# Compare the two DataFrames and find the differences
diff = pd.concat([df, previous_data]).drop_duplicates(keep=False)

# Save the current data for future comparison
df.to_csv('previous_data.csv', index=False)

# Prepare the email
message = MIMEMultipart()
message['From'] = 'replitclient@example.com'
message['To'] = 'replitclientemployee@example.com'
message['Subject'] = 'Inventory Update'
message.attach(MIMEText(diff.to_string(), 'plain'))

# Send the email
smtp = smtplib.SMTP('smtp.example.com', 587)
smtp.starttls()
smtp.login(message['From'], 'password')
text = message.as_string()
smtp.sendmail(message['From'], message['To'], text)
smtp.quit()
