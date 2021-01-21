import bs4
import requests
import os

def fetch(city):
	LANGUAGE = "zh-CN"
	UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
	headers = {
		'Accept-Language': LANGUAGE,
		'User-Agent': UA,
	}
	r = requests.get(os.path.join('https://wttr.in', city), headers=headers)
	return r.text

def get_weather_info(html):
	soup = bs4.BeautifulSoup(html,'html5lib')
	info = soup.findAll(name="pre")
	return str(info[0])

with open('./city.list', 'r', encoding='utf-8') as f:
	citys = f.read().split('\n')
	weather_info = ''
	for city in citys:
		weather_info += get_weather_info(fetch(city))

with open('./template.html', 'r', encoding='utf-8') as f:
    print(f.read().replace('REPLACE', weather_info))