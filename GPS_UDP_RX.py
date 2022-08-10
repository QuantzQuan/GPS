import socket


def udp_rx():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_code = (socket.gethostname(), 2000)
    udp.bind(receive_code)
    context, address = udp.recvfrom(124)
    cur = context.decode().split(",")
    return cur[0], cur[1], cur[2], cur[3], cur[4], cur[5]


if __name__ == '__main__':
    while True:
        print(udp_rx())
