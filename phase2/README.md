## README

b10705005 陳思如

#### Phase 2 Project Description

We start the server by running the following comand in the terminal:

```
python server.py
```

The server will start a multithread-https server with socket in the **localhost** and **port 8181**.

#### 1. User Register/Login/Logout

The client has to login to use the message board feature.

The first page that the first-visited client will be directed to is the "register/login" page.

The user has to input the username and password field. If the user input is not correct or some not desired input, the server will show the corresponding wrong message.

<img src="C:\Users\Lala\AppData\Roaming\Typora\typora-user-images\image-20231225165438469.png" alt="image-20231225165438469" style="zoom:67%;" />

- Register
  - make sure that the username is not repeated with the existed user data
  - username has to be at at least 1 character
  - password has to be at least 3 characters
  - save the registered data into the `info.json`
-   Login
  - Check the username and password pair
  - We ensure that the username is in the `info.json`

#### 2. Message Board

Users can send message with the HTML form attribute.

Then the server will receive a POST request, then it will parse the request and save the message and the connected client username to the `message.json` file.

The server later will parse the `message.json` to display all the messages to the board from different user.

Here is an example image of the message board:

<img src="C:\Users\Lala\AppData\Roaming\Typora\typora-user-images\image-20231225165719429.png" alt="image-20231225165719429" style="zoom:67%;" />

#### 3. MultiThread

implemented with the `server.listen(10)`, so the web server can handle at most 10 client requests at the same time.

Since know the data we are transmitting is really small and fast. So, there is actually not quite a scenario to demonstrate the usage of multithread.

#### 4. HTTPS Self-signed certificate

I used the Openssl to generate and signed the certificate of this server. Then installed into my chrome browser.

Here is the image that shows it is safe and have efficient certificate:

 <img src="C:\Users\Lala\Pictures\Screenshots\螢幕擷取畫面 2023-12-25 170051.png" style="zoom:67%;" />

#### 5. Audio stream

I add a handler in the server GET response. It sends the audio in `audio/wav` type and divides the whole file into chunk. It reads the file and sends the file concurrently.

#### 6. Video stream

I add a handler in the server GET response. It sends the audio in `video/mp4` type and divides the whole file into chunk. It reads the file and sends the file concurrently.

