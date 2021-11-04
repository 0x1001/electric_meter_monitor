from datetime import datetime
import time
import serial
import re
import os

file_path = "/home/pi/gitwork/electric_meter_web/electric_meter/data/meter_data.csv"
meter_device = '/dev/ttyUSB0'

def get_reading():
    CMD = b'/?!\x0D\x0A'

    ser = serial.Serial(meter_device, baudrate=300, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=5)

    first = datetime.now()
    ser.write(CMD)
    energy_1 = _parse_meter_reading(ser.readlines())  # unit kWh

    second = datetime.now()
    ser.write(CMD)
    energy_2 = _parse_meter_reading(ser.readlines())  # unit kWh
    
    power = ((energy_2 - energy_1) / ((second - first).total_seconds()/(60*60))) * 1000  # unit W

    ser.close()
    
    if energy_1 and energy_2:
        return energy_2, power
    else:
        return 0, 0

def _parse_meter_reading(data):
    for line in data:
        line = line.decode('utf-8').strip()
        found = re.match(r'.*\(([\d.]*)\*kWh\)', line)

        if found:
            return float(found.group(1))
            
    return 0

def write_csv(energy, power):
    if not os.path.isfile(file_path):
        with open(file_path, "w") as fp:
            fp.write("\"Date\",\"Total Energy [kWh]\",\"Current Power [W]\"\n")

    with open(file_path, "a") as fp:
        fp.write("\"{0}\",{1},{2}\n".format(datetime.now().strftime("%H:%M:%S %d.%m.%Y"), energy, power))


def main():
    while True:
        energy, power = get_reading()
        if energy:
            print("{0} - Total Energy: {1:.3f} kWh, Current Power: {2:.2f} W".format(datetime.now().strftime("%H:%M:%S %d.%m.%Y"), energy, power))
            write_csv(energy, power)
        else:
            pass  # in case energy is 0, don't log and continue reading

        
if __name__ == "__main__":
    main()