import cv
import sys
import urllib
import time
import os
import pycurl
import twitter
import imgur

# Settings
camera_ip = ""
haar_file = "" # Ex: "C:\OpenCV2.0\data\haarcascades\haarcascade_frontalface_default.xml"
twitter_user = ""
twitter_pass = ""
imgur_api_key = ""

# Loop over the views
views = ["9ff,4ff,24","6ff,4ff,24","0,2ff,24"]
for index, v in enumerate(views):
	# Pan the camera to the view
    params = urllib.urlencode({'AbsolutePanTilt': v})
    f = urllib.urlopen("http://"+camera_ip+"/command/ptzf.cgi", params)
    f.read()
    stamp = time.strftime("%y%d%m%H%M%S",time.localtime())
    source = os.path.join('./', stamp + '.jpg') 
    data = urllib.urlretrieve("http://"+camera_ip+"/oneshotimage.jpg", source)
    hc = cv.Load(haar_file)
    img = cv.LoadImage(source, 0)
    faces = cv.HaarDetectObjects(img, hc, cv.CreateMemStorage())
    for (x,y,w,h),n in faces:
        cv.Rectangle(img, (x,y), (x+w,y+h), 255)
    cv.SaveImage(source, img)

    tweet = "Total people found in view ("+str(index+1)+"): "+str(len(faces))

    print tweet

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

