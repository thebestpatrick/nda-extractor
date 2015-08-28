#!/bin/python3.4
import sys, getopt
import binascii
import time
import math
import datetime

header_size = 2304

file_size = header_size
byte_line = []

line_size = 59
mini_header_size = 0

line_number = 0
main_data = False


# Return a dict containing the relevant data.  all nice and pretty like.
def process_byte_stream(byte_stream):
    curr_dict = {}

    # Line ID
    line_idb = int.from_bytes(byte_stream[0:4], byteorder='little')
    curr_dict['line_id'] = line_idb
    # End line ID

    # Second column, not sure what it is?
    col2 = int.from_bytes(byte_stream[4:8], byteorder='little')
    curr_dict['col2'] = col2
    # end second column

    # Step ID? Might secretly be involved with col2
    sid = int.from_bytes(byte_stream[8:9], byteorder='little')
    curr_dict['step_id'] = sid
    # End Step ID

    # Step Job? Might be with step ID too.  In any case, probably an
    # identifier for charge, rest, discharge, etc.
    # 4=REST. 1=CC_Chg. 7=CCCV_Chg. 
    sjob = int.from_bytes(byte_stream[9:10], byteorder='little')
    curr_dict['step_job'] = sjob
    # End step job

    # Time in step
    tis = int.from_bytes(byte_stream[10:14], byteorder='little')
    curr_dict['time_in_step'] = tis
    #print(tic)
    # end time in step

    # Voltage? Have to ask Will
    volts = int.from_bytes(byte_stream[14:18], byteorder='little')
    if volts > 0x7FFFFFFFFF:
        volts -= 0x100000000000000
    curr_dict['voltage'] = volts/10000
    # End capacity?
    
    # Current?
    current = int.from_bytes(byte_stream[18:22], byteorder='little')
    if current > 0x7FFFFFFF:
            current -= 0x100000000
    curr_dict['current'] = current / 10000
    # End Current?
    
    # blank? This section seems to be blank, but it might not be?
    blank = int.from_bytes(byte_stream[22:30], byteorder='little')
    curr_dict['blank'] = blank
    # end blank?

    # FIXME not sure how this works, though it seems to be related to the 
    # column right before the timestamp, which is allegedly some kind of 
    # total charge measure.  
    comp1 = int.from_bytes(byte_stream[30:38], byteorder='little')

    comp2 = int.from_bytes(byte_stream[38:46], byteorder='little')
    diff = round(((comp1 + comp2)/100)/.86, 2)

    curr_dict['comp1'] = comp1
    curr_dict['comp2'] = comp2
    curr_dict['algo_comp'] = diff

    # end FIXME

    # Time and date
    timestamp = int.from_bytes(byte_stream[46:54], byteorder='little')
    newt = datetime.datetime.fromtimestamp(timestamp)
    curr_dict['timestamp'] = newt.strftime('%Y-%m-%d %H:%M:%S')
    # end time and date
    
    # last 5?  silly number.  The last one might be an indicator, and the other 
    # 4 might be a number
    last = int.from_bytes(byte_stream[54:58], byteorder='little')
    curr_dict['last'] = last
    # end

    #stuff = []
    #for a in byte_stream:
    #    stuff.append(a)
    
    #print(curr_dict)
    raw_bin = str(binascii.hexlify(bytearray(byte_stream)))
    curr_dict['RAW_BIN'] = raw_bin
    #time.sleep(.1)
    return curr_dict


def dict_to_csv_line(indict, lorder):
    csv_line = ""
    for a in lorder:
        if a == 'time_in_step':
            seconds = indict[a]
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            csv_line += "%d:%02d:%02d" % (h, m, s) + ','
        else:
            csv_line += str(indict[a]) + ','
    csv_line += '\n'
    return csv_line

# TODO: load from config
csv_line_order = ['line_id', 'col2', 'step_id', 'step_job','time_in_step', 
            'voltage', 'current', 'blank', 'comp1', 'comp2', 'algo_comp', 
            'timestamp', 'last', 'RAW_BIN']

outfile = open("test.csv", 'w')
for x in csv_line_order:
    outfile.write(x + ',')
outfile.write('\n')

with open(sys.argv[1], "rb") as f:
    f.seek(header_size) # TODO: header decoding, including finding a mass
    byte = f.read(1)  
    pos = 0
    while byte:
        file_size += 1
        if not main_data:
            local = int.from_bytes(byte, byteorder='little')
            if local == 255:
                main_data = True
                # TODO: Secondary header decoding
                f.seek(mini_header_size, 1)
                continue
            else:
                #print(local)
                #time.sleep(.1)
                byte = f.read(1)
                continue
        
        line = f.read(59)
        if line == b'':
            break
               
        dict_line = process_byte_stream(line)
        csv_line = dict_to_csv_line(dict_line, csv_line_order)
        #print(csv_line)
        outfile.write(csv_line)

outfile.close()
