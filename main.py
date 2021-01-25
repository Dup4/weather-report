import bs4
import requests
import os
import time
import argparse

def fetch(city):
	LANGUAGE = "zh-CN"
	UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
	headers = {
		'Accept-Language': LANGUAGE,
		'User-Agent': UA,
	}
	params = {
		'm': '',
	}
	r = requests.get(os.path.join('https://wttr.in', city), headers=headers, params=params)
	return r.text

def get_weather_info(html):
	soup = bs4.BeautifulSoup(html,'html5lib')
	info = soup.findAll(name="pre")
	return str(info[0])

parser = argparse.ArgumentParser(description='Fetch Weather.')
parser.add_argument('-t', '--time', type=str, help='time of fetch data')
args = parser.parse_args()

title = 'Weather Report'
if args.time: title = title + ' （{}）'.format(args.time)

with open('./city.list', 'r', encoding='utf-8') as f:
	citys = f.read().split('\n')
	weather_info = ''
	invalid_list = [
		'Sorry'
	]
	for city in citys:
		html = ''
		print('Fetch The Weather Of {} Begin!'.format(city))
		for __i in range(10):
			print('Number Of Attempts: {}'.format(__i + 1))
			html = get_weather_info(fetch(city))
			ok = 1
			for invalid_word in invalid_list:
				if html.find(invalid_word) != -1:
					ok = 0
					break
			if ok == 1:
				break
			time.sleep(10)	
		weather_info += get_weather_info(fetch(city))
		print('Fetch The Weather of {} Done!'.format(city))

result = ''
with open('./template.html', 'r', encoding='utf-8') as f:
	result = f.read()
				.replace('#REPLACE', weather_info)
				.replace('#TITLE', title)

with open('./index.html', 'w', encoding='utf-8') as f:
	f.write(result)

