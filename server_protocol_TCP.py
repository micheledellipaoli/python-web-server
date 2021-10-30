from socket import *
from cryptography.fernet import Fernet
from _thread import *

# Creazione di fernet_object originato da una key
key = b"x2pXHXqCcUGjcq4HTcvdqH5xSEF_SLATO6p1Xk3tejM="
fernet_object = Fernet(key)

password_to_compare = "pippo"


def thread_server(connection, client_TCP):
    address_client_TCP = client_TCP[0]
    port_client_TCP = client_TCP[1]
    print("Server - connessione stabilita con: \nAddress IP: " + address_client_TCP + " , port: " + str(port_client_TCP) + "\n\n")

    message_received = ""
    loop = True
    client_name = ""

    while loop:
                # il server riceve un messaggio dal client con cui ha instaturato la connessione
                bytesReceived = connection.recvfrom(2048)[0]
                decrypted_message = fernet_object.decrypt(bytesReceived)
                message_received = decrypted_message.decode()

                print("Server - Messaggio ricevuto da [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "]:\n    " + str(message_received) + "\n")

                words = message_received.split("|")

                if words[0] == "DCN":
                    # il server memorizza il nome ed il cognome nella variabile client_name
                    client_name = words[1]
                    client_name.replace("-", " ")


                if words[0] == "DCP":
                    if words[1] == password_to_compare:
                        # il server invia un messaggio di risposta al client
                        message_to_send = "DCR|Benvenuto-" + client_name
                        encrypted_message = fernet_object.encrypt(message_to_send.encode())
                        connection.sendto(encrypted_message, (address_client_TCP, port_client_TCP))
                        print("Server - Messaggio di risposta inviato a [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "]:\n    " + str(message_to_send) + "\n")
                    else:
                        # il server invia un messaggio di risposta al client
                        message_to_send = "DCE|Utente-non-riconosciuto"
                        encrypted_message = fernet_object.encrypt(message_to_send.encode())
                        connection.sendto(encrypted_message, (address_client_TCP, port_client_TCP))
                        print("Server - Messaggio di risposta inviato a [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "]:\n    " + str(message_to_send) + "\n")
                        print("Server - Connessione con il client [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "] chiusa.\n")
                        print("-----------------------------------------------------------\n")
                        connection.close()
                        loop = False
                        break


                if words[0] == "DCM":
                    message_to_send = message_received
                    encrypted_message = fernet_object.encrypt(message_to_send.encode())
                    # il server invia un messaggio di risposta al client
                    connection.sendto(encrypted_message, (address_client_TCP, port_client_TCP))
                    print("Server - Messaggio di risposta inviato a [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "]:\n    " + str(message_to_send) + "\n")


                if words[0] == "DCQ":
                    print("Server - Connessione con il client [" + str(address_client_TCP) + ", port: " + str(port_client_TCP) + "] chiusa.\n")
                    print("-----------------------------------------------------------\n")
                    connection.close()
                    loop = False
                    break

                if words[0] != "DCN" and words[0] != "DCP" and words[0] != "DCM" and words[0] != "DCQ":
                    print("Client - Comando non valido.\n")
                    connection.close()
                    loop = False
                    break



def server_protocol_TCP():
    local_ip = '127.0.0.1'
    local_port = 8004

    threadCount = 0


    # creazione dell'oggetto Socket per il server (AF_INET indica l'utilizzo di IPv4, SOCK_STREAM indica pacchetti per TCP)
    server_socket_TCP = socket(AF_INET, SOCK_STREAM)

    # attivazione del socket sull'indirizzo 'local_ip', che riceve sulla porta 'local_port'
    server_socket_TCP.bind((local_ip, local_port))

    # il server è in continuo ascolto (while) di richieste di connessioni da parte del client
    server_socket_TCP.listen(1)
    print("\nServer TCP attivo ed in ascolto.\n")
    print("-----------------------------------------------------------\n")

    while True:
        # il server, che è in ascolto, accetta la connessione con un client
        connection, client_TCP = server_socket_TCP.accept()

        start_new_thread(thread_server, ((connection, client_TCP)))
        threadCount = threadCount + 1


def main():
    server_protocol_TCP()

if __name__ == "__main__":
    main()