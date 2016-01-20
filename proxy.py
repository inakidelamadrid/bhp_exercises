import sys
import socket
import threading


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """
        Args.
        client_socket(socket.Socket): keeps connection between proxy and
        the local client
    """

    # create the remote socket
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)


def server_loop(local_host, local_port, remote_host, remote_port,
                receive_first):
    """
    The proxy is represented by the local host and port. The remote host and
    port represent the service's server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))  # argument is a tuple
    except:
        # I recomment using port 3000 or greater
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host, local_port)
    server.listen(5)

    while(True):
        client_socket, addr = server.accept()
        # print out info of the local socket assigned
        print "[==>] Received incoming connection from %s:%d" % (
            addr[0], addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        # check above that proxy_handler is a function defined before this call
        # to threading.Thread
        proxy_thread.start()
