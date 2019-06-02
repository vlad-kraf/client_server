def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


import asyncio
class ClientServerProtocol(asyncio.Protocol):

    _buf = b""
    _database = {}


    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, data):

        output = ""
        temp = data.split()

        if temp[0] == "put":
            temp.remove("put")

            i = 0
            for _ in range(int(len(temp) / 3)):
                if temp[i] not in self._database:
                    self._database[temp[i]] = []
                    self._database[temp[i]].append((float(temp[i + 1]), int(temp[i + 2])))
                    print (f"1: {self._database}")
                elif temp[i] in self._database:
                    content = (float(temp[i + 1]), int(temp[i + 2]))
                    if content not in self._database.get(temp[i]):
                        self._database[temp[i]].append(content)
                        print(f"2: {self._database}")
                i += 3

            output = "ok\n\n"

        elif temp[0] == "get":
            temp.remove("get")

            if temp[0] == "*":
                output += "ok\n"
                for key in self._database:
                    for item in self._database.get(key):
                        value = item[0]
                        timestamp = item[1]
                        metric = f"{key} {value} {timestamp}\n"
                        output += metric
                output += "\n"
            else:
                output += "ok\n"

                if temp[0] in self._database:
                    for item in self._database.get(temp[0]):
                        value = item[0]
                        timestamp = item[1]
                        metric = f"{temp[0]} {value} {timestamp}\n"
                        output += metric

                output += "\n"
        else:
            output = "error\nwrong command\n\n"

        return output

    def data_received(self, data):

        # накапливаем буфер, пока не встретим "\n" в конце команды
        self._buf += data
        if self._buf.endswith(b"\n"):
            # вызываем функцию генерации ответа
            resp = self.process_data(self._buf.decode())
            # пишем ответ в сокет
            self.transport.write(resp.encode())
            # очищаем буфер
            self._buf = b""




"""
python my_server.py
python ckeck_server.py

telnet 127.0.0.1 8888

put test_key 12.0 1503319740
put test_key 13.0 1503319739
put another_key 10 1503319739

get *

"""
