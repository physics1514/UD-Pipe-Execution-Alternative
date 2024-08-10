import os
import time
import subprocess 
import socket
import random # for key
import re
import requests #just incase u use the alternative http method on like 70 or smt
from flask import Flask, request
from urllib.request import urlopen

def getappend(filename): # it writes, no appends lol
    return os.path.getmtime(filename)

def generateKey(length=8):
    key = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return key

scriptFileName = "script.txt" # change this as you want
keyFileName = "" # key is optional, used to make it easy

if not os.path.exists(scriptFileName): 
    print("Creating script file...")
    with open(scriptFileName, "x"): # we use 'x' so that we dont need a script.txt file to start with, if it doesnt exist, a new one is created
        pass
    print("Done.")
else:
    print("Script file already exists.")

if not os.path.exists(keyFileName): 
    print("Creating key file...")
    with open(keyFileName, "x"): 
        pass
    print("Done.")
else:
    print("Key file already exists.")


def checkPort(port):    # thank god for socket docs
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0 # checks if the port is running by attempting to connect, returns 'True' if successful

def localHost(port):
    while checkPort(port):
        print(f"Port 3000 is already in use. Waiting...") # im sure you can search up how to kill a local host port...
        time.sleep(1)
    subprocess.Popen(["python", "-m", "http.server", str(port)])    # I only knew how to open local host using terminal so i used subprocess to emulate that ig

localHost(3000) # starts the local host!

def extractUrl(content):
    match = re.search(r'game:HttpGet\("([^"]+)"\)', content)
    if match:
        return match.group(1)
    return None
# basic base func for the basic http:get (gets the url)


def execute(content):
    url = extractUrl(content)
    if url: # If it is an http:get loadstring
        print("Extracted url:", url) # optional, helps debug errors with links
        print("Getting data from url...") 
      
        # Feel free to remove this part from here...
        print("If you get any errors here, change your decode method.")
        print("------------------------------------------------------\n")
        time.sleep(1)
        # ...to here.
      
        data = urlopen(url).read() 
        #alternative (untested probably recommended):
        '''
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses
        data_str = response.text  # Automatically decodes to string
        '''
        print("Done. Encoding...")
        data_str = data.decode('utf-8')    # I recommend using json decode, bcus this will probably only work for like pastebin lol
        print("Got data. Writing...")
        print("Creating key...")
        generateKey()
        print("Writing script...")
        writeFile = open("key.txt", "w")
        writeFile = open("script.txt", "w")
        writeFile.write(data_str)
        writeFile.close()
    else: #If its not a loadstring:
        print("Writing script set to script.txt at local host 3000...")
        writeFile = open("script.txt", "w")
        writeFile.write(content)
        writeFile.close()

# IMPORTANT!1!1!!!1!!1!!1!:    make sure that something is reading the script file and executing it! ill create a py script that does that for example, but whatever you want to read it has to have access to read from localhost otherwise it will ofc not work.

# This is where you run your external exec ui, and use the functions. DM me for help or smt Discord: physics1514_ byee
