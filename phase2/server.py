import socket 
import json
import os
import ssl
import threading
from lib import *

NOTYET_REGISTER = 0
WRONGPASSWORD = 1
CORRECT_CREDENTIAL = 2
USERNAME_USED = 3
SUCCESS_REGISTER = 4
PKT = 1024

def get_state(ip):
    #empty, you are the first client 
    #add yourself to the json
    if not os.path.exists('cookie.json') or os.stat("cookie.json").st_size == 0:
        newClient = {'ip': ip, 'state': 0, 'username': ""}
        cookies = [newClient]
        with open('cookie.json', 'w') as file:
            json.dump(cookies , file, indent=4)
        return 0, ""
    
    with open('cookie.json', 'r') as file:
        cookies = json.load(file)
    # check is is in the cookie list
    for cookie in cookies:
        if cookie['ip'] == ip:
            return cookie['state'], cookie['username']
    
    # not in the list then append
    newClient = {'ip': ip, 'state': 0, 'username': ""}
    cookies.append(newClient)
    with open('cookie.json', 'w') as file:
            json.dump(cookies , file, indent=4)
    return 0, ""
    
def change_state(ip, new):
    with open('cookie.json', 'r') as file:
        cookies = json.load(file)
    # modify the state    
    for cookie in cookies:
        if cookie['ip'] == ip:
            cookie['state'] = new
    with open('cookie.json', 'w') as file:
            json.dump(cookies , file, indent=4)
    return new

def check_user(ip, req):
    if not os.path.exists('info.json') or os.stat("info.json").st_size == 0:
        return NOTYET_REGISTER
    
    username = req.split('username=')[-1]
    username = username.split('&')[0]

    password = req.split('password=')[-1]
    password = password.split('&')[0]
    
    with open('info.json', 'r') as file:
        infos = json.load(file)
    #check the user has register or not or password is corrected
    for info in infos:
        if info['username'] == username:
            if info['password'] == password:
                # going to log in # update username
                with open('cookie.json', 'r') as file:
                    cookies = json.load(file)
                # modify the username in cookie   
                for cookie in cookies:
                    if cookie['ip'] == ip:
                        cookie['username'] = username
                with open('cookie.json', 'w') as file:
                        json.dump(cookies , file, indent=4)
                return CORRECT_CREDENTIAL
            else:
                return WRONGPASSWORD
    return NOTYET_REGISTER
    
def add_user(req):
    username = req.split('username=')[-1]
    username = username.split('&')[0]

    password = req.split('password=')[-1]
    password = password.split('&')[0]
    infos = []
    
    if os.path.exists('info.json') and os.stat("info.json").st_size != 0:
        with open('info.json', 'r') as file:
            infos = json.load(file)
        
        #check if there is duplicate username
        for info in infos:
            if info['username'] == username:
                return USERNAME_USED
        
    infos.append({'username':username, 'password':password})
    with open('info.json', 'w') as file:
        json.dump(infos , file, indent=4)
    return SUCCESS_REGISTER

def logout(ip):
    with open('cookie.json', 'r') as file:
        cookies = json.load(file)
    # modify the username to null since logout 
    for cookie in cookies:
        if cookie['ip'] == ip:
            cookie['username'] = ""
    with open('cookie.json', 'w') as file:
            json.dump(cookies , file, indent=4)
    return

def updatemessage(username, req):
    content = req.split('message=')[-1]
    content = content.split('&')[0]
    messages = []
    
    if os.path.exists('message.json') and os.stat("message.json").st_size != 0:
        with open('message.json', 'r') as file:
            messages = json.load(file)
        
    messages.append({'username':username, 'message':content})
    with open('message.json', 'w') as file:
            json.dump(messages , file, indent=4)
    return

def client_thread(conn, addr):
    # prints the address of the user that just connected at server side
    print (addr[0] + " connected")
    # use the client addr to find the last state
    state, username = get_state(addr[0])
    # read client request
    req = conn.recv(4096)
    req = req.decode('utf-8')
    # print(req)
    # get the request type
    type = req.split(' ')[0]
    # get the corresponding action for the current state and request
    if type == "GET":
        if "mp4" in req:
            get_video(conn)
            return
        if "wav" in req:
            get_audio(conn)
            return 
        status = -1
        print("get client HTTP GET request")
    elif type == "POST":
        if state == 0: #login #register
            if "login" in req:
                status = check_user(addr[0], req)
                if status == CORRECT_CREDENTIAL:
                    state = change_state(addr[0], 1)
                    state, username = get_state(addr[0])
            elif "register" in req:
                status = add_user(req)
        elif state == 1: #stream #message #logout
            if "messageBoard" in req:
                state = change_state(addr[0], 2)
            elif "logout" in req:
                logout(addr[0])
                state = change_state(addr[0], 0)
                status = -1
            elif "stream" in req:
                state = change_state(addr[0], 3)
        elif state == 2: #submit #logout #return
            if "submit" in req:
                updatemessage(username, req)
            elif "logout" in req:
                logout(addr[0])
                state = change_state(addr[0], 0)
                status = -1
            elif "return" in req:
                state = change_state(addr[0], 1)
        elif state == 3:
            if "logout" in req:
                logout(addr[0])
                state = change_state(addr[0], 0)
                status = -1
            elif "return" in req:
                state = change_state(addr[0], 1)
        print("get client HTTP POST request")
    
    if state == 0: #initial
        if status == -1:
            response = get_initial("")
        elif status == NOTYET_REGISTER:
            response = get_initial("<p style='color:red'>This username hasn't been registered. Please register first.</p>")
        elif status == WRONGPASSWORD:
            response = get_initial("<p style='color:red'>The password is wrong. Please try again.</p>")
        elif status == USERNAME_USED:
            response = get_initial("<p style='color:red'>This username has been registered by others. Please register with another name.</p>")
        elif status == SUCCESS_REGISTER:
            response = get_initial("<p style='color:blue'>You have been registered. Please enter again to login. Thanks</p>")
        conn.sendall(response.encode('utf-8'))
    elif state == 1: #option
        response = get_option(username)
        conn.sendall(response.encode('utf-8'))
    elif state == 2: #message
        response = get_message(username)
        conn.sendall(response.encode('utf-8'))
    elif state == 3:
        response = get_streaming(username)
        conn.sendall(response.encode('utf-8'))
    conn.close()

# ssl 
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="./cert/localhost.crt",
                        keyfile="./cert/localhost.key")

# server configuration
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
IP_address = "localhost"
Port = 8181
server.bind((IP_address, Port)) 
# multithread client number
server.listen(10) 

all_threads = []
try:
    while True: 
        conn, addr = server.accept() 
        secure_conn = context.wrap_socket(conn, server_side=True)
        t = threading.Thread(target=client_thread, args=(secure_conn, addr), daemon=True)
        all_threads.append(t)
        t.start()
except KeyboardInterrupt:
    print("Terminated by Ctrl C.")
finally:
    if server:
        server.close()
    for thread in all_threads:
        thread.join()