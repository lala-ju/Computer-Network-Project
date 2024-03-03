#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>
using namespace std;

int client_socket;
void quit_handler(int signum) {
   cout << "Quit signal sent"<< endl;
   // Terminate program
   close(client_socket);
   exit(signum);
}

int main(int argc, char* argv[]) {
    //define bye keyword
    char BYE_KEYWORD[1024] = "bye";

    //server info
    char ip[512] = "localhost"; //localhost
    int port = 8080;

    //connect to server
    sockaddr_in server_address;
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &(server_address.sin_addr));
    connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address));

    //send hello message to server
    char message[1024] = "Hello, I am connecting to the socket server at ";
    char serverip[1024] = {0};
    inet_ntop(AF_INET, &server_address.sin_addr, serverip, sizeof(serverip));
    strcat(message, serverip);
    send(client_socket, message, strlen(message), 0);
    //get welcome message from server
    char buffer[1024] = {0};
    read(client_socket, buffer, sizeof(buffer));
    cout << "Greeting from server: " << endl << buffer << endl;

    //message communicating between server and client
    while(true){
        char msg[1024] = {0};
        char buf[1024] = {0};
        cout << "Message to server:";
        cin >> msg;
        //send message to server
        send(client_socket, msg, strlen(msg), 0);
        //read response from server
        int status = read(client_socket, buf, sizeof(buf));
        //check if connection is closed
        if(status == 0)
            break;
        cout << "Server replied: " << endl << buf << endl;
        // keywords when the client wants to leave
        if(strcmp(msg, BYE_KEYWORD) == 0)
            break;
    }
    //close connection
    close(client_socket);
    return 0;
}