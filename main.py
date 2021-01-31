#!/usr/bin/env python3

import subprocess,sys,os, re,qrcode,pathlib

    
def run_command(command):
    '''Function to prevent retyping of the same execution step needed for every command on shell'''
    
    output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True).communicate()  # utilising the subprocess module to execute command

    return output.decode("utf-8")

def __winExtraction__(arg=0,_ssid=""):
    if int(arg)==1:
        _ssid = run_command("netsh wlan show interfaces | findstr SSID").replace("\r","")
        _ssid = re.findall(r"[^B]SSID\s+:\s(.*)", _ssid)[0]
        return _ssid
    elif int(arg)==2:
        pwd = run_command(f"netsh wlan show profile name=\"{_ssid}\" key=clear | findstr Key").replace("\r", "")
        pwd = re.findall(r"Key Content\s+:\s(.*)", pwd)[0]
        return pwd
    else:
        raise Exception("Sorry, Please check if it is actually a windows environment...\n\n\n")


def get_ssid():

    if sys.platform=="win32":
        ssid=__winExtraction__(1)
        if ssid =="":
            print("SSID was not found")
            sys.exit(1)
    return ssid


def get_password(ssid):
    
    if ssid == "":
        print("SSID is not defined")
        
    if sys.platform == "win32":
        password = __winExtraction__(2,ssid)

    if password == "":
        print("Could not find password")
        sys.exit(1)

    return password


def generate_qr_code(ssid, password):
    text = f"WIFI:T:WPA;S:{ssid};P:{password};;"    # refer: https://feeding.cloud.geek.nz/posts/encoding-wifi-access-point-passwords-qr-code/

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(text)
    file_name = f"{ssid}.png"      # might want to update this in future
    img = qr.make_image()
    img.save(file_name)
    print("QR code has been saved to {0}".format(file_name))
    show_qr_code(file_name)


def show_qr_code(file_name):
    # importing required packages 
    import tkinter   
    from PIL import ImageTk, Image   

    # creating main window 
    root = tkinter.Tk()
    root.title(file_name[:-4])

    # arranging application parameters 
    canvas = tkinter.Canvas(root, width = 400,          ## IF YOUR QR DOES NOT FIT YOU MAY WANT TO INCREASE THESE VALUES 
                        height = 400)   

    canvas.pack()   

    # loading the image 
    img = ImageTk.PhotoImage(Image.open(file_name))   

    # arranging image parameters  
    # in the application 
    canvas.create_image(20, 20,anchor='nw',image = img)  

    # running the application 
    root.mainloop()  


if __name__ =="__main__":
    print(get_ssid())
    print(get_password(get_ssid()))
    generate_qr_code(get_ssid(),get_password(get_ssid()))
    
    












