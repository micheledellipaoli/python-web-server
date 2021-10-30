from socket import *
from cryptography.fernet import Fernet


def client_protocol_TCP():
    server_name = '127.0.0.1'
    server_port = 8004

    # Creazione di fernet_object originato da una key_word
    key = b"x2pXHXqCcUGjcq4HTcvdqH5xSEF_SLATO6p1Xk3tejM="
    fernet_object = Fernet(key)

    # creazione dell'oggetto Socket per il client (AF_INET indica l'utilizzo di IPv4, SOCK_STREAM indica pacchetti per TCP)
    client_socket_TCP = socket(AF_INET, SOCK_STREAM)

    #il client avvia una connessione con il server
    client_socket_TCP.connect((server_name, server_port))
    print("\nClient - Connessione con il server stabilita.\n")

    loop = True

    while loop:
        command = input("---------------------------------------\n"
                        "1: Invia nome e cognome dell'Utente.\n"
                        "2: Invia password dell'Utente.\n"
                        "3: Invia un messaggio.\n"
                        "4: Chiudi connessione.\n"
                        "---------------------------------------\n\n"
                        "Seleziona un comando: "
                        )

        if command == "1":
            message1 = input("Scrivi il tuo nome: \n")
            message2 = input("Scrivi il tuo cognome: \n")

            message_to_send = "DCN|" + message1.replace(" ", "-") + "-" + message2.replace(" ", "-")
            encrypted_message = fernet_object.encrypt(message_to_send.encode())

            # il client invia un messaggio al server
            client_socket_TCP.sendall(encrypted_message)
            print("\nClient - Nome e cognome inviati:\n    " + str(message_to_send) + "\n")

        if command == "2":
            message1 = input("Scrivi password utente: \n")

            message_to_send = "DCP|" + message1.replace(" ", "-")
            encrypted_message = fernet_object.encrypt(message_to_send.encode())

            # il client invia un messaggio al server
            client_socket_TCP.sendall(encrypted_message)
            print("\nClient - password inviata:\n    " + str(message_to_send) + "\n")

            # il client riceve un messaggio di risposta dal server con cui ha instaturato la connessione
            bytesReceived = client_socket_TCP.recvfrom(2048)[0]

            decrypted_message = fernet_object.decrypt(bytesReceived)
            message_received = decrypted_message.decode()

            print("Client - Messaggio di risposta ricevuto:\n    " + str(message_received) + "\n")

            words = message_received.split("|")

            if words[0] == "DCE":
                print("\nClient - Connessione con il server chiusa.\n")
                print("-----------------------------------------------------------\n")
                client_socket_TCP.close()
                loop = False
                break

        if command == "3":
            message = input("Scrivi un messaggio da inviare:\n ")

            message.replace(" ", "-")
            message_to_send = "DCM|" + message
            encrypted_message = fernet_object.encrypt(message_to_send.encode())

            # il client invia un messaggio al server
            client_socket_TCP.sendall(encrypted_message)
            print("\nClient - messaggio inviato:\n    " + str(message_to_send) + "\n")

            # il client riceve un messaggio di risposta dal server con cui ha instaturato la connessione
            bytesReceived = client_socket_TCP.recvfrom(2048)[0]
            decrypted_message = fernet_object.decrypt(bytesReceived)
            message_received = decrypted_message.decode()
            print("Client - Messaggio di risposta ricevuto:\n    " + str(message_received) + "\n")

        if command == "4":
            message_to_send = "DCQ|"
            encrypted_message = fernet_object.encrypt(message_to_send.encode())

            # il client invia un messaggio al server
            client_socket_TCP.sendall(encrypted_message)
            print("\nClient - Connessione con il server chiusa.\n")
            print("-----------------------------------------------------------\n")
            client_socket_TCP.close()
            loop = False
            break

        if command != "1" and command != "2" and command != "3" and command != "4":
            print("Client - Comando non valido.\n")



def main():
    client_protocol_TCP()

if __name__ == "__main__":
    main()