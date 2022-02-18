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
user_ids = '296213477'
order = 'hints'
fields ='sex, country, schools, bdate, last_seen, city, has_mobile'
with open('data.csv', 'w') as fileq:
	aq_pen = csv.writer(fileq)
	aq_pen.writerow(['id', 'Имя', 'Фамилия', 'День Рождения', 'Страна', 'Город'])

def getInfoInCSV(idUser, first_name, last_name, bdate, country, city):

	with open('data.csv', 'a') as file:
		a_pen = csv.writer(file)
		my_list = [idUser, first_name, last_name, bdate, country, city]
		a_pen.writerow(my_list)

def getVariable(htmlp):
	try:
		idUser = htmlp.json()['response'][0]['id']
	except: 
		idUser = "None"
	try:
		first_name = htmlp.json()['response'][0]['first_name']
	except: 
		first_name = "None"
	try:
		last_name = htmlp.json()['response'][0]['last_name']
	except: 
		last_name = "None"
	try:
		bdate = htmlp.json()['response'][0]['bdate']
	except:
		bdate = "None"
	try:
		sex = htmlp.json()['response'][0]['sex']
	except: 
		sex = "None"
	try:
		country = htmlp.json()['response'][0]['country']['title']
	except: 
		country =  "None"
	try:
		city = htmlp.json()['response'][0]['city']['title']
	except: 
		city = "None"
	try:
		last_seen_platform = htmlp.json()['response'][0]['last_seen']['platform']
	except: 
		last_seen_time = "None"
	try:
		last_seen_time = htmlp.json()['response'][0]['last_seen']['time']
		value = datetime.datetime.fromtimestamp(last_seen_time)
	except: 
		value = "None"
	try:
		has_mobile = htmlp.json()['response'][0]['has_mobile']
	except: 
		has_mobile = "None"

	if has_mobile == 0:
		has_mobile = 'не найден'
	else:
		has_mobile = 'найден'

	if sex == 1:
		sex = "Женский"
	else:
		sex = "Мужской"

	getInfoInCSV(idUser, first_name, last_name, bdate, country, city)

def getInfo(user_id):
	response = requests.get('https://api.vk.com/method/friends.get', params={
		'access_token':token, 
		'v':version, 
		'user_id': user_id,
		'order':order
	})
	data = response.json()['response']['items']
	for i in data:
	#write data about friend id
		htmlp = requests.get('https://api.vk.com/method/users.get', params={
			'access_token':token, 
			'v':version, 
			'user_ids': str(i),
			'fields':fields
			})
		print(i)
		try:
			getVariable(htmlp)
		except Exception as e:
			raise e

	print("\033[32m {}".format("Done"))

	
	# addr_from = "shatohinn267@gmail.com"                
	# password  = "shatohin6701" 
	# addr_to = "alexander.onthe@gmail.com"
	# files = ["data.csv"]

def send_email():
	try:
		addr_from = "shatohinn267@gmail.com"  
		addr_to = str(input("send to: "))                
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

def getID(user_link):
	user_id = user_link[17:]
	if user_link == ('https://vk.com/id' + user_id):
		return user_id
	else:
		idUserName = user_link[15:]
		user_id = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
			'access_token':token, 
			'v':version, 
			'screen_name': idUserName
		})
		user_id = user_id.json()["response"]["object_id"]
		return user_id
		
def baner():
	command_terminal = input()
	if command_terminal == "send mail":
		send_email()
		return baner()
	if command_terminal == "get info":
		main()
		return baner()
	if command_terminal == "exit":
		return

def main():
	user_link = input("link on user: ")
	user_id = getID(user_link)
	getInfo(user_id)
baner()