import socketserver
import helper

port = 8000

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        res = helper.parse_get(self.data)
        print("\nRes output:", res, "\n")

        if(res == 'index'):
            self.request.sendall(helper.ok('text/html', helper.getByteLength('templates/index.html'), ''))
            f = open('templates/index.html', "r")
            output = f.read()
            f.close()
            for char in output:
                self.request.send(char.encode("utf-8"))
        elif(res == 'button'):
            self.request.sendall(helper.ok('text/html', helper.getByteLength('button.html'), ''))
            f = open('button.html', "r")
            output = f.read()
            f.close()
            for char in output:
                self.request.send(char.encode("utf-8"))
        elif(res == '404'):
            self.request.sendall(helper.notFound('text/plain', 17, 'Content Not Found'))


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", port

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()    
