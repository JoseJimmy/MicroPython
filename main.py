#https://realpython.com/micropython/#fading-leds
# http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/Lectures/Topic%2015%20-%20Using%20MicroPython%20on%20ESP32%20(notes).pdf
#!!! >> https://micronote.tech/2020/07/I2C-Bus-with-a-NodeMCU-and-MicroPython/
# esptool.py --chip esp32 erase_flash
#esptool --chip esp32 --port COM3 write_flash -z 0x1000 C:\Python\WaterAi\esp32-idf4-20210202-v1.14.bin
#FFT code

import socket

from machine import SoftI2C, Pin
from time import sleep_ms
from ntptime import settime
import utime


MPU6050_ADDR = 0x68

MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_XOUT_L = 0x3C
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_YOUT_L = 0x3E
MPU6050_ACCEL_ZOUT_H = 0x3F
MPU6050_ACCEL_ZOUT_L = 0x40
MPU6050_PWR_MGMT_1 = 0x6B

MPU6050_LSBC = 340.0
MPU6050_TEMP_OFFSET = 36.53
MPU6050_LSBG = 16384.0
MPU6050_LSBDS = 131.0


def mpu6050_init(i2c):
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, bytes([0]))


def combine_register_values(h, l):
    if not h[0] & 0x80:
        return h[0] << 8 | l[0]
    return -((h[0] ^ 255) << 8) | (l[0] ^ 255) + 1


def mpu6050_get_accel(i2c):

    accel_x_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_H, 1)
    accel_x_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_L, 1)
    accel_y_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_H, 1)
    accel_y_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_L, 1)
    accel_z_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_H, 1)
    accel_z_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_L, 1)
    x = combine_register_values(accel_x_h, accel_x_l) / MPU6050_LSBG
    y = combine_register_values(accel_y_h, accel_y_l) / MPU6050_LSBG
    z = combine_register_values(accel_z_h, accel_z_l) / MPU6050_LSBG
    txt = '%1.4f_%1.4f_%1.4f'%(x,y,z)
    return txt
#CXNK00207AB6
#807f7e6afbd5a42f
# Function to connect to the WiFi
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        # print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('CXNK00207AB6', '807f7e6afbd5a42f')
        while not sta_if.isconnected():
            pass
    # print('network config:', sta_if.ifconfig())

# Function to send an HTTP request
def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            pass # print(str(data, 'utf8'), end='')
        else:
            break

if __name__ == "__main__":
    i2c = SoftI2C(scl=Pin(15), sda=Pin(2))
    do_connect()
    settime()
    sleep_ms(3000)
    mpu6050_init(i2c)
    txt = ''
    while True:
        if(len(txt)<1900):
            txt = txt +':'+mpu6050_get_accel(i2c)
        else:
            # print("%d:\t %s"%(len(txt), txt))
            url = 'https://dweet.io/dweet/for/Jespy32?data='+str(utime.time())+'~'+txt
            # print("****%d:\t*********\n %s"%(len(url), url))
            http_get(url);
            txt = ''

        sleep_ms(100)


