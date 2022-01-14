"""
The bytestream consists of 74 byte long messages wrapped in curly braces (`{` (0x7b) and `}` (0x7d)).

7B 9E 84 84  D0 85 80 EE  81 81 81 80  81 94 8A 80
81 96 82 8A  82 8E 86 81  81 80 8A 80  8A 80 8C B2
80 82 95 87  CC 80 80 80  80 8D CF 80  BA 83 D8 83
D6 80 80 80  80 80 80 80  80 80 80 80  80 80 80 80
80 80 80 80  80 80 81 8F  A4 38 30 7D

The last two bytes each contain 4 bits of the 8-bit checksum of the first 72 bytes:

(0x9e + 0x84 + … + 0x8f + 0xa4) % 0x100 = 0x80 -> 0x38 0x30
The 72 data-bytes all have their high 0x80 bit set, they only contains 7 bits of data each. For the rest of this discussion,
I’m only referring to the lower 7 bits of each byte. Here are the data-pieces that I discovered.
Byte numbers start at 0 for the first data byte (i.e. 0x9e in the example above).

Byte 7 contains part of the state
bit 0x01 is set when charging, clear when discharging
bit 0x10 is set when cycling, clear when single charging or discharging
Byte 8 contains the set NiCd charge current in dA
Byte 9 contains the set NiCd discharge current in dA
Byte 12 contains the set NiMH charge current in dA
Byte 13 contains the set NiMH discharge current in dA
Byte 14, bit 0x01 contains the cycle mode, set for {Charge,Discharge}, clear for {Discharge,Charge}
Byte 15 contains the cycle count
Byte 16 contains the set Li__ charge current in dA
Byte 17 contains the set Li__ charge cell count
Byte 18 contains the set Li__ discharge current in dA
Byte 19 contains the set Li__ discharge cell count
Byte 20 contains the set Pb charge current in dA
Byte 21 contains the set Pb cell count
Byte 22 contains the mode:
    0x80: Config
    0x81: Li
    0x82: NiMH
    0x83: NiCd
    0x84: Pb
    0x85: Save
    0x86: Load
Byte 23 contains the running state: bit 0x01 is set when running, cleared when standby
Byte 24 & 25 contain the set NiMH discharge voltage in daV and cV
Byte 26 & 27 contains the set NiCd discharge voltage in daV and cV
Byte 32 & 33 contain the actual current in A and cA
Byte 34 & 35 contain the catual voltage in V and cV
Byte 40 & 41 contain the input voltage in V and cV
Byte 42 & 43 contain the charge in dAh and mAh
Bytes 44 & 45; 46 & 47; 48 & 49; 50 & 51; 52 & 53; 54 & 55 contain the individual Li__ cell voltages in V and cV
Byte 69 contains the time in minutes
"""

import serial

def serial_init():
    ser = serial.Serial(
        port='COM13',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        #timeout=10
    )
    return ser


try:
    com = serial_init()
    data = bytes()
    ck_sum = bytes()
    while True:
        while True:
            if com.read() == bytes.fromhex("7B"):
                data = com.read(74)
                ck_sum = sum(data[:72]) % 0x0100
                ck_byte1 = (data[72] & 0x0F) << 4
                ck_byte2 = data[73] & 0x0F
                ck_byte = ck_byte1 | ck_byte2
                if ck_byte == ck_sum:
                    print(data)
                else:
                    print("Checksum error")

    com.close()
except serial.SerialException:
    print("Can't open port")





# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
