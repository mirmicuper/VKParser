import requests
import csv
import datetime, time
import smtplib
import os
from bs4 import BeautifulSoup as BS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# const
token = 'abbf5a7cabbf5a7cabbf5a7cbeabc44283aabbfabbf5a7cca4700031cbc96ae8f1e2bdd'
version = 5.131
#Изменяемый параметр user_id

user_id = str(input("Введите ID: ")) #329743555 
print("Expectation...")
user_ids = '296213477'
order = 'hints'
fields ='sex, country, schools, bdate, last_seen, city, has_mobile'

#write friends id of acc
response = requests.get('https://api.vk.com/method/friends.get', params={
	'access_token':token, 
	'v':version, 
	'user_id':user_id,
	'order':order
	})
data = response.json()['response']['items']
#create theader in csv-file
with open('data.csv', 'w') as file:
	a_pen = csv.writer(file)
	a_pen.writerow(['id', 'Имя', 'Фамилия', 'День Рождения', 'Страна', 'Город'])


#function write rows with data of friends 
def getInfoInCSV(idUser, first_name, last_name, bdate, country, city):
	with open('data.csv', 'a') as file:
		a_pen = csv.writer(file)
		my_list = [idUser, first_name, last_name, bdate, country, city]
		a_pen.writerow(my_list)

def getVariable(htmlp):
	try:
		idUser = htmlp.json()['response'][0]['id']
	except: 
		print("ID: None")

	try:
		first_name = htmlp.json()['response'][0]['first_name']
	except: 
		print("Имя: None")

	try:
		last_name = htmlp.json()['response'][0]['last_name']
	except: 
		print("Фамилия: None")

	try:
		bdate = htmlp.json()['response'][0]['bdate']
	except:
		print("День Рождения: None")

	try:
		sex = htmlp.json()['response'][0]['sex']
	except: 
		print("Пол: None")

	try:
		country = htmlp.json()['response'][0]['country']['title']
	except: 
		print("Страна: None")

	try:
		city = htmlp.json()['response'][0]['city']['title']
	except: 
		print("Город: None")

	try:
		last_seen_platform = htmlp.json()['response'][0]['last_seen']['platform']
	except: 
		print("Устройство: None")

	try:
		last_seen_time = htmlp.json()['response'][0]['last_seen']['time']
		value = datetime.datetime.fromtimestamp(last_seen_time)
	except: 
		print("Онлайн: None")

	try:
		has_mobile = htmlp.json()['response'][0]['has_mobile']
	except: 
		print("Наличие телефона: None")


	if has_mobile == 0:
		has_mobile = 'не найден'
	else:
		has_mobile = 'найден'

	if sex == 1:
		sex = "Женский"
	else:
		sex = "Мужской"

	getInfoInCSV(idUser, first_name, last_name, bdate, country, city)

#general function (data about friends)
def getInfo(data):
	for i in data:
	#write data about friend id
		htmlp = requests.get('https://api.vk.com/method/users.get', params={
			'access_token':token, 
			'v':version, 
			'user_ids': str(i),
			'fields':fields
			})
		getVariable(htmlp)

	print("\033[32m {}".format("Done"))

	
	# addr_from = "shatohinn267@gmail.com"                
	# password  = "shatohin6701" 
	# addr_to = "alexander.onthe@gmail.com"
	# files = ["data.csv"]


def send_email():
	try:
		addr_from = "shatohinn267@gmail.com"         
		addr_to = "alexander.onthe@gmail.com"                     
		password = "shatohin6701"                          

		msg = MIMEMultipart()                              
		msg['From'] = addr_from                        
		msg['To'] = addr_to                             
		msg['Subject'] = 'Тема сообщения'              

		body = "Текст сообщения"
		msg.attach(MIMEText(body, 'plain'))
		with open('data.csv') as f:
			file = MIMEText(f.read())

		file.add_header('content-disposition', 'attachment', filename='data.csv')
		msg.attach(file)

	
		server = smtplib.SMTP('smtp.gmail.com', 587)                              
		server.starttls()                             
		server.login(addr_from, password)             
		server.send_message(msg)
	
		print("\033[32m {}".format("The message was sent successfully!"))

	except Exception as _ex:
		return f"{_ex}\nCheck your login or password please!"                         

getInfo(data)
send_email()


