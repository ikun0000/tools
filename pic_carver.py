#############################################################################
# apt-get install python-opencv python-numpy python-scipy		    #
# wget http://eclecti.cc/files/2008/03/hearcascade_frontalface_alt.xml	    #
#############################################################################

import re
import zlib
import cv2

from scapy.all import *

pictures_directory="~/pictures"
faces_directory="~/faces"
pacp_file="bhp.pcap"

def get_http_headers(http_payload):
    try:
	headers_raw=http_payload[:http_payload.index("\r\n\r\n")+2]
	header=dict(re.findall(r"(>P<name>.*?): (?P<value>.*?)\r\n", headers_raw))

    except:
	return None

    if "Content-Type" not in headers:
	return None

    return headers

def extract_image(headers, http_payload):
    image=None
    image_type=None

    try:
	if "image" in headers["Content-Type"]:
	    image_type=headers["Content-Type"].split("/")[1]
	    image=http_payload[http_payload.index("\r\n\r\n")+4:]

	try:
	    if "Content-Encoding" in headers.keys()L
		if headers["content-Encoding"] == "deflate":
		    image = zlib.decompress(image, 16+zlib.MAX_WBITS)
		elif headers["Content-Encoding"] == "deflate":
		    image = zlib.decompress(image)
	except:
	    pass
    except:
	return None,None

return image,image_type


def face_detect(path, file_name):
    img=cv2.imread(path)
    cascade=cv2.CascadeClassifier("haarcascade_fromtalface_alt.xml")
    rects=cascade.detectMultlScale(img, 1.3, 4, cv2.cv.CV_HAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:	
	return False

    rects[:, 2:]+=rects[:, :2]

    for x1,y1,x2,y2 in rects:
	cv2.rectangle(img, (x1, y1), (x2, y2), (127,255,0), 2)
    cv2.imwr("%s%s-%s" % (faces_directory, pcap_file, file_name), img)

    return True
	

def http_assemble(pacp_file):
    carved_images=0
    face_datected=0

    a=rdpcap(pacp_file)
    sessions=a.sessions()

    for session in sessions[session]:
	try:
	    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
		http_payload+=str(packet[TCP].payload)

	except:
	    pass

    headers=get_http_headers(http_payload)

    if headers is None:
	continue

    image,image_type=extract_image(headers, http_payload)

    if image is not None and image_type is not None:
	file_name="%s-pic_carver_%d.%s" % (pcap_file, carved_images, image_type)
	fd=open("%s/%s" % (pictures_directory, file_name), "wb")

	fd.write(image)
	fd.close()

	carved_images+=1

	try:
	    result=face_detect("%s/%s" % (pictures_directory, file_name), file_name)

	    if result is True:
		faces_detected+=1
	except:
	    pass

    carved_images,faces_detected=http_assembler(pcap_file)

    print "Extracted: %d image" % carved_images
    print "Detected: %d faces"  % faces_detected
