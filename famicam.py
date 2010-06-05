import cv
import sys
import urllib
import time
import os
import pycurl
import twitter
import imgur
from pygame.transform import scale
from pygame import image

# Settings
camera_ip = ""
haar_file = "" # Ex: "C:\OpenCV2.0\data\haarcascades\haarcascade_frontalface_default.xml"
twitter_user = ""
twitter_pass = ""
imgur_api_key = ""
WIDTH = 640
HEIGHT = 480

# Common Objects
hc = cv.Load(haar_file)
laughingman = image.load('laughing_man.png')
stamp = time.strftime("%y%d%m%H%M%S",time.localtime())

# Loop over the views
views = ["9ff,4ff,24","6ff,4ff,24","3ff,4ff,24", "ff,2ff,24"]
for index, v in enumerate(views):
    # Pan the camera to the view
    params = urllib.urlencode({'AbsolutePanTilt': v})
    f = urllib.urlopen("http://"+camera_ip+"/command/ptzf.cgi", params)
    f.read()
    
    # Collect image (color, and black and white versions)
    source = os.path.join('./', stamp + '.jpg') 
    data = urllib.urlretrieve("http://"+camera_ip+"/oneshotimage.jpg", source)
    bwimg = cv.LoadImage(source, 0)
    img = cv.LoadImage(source)

    # Create pygame surfaces for bitblitting
    pygameimg = img.tostring()
    with_laughingman = image.fromstring(pygameimg, (WIDTH,HEIGHT), "RGB")
    
    # Detect faces and bitblit the laughingman
    faces = cv.HaarDetectObjects(bwimg, hc, cv.CreateMemStorage())
    for (fx,fy,fw,fh),n in faces:
        (x,y,w,h) = (fx-10, fy-10, fw+20, fh+20)
	laughingman_scaled = scale(laughingman, (w,h))
        with_laughingman.blit(laughingman_scaled, (x,y))

    # Save the image
    image.save(with_laughingman, source)

    tweet = "Total people found in view ("+str(index+1)+"): "+str(len(faces))

    print tweet	


    # Check if the room is dark
    hist = cv.CreateHist([32], cv.CV_HIST_ARRAY, [[0, 255]], 1)

    cv.CalcHist([bwimg], hist, 0, None)
    hist_img = cv.CreateImage((32*10,255), 8, 3)
    (_,max_value,_,_) = cv.GetMinMaxHistValue(hist)

    (sizex, sizey) = cv.GetSize(bwimg)

    darkcount = 0
    for i in range(8):
       darkcount = darkcount + cv.QueryHistValue_1D(hist, i)

    if darkcount > (.7 * (sizex * sizey)):
        print "Image is dark. Not sending data."
    else:
        print "Image is light. Sending data."
	
        if len(faces) > 0:
	        try:
		        imgapi = imgur.imgur(apikey=imgur_api_key)
		        imgurl = imgapi.upload(stamp+".jpg")
		        api = twitter.Api(username=twitter_user, password=twitter_pass)
		        status = api.PostUpdate(tweet+" "+imgurl['rsp']['image']['original_image'])
	        except:
		        print "Failed!"
				
    # Clean up our mess
    os.remove(source)