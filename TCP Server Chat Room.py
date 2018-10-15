from socket import AF_INET, socket, SOCK_STREAM
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

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = server_socket.accept()
        print(f"Client is {client}")
        print(f"Client address is {client_address}")
        print(f"{client_address} connected.")
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    # Runs only one to get the name of the person, and then stays in the while loop
    name = client.recv(1024).decode("utf8")
    name = morseToString(name)
    print(f"{name} has joined the chat!")
    join_msg = stringToMorse(f"{name} has joined the chat!")
    broadcast(join_msg.encode("utf8"))
    clients[client] = name

    while True:
        msg = client.recv(1024)

        if msg.decode("utf8") != "_quit_":
            broadcast(msg, name+": ")
        else:
            del clients[client]
            broadcast(stringToMorse(f"{name} has left the chat.").encode("utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    print(f"Prefix before is {prefix}")
    prefix = stringToMorse(prefix)
    print(f"Prefix after is {prefix}")
    for sock in clients:
        sock.send(prefix.encode("utf8")+msg)

def main():
    global first_send
    first_send = True


clients = {}
addresses = {}

host = ''
port = 55554
server_address = (host, port)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(server_address)

if __name__ == "__main__":
    server_socket.listen(5)
    print("Waiting for connection...")
    accepting_thread = Thread(target=accept_incoming_connections)
    accepting_thread.start()
    accepting_thread.join()
    server_socket.close()