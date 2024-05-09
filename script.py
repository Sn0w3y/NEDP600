import struct
import socket

host = '192.168.178.191'
port = 8899

hex_string = "7937004015000000ffffffffffff0c00eeeeeeeeffffffff010000000000010000c8000000000000000000000000000000000000000000000000dca50000"

payload = bytes.fromhex(hex_string)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(payload)
    print("String successfully sent to the inverter.")

    response = s.recv(1024)

    hex_response = response.hex().upper()


def parse_response(response_bytes):

    if len(response_bytes) < 32:
        raise ValueError("Response too short!")

    header = response_bytes[:2].hex()
    length = struct.unpack(">H", response_bytes[2:4])[0]
    msg_type = response_bytes[4:6].hex()
    status = response_bytes[6:10].hex()
    reserved = response_bytes[10:12].hex()
    sequence = struct.unpack(">H", response_bytes[12:14])[0]
    checksum = response_bytes[14:18].hex()
    device1 = response_bytes[18:20].hex()
    device2 = response_bytes[20:22].hex()
    device3 = response_bytes[22:24].hex()
    device4 = response_bytes[24:26].hex()
    device5 = response_bytes[26:28].hex()
    device6 = response_bytes[28:30].hex()
    device7 = response_bytes[30:32].hex()

    values = []
    for i in range(32, len(response_bytes), 2):
        if i + 1 < len(response_bytes):
            values.append(struct.unpack(">H", response_bytes[i:i + 2])[0])


    byte_value = response_bytes[32]
    interpreted_value = byte_value * 4

    parsed_data = {
        "Header": header,
        "Length": length,
        "Type": msg_type,
        "Status": {
            "Flags": status[:2],
            "Remaining": status[2:]
        },
        "Reserved": reserved,
        "Sequence": sequence,
        "Checksum": checksum,
        "Devices": {
            "Device1": device1,
            "Device2": device2,
            "Device3": device3,
            "Device4": device4,
            "Device5": device5,
            "Device6": device6,
            "Device7": device7
        },
        "Values": values,
        "Interpreted Value": interpreted_value
    }

    return parsed_data


def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)


def main():
    response_bytes = hex_to_bytes(hex_response)

    if response_bytes:
        try:
            interpreted_data = parse_response(response_bytes)
            print("Interpreted Response:")
            for key, value in interpreted_data.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")
                else:
                    print(f"{key}: {value}")
        except ValueError as e:
            print(f"Error parsing response: {e}")
    else:
        print("No response data available.")


if __name__ == "__main__":
    main()
