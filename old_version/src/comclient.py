import socket
import threading
import socketserver
import time
from time import sleep

class ComunicationClient():

    class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    
        def handle(self):
            addr = self.client_address
            print("Connection from: {} ".format(str(addr)))
            while True:
                try:
                    data = self.request.recv(1024)
                except:
                    print("conexion terminated")
                    break
                if not data:
                    break
                data = str(data,'ascii')
                print("from connected server: " + data)
                if data == 'time':
                    data = str(self.server.gettime())
                    self.request.sendall(bytes(data,'ascii'))
                if data == 'start_streaming':
                    print("starting streamming")
                    output = self.server.main_instance.start_streaming()
                    self.request.sendall(bytes("started_streaming:{}".format(output),'ascii'))
                if data == 'stop_streaming':
                    print("stoping streamming")
                    output = self.server.main_instance.stop_streaming()
                    self.request.sendall(bytes("stoped_streaming:{}".format(output),'ascii'))
                if data == 'start_recording':
                    print("starting recording")
                    output = self.server.main_instance.start_recording()
                    self.request.sendall(bytes("started_recording:{}".format(output),'ascii'))
                if data == 'stop_recording':
                    print("stoping recording")
                    output = self.server.main_instance.stop_recording()
                    self.request.sendall(bytes("stoped_recording:{}".format(output),'ascii'))
                else:
                    self.request.sendall(bytes("Unknown command",'ascii'))
            self.request.close()
            self.server.connect(self.server.host,self.server.port)

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True
        clientport = None
        main_instance = None

        def gettime(self):
            return time.time()

        def connect(self,host='',port=9999):
            self.host = host
            self.port = port
            self.s = socket.socket()
            print("Connecting to {},{}".format(host,port))
            try:
                self.s.connect((host,port))
                self.s.send(bytes("SERVERPORT:{}".format(self.clientport),'ascii'))
                returndata = str(self.s.recv(1024),'ascii')
                print("return data = {}".format(returndata))
                if not returndata =="OK":
                    self.connect(host,port)
            except:
                try:
                    sleep(1)
                    self.connect(host,port)
                except KeyboardInterrupt:
                    pass

        def send_input(self):
            message = input("-> ")
            while message != 'q':
                if len(message)>0:
                    data = self.send(message)
                    # data = self.recv()
                    print('Received from server: ' + str(data,'ascii'))
                message = input("-> ")

        def send(self,message):
            if self.isconected():
                self.s.send(bytes(message,'ascii'))
                return self.s.recv(1024)
        
        # CORREGIR ESTO QUE NO FUNCIONA
        def isconected(self):
            try:
                self.s.send(bytes("Still Conected",'ascii'))
                data = self.s.recv(1024)
                if str(data,'ascii') == "YES":
                    return True
                else:
                    self.connect()
                    return True 
            except:
                self.connect()
                return True

    def __init__(self, dhost='',dport=9999):
        self.init(dhost,dport)

    def init(self,dhost='',dport=9999):
        # Port 0 means to select an arbitrary unused port
        HOST =  ''
        PORT = 0
        self.server = self.ThreadedTCPServer((HOST, PORT),self.ThreadedTCPRequestHandler)
        self.ip, self.server.clientport = self.server.server_address
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print("Client Server loop running in thread:", self.server_thread.name)
        print("Client Server loop IP:{} PORT:{}".format(self.ip,self.server.clientport))
        self.server.main_instance = self
        self.connect(dhost,dport)
        self.keep_connected()
    
    def keep_connected(self):
        while True:
            try:
                sleep(1)
            except KeyboardInterrupt:
                break
    
    def connect(self,host = '',port=9999):
        self.server.connect(host,port)
   
    def close(self):
        self.server.s.close()
        self.server.shutdown()
        self.server.server_close()
    
    #to be overwriten by child
    def start_streaming(self):
        pass

    #to be overwriten by child
    def stop_streaming(self): 
        pass

if __name__ == "__main__":
    client = ComunicationClient('replaybox001')
    # import code
    # code.interact(local=dict(globals(), **locals()))
    # client.server.send_input()
    # sleep(100)
    client.close()
    
    