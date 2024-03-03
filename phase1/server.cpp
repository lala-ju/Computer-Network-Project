#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>
using namespace std;

int server_socket, client_socket;

void quit_handler(int signum) {
   cout << "Quit signal sent"<< endl;
   // Terminate program
   close(server_socket);
   close(client_socket);
   exit(signum);
}

int main(int argc, char* argv[]){
     //Register the quit signal
    signal(SIGINT, quit_handler);
    //define close connection keyword
    char BYE_KEYWORD[1024] = "bye";
    //server info
    char ip[512] = "localhost"; //localhost
    int port = 8080;
    
    //initialize server settings //starts the socket server
    sockaddr_in server_address, client_address;
    socklen_t client_length;
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &(server_address.sin_addr));
    bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address));
    listen(server_socket, 1); //only set one client can listen to the server at a time
    cout << "Server is listening on addr: " << ip << endl;
    cout << "Server is listening on port: " << port << endl;


    //listens for client connection
    client_length = sizeof(client_address);
    client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_length);

    //get client greeting msg
    char clientmessage[1024] = {0};
    read(client_socket, clientmessage, sizeof(clientmessage));
    cout << "Greeting from client: " << endl << clientmessage << endl;
    //send welcome msg back to client
    char servermessage[1024] = "Hello, the client from ";
    char clientip[1024] = {0};
    inet_ntop(AF_INET, &client_address.sin_addr, clientip, sizeof(clientip));
    strcat(servermessage, clientip);
    strcat(servermessage, " is connected to this server");
    send(client_socket, servermessage, strlen(servermessage), 0);

    //message communicating with client
    // receive msg from client then send back the same msg back to client
    while(true){
        char message[1024] = {0};
        int status = read(client_socket, message, sizeof(message));
        // check if connection is closed
        if(status == 0)
            break;
        cout << "Received: " << endl << message << endl;
        send(client_socket, message, strlen(message), 0);
        //check if the client wants to leave
        if(strcmp(message, BYE_KEYWORD)==0)
            break;
    }

    //close connection since the connected client leaves
    //also close the socket server
    close(client_socket);
    close(server_socket);
    return 0;
}