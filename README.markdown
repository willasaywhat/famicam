# famicam #

## Description ##

This script captures a trio of images from a Sony IPELA SNC-RX550N. Following that, it will run a simple face detection script from the OpenCV library. It will then post any photos with greater than zero faces to a twitter account using imgur to post the images. 

## Settings ##

Remember to set the variables at the beginning of the script to your own settings. 

- camera_ip: This is the IP or hostname of the IPELA camera.
- haar_file: On Windows for example, the example haar classifier may be located at: "C:\OpenCV2.0\data\haarcascades\haarcascade_frontalface_default.xml"
- twitter_user: Twitter username to post with.
- twitter_pass: Password for the twitter user.
- imgur_api_key: API key from imgur.com which you can get at http://imgur.com/register/api/

## Dependencies ##

- OpenCV 2.0 with the Python extensions
- pyimgur (Specifically [my fork](http://github.com/abyssknight/pyimgur).)
- python-twitter
