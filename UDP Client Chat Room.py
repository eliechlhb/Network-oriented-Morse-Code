# from socket import AF_INET, socket, SOCK_STREAM
import socket
import time
from threading import Thread
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os
import pyttsx3
import speech_recognition as sr

global first_send
global name

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
                 '8': " ---..",    '9': " ----.",
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

def receive():
    print("Received outside of while")
    """Handles receiving of messages."""
    global name

    while True:
        print("Received inside of while")
        try:
            msg, server = client_socket.recvfrom(1024)
            msg = msg.decode("utf8")
            string_msg = morseToString(msg)

            print(f"\nMessage is {string_msg}\n")
            print(f"My name is {my_name.lower()}")
            print(f"Name is {string_msg.split(' has')[0]}")
            # Show joined chat message only to other clients
            if "has joined the chat!" in string_msg:
                if  my_name.lower() != string_msg.split(' has')[0]:
                    print("Not the same person")
                    msg_list.insert(tkinter.END, string_msg)
            else:
                print("This is the same person")
                if "from textfile" not in string_msg and "from mic" not in string_msg:
                    print("Normal input")
                    msg_list.insert(tkinter.END, string_msg)
                
                else:
                    if "from mic"  in string_msg:
                        print("Voice input")
                        
                        # Take the person's name
                        person_name = string_msg.split(':')[0]
                        message = f"{person_name}: Audio..."
                        msg_list.insert(tkinter.END, message)
                        
                        # Speak the message if it's not the user who sent it
                        #global name
                        if my_name.lower() != string_msg.split(':')[0]:
                            print(f"Name is {my_name}")
                            print(f"String is {string_msg.split(':')[0]}")
                            #engine = pyttsx3.init("sapi5");
                            engine = pyttsx3.init()
                            text = string_msg.split('mic: ')[1].lstrip(string_msg.split('from mic')[0])
                            print(f"The text is {text}")
                            engine.say(text);
                            engine.runAndWait() ;
                        
                    else:
                        print("File input")
                        # Take the person's name and the message after 'from textfile *.txt: "
                        message = string_msg.split(':')[0] + ": " + string_msg.split('.txt: ')[-1]
                        msg_list.insert(tkinter.END, message)                        # Write the message to a file if it's not the user who sent it
                        if my_name != string_msg.split(':')[0]:
                            filename = string_msg.split('.txt')[0].lstrip(string_msg.split('from textfile ')[0])
                            print(filename)
                            filename = filename.lstrip('from textfile ') + ".txt"
                            with open(filename, "w") as text_file:
                                print(message.split(': ')[-1], file=text_file)
##                if "from textfile" not in string_msg:
##                    print("Normal input")
##                    msg_list.insert(tkinter.END, string_msg)
##                else:
##                    print("File input")
##                    # Take the person's name and the message after 'from textfile *.txt: "
##                    message = string_msg.split(':')[0] + ": " + string_msg.split('.txt: ')[-1]
##                    msg_list.insert(tkinter.END, message)
##
##                    # Write the message to a file if it's not the user who sent it
##                    global name
##                    if my_name != string_msg.split(':')[0]:
##                        filename = string_msg.split('.txt')[0].lstrip(string_msg.split('from textfile ')[0])
##                        print(filename)
##                        filename = filename.lstrip('from textfile ') + ".txt"
##                        with open(f"{filename}", "w") as text_file:
##                            print(message.split(': ')[-1], file=text_file)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    global first_send
    global name

##    if msg == "_quit_":
##        client_socket.sendto((my_name + ': _quit_').encode("utf8"), server_address)
##        client_socket.close()
##        top.quit()
##    elif msg:
##        print(f"Now sending by: {ADDR}")
##        print(f"Sending {msg}")
##        client_socket.sendto(stringToMorse(my_name + ': ' + msg).encode("utf8"), server_address)

    if msg != "_quit_" and msg != "_voice_":
          client_socket.sendto(stringToMorse(my_name + ': ' + msg).encode("utf8"), server_address)
    else:
      if msg == "_quit_":
          top.destroy()
          client_socket.sendto((my_name + ': _quit_').encode("utf8"), server_address)
          client_socket.close()
          #top.quit()


      elif msg == "_voice_":
      
           # get audio from the microphone
           r = sr.Recognizer()
           with sr.Microphone() as source:
               print("Speak:")
               audio = r.listen(source)

           try:
               print( my_name, " recorded : " + r.recognize_google(audio))
               my_msg.set("From mic: " + r.recognize_google(audio))
               #client_socket.send(stringToMorse(r.recognize_google(audio)).encode("utf8"))
           except sr.UnknownValueError:
               print("Could not understand audio")
           except sr.RequestError as e:
               print("Could not request results; {0}".format(e))

def browse(event=None):
    print("Pressed open")
    fname = askopenfilename(filetypes=(("All files", "*.*"),
                                       ("HTML files", "*.html;*.htm")))
    if fname:
        try:
            print(f"File name is: {fname}")
            file = open(fname)
            global file_name
            file_name = os.path.basename(os.path.normpath(fname))
            messages = ""
            count_lines = 0
            for line in file:
                count_lines = count_lines + 1
                if line != "\n":
                    print(line)
                    messages = messages + line

                if count_lines > 1:
                    messages = messages + ". "

            if count_lines > 1:
                messages = messages.rstrip('. ')

            messages = messages.replace("\n", "")
            my_msg.set("From textfile " + file_name +  ": " + messages)
        except:  # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("_quit_")
    send()

def main():
    global first_send
    global name
    global file_name
    first_send = True
    file_name = ""

global first_send
first_send = True

top = tkinter.Tk()
top.title("EEN 442 Chat Room")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=35, width=130, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
msg_list.insert(tkinter.END, "Welcome to the EEN 442 Chat Room!")
msg_list.insert(tkinter.END, "-----------------------------------------------------------------------------")

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
send_button = tkinter.Button(top, text="Send", command=send)
open_button = tkinter.Button(top, text="Open", command=browse)

open_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
send_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
entry_field.pack(side=tkinter.BOTTOM, fill=tkinter.X)

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter host: ')
PORT = input('Enter port: ')
PORT = int(PORT)
my_name = input('Enter username: ')
ADDR = (HOST, PORT)
server_address = (HOST, 55554)
print(ADDR)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.bind(('', PORT))

msg_list.insert(tkinter.END, f"Welcome {my_name}! If you ever want to quit, type _quit_ to exit.")
top.title(f"EEN 442 Chat Room - {my_name}")
msg_list.insert(tkinter.END, "-----------------------------------------------------------------------------")



receive_thread = Thread(target=receive)
client_socket.sendto(stringToMorse(f"{my_name} has joined the chat!").encode("utf8"), server_address)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

