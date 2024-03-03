## README

b10705005 陳思如

#### Phase 1 Project Description

#### 1. Socket sending text

I have implemented a server and a client socket to send text to each other. 

The ip address of the server: **localhost**, listening port: **8080**

- Server

  Receive message from client.

  Print out the received message out in the terminal.

  Send the orginal message back to client. 

- Client

  Connects to the specific server that sent in the argument.

  Send message to the server based on the user input.

  Print out the message the reply from the server.

The server and client can send messages to each other continuously until the client send out the quit keyword **"bye"**, then the socket connection will close.

- **How to compile**

  Compile the two cpp files with the following command to get two executables `server` for socket server and `client` for socket client.

  ```
  g++ -o server server.cpp
  g++ -o client client.cpp
  ```

- **How to run**

  Need to run the server in advance so that the client can connect to it.

  1. Start the server with following command:

  ```
  ./server
  ```

  2. Start the client with follwing commnd: 

  ```
  ./client
  ```

  3. you can start to send message with socket server by inputting your message. 

- **How to terminate**	

  Option 1:

  You can enter "ctrl+c" in both terminal to terminate the socket server and client server.

  Option 2:

  Enter "bye" message in the client terminal to end the connection gracefully.

<div style="page-break-after: always;"></div>

#### 2. Personal Page

The link is **localhost:8181**

You can see the title, name, student id, and a "Hello word" text message on it.

I have built a personal page with c++ socket. I don't have the resources to make the server run continuously. So we have to start the server before we want to view our personal page. 

Once the server is started, it can handle multiple requests from different client. But the requests cannot be simultaneous. The server keeps listening to the requests until you terminate it with "ctrl+c".

- **How to compile**

- Compile the `page.cpp` to generate the executables `page`

  ```
  g++ -o page page.cpp
  ```

- **How to run**

  Then we run the `page` executables in the terminal to start the server to handle browser request later.

  ```
  ./page
  ```

- **View the page**

  We type in the link <u>localhost:8181</u> in the browser to reach to the personal page.