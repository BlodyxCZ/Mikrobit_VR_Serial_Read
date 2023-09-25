import serial
import json

ser = serial.Serial('COM6', 115200)
d_path = "C:\\Users\\kjube\\AppData\\Roaming\\Godot\\app_userdata\\VR Space Driver\\"
device = "Gun"


def strtobool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        return False


while True:
    try:
        data = ser.readline().strip()
        if len(data) > 50:
            break
        data = str(data)
        data = data.lstrip("b'")
        data = data.rstrip("'")
        if data[:1] == "G":
            device = "Gun"
            data = data.lstrip("G")
            data = data.split(",")
            if len(data) != 11:
                break
            json_data = {"raw": data[0], "pitch": data[1], "rotation": data[2], "vel_x": data[3],
                         "vel_z": data[4], "A": strtobool(data[5]), "B": strtobool(data[6]),
                         "C": strtobool(data[7]), "D": strtobool(data[8]), "E": strtobool(data[9]),
                         "F": strtobool(data[10]), "device": device}
        else:
            device = "Head"
            data = data.lstrip("H")
            data = data.split(",")
            if len(data) != 4:
                break
            json_data = {"raw": data[0], "pitch": data[1], "vel_y": data[2], "rotation": data[3],
                         "device": device}

        path = d_path + device + ".txt"
        with open(path, "w") as f:
            f.write(json.dumps(json_data))
        print(json.dumps(json_data))

    except UnicodeDecodeError:
        print("Error reading the serial line...")
