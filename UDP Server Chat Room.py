# from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread

def charToMorse(character):
    morseDict = {' ': " /",        '': "",
                 'a': " .-",
                 'b': " -...",
                 'c': " -.-.",
                 'd': " -..",
                 'e': " .",
                 'f': " ..-.",
                 'g': " --.",
                 'h': " ....",
                 'i': " ..",
                 'j': " .---",
                 'k': " -.-",
                 'l': " .-..",
                 'm': " --",
                 'n': " -.",
                 'o': " ---",
                 'p': " .--.",
                 'q': " --.-",
                 'r': " .-.",
                 's': " ...",
                 't': " -",
                 'u': " ..-",
                 'v': " ...-",
                 'w': " .--",
                 'x': " -..-",
                 'y': " -.--",
                 'z': " --..",
                 '0': " -----",    '1': " .----",
                 '2': " ..---",    '3': " ...--",
                 '4': " ....-",    '5': " .....",
                 '6': " -....",    '7': " --...",
                 '.': " .-.-.-",   ',': " --..--",
                 ':': " ---...",   '?': " ..--..",
                 "'": " .----.",   '-': " -....-",
                 '_': " ..--.-",   '!': " -.-.--"}

    return morseDict[character]

def stringToMorse(string):
    morseMessage = ""
    string = string.lower()
    for letter in string:
        morseMessage = morseMessage + charToMorse(letter)

    return morseMessage

def morseToChar(morse):
    charDict = {'/': " ",        '': "",
                 '.-': "a",
                 '-...': "b",
                 '-.-.': "c",
                 '-..': "d",
                 '.': "e",
                 '..-.': "f",
                 '--.': "g",
                 '....': "h",
                 '..': "i",
                 '.---': "j",
                 '-.-': "k",
                 '.-..': "l",
                 '--': "m",
                 '-.': "n",
                 '---': "o",
                 '.--.': "p",
                 '--.-': "q",
                 '.-.': "r",
                 '...': "s",
                 '-': "t",
                 '..-': "u",
                 '...-': "v",
                 '.--': "w",
                 '-..-': "x",
                 '-.--': "y",
                 '--..': "z",
                 '-----': "0",    '.----': "1",
                 '..---': "2",    '...--': "3",
                 '....-': "4",    '.....': "5",
                 '-....': "6",    '--...': "7",
                 '.-.-.-': ".",   '--..--': ",",
                 '---...': ":",   '..--..': "?",
                 ".----.": "'",   '-....-': "-",
                 '..--.-': "_",   '-.-.--': "!"}

    return charDict[morse]

def morseToString(morse):
    character = ""
    originalMessage = ""

    # To catch the last character, append a space
    morse = morse + " "

    for letter in morse:
        if letter != " ":
            character = character + letter
        else:
            originalMessage = originalMessage + morseToChar(character)
            character = ""

    return originalMessage

global first_send

clients = []

host = ''
port = 55554
server_address = (host, port)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_socket.bind(server_address)
# server_socket.setblocking(0)
print("Starting")

def handle():
    quitting = False
    print("Server Started.")
    # entered_first = True
    # name, addr = server_socket.recvfrom(1024)
    #
    # client_name = morseToString(name.decode('utf8'))
    # print(f"His name is {client_name}")

    # while not quitting:
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)  # Here, 1024 is the buffer, which can be set to any value

            if addr not in clients:
                clients.append(addr)

            print(f"\n\n\nData is {data.decode('utf8')}")
            print(f"Address is {addr}")
            print(f"Clients are {clients}")


            # message = f"{stringToMorse(client_name + ':')} {data.decode('utf8')}"
            # print(f"Message is {message}")

            if ": _quit_" not in data.decode("utf8"):
                print("Not quitting")
                for client in clients:
                    server_socket.sendto(data, client)
            else:
                print("Ata3 1")
                name_client = data.decode('utf8').split(':')[0]
                print("Ata3 2")
                print(f"Client's name is {name_client}")
                print("Ata3 4")
                for client in clients:
                    print(f"Sending to {client}")
                    # if client != addr:
                    #     print("Ata3 5")
                    server_socket.sendto(stringToMorse(f"{name_client} has left the chat.").encode("utf8"), client)
                print("Quitting")
                # del clients[addr]
                # print(f"Clients are now {clients}")
                # quitting = True
        except:
            pass


