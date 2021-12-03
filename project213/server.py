import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from remote_keyboard import IP_ADDRESS, PORT
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller

SERVER = None
Port = 8000
IP_ADDRESS = "192.168.0.111"
screen_width = None
screen_height = None

Keyboard = Controller()


def acceptConnection():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection ESTABLISHED WITH {client_socket}:{addr}")
        thread1 = Thread(target=recvMessage, args=(client_socket))
        thread1.start()

def getDeviceSize():
    global screen_height
    global screen_width

    for m in get_monitors():
        screen_width = int(str(m).split(',')[2].strip().split('width=')[1])
        screen_height = int(str(m).split(',')[3].strip().split('heigth=')[1])

def recvMessage(client_socket):
    global Keyboard

    while True:
        try:
            message = client_socket.recv(2048).decode()

            if(message):
                Keyboard.press(message)
                Keyboard.release(message)

                print(message)

        except Exception as error:
            pass               

def setup():
    print('\n\t\t\t\t\t^^^ Welcome To Remote Keyboard ^^^\n')
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print('\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n')
    getDeviceSize()
    acceptConnection()

setup()
