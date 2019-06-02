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
            timestamp = str(int(time.time()))

        self.sock.send(f"put {key} {value} {timestamp}\n".encode("utf8"))

        data = b""
        while not data:
            data += self.sock.recv(1024)

        data = data.decode("utf8")

        if data == 'error\nwrong command\n\n':
            raise ClientError


    def get(self, key):

        self.sock.send(f"get {key}\n".encode("utf8"))

        data = b""
        while not data:
            data += self.sock.recv(1024)

        data = data.decode("utf8")

        # Обработка и вывод ответа сервера:
        # создаем пустой словарь для вывода данных.
        output = {}

        # если сервер не нашел метрик, то возвращаем пустой словарь в ответе.
        if data == 'ok\n\n':
            return output

        # если сервер вернул ошибку, то райзим ClientError.
        elif data == 'error\nwrong command\n\n':
            raise ClientError

        else:
            # разделяем строку на подстроки и кладем их в темповый список.
            temp = data.split()
            # удаляем из темпового массива маркер ответа сервера, оставляем только логи.
            if temp[0] == 'ok':
                temp.remove('ok')

            # cоздаем ordered dict который будет использован для сортировки логов по дате.
            sorted_by_date_data = collections.OrderedDict()
            # переносим данные из темпового списка в OrderedDict с ключем равным дате.
            i = 0
            for _ in range(int(len(temp) / 3)):
                sorted_by_date_data[temp[i + 2]] = (temp[i], temp[i + 1])
                i += 3
            # сортируем логи по дате в OrderedDict.
            sorted_by_date_data = sorted(sorted_by_date_data.items())

            # кновертируем логи отсортированные по дате в формат нужный для вывода.
            i = 0
            for k, v in sorted_by_date_data:
                if v[0] in output:
                    output[v[0]].append((int(k), float(v[1])))
                else:
                    output[v[0]] = []
                    output[v[0]].append((int(k), float(v[1])))
                i += 3

            return output
