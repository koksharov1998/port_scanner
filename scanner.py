import socket
import argparse
from multiprocessing.dummy import Pool
import multiprocessing

tcp_opened_ports = []
udp_opened_ports = []
address = ""


MIN_PORT = 0
MAX_PORT = 65535

def main():
    global address
    args = parse_args()
    address = args["address"]
    print(address)
    start_position = int(args["start"]) if int(args["start"]) > 0 else 0
    end_position = int(args["end"]) if int(args["end"]) < MAX_PORT else MAX_PORT
    pool = Pool(500)
    pool.map(scan_ports, range(start_position, end_position + 1))
    pool.close()
    pool.join()
    print(f"TCP opened ports: {tcp_opened_ports}")
    print(f"UDP opened ports: {udp_opened_ports}")


def scan_tcp_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((address, port))
            tcp_opened_ports.append(port)
            print(f"TCP port {port} is opened")
        except socket.error:
            pass
            # print(f"TCP port {port} is closed")


def scan_udp_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(1)
        sock.sendto(b'Hi, port!', (address, port))
        try:
            print('Error f' + sock.recvfrom(2048)[0].decode())
            udp_opened_ports.append(port)
            print(f"UDP port {port} is opened")
        except socket.error as e:
            #pass
            if str(e) == 'timed out':
                print(e)
                print(port)
            #print(f"UDP port {port} is closed")


def scan_ports(port):
    scan_tcp_port(port)
    scan_udp_port(port)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-address", help="set ip you want to scan", default="127.0.0.1")
    parser.add_argument("-start", help="set the port to start from for scanner", default=0)
    parser.add_argument("-end", help="set the port to end with for scanner", default=25000)
    return vars(parser.parse_args())


if __name__ == "__main__":
    se = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    se.bind(("localhost", 8080))
    se.setblocking(False)
    print('d')
    main()
    multiprocessing.Process(target=print(se.recvfrom(1024))).start()
    print('2')
