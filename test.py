# Create an image
from PIL import Image, ImageDraw, ImageFont
image = Image.new("1", (128,32),(1))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("small_pixel.ttf", 8)

# Pull data from GoTracker Website
import urllib2
url = "http://gotracker.ca/GoTracker/mobile/StationStatus/Service/09/Station/16"
output = urllib2.urlopen(url).read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(output, 'html.parser')
times = []
expec = []
for trip in soup.find_all('td',{'class':'colTripScheduled'}):
	times.append(trip.text)
for trip in soup.find_all('td',{'class':'colTripExpected'}):
	expec.append(trip.text)
comb = zip(times,expec)

# Render website data to image
y = -1
count = 0
for row in comb:
	if count <4:
		text = "%s %s"%row
		print(text)
		t,s = row
		draw.text((52, y), t, (0), font=font)
		draw.text((84, y), s, (0), font=font)
		y+= 7
	count += 1
draw.text((4,21), "Rouge Hill", (0), font=font)
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

