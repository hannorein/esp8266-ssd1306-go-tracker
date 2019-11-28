# -*- coding: utf-8 -*-
# Create an image
from datetime import datetime
from pytz import timezone    
et = timezone('US/Eastern')
utc = timezone('UTC')
et_time = datetime.now(et)
import urllib2
import json
degree_sign= u'\N{DEGREE SIGN}'

from PIL import Image, ImageDraw, ImageFont

# Bit flips 
# (yes, there is probably a better way)
def reverse(by):
	by = ord(by)
	r = 0
	for i in range(8):
		if ((0x01 << i) & by):
			r += 2**(7-i)
	return chr(r)


# Weather data
image = Image.new("1", (128,32),(1))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("small_pixel.ttf", 8)
with open('openweathermap_key.txt', 'r') as content_file:
    key = content_file.read().strip()
url = "http://api.openweathermap.org/data/2.5/weather?q=Toronto&units=metric&APPID="+key
output = urllib2.urlopen(url, timeout=160).read()
j = json.loads(output)
temp = j["main"]["temp"]
y = -4
hours = 0
draw.text((0, y), "Now", (0), font=font)
draw.text((25, y), "%.1f%sC"%(temp,degree_sign), (0), font=font)
draw.text((60, y), j["weather"][0]["description"], (0), font=font)
y += 8

url = "https://api.openweathermap.org/data/2.5/forecast?q=Toronto&units=metric&appid="+key
output = urllib2.urlopen(url, timeout=160).read()
jf = json.loads(output)
forecasts = jf["list"]
for i in range(3):
	time = utc.localize(datetime.fromtimestamp(forecasts[i]["dt"])).astimezone(et).strftime("%Hh")
	draw.text((0, y), time, (0), font=font)
	draw.text((24, y), "%.1f%sC"%(forecasts[i]["main"]["temp"],degree_sign), (0), font=font)
	draw.text((60, y), forecasts[i]["weather"][0]["description"], (0), font=font)
	y+=8

b = image.tobytes()
with open("temp.xbm", 'wb') as f:
    for x in b:
        f.write(reverse(x))
image.save("temp.png", "png")

# Pull data from GoTracker Website
image = Image.new("1", (128,32),(1))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("small_pixel.ttf", 8)
url = "http://gotracker.ca/GoTracker/mobile/StationStatus/Service/09/Station/12"
output = urllib2.urlopen(url, timeout=160).read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(output, 'html.parser')
times = []
expec = []
start = soup.find("th",text="Eastbound towards Oshawa").parent
for i in range(4):
	try:
		start = start.next_sibling
		trip = start.find('td',{'class':'colTripScheduled'})
		times.append(trip.text)
		trip = start.find('td',{'class':'colTripExpected'})
		expec.append(trip.text)
	except:
		continue
comb = zip(times,expec)

# Render website data to image
y = -4
count = 0
for row in comb:
	if count <4:
		text = "%s %s"%row
		print(text)
		t,s = row
		draw.text((54, y), t, (0), font=font)
		draw.text((86, y), s, (0), font=font)
		y+= 8
	count += 1
ct = et_time.strftime("%H:%M")
draw.text((0,20), "%s"%ct, (0), font=font)
b = image.tobytes()

# output as binary and png	
with open("danforth.xbm", 'wb') as f:
	for x in b:
		f.write(reverse(x))
image.save("danforth.png", "png")

