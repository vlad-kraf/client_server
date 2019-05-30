import socket
import time
import collections


class ClientError(Exception):
    pass


class Client():

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def put(self, key, value, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        self.sock.send(f"put {key} {value} {timestamp}\n".encode("utf8"))

        while True:
            data = self.sock.recv(1024)
            if not data:
                break

            data = data.decode("utf8")

            print(f"получен ответ сервера: {data}" )
            if data != 'ok\n\n':
                raise ClientError


    def get(self, key):

        self.sock.send(f"get {key}\n".encode("utf8"))

        while True:
            data = self.sock.recv(1024)
            if not data:
                break

            data = data.decode("utf8")

            output = dict()
            temp = data.strip().split()
            sorted_by_date_data = collections.OrderedDict()

            if temp[0] == 'ok':
                temp.remove('ok')

            i = 0
            for _ in range(int(len(temp) / 3)):
                sorted_by_date_data[int(temp[i + 2])] = (temp[i], temp[i + 1])
                i += 3

            sorted_by_date_data = sorted(sorted_by_date_data.items())

            i = 0
            for k, v in sorted_by_date_data:
                if v[0] in output:
                    output[v[0]].append(( k, float(v[1]) ))
                else:
                    output[v[0]] = []
                    output[v[0]].append(( k, float(v[1]) ))
                i += 3

            return output


