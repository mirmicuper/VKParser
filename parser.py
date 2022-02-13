import requests
import csv
import datetime, time
from bs4 import BeautifulSoup as BS


#const
token = 'abbf5a7cabbf5a7cabbf5a7cbeabc44283aabbfabbf5a7cca4700031cbc96ae8f1e2bdd'
version = 5.131
#Изменяемый параметр user_id
user_id = 329743555 
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
print(data)
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

	print('ID: ' + str(idUser))
	print('Имя: ' + str(first_name))
	print('Фамилия: ' + str(last_name))
	print('День Рождения: ' + str(bdate))
	print('Пол: ' + str(sex))
	print('Страна: ' + str(country))
	print('Город: ' + str(city))
	print('Онлайн: ' + str(value.strftime('%Y-%m-%d %H:%M:%S')))
	print('Наличие телефона: ' + str(has_mobile))
	print('**********************')
	print()
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
		#try execute
		try:
			getVariable(htmlp)
		except: 
			print("Информация не найдена")
			print('**********************')
			print()

getInfo(data)
 

