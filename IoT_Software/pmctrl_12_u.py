#intgrating the mmctrl_1 and P19
#need to do !
# LBS11,12,21,22,13,23 MAPPING NEED TO BE DONE
# AND ALSO  incoming_breakers_list NEEDES TO BE MODIFIED WITH THE MBREG ADDRESS
# AND ALSO  NEEDS TO BE MODIFIED

import socket
import time
import RPi.GPIO as GPIO
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient  # initialize a serial RTU client instance

# Pin Definitons:
GPIO.setwarnings(False)
led1 = 23  # Broadcom pin 23 (P1 pin 16)
led2 = 24  # Broadcom pin 24 (P1 pin 18)
# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(led1, GPIO.OUT)  # LED1 pin set as output
GPIO.setup(led2, GPIO.OUT)  # LED2 pin set as output
# Initial state for LEDs:
GPIO.output(led1, GPIO.LOW)
GPIO.output(led2, GPIO.LOW)


client = ModbusClient(method="rtu", port='/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.25, rtscts=1)


'''
client = ModbusClient(method="rtu", port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.25, rtscts=1)
'''

# client = ModbusClient(method = "rtu", port='COM08', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.25, rtscts=1)


MBREG = [0] * 120
rows, cols = 26, 4
breaker_list = [[0 for _ in range(cols)] for _ in range(rows)]
ModbusError_Flag = 1

def SendTOMaster1(message):
    print("Sending info to the Master - 1")
    host = '10.172.11.6'  # Get local machine name 102 it was in can bus , 101 it will be outside
    port = 50763  # port
    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:  # socket.error, msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    try:
        s.connect((host, port))
        s.send(str(message).encode())
        print('\n sent')
    except Exception as e:
        print("something's wrong with %s:%d. Exception is %s" % (host, port, e))
        time.sleep(1)
        s.close()
        # print 'Message send successfully'
    return


def SendTOMaster2(message):
    print("Sending info to the Master - 2")
    host = '10.171.4.35'  # Get local machine name 102 it was in can bus , 101 it will be outside
    port = 50763  # port
    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:  # socket.error, msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    try:
        s.connect((host, port))
        s.send(str(message).encode())
        print('\n sent')
    except Exception as e:
        print("something's wrong with %s:%d. Exception is %s" % (host, port, e))
        time.sleep(1)
        s.close()
        # print 'Message send successfully'
    return

def SendTOMaster3(message):
    print("Sending info to the Master - 3")
    host = '10.174.5.6'  # Get local machine name 102 it was in can bus , 101 it will be outside
    port = 50763  # port
    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:  # socket.error, msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    try:
        s.connect((host, port))
        s.send(str(message).encode())
        print('\n sent')
    except Exception as e:
        print("something's wrong with %s:%d. Exception is %s" % (host, port, e))
        time.sleep(1)
        s.close()
        # print 'Message send successfully'
    return


def int_to_bcd(x):
    if x < 0:
        raise ValueError("Cannot be a negative integer")

    bcdstring = ''
    if x == 0:
        bcdstring = '0'
    while x > 0:
        nibble = x % 16
        bcdstring = str(nibble) + bcdstring
        x >>= 4
    return int(bcdstring)


def int16Handle(x):
    if x > 32767:
        x = x - 65536
    return x

'''
def Read_Breaker_details():
    global ModbusError_Flag
    Data = []
    TempData = []
    index1 = 0
    for Index in range(0, 8):
        result = client.read_holding_registers(Index*16, 16, unit=1)
        print("result=",result)
        if result:
            TempData.append(result.registers)
            print(TempData)
            for J in range(0, 16):
                Data.append(int16Handle(TempData[index1][J]))
            index1 = index1 + 1
    #if (len(Data) == 102): #102 ( 24*4 = 96 | 3*2 RSS incoming circuits so totaly 102 )
    if (len(Data) == 127):  # 102 ( 24*4 = 96 | 3*2 RSS incoming circuits so totaly 102 )
        global MBREG
        MBREG = []
        for index in range(0, 127):
            MBREG.append(Data[index])
            ModbusError_Flag = 0
    print("MODBUS READ SUCCESSFUL")

'''

def Read_Breaker_details():
    try:
        global ModbusError_Flag
        Data = []
        TempData = []
        index1 = 0
        for Index in range(0, 8):
            result = client.read_holding_registers(Index * 16, 16, unit=2)
            if result:
                TempData.append(result.registers)
                # print(TempData)
                for J in range(0, 16):
                    Data.append(int16Handle(TempData[index1][J]))
                index1 = index1 + 1
        #if (len(Data) == 102): #102 ( 24*4 = 96 | 3*2 RSS incoming circuits so totaly 102 )
        # print("Data leng=",len(Data))
        if (len(Data) == 128):  # 102 ( 24*4 = 96 | 3*2 RSS incoming circuits so totaly 102 )
            global MBREG
            MBREG = []
            for index in range(0, 127):
                MBREG.append(Data[index])
                ModbusError_Flag = 0
        print("MODBUS READ SUCCESSFUL")
    except:
        print("MODBUS ERROR ...")
        ModbusError_Flag = 1



def FrameBreakerSeq():
    global ModbusError_Flag

    if (ModbusError_Flag == 0):
        global MBREG
        global breaker_list

        z = 0 # this required because the we are reading from 480 but actual registers starts from 500
        for tkd in range(0,127):
            if(MBREG[tkd]==2): MBREG[tkd] = 1
            elif(MBREG[tkd]==1):MBREG[tkd] = 0
            else:MBREG[tkd] = 0
        for x in range(0, 26):
            for y in range(0, 4):
                breaker_list[x][y] = MBREG[z]
                #print(breaker_list[x][y])
                z = z + 1
    #return breaker_list


def CompileMasterMessage(rss_slaves,MID): #MID - Master ID
    star_code = '329'
    Master_id = MID
    end_code = '829'
    slaves_len = 0
    Master_Message = ""
    for x in range(0, len(rss_slaves)):
        if(rss_slaves[x] != 0):
            Master_Message = Master_Message + str(x+1).zfill(2)
            slaves_len = slaves_len + 1
            if(slaves_len >= 16): slaves_len = 16 #restricsted for 16 slaves
    Master1Message_index = star_code + Master_id + str(slaves_len).zfill(2)
    Master_Message = Master1Message_index + Master_Message[0:32]
    # adding the padding zeros
    for x in range(0, (16 - slaves_len)):
        Master_Message = Master_Message + '00'
    Master_Message = Master_Message + end_code
    #print(Master_Message)
    #print(len(Master_Message))
    return Master_Message

def station_id_to_slave_id(station_string):

    # Extract parts of the string
    starting_id = station_string[:3]
    master_id = station_string[3:5]
    slaves_connected = station_string[5:7]
    device_connected = station_string[7:39]
    ending_id = station_string[39:]

    # Split device connected section into a list of 2-digit values
    device_ids = [device_connected[i:i+2] for i in range(0, len(device_connected), 2)]

    # Define the mapping rules
    # 00 will be used for non installed location
    # Slave ID location will be provided
    mapping = {
        "01": "00",
        "02": "01",
        "03": "02",
        "04": "03",
        "05": "04",
        "06": "05",
        "07": "06",
        "08": "07",
        "09": "00",
        "10": "08",
        "11": "09",
        "12": "00",
        "13": "00",
        "14": "10",
        "15": "00",
        "16": "11",
        "17": "12",
        "18": "13",
        "19": "14",
        "20": "15",
        "21": "00",
        "22": "00",
        "23": "00",
        "24": "00",
        "25": "16",
    }

    # Apply mapping
    mapped_devices = [mapping.get(device, device) for device in device_ids]

    # Remove unwanted "00" values
    filtered_devices = [device for device in mapped_devices if device != "00"]

    # Count non-zero devices and update slaves_connected
    new_slaves_connected = str(len(filtered_devices)).zfill(2)  # Keep it two digits

    # Sort in ascending order and renumber starting from "01"
    sorted_devices = sorted(filtered_devices)

    # renumbered_devices = [f"{str(i+1).zfill(2)}" for i in range(len(sorted_devices))]

    # Reconstruct the final string
    new_device_string = "".join(sorted_devices).ljust(32, "0")  # Pad with zeros to maintain length
    new_string = f"{starting_id}{master_id}{new_slaves_connected}{new_device_string}{ending_id}"

    return new_string

# function will return a list of breaker which is opened in the circuit 1 No Relationship with respect to the RSS
def fetech_circuit_details(breakers_list, circuit_number):
    LBS11_NO = []
    LBS12_NO = []

    if (circuit_number == 1):
        sublist_id_0 = 0
        sublist_id_1 = 1
    if (circuit_number == 2):
        sublist_id_0 = 2
        sublist_id_1 = 3

    # exclude from the network connection
    for i, sublist in enumerate(breakers_list):
        if (sublist[sublist_id_0] == 0):
            LBS11_NO.append(i)

    # include to the network connection
    for i, sublist in enumerate(breakers_list):
        if (sublist[sublist_id_1] == 0):
            LBS12_NO.append(i)
    #print("LBS11_NO=", LBS11_NO)
    #print("LBS12_NO=", LBS12_NO)
    return LBS11_NO, LBS12_NO


def get_circuit1_electrical_network_details(NO_list, RSS_entry,
                                            circuit_number):  # NO_list - Networked opened list , RSS_entry , circuit number

    global RSS_y_number, HV_x_number
    #print("#######################<<<<<<<<<<<" + "CIR=" + str(
    #    circuit_number) + ">>>>>>>>>>>>>>>>##################################################")
    RSS_clearence = 0
    if (circuit_number == 1):
        sublist_id_forward = 1
        sublist_id_reverse = 0
        if (incoming_breakers_list[(RSS_y_number * 2)] != 0):
            RSS_clearence = 1
        else:
            RSS_clearence = 0
    if (circuit_number == 2):
        if (incoming_breakers_list[(RSS_y_number * 2) + 1] != 0):
            RSS_clearence = 1
        else:
            RSS_clearence = 0
        sublist_id_forward = 3
        sublist_id_reverse = 2

    # getting the station number details for LBS11_No
    LBS11_NO_station_details = [x + 1 for x in NO_list[0]]

    # getting the station number details for LBS11_No
    LBS12_NO_station_details = [x + 1 for x in NO_list[1]]

    #print("LBS11_NO_station_details=", LBS11_NO_station_details)
    #print("LBS12_NO_station_details=", LBS12_NO_station_details)
    # Bug Fix need to implement 18-feb-2024 also need check the respstive RSS point
    if ((breaker_list[RSS_entry-1][sublist_id_forward] == 1) and (RSS_clearence == 1)):
        # Forward direction exculde LBS11_NO_station_details & include LBS12_NO_station_details
        #print("FORWARD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # taking account of NO's only in the forward direction(Top to Bottom) from the entry point
        LBS11_NO_forward = [x for x in LBS11_NO_station_details if x > RSS_entry]
        LBS12_NO_forward = [x for x in LBS12_NO_station_details if x >= RSS_entry]

        # in forward direction we need to sort from accending order
        LBS11_NO_forward = sorted(LBS11_NO_forward)
        LBS12_NO_forward = sorted(LBS12_NO_forward)

        # on the forward direction if there is LBS11_NO / LBS12_NO ,
        # which means LBS11_NO_Forward / LBS12_NO_Forward  is connected till the end.
        # so the end of the network will be last value
        if (LBS11_NO_forward == []): LBS11_NO_forward = [network_ending_point + 1]  # fail safe condition
        if (LBS12_NO_forward == []): LBS12_NO_forward = [network_ending_point]  # fail safe condition

        #print("LBS11_NO_forward", LBS11_NO_forward)
        #print("LBS12_NO_forward", LBS12_NO_forward)
        '''
        Concept is simple 
        getting the first open points in a the network , for both circuit 1 and also circuit 2 ( circuit change over happing at the inner loop)
        framing all zero till the network end point 

        for the forward direction LBS11 is opened then that point of the station must be excluded

        '''
        # Framing circuit 1 Master 1 station list - forward direction - Include point
        circuit1_M1_station_list_A = []
        for x in range(0, network_ending_point): circuit1_M1_station_list_A.append(0)
        for x in range(RSS_entry, LBS12_NO_forward[0] + 1):
            circuit1_M1_station_list_A[x - 1] = 1
            if (x == network_ending_point): break
        #print("circuit1_M1_station_list_A", circuit1_M1_station_list_A)
        #print("N=", len(circuit1_M1_station_list_A))
        # Framing circuit 1 Master 1 station list - forward direction - exclude point
        circuit1_M1_station_list_B = []
        for x in range(0, network_ending_point): circuit1_M1_station_list_B.append(0)
        for x in range(RSS_entry, LBS11_NO_forward[0]):
            circuit1_M1_station_list_B[x - 1] = 1
            if (x == network_ending_point): break
        #print("circuit1_M1_station_list_B", circuit1_M1_station_list_B)
        #print("N=", len(circuit1_M1_station_list_B))
        circuit1_M1_station_forward_list = [a & b for a, b in
                                            zip(circuit1_M1_station_list_A, circuit1_M1_station_list_B)]
        #print("circuit1_M1_station_forward_list", circuit1_M1_station_forward_list)
    else:
        circuit1_M1_station_forward_list = []
        for x in range(0, network_ending_point): circuit1_M1_station_forward_list.append(0)

    #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    #print("RSS_entry=",RSS_entry)
    #print("RSS_entry-1=", RSS_entry-1)
    #print("sublist_id_reverse=", sublist_id_reverse)
    #print("breaker_list=",breaker_list)
    #print("breaker_list[RSS_entry - 1]=",breaker_list[RSS_entry - 1])
    #print("breaker_list[RSS_entry - 1][sublist_id_reverse]",breaker_list[RSS_entry - 1][sublist_id_reverse])
    #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    if ((breaker_list[RSS_entry-1][sublist_id_reverse] == 1) and (RSS_clearence == 1)):
        #print("Reverse>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # Reverse direction Inculdes LBS11_NO_station_details & Exculdes LBS12_NO_station_details

        #print("LBS11_NO_station_details=", LBS11_NO_station_details)
        #print("LBS12_NO_station_details=", LBS12_NO_station_details)

        # taking account of NO's only in the reverse direction(Bottom to top) from the entry point
        LBS11_NO_reverse = [x for x in LBS11_NO_station_details if x <= RSS_entry]
        LBS12_NO_reverse = [x for x in LBS12_NO_station_details if
                            x <= RSS_entry]  # 22-jan-2025 earlier if x < RSS_entry

        #print(">>>>>>>>", LBS11_NO_reverse)
        #print(">>>>>>>>", LBS12_NO_reverse)
        if (LBS11_NO_reverse == []): LBS11_NO_reverse = [network_stating_point - 1]
        if (LBS12_NO_reverse == []): LBS12_NO_reverse = [network_stating_point - 1]

        # in reverse direction we need to sort from decending order
        LBS11_NO_reverse = sorted(LBS11_NO_reverse, reverse=True)
        LBS12_NO_reverse = sorted(LBS12_NO_reverse, reverse=True)

        #print("LBS11_NO_reverse", LBS11_NO_reverse)
        #print("LBS12_NO_reverse", LBS12_NO_reverse)

        # on the reverse direction if there is LBS11_NO / LBS12_NO ,
        # which means LBS11_NO_reverse / LBS12_NO_reverse  is connected till the end.
        # so the end of the network will be last value
        # This can arrive even when both end of the RSS are opened we must make sure
        # atleast one of the breakers must be ON so that this logic will work
        #if (LBS11_NO_reverse == []): LBS11_NO_reverse = [network_stating_point - 1]
        #if (LBS12_NO_reverse == []): LBS12_NO_reverse = [network_stating_point - 1]

        # Framing circuit 1 Master 1 station list - reverse direction - Include point
        circuit1_M1_station_list_A = []
        #print("RSS_entry=", RSS_entry)
        #print("LBS11_NO_reverse[0]=", LBS11_NO_reverse[0])
        #print("LBS12_NO_reverse[0]=", LBS12_NO_reverse[0])


        if (RSS_entry == LBS11_NO_reverse[0]): LBS11_NO_reverse[0] = LBS11_NO_reverse[0] - 1
        if (len(LBS12_NO_reverse)== 1 and RSS_entry == LBS12_NO_reverse[0]): LBS12_NO_reverse[0] = 0 #LBS12_NO_reverse[0] - 1
        elif (len(LBS12_NO_reverse)> 1 and RSS_entry == LBS12_NO_reverse[0]): LBS12_NO_reverse[0] = LBS12_NO_reverse[1]


        for x in range(0, network_ending_point): circuit1_M1_station_list_A.append(0)
        for x in range(RSS_entry, LBS11_NO_reverse[0]-1, -1):  # logic chnaged on 22-Jan-25 #earlier it was  for x in range(RSS_entry, LBS11_NO_reverse[0] - 1, -1):
            circuit1_M1_station_list_A[x - 1] = 1
            if (x == network_stating_point): break
        #print("circuit1_M1_station_list_A", circuit1_M1_station_list_A)
        # Framing circuit 1 Master 1 station list - reverse direction - exclude point
        circuit1_M1_station_list_B = []
        for x in range(0, network_ending_point): circuit1_M1_station_list_B.append(0)
        for x in range(RSS_entry, LBS12_NO_reverse[0], -1):  # logic chnaged on 22-Jan-25 #for x in range(RSS_entry, LBS12_NO_reverse[0], -1):
            circuit1_M1_station_list_B[x - 1] = 1
            if (x == network_stating_point): break
        #print("circuit1_M1_station_list_B", circuit1_M1_station_list_B)
        circuit1_M1_station_reverse_list = [a & b for a, b in
                                            zip(circuit1_M1_station_list_A, circuit1_M1_station_list_B)]
        # [a & b for a, b in
        #                                    zip(circuit1_M1_station_list_A, circuit1_M1_station_list_B)]
        #print("circuit1_M1_station_reverse_list", circuit1_M1_station_reverse_list)
    else:
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        circuit1_M1_station_reverse_list = []
        for x in range(0, network_ending_point): circuit1_M1_station_reverse_list.append(0)

    #print("circuit1_M1_station_forward_list",circuit1_M1_station_forward_list)
    # max(x, y)
    circuit1_M1_station = [max(x, y) for x, y in
                           zip(circuit1_M1_station_forward_list, circuit1_M1_station_reverse_list)]

    #print("circuit1_M1_station==", circuit1_M1_station)
    return circuit1_M1_station

Master1DataString_default = "329010901020304050607080900000000000000829"
Master2DataString_default = "329020710111213141516000000000000000000829"
Master3DataString_default = "329030710111213141516000000000000000000829"

network_stating_point = 1
network_ending_point = 25

# this code will work only when stating and ending is having the RSS and middle one RSS
#RSS_station_list = [1,19]
RSS_station_list = [1, 15, 25]
# each RSS_station will have a main incomer breaker which must be enable to power the respective circuit 1 or 2
#incoming_breakers_list = [1,1,1,1]
incoming_breakers_list = [MBREG[108], MBREG[109], MBREG[110], MBREG[111], MBREG[112], MBREG[113]]

# input - end

# creating the empty list for the master list of each stations
final_master_list = []
for s in range(0, len(RSS_station_list)): final_master_list.append(0)

# creating a empty list for the main incomer itself closed
empty_list = []
for x in range(0, network_ending_point): empty_list.append(0)

# crearting a empty list for the direction circuit_NO_status circuit1_station_list
circuit_NO_status = [0, 0]
circuit_station_list = [0, 0]

# bug fix inti
RSS_y_number = 0
HV_x_number = 0


while True:
    GPIO.output(led1, GPIO.HIGH)
    GPIO.output(led2, GPIO.HIGH)
    print("reading the Breaker status")
    Read_Breaker_details() #MMCTRL
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    print("Framing the breaker status")
    FrameBreakerSeq() ##MMCTRL

    incoming_breakers_list = [MBREG[108], MBREG[109], MBREG[110], MBREG[111], MBREG[112], MBREG[113]]

    breaker_list[24][1] = MBREG[100] & MBREG[101]
    breaker_list[24][3] = MBREG[102] & MBREG[103]
    breaker_list[25][0] = MBREG[104] & MBREG[105]
    breaker_list[25][2] = MBREG[106] & MBREG[107]

    print("incoming_breakers=",incoming_breakers_list)
    for d in range(0,25):
        print("Station Details="+str(d+1).zfill(2),  breaker_list[d])
    print("MBREG=", MBREG[2])
    for y in range(0, len(RSS_station_list)):  # where y is RSS citcuit numbers # this loop is for number of RSS
        # looping twice 0 for forward direction , 1 for reverse direction
        RSS_y_number = y
        # print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" + str(
        #    y) + "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        for x in range(0, 2):  # where x 33 line is circuit number  # 0 for circuit 1 and 1 for circuit -2
            HV_x_number = x
            # Circuit 1 process
            circuit_NO_status[x] = fetech_circuit_details(breaker_list, x + 1)
            # print("CNS=", circuit_NO_status[x])
            # circuit1_station_list = get_electrical_network_details(circuit1_NO_status,RSS1_station_number,1)
            # every timing we need to give the direction for front and back for one RSS
            # this function must be called only if RS13 is enabled
            # print("<<<<<<<<<<<<<<<<<CCCCC"+str(RSS_station_list[y])+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"+"<<<<<<<<<"+str(x))
            if incoming_breakers_list[(y * 2)] != 0 or incoming_breakers_list[(y * 2) + 1] != 0:
                circuit_station_list[x] = get_circuit1_electrical_network_details(circuit_NO_status[x],
                                                                                  RSS_station_list[y],
                                                                                  x + 1)
            else:
                circuit_station_list[x] = empty_list

        final_master_list[y] = [max(x, y) for x, y in
                                zip(circuit_station_list[0], circuit_station_list[
                                    1])]  # circuit_station_list[0] - for circuit 1 | circuit_station_list[1] for circuit 2

        #print("RSS_Station_number: {:02d}, Final_list: {}".format(RSS_station_list[y], final_master_list[y]))
        # print("RSS_Station_number: {}, Legnth: {}".format(RSS_station_list[y], len(final_master_list[y])))

    #print("->RSS_Station_number: {:02d}, Final_list: {}".format(RSS_station_list[0], final_master_list[0]))
    #print("->RSS_Station_number: {:02d}, Final_list: {}".format(RSS_station_list[1], final_master_list[1]))
    #print("->RSS_Station_number: {:02d}, Final_list: {}".format(RSS_station_list[2], final_master_list[2]))

    #compling the final message
    Master1DataString = CompileMasterMessage(final_master_list[0],"01")
    Master2DataString = CompileMasterMessage(final_master_list[1],"02")
    Master3DataString = CompileMasterMessage(final_master_list[2],"03")

    '''
    print("UNCOMMENT WHEN NEEDED")
    print(Master1DataString)
    print("Master ID = ", Master1DataString[3:5])
    print("Slaves connected = ", Master1DataString[5:7])
    print(Master2DataString)
    print("Master ID = ", Master2DataString[3:5])
    print("Slaves connected = ", Master2DataString[5:7])
    print(Master3DataString)
    print("Master ID = ", Master3DataString[3:5])
    print("Slaves connected = ", Master3DataString[5:7])
    '''
    print("**********************RE-MAPPED DATA************************************")
    # Master - 1
    if (Master1DataString[5:7] != str(16)):
        processed_string_M1 = station_id_to_slave_id(Master1DataString)
    else:
        processed_string_M1 = Master1DataString
    print(processed_string_M1)
    print("Master ID = ", processed_string_M1[3:5])
    print("Slaves connected = ", processed_string_M1[5:7])
    # Master - 2
    if (Master2DataString[5:7] != str(16)):
        processed_string_M2 = station_id_to_slave_id(Master2DataString)
    else:
        print("16 Slave connected to M2")
        processed_string_M2 = Master2DataString
    print(processed_string_M2)
    print("Master ID = ", processed_string_M2[3:5])
    print("Slaves connected = ", processed_string_M2[5:7])
    # Master - 3
    if (Master3DataString[5:7] != str(16)):
        processed_string_M3 = station_id_to_slave_id(Master3DataString)
    else:
        processed_string_M3 = Master3DataString
    print(processed_string_M3)
    print("Master ID = ", processed_string_M3[3:5])
    print("Slaves connected = ", processed_string_M3[5:7])

    print("***********************************************************************")

    GPIO.output(led1, GPIO.HIGH)

    if (str(Master1DataString_default) != str(processed_string_M1)): #MMCTRL
        SendTOMaster1(processed_string_M1)
        print("SENDING M1")
    else:
        SendTOMaster1(processed_string_M1)
        print("Default M1")
    if (str(Master2DataString_default) != str(processed_string_M2)): #MMCTRL
        SendTOMaster2(processed_string_M2)
        print("SENDING M2")
    else:
        SendTOMaster2(processed_string_M2)
        print("Default M2")
    if (str(Master3DataString_default) != str(processed_string_M3)): #MMCTRL
        #SendTOMaster3(Master3DataString)
        print("SENDING M3")
    else:
        # SendTOMaster3(Master3DataString)
        print("Default M3")
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.HIGH)
    GPIO.output(led2, GPIO.LOW)
    print("Sleeping.....")
    print("***************************************************************************************")
    for slt in range(0,60):
        if(slt%2 == 0):
            GPIO.output(led1, GPIO.HIGH)
            GPIO.output(led2, GPIO.HIGH)
        else:
            GPIO.output(led1, GPIO.LOW)
            GPIO.output(led2, GPIO.LOW)
        time.sleep(1)

#RSS REGISTERS AND THE NUMBER OF REGISTERS TO READ IS NOT INCLUDED HERE