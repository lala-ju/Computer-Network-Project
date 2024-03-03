import json
import os
# response
header = "HTTP/1.1 200 OK\r\n"
header += "Content-Type: text/html\r\n"
header += "Connection: keep-alive\r\n"
header += "Access-Control-Allow-Origin: *\r\n\n"
header += "<html><head><title>CN 2023 Phase 2 project</title></head>"
header += "<body><h1>CN 2023 Phase 2 project</h1><h3>Student id:B10705005   Name: Szu-Ju, Chen</h3><p>Hello world!<br></p>"
# state 0 username and password to login or register
credential = "<p>Input your username and password to get to the message board feature.<br><br>"
credential += "<form method='POST'>"
credential += "<label for='username'> username:</label><input type='text' id='username' name='username' minlength='1' maxlength='100' required><br>"
credential += "<label for='password'> password:</label><input type='password' id='password' name='password' minlength='3' maxlength='100' required><br><br>"
credential += "<input type='submit' name='register' value='Register'>"
credential += "<input type='submit' name='login' value='Login'></form></p>"
# login welcome message for after state and a logout option
welcome = "<p>Hello world to the user " #+ <b>username !</b>
logout = "<form method='POST'><input type='submit' name='logout' value='Logout'></form><br><br>"
# feature options to check it out
option = "<p>Please choose one feature to try out! <br><br>"
option += "<form method='POST'>"
option += "<input type='submit' name='streaming' value='Streaming'><br>"
option += "<input type='submit' name='messageBoard' value='MessageBoard'></form><br><br></p>"
# message board page
message = "<form method='POST'>"
message += "<label for='message'> Please enter your message to the board:</label>"
message += "<input type='text' id='message' name='message' minlength='1' maxlength='100' required>"
message += "<input type='submit' name='submit' value='Submit'></form>"
message += "<h3>---- HERE IS THE MESSAGEBOARD FROM ALL USERS ----</h3>"
# audio
audio = "<p> Press play button to listen to the sample audio. <br></p>"
audio += "<audio controls>"
audio += "<source src='/audio/classical.wav' type='audio/wav'>"
audio += "Your browser does not support the audio tag."
audio += "</audio>"
# video
video = "<p> Press play button to listen to the sample video. <br></p>"
video += "<video controls width='640' height='360'>"
video += "<source src='/video/bunny.mp4' type='video/mp4'>"
video += "Your browser does not support the video tag."
video += "</video><br>"
# response end
backtooption = "<form method='POST'><input type='submit' name='return' value='return'></form><br><br>"
end = "</body></html>"

def get_initial(wrong_message):
    return header+credential+wrong_message+end

def get_option(username):
    custom_welcome = welcome + f"<b>{username} !</b></p>"
    return header+custom_welcome+logout+option+end

def get_message(username):
    custom_welcome = welcome + f"<b>{username} !</b></p>"
    all_message = message 
    if os.path.exists('message.json'):
        with open("message.json") as file:
            messages = json.load(file)
        for msg in messages:
            user = f"[{msg['username']}]"
            all_message += f"<p>{user} posted: {msg['message']}</p>"
    return header+custom_welcome+logout+all_message+backtooption+end

def get_streaming(username):
    custom_welcome = welcome + f"<b>{username} !</b></p>"
    return header+custom_welcome+logout+audio+video+backtooption+end

def get_audio(conn):
    audio_path = './audio/classical.wav'
    size = os.path.getsize(audio_path)
    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: audio/wav\r\n"
    response += f"Content-Length: {size}" + "\r\n\r\n" 
    conn.send(response.encode('utf-8'))
    
    with open(audio_path, "rb") as audio:
        while True:
            data = audio.read(1024)
            if not data:
                break
            conn.send(data)
            
    conn.close()
    
def get_video(conn):
    video_path = './video/bunny.mp4'
    size = os.path.getsize(video_path)
    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: video/mp4\r\n"
    response += f"Content-Length: {size}" + "\r\n\r\n" 
    conn.send(response.encode('utf-8'))
    
    with open(video_path, "rb") as video:
        while True:
            data = video.read(1024)
            if not data:
                break
            conn.send(data)
            
    conn.close()
    