#  coding: utf-8 
from pathlib import Path
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        decoded = self.data.decode('utf-8')
        arrivalHeaders = decoded.split("\n")
        intermediary = arrivalHeaders[0].strip().split()
        if len(intermediary) < 2:
            return
        print(arrivalHeaders)
        print(intermediary)
        methodRequested = intermediary[0]
        path = intermediary[1]
        # print(methodRequested)
        # print(path)

        if not methodRequested == "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method not allowed\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + """
                                           <!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>405 Method not allowed</title>
                                                        <meta http-equiv="Content-Type"
                                                        content="text/html;charset=utf-8"/>
                                                </head>

                                                <body>
                                                    <div>
                                                        <h1>405 Method not allowed</h1>
                                                    </div>
                                                </body>
                                                </html> """
                                           ,'utf-8'))
            return

        if not (path.endswith(".css") or path.endswith(".html")) and (not path.endswith("/")):
            print(path)
            path += "/"
            response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + path + "\r\n\r\n"
            self.request.sendall(bytearray(response,'utf-8'))
            print(path)
        elif path.endswith(".css/") or path.endswith(".html/"):
            self.request.sendall(bytearray("HTTP/1.1 404 Not found\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + """
                                           <!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>404 Not found</title>
                                                        <meta http-equiv="Content-Type"
                                                        content="text/html;charset=utf-8"/>
                                                </head>

                                                <body>
                                                    <div>
                                                        <h1>404 Not found</h1>
                                                    </div>
                                                </body>
                                                </html> """
                                           ,'utf-8'))
            return

        readPath = path

        # If file does not exist respond with 404 Not Found
        if not (Path("./www" + readPath).exists()):
            self.request.sendall(bytearray("HTTP/1.1 404 Not found\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + """
                                           <!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>404 Not found</title>
                                                        <meta http-equiv="Content-Type"
                                                        content="text/html;charset=utf-8"/>
                                                </head>

                                                <body>
                                                    <div>
                                                        <h1>404 Not found</h1>
                                                    </div>
                                                </body>
                                                </html> """
                                           ,'utf-8'))
            return

        # Re-direct if no path is given
        if path == "/":
            # response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + readPath + "index.html\r\n\r\n"
            # self.request.sendall(bytearray(response,'utf-8'))
            print("here1: " + readPath + "index.html")
            content = self.readFile(readPath + "index.html")
            departureHeaders = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(content)) + "\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
            response = departureHeaders + content + "\r\n"
            self.request.sendall(bytearray(response,'utf-8'))
        elif path == "/deep/":
            content = self.readFile(readPath + "index.html")
            departureHeaders = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(content)) + "\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
            response = departureHeaders + content + "\r\n"
            self.request.sendall(bytearray(response,'utf-8'))
        else:
            print("here: " + readPath)
            if readPath.endswith("/"):
                readPath += "index.html"
            content = self.readFile(readPath)
            departureHeaders = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(content)) + "\r\n"
            if readPath.endswith(".html"):
                departureHeaders += "Content-Type: text/html\r\n"
            elif readPath.endswith(".css"):
                departureHeaders += "Content-Type: text/css\r\n"
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not found\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + """
                                           <!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>404 Not found</title>
                                                        <meta http-equiv="Content-Type"
                                                        content="text/html;charset=utf-8"/>
                                                </head>

                                                <body>
                                                    <div>
                                                        <h1>404 Not found</h1>
                                                    </div>
                                                </body>
                                                </html> """
                                           ,'utf-8'))
                return
            departureHeaders += "Connection: close\r\n\r\n"
            response = departureHeaders + content
            self.request.sendall(bytearray(response,'utf-8'))

    def readFile(self, filename):
        file = open("./www" + filename, "r")
        content = file.read()
        file.close()
        return content


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
