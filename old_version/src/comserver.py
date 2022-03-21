import socket
import threading
import socketserver
import time
from time import sleep

class ComunicationServer():

    class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    
        def handle(self):
            addr = self.client_address
            print("Connection from: {} ".format(str(addr)))
            self.server.init()
            while True:
                try:
                    data = self.request.recv(1024)
                except:
                    print("conexion terminated")
                    break
                if not data:
                    break
                data = str(data,'ascii')
                print("from connected user: " + data)
                if data == 'time':
                    data = str(self.server.gettime())
                    self.request.sendall(bytes(data,'ascii'))
                elif data[:11] == "SERVERPORT:":
                    serverport = data[11:]
                    self.server.addr = tuple([addr[0],int(serverport)])
                    self.server.connecttopeer(self.server.addr)
                    self.request.sendall(bytes("OK",'ascii'))
                elif data == "Still Conected":
                    self.request.sendall(bytes("YES",'ascii'))
                else:
                    self.request.sendall(bytes("Unknown command",'ascii'))
            self.server.s.close()
            self.request.close()

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True
        addr = None
        main = None # main instance of the parent class

        def init(self):
            self.s = socket.socket()
            self.s.close()
            

        def gettime(self):
            return time.time()

        def connecttopeer(self,address):
            self.s.close()
            self.s = socket.socket()
            self.s.connect(address)

        # def reconect(self):
        #     if self.addr is not None:
        #         try:
        #             self.connecttopeer(self.addr)
        #         except:
        #             print("Trying to reconect to peer. Address: {}".format(self.addr))
        #             sleep(1)
        #             self.reconect()

    def __init__(self, *args, **kwargs):
        self.init()

    def init(self):

        # Port 0 means to select an arbitrary unused port
        HOST =  ""
        PORT = 9999
        self.server = self.ThreadedTCPServer((HOST, PORT),self.ThreadedTCPRequestHandler)
        
        # Adding stuff to nested class
        self.server.main = self
        ip, port = self.server.server_address
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print("Server loop running in thread:", self.server_thread.name)
        print("Server loop IP:{} PORT:{}".format(ip,port))
        self.server.s = socket.socket()
        self.server.s.close()

    # used by server
    def broadcast(self,message):
        if not self.server.s._closed:
            self.server.s.sendall(bytes(message,'ascii'))
            data = self.server.s.recv(1024)
            return data
        else:
            print("Client Disconected")
            return bytes("",'ascii')

    def send_input(self):
        message = input("-> ")
        while message != 'q':
            if len(message)>0:
                data = self.broadcast(message)
                print('Received from client: {}'.format(data))
            message = input("-> ")

    # for servers
    def checksync(self):
        if not self.server.s._closed:
            mytime = time.time()
            clienttime = float(self.broadcast("time"))
            diff = mytime - clienttime
            print("time difference: {}".format(diff))
            return diff
    
    def get_peer_name(self):
        try:
            peername = self.server.s.getpeername()
        except:
            return None
        return peername[0]

    def close(self):
        self.server.s.close()
        self.server.shutdown()
        self.server.server_close()
        print("ComunicationServer closed")

   
if __name__ == "__main__":
    mycom = ComunicationServer()
    mycom.send_input()
    sleep(2)
    mycom.checksync()
    mycom.close()
    
    