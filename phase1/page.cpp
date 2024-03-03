#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>
using namespace std;

int server_socket, client_socket;
char replyCode[1024] = "HTTP/1.1 200 OK\n\n";
char replyContent[1024] = "<h1>---Computer Network Project Phase 1-----</h1><p>Student id:B10705005</p><p>Name: Szu-Ju, Chen</p><p>Hello world!</p>";

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
    //server info
    char ip[512] = "localhost"; //my workstation external ip
    int port = 8181;

    //create server socket
    sockaddr_in server_address, client_address;
    socklen_t client_length;
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &(server_address.sin_addr));
    bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address));
    listen(server_socket, 1); //just handle one user at a time
    cout << "Server is listening on addr: " << ip << endl;
    cout << "Server is listening on port: " << port << endl;

    while(true){
        //listens for client connection
        client_length = sizeof(client_address);
        client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_length);

        char clientmessage[1024] = {0};
        char *requestType;
        int status = 200;
        char *strPter;
        // get client request
        read(client_socket, clientmessage, sizeof(clientmessage));
        // cout << "Received:\n " << clientmessage << endl;
        // split the msg to check the request type
        requestType = strtok(clientmessage, " ");
        if(strcmp(requestType, "GET") != 0)
            status = 501; //not implemented for other request
        else    
            cout << "request GET" << endl;

        //sent the reposnse to client get request
        char reply[1024] = "";
        strcat(reply, replyCode);
        strcat(reply, replyContent);
        // cout << "Response to client:\n" << reply << endl;
        send(client_socket, reply, strlen(reply), 0);
        //close the socket connection
        //the response is sent then next connection is activate if another request is sent
        shutdown(client_socket, SHUT_RDWR);
    }
    
    close(client_socket);
    close(server_socket);
    return 0;
}