if __name__ == "__main__":
    accepting_thread = Thread(target=handle)
    accepting_thread.start()
    accepting_thread.join()
    server_socket.close()


# def accept_incoming_connections():
#     """Sets up handling for incoming clients."""


        # client_name, client_address = server_socket.recvfrom(1024)
        # client_name = client_name.decode('utf8')
        # client = (client_name, client_address)
        # print(f"Client is is {client}")
        # print(f"{client_address} connected.")
        # addresses[client] = client_address


# def handle_client():  # Takes client socket as argument.
#     """Handles a single client connection."""
#     while True:
#         client_name, address = server_socket.recvfrom(1024)
#         client_name = client_name.decode("utf8")
#         print(f"Handled {client_name}")
#         client = (client_name, address)
#         global clients_list
#         print(clients_list)
#         if address not in addresses:
#             addresses.append(address)
#             clients_list[address] = client_name
#             print(f"Added {client} to list")
#             Thread(target=start_client, args=(client,)).start()
#
# def start_client():
#     # client_name, address = server_socket.recvfrom(1024)
#
#     # if address not in addresses:
#     #     client_name = client_name.decode("utf8")
#     #     print(f"Handled {client_name}")
#     #     client = (client_name, address)
#     #     global clients_list
#     #     print(clients_list)
#     #     addresses.append(address)
#     #     clients_list[address] = client_name
#     #     print(f"Added {client} to list")
#
#         client_name = morseToString(client_name)
#         print(f"{client_name} has joined the chat!")
#         join_msg = stringToMorse(f"{client_name} has joined the chat!")
#         broadcast(join_msg.encode("utf8"))
#
#         while True:
#             msg, address = server_socket.recvfrom(1024)
#
#             if msg.decode("utf8") != "_quit_":
#                 print(f"{client_name} is now sending")
#                 broadcast(msg, client_name + ": ")
#             else:
#                 del clients[client]
#                 del clients_list[address]
#                 broadcast(stringToMorse(f"{client_name} has left the chat.").encode("utf8"))
#                 break

    # Runs only once to get the name of the person, and then stays in the while loop
    # addresses[name] = address
    # clients_lists[client] = name
    # print(f"\nClients are {clients}")
    # print(f"\nAddresses are: {addresses}\n")



#
# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""
#     prefix = stringToMorse(prefix)
#     global clients_list
#     global clients
#
#     print(f"Clients are: {clients}")
#     print(f"Client lists is: {clients_list}")
#     for client in clients:
#         sock.sendto(prefix.encode("utf8")+msg, client)
#
# def main():
#     global first_send
#     global client_name
#     client_name = ""
#     first_send = True
#
#
# addresses = []
# global client_name
#
#
#
#
# def do():
#     while True:
#         name, address = server_socket.recvfrom(1024)
#         client = (name, address)
#         clients[client] = name
#         global addresses
#         print(addresses)
#         if address not in addresses:
#             addresses.append(address)
#             name = name.decode('utf8')
#             name = morseToString(name)
#             clients_list[address] = name
#             global client_name
#             client_name = name
#             client = (name, address)
#             print(f"Added {client} to list")
#             print(f"{name} has joined the chat!")
#             join_msg = stringToMorse(f"{client_name} has joined the chat!")
#             broadcast(join_msg.encode("utf8"))
#
#         while True:
#             msg, address = server_socket.recvfrom(1024)
#             if msg.decode("utf8") != "_quit_":
#                 print(f"{client_name} is now sending")
#                 broadcast(msg, client_name + ": ")
#             else:
#                 del clients[client]
#                 del clients_list[address]
#                 broadcast(stringToMorse(f"{client_name} has left the chat.").encode("utf8"))
#                 break
#
#
#
# if __name__ == "__main__":
#     global first_send
#     global clients_list
#     clients_list = {}
#     first_send = True
#     print("Waiting for connection...")
#     accepting_thread = Thread(target=do)
#     accepting_thread.start()
#     accepting_thread.join()
#     server_socket.close()