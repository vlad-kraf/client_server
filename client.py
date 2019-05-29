import socket
import time
import collections


                
class ClientError(Exception):
    pass
        

class Client():

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = float(timeout)
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        
    def put(self, key, value, timestamp = str(int(time.time()))):     
        self.sock.sendall(f"put {key} {value} {timestamp}\\n".encode("utf8"))
        data = self.sock.recv(4096).decode("utf8")
            
        if data != 'ok\n\n':
            raise ClientError
        
                
    def get(self, key):
        self.sock.sendall(f"get {key}\\n".encode("utf8"))
        data = self.sock.recv(4096).decode("utf8")
        output = dict()

        if len(data) > 4:
            temp = data.split()
            sorted_by_date_data = collections.OrderedDict()

            if temp[0] == 'ok':
                temp.remove('ok')

            i = 0
            for _ in range(int(len(temp) / 3)):
                sorted_by_date_data[temp[i + 2]] = (temp[i], temp[i + 1])
                i += 3

            sorted_by_date_data = sorted(sorted_by_date_data.items())

            i = 0
            for k, v in sorted_by_date_data:
                if v[0] in output:
                    output[v[0]].append((k, v[1]))
                else:
                    output[v[0]] = []
                    output[v[0]].append((k, v[1]))
                i += 3
            return output

        elif data == 'ok\n\n':
            return output

        
                               