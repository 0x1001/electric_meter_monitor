from datetime import datetime
import time
import serial
import re
import os

file_path = "/home/pi/gitwork/electric_meter_web/electric_meter/data/meter_data.csv"
meter_device = '/dev/ttyUSB0'

class Meter:
    def __init__(self):
        self.last_energy_value = None
        self.last_time = None
        
    def get_reading(self):
        CMD = b'/?!\x0D\x0A'

        ser = serial.Serial(meter_device, baudrate=300, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=6)

        read_time = datetime.now()
        ser.write(CMD)
        energy_value = _parse_meter_reading(ser.readlines())  # unit kWh

        if self.last_energy_value is None:
            print("First reading..")
            self.last_energy_value = energy_value
            self.last_time = read_time
            
            read_time = datetime.now()
            ser.write(CMD)
            energy_value = _parse_meter_reading(ser.readlines())  # unit kWh
        
        power = ((energy_value - self.last_energy_value) / ((read_time - self.last_time).total_seconds()/(60*60))) * 1000  # unit W
        
        self.last_energy_value = energy_value
        self.last_time = read_time
        
        ser.close()
        
        if self.last_energy_value and energy_value:
            return energy_value, power
        else:
            self.last_energy_value = None
            self.last_time = None
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
    meter = Meter()
    
    while True:
        try:
            energy, power = meter.get_reading()
        except Exception as error:
            print("Unexpected error while reading meter: {0}".format(error))
            energy = None

        if energy:
            print("{0} - Total Energy: {1:.3f} kWh, Current Power: {2:.2f} W".format(datetime.now().strftime("%H:%M:%S %d.%m.%Y"), energy, power))
            write_csv(energy, power)
        else:
            print("No data :(")
            # in case energy is 0, don't log and continue reading
        
        time.sleep(30)

        
if __name__ == "__main__":
    main()