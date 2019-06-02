import asyncio


class ClientServerProtocol(asyncio.Protocol):

    _buf = b""

    def connection_made(self, transport):
        self.transport = transport

    def process_data(self, data):

        output = str(f"Had reseived request '{data}' and returned respose")
        return output


    def data_received(self, data):

        # накапливаем буфер, пока не встретим "\n" в конце команды
        self._buf += data
        if self._buf.endswith(b"\n"):
            # вызываем функцию генерации ответа
            resp = self.process_data(self._buf.decode())
            # пишем ответ в сокет
            self.transport.write(resp.encode())
            #очищаем буфер
            self._buf = b""


loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8888
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()