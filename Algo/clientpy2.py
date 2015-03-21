import socket
import sys
import time
    
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            return rline.strip()
            rline = sfile.readline()
    finally:
        sock.close()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()


def parse():
    string = run("SpeedTraders", "speedtraders", "SECURITIES")
    data = string.split(" ")
    data = data[1:]
    struct = []
    lst = []
    i=0
    while i < len(data):
        n = i
        while n < 4+i:
            lst.append(data[n])
            n+=1
        struct.append(lst)
        lst = []
        i+=4
    print struct
    return struct

def spread(stock):
    fileLine = run("SpeedTraders", "speedtraders", "ORDERS "+stock)
        
    bidArr = []
    askArr = []

    datas = fileLine.split(" ")
    isBid = False
    i = 0
    for data in datas:
        if not(data == "SECURITY_ORDERS_OUT BID" or data == stock):
            if data == "BID":
                isBid = True
            elif data == "ASK":
                isBid = False
            elif isBid:
                bidArr.append(data)
            elif not isBid:
                askArr.append(data)
    askArr = askArr[1:]
    bidArr = bidArr[::2]
    askArr = askArr[::2]
    return (float(askArr[0]) - float(bidArr[0]))/((float(askArr[0]) + float(bidArr[0]))/2)

def ratio(struct):
    lst = []
    for i in range(0,9):
        if float(spread(struct[i][0])) == 0:
            lst.append((10000000, struct[i][0]))
        else:
            lst.append((float(struct[i][2])/float(spread(struct[i][0])), struct[i][0]))
    return lst  

while True:
    struct = parse()
    lst = ratio(struct)
    lst = sorted(lst,key=lambda x: x[0])
    print lst
    time.sleep(1)