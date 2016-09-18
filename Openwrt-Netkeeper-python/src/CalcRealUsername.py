#!/usr/bin/env python
#encoding=utf-8
__author__ = 'kebe'
import time,hashlib,struct,sys

def getRealUsername(oldUsername,RADIUS = "cqxinliradius002"): #对用户名的加密
    timeHash = [0 for i in range(4)]
    nowTime = int(time.time())//5
    for i in range(0,4):
        for j in range(0,8):
            timeHash[i] = timeHash[i]+(((nowTime>>(i+4*j))&1)<<(7-j))
    md5Hash = hashlib.md5()
    bm = struct.pack('>I',nowTime)+(oldUsername.split('@')[0]+RADIUS).encode('ascii')
    md5Hash.update(bm)
    pk = md5Hash.hexdigest()[0:2]
    PIN27=[0,0,0,0,0,0]
    PIN2=''

    PIN27[0] = ((timeHash[0]>>2)&0x3F)
    PIN27[1] = ((timeHash[0]&0x03)<<4&0xff)|((timeHash[1]>>4)&0x0F)
    PIN27[2] = ((timeHash[1]&0x0F)<<2&0xff)|((timeHash[2]>>6)&0x03)
    PIN27[3] = timeHash[2]&0x3F
    PIN27[4] = ((timeHash[3]>>2)&0x3F)
    PIN27[5] = ((timeHash[3]&0x03)<<4&0xff)
    for i in range(6):
        PIN27[i] = {True:(PIN27[i]+0x20)&0xff,False:(PIN27[i]+0x21)&0xff}[((PIN27[i]+0x20)&0xff)<0x40]
    for i in range(6):
            PIN2 = PIN2+chr(PIN27[i])
    realUsername = '\r\n'+PIN2+pk+oldUsername
    return realUsername
if __name__ == '__main__':
    print getRealUsername(sys.argv[1])
