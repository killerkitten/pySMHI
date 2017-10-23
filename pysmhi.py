import json
import urllib2
from pprint import pprint
from datetime import datetime
import time


current_milli_time = lambda: int(round(time.time() * 1000))

location_url = "http://freegeoip.net/json/"
with open('last_position.json', 'r+') as json_file:
    last_position = json.load(json_file)
    json_file.close()

if last_position['last_checked'] == 0:
    last_position['last_checked'] = current_milli_time()
    json_file = open("last_position.json", 'w+')
    json_file.write(json.dumps(last_position))
    json_file.close()

if (current_milli_time() - last_position['last_checked']) >= 3600000:

    current_location = json.load(urllib2.urlopen(location_url))
    print current_milli_time() - last_position['last_checked']

    tmp = last_position['last_checked']
    last_position['last_checked'] = current_milli_time()
    last_position['city'] = current_location['city']
    last_position['region_name'] = current_location['region_name']
    last_position['country_name'] = current_location['country_name']
    last_position['longitude'] = current_location['longitude']
    last_position['latitude'] = current_location['latitude']


    json_file = open("last_position.json", 'w+')
    json_file.write(json.dumps(last_position))
    json_file.close()

else:
    with open('last_position.json', 'r+') as json_file:
        last_position = json.load(json_file)
    location_city = last_position['city']
    location_state = last_position['region_name']
    location_country = last_position['country_name']
    location_long = last_position['longitude']
    location_lat = last_position['latitude']
    location_lat = str(location_lat)
    location_long = str(location_long)
    json_file.close()


weather_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/" + location_long + "/lat/" + location_lat +"/data.json"
current_weather = json.load(urllib2.urlopen(weather_url))

with open('weather_desc.json', 'r+') as json_file:
    weather_desc = json.load(json_file)
json_file.close()
print('Updated ' + current_weather['approvedTime'][11:16] + ' ' + current_weather['approvedTime'][0:10])
# Get next 48h of weather present only forcasts for mid day and night.
for x in range (0, 48):
    if current_weather['timeSeries'][x]['validTime'][11:16]=='12:00' or current_weather['timeSeries'][x]['validTime'][11:16] == '00:00':
        print('  --------------------------------------  ')
        print(location_city)
        print ('Date: ' + current_weather['timeSeries'][x]['validTime'][0:10])
        print('Time: ' + current_weather['timeSeries'][x]['validTime'][11:16])

        # Get symbols for the weather.
        for weather in weather_desc['weathers']:
            if current_weather['timeSeries'][x]['parameters'][18]['values'][0] == weather['value']:
                print('Weather: ' + weather['name'] + '  ' + weather['symbol'])
                print('Temperature: ' +  str(current_weather['timeSeries'][x]['parameters'][11]['values'][0])) + ' C '
