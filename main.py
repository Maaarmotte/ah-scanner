import socket

from scanner import WakfuScanner

CLEAR_TRAFFIC_SERVER_ADDR = '127.0.0.1'
CLEAR_TRAFFIC_SERVER_PORT = 5558

scanner = WakfuScanner()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as consumer_socket:
    consumer_socket.connect((CLEAR_TRAFFIC_SERVER_ADDR, CLEAR_TRAFFIC_SERVER_PORT))
    data = b''
    while True:
        while len(data) < 5:
            data += consumer_socket.recv(4096)

        source = 'client' if data[0:1] == b'\x00' else 'server'
        length = int.from_bytes(data[1:5], byteorder='big')

        while len(data) < length + 5:
            data += consumer_socket.recv(4096)

        direction = '-->' if source == 'client' else '<--'
        scanner.parse_raw_data(source, data[5:length+5])
        data = data[length + 5:]
