# Create an image
from datetime import datetime
from pytz import timezone    
et = timezone('US/Eastern')
et_time = datetime.now(et)


from PIL import Image, ImageDraw, ImageFont
image = Image.new("1", (128,32),(1))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("small_pixel.ttf", 8)

# Pull data from GoTracker Website
import urllib2
url = "http://gotracker.ca/GoTracker/mobile/StationStatus/Service/09/Station/12"
output = urllib2.urlopen(url, timeout=160).read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(output, 'html.parser')
times = []
expec = []
start = soup.find("td",text="Eastbound towards Oshawa").parent
for i in range(4):
	try:
		start = start.next_sibling
		trip = start.find('td',{'class':'colTripScheduled'})
		times.append(trip.text)
		trip = start.find('td',{'class':'colTripExpected'})
		expec.append(trip.text)
	except:
		break
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
		y+= 7
	count += 1
ct = et_time.strftime("%H:%M")
draw.text((0,21), "Now: %s"%ct, (0), font=font)
b = image.tobytes()

# Bit flips 
# (yes, there is probably a better way)
def reverse(by):
	by = ord(by)
	r = 0
	for i in range(8):
		j = i
		if ((0x01 << j) & by):
			r += 2**(7-i)
	return chr(r)

# output as binary and png	
with open("rougehill.xbm", 'wb') as f:
	for x in b:
		f.write(reverse(x))
image.save("rougehill.png", "png")

