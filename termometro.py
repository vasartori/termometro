import datetime
import time

import serial


class PortNotOpen(Exception):
    pass

class SerialPortError(Exception):
    pass


def read_data_from_termo():
    serial_port = '/dev/ttyACM0'
    baudrate = 9600

    try:
        s = serial.Serial(port=serial_port, baudrate=baudrate)
    except BaseException as e:
        raise SerialPortError(e)

    if not s.isOpen():
        raise PortNotOpen("The port {} is not open".format(serial_port))
    s.flushOutput()
    return s.read(11).split(',')


def format_temp():
    temp = read_data_from_termo()
    return ",".join(
        ["{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),
         temp[0],
         temp[1]])


def write_temp_on_file():
    with open('temperaturas.csv', "a") as temp_file:
        temp_file.write(format_temp() + "\r\n")


if __name__ == '__main__':
    while True:
        try:
            write_temp_on_file()
            time.sleep(60)
        except BaseException as e:
            print("ERROR - {}".format(e))
            time.sleep(1)