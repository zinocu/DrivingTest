import requests
import json
from time import time, sleep, asctime

session = requests.Session()
session.cookies.update({
	'dmid': '', # replace
	'auditLogToken': '', # replace
	'__90518-eng': 'survey%20popped',
	'JSESSIONID': '', # replace
	'token': '' # replace
})

headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
	'accept': 'application/json, text/plain, */*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.5',
	'connection': 'keep-alive',
	'referer': 'https://drivetest.ca/book-a-road-test/booking.html'
}

base_url = 'https://drivetest.ca/booking/v1/booking/{}'

months = {
	6: lambda day: day >= 24,
	7: lambda day: day <= 4
 } # June, July

locations = {
	'Oakville': '18292',
	'Etobicoke': '18298',
	'Brampton': '18273'
}

def query(url, month, day_filter):
	params = {'month': month, 'year': 2018}
	res = session.get(url, headers=headers, params=params)
	res.raise_for_status()
	
	session.cookies.update(res.cookies)
	session.cookies['token'] = res.cookies['token']
	data = json.loads(res.text)
	
	available = []
	
	for day_data in data['availableBookingDates']:
		day = day_data['day']
		if day_filter(day):
			if day_data['description'].strip().lower() == 'open':
				available.append(str(day))
	
	return available

def search():
	for location, location_code in locations.items():
		url = base_url.format(location_code)
		for month, day_filter in months.items():
			available = query(url, month, day_filter)
			if available:
				print('FOUND in {location} month: {month}, days: {days}'.format(location=location, month=month, days=', '.join(available)))
			
			sleep(1)

if __name__ == '__main__':
	print_time = time()
	while True:
		if time() - print_time > 60 * 2:
			print(asctime())
			print_time = time()
		search()