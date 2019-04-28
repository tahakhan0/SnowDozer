import requests
import json
import time


"""
Powered by Dark Sky
https://darksky.net/poweredby/
"""

def index(coordinates):
	url = "https://api.darksky.net/forecast/bb04f6fe6c344b6e31af5f66f0760f6e/{}".format(coordinates)
	api_val = requests.get(url).json()
	"""	
	temp, any percipitation, 
	print(api_val['currently']['precipProbability'])
	print(api_val['currently']['precipIntensity'])
	"""
	if "code" not in api_val:
		weather = {
				"time": time.ctime(api_val["currently"]["time"]),
				'icon': api_val["currently"]["icon"],
				'temperature': str(round((((1*api_val["currently"]["temperature"]) - 32) * (5/9)),2)),
				'percipitation': api_val['currently']['precipProbability'],
				}
		return weather
	else:
		return "Invalid"

#print(index("40.7178,-74.0431"))