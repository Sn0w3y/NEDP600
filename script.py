import socket

# IP-Adresse und Port des Wechselrichters
host = '10.10.100.254'
port = 8899

# Der Hexadezimal-String für 800W
hex_string = "7937004015000000ffffffffffff0c00eeeeeeeeffffffff010000000000010000c8000000000000000000000000000000000000000000000000dca50000"

# Konvertieren des Hexadezimal-Strings in Bytes
payload = bytes.fromhex(hex_string)

# Senden des Byte-Strings an den Wechselrichter über den Socket und auf eine Antwort warten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(payload)
    print("String erfolgreich an den Wechselrichter gesendet.")

    # Auf eine Antwort vom Wechselrichter warten
    response = s.recv(1024)  # Empfange bis zu 1024 Bytes
    print("Antwort vom Wechselrichter:", response.decode())
