# -*- coding: utf-8 -*-
import json
import urllib2
import time
import pprint

current_milli_time = lambda: int(round(time.time() * 1000))


def get_forecast(location_lat,location_long):
    weather_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/" + location_long + "/lat/" + location_lat +"/data.json"
    current_weather = json.load(urllib2.urlopen(weather_url))
    return current_weather

def calulate_direction(target):
    with open("weather_desc.json", "r+") as json_file:
        weather_desc = json.load(json_file)
    json_file.close()
    directions = weather_desc["directions"]
    diff = 360
    direction = ""
    index = 0

    for i in range(0,len(directions)):
        if directions[i]["value"] == target:
            direction = directions[i]["name"]
            return direction
        if abs(target - directions[i]["value"]) < diff:
            diff =  target - abs(directions[i]["value"])
            direction = directions[i]["name"]
            index = i
    return directions[index]["name"]

def write_forecast(current_weather):
    with open("last_position.json", "r+") as json_file:
        data = json.load(json_file)
    json_file.close()

    if current_weather["approvedTime"][0:10] + ":" + current_weather["approvedTime"][11:16]  == data["last_published_forecast"].encode('utf-8'):
        print("No new forecast")
    else:
        data["last_published_forecast"] = current_weather["approvedTime"][0:10] + " -- " + current_weather["approvedTime"][11:16]
        weathers =[]
        with open("weather_desc.json", "r+") as json_file:
            weather_desc = json.load(json_file)
        json_file.close()
        directions = weather_desc["directions"]
        print directions

        for x in range (0, 48):
            if current_weather["timeSeries"][x]["validTime"][11:16]=="12:00" or current_weather["timeSeries"][x]["validTime"][11:16] == "00:00":
                # print ("date: " + current_weather["timeSeries"][x]["validTime"][0:10])
                # print("time: " + current_weather["timeSeries"][x]["validTime"][11:16])
                weather = {}
                weather["wind"] = str(current_weather["timeSeries"][x]["parameters"][15]["values"][0]).encode("utf-8")
                weather["wind_direction"] = calulate_direction(current_weather["timeSeries"][x]["parameters"][14]["values"][0])
                weather["wind_gust"] = str(current_weather["timeSeries"][x]["parameters"][17]["values"][0]).encode("utf-8")
                weather["temperature"] = str(current_weather["timeSeries"][x]["parameters"][11]["values"][0]).encode("utf-8")
                weather["time"] = str(current_weather["timeSeries"][x]["validTime"][11:16]).encode("utf-8")
                weather["date"] = str(current_weather["timeSeries"][x]["validTime"][0:10]).encode("utf-8")

                for symbols in weather_desc["weathers"]:
                    if current_weather["timeSeries"][x]["parameters"][18]["values"][0] == symbols["value"]:
                        weather["symbol"] = symbols["symbol"]
                        weather["weather"] = symbols["name"]
                weathers.append(weather)


    data["last_position"]["weathers"] = weathers

    with open("last_position.json", "w") as json_file:
        json.dump(data, json_file)
    json_file.close()


def print_forecast():
    with open("last_position.json", "r+") as json_file:
        data = json.load(json_file)
    json_file.close()
    d = u'\u00B0'
    print d
    print("__________________________________")
    print (" Last updated: ") + data["last_published_forecast"]
    print ("----------------------------------")
    for weather in data["last_position"]["weathers"]:
        print("" +data["last_position"]["city"] + ": " + weather["date"] + " " + weather["time"])
        print(" Temperature: " +  weather["temperature"] + d + "C " + weather["symbol"] )
        print(" Weather: " + weather["weather"] )
        print(" Wind: " + str(weather["wind"]) + " (" + weather["wind_gust"] + ") m/s "  + weather["wind_direction"])
        print ("-------------------------")



def get_location():
    with open("last_position.json", "r+") as json_file:
        data = json.load(json_file)
    json_file.close()

    location_url = "http://freegeoip.net/json/"
    current_location = json.load(urllib2.urlopen(location_url))

    data["last_checked"] = current_milli_time()
    data["last_position"]["city"] = current_location["city"].encode('utf-8').strip()
    data["last_position"]["region"] = current_location["region_name"].encode('utf-8').strip()
    data["last_position"]["country"] = current_location["country_name"].encode('utf-8').strip()
    data["last_position"]["longitude"] = str(current_location["longitude"]).encode('utf-8').strip()
    data["last_position"]["latitude"] = str(current_location["latitude"]).encode('utf-8').strip()

    json_file = open("last_position.json", "w+")
    json_file.write(json.dumps(data))
    json_file.close()

    position = []

    position.extend ([
    data["last_position"]["longitude"],
    data["last_position"]["latitude"]
    ])

    return position

def create_json_template():
    data = {}

    data["last_position"] = {}
    data["last_position"]["city"] = ""
    data["last_position"]["region"] = ""
    data["last_position"]["country"] = ""
    data["last_position"]["latitude"] = ""
    data["last_position"]["longitude"] = ""


    data["last_position"]["weathers"] = []

    weather = {}
    weather["id"] = 0
    weather["time"] = ""
    weather["temperature"] = ""
    weather["wind"] = ""
    weather["wind_direction"] = ""
    weather["wind_gust"] = ""
    weather["symbol"] = ""
    weather["weather"] = ""

    data["last_position"]["weathers"].append(weather)
    data["last_checked"] = 0
    data["last_published_forecast"] = ""

    with open("last_position.json", "w") as json_file:
        json.dump(data,  json_file)
    json_file.close()


try:
    with open("last_position.json", "r+") as json_file:
        last_position = json.load(json_file)

except IOError as e:
    print e
    create_json_template()

if (current_milli_time() - last_position["last_checked"]) >= 360000:
    location = get_location()
    loc_long = str(location.pop(0))
    loc_lat = str(location.pop(0))

    write_forecast(get_forecast(loc_lat,loc_long))

    print_forecast()
else:
    print_forecast()
json_file.close()
