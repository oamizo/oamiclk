"""
Oamiclk
Version: 0.0.1
Author: Oamizo
"""
import machine
import network
from time import sleep
import epddriver
import epdconfig
from centerwriter import CenterWriter
from writer import Writer
import bebasNeue229
import bebasNeue50
import json
import requests
import math

# Version
_program = "Oamiclk"
_version = "v0.0.1"

# Wi-Fi credentials
wifiSSID = 'YOU_WIFI_SSID'
wifiPass = 'YOU_WIFI_PASSWORD'

# Define display pin
rst_pin = [12, 12, 12, 12, 12, 12, 12]
cs_pin = [0, 3, 6, 9, 15, 18, 21]
dc_pin = [1, 4, 7, 13, 16, 19, 22]
busy_pin = [2, 5, 8, 14, 17, 20, 26]
led_pin = machine.Pin('LED', machine.Pin.OUT)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(hostname="Oamiclk")
    wlan.connect(wifiSSID, wifiPass)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        led_pin.value(True)
        sleep(1)
        led_pin.value(False)
    print(wlan.ifconfig())
    led_pin.value(True)

def add_zero_to_six_digits(number):
    num_str = str(number)
    zeros_to_add = 6 - len(num_str)
    formatted_number = " " * zeros_to_add + num_str
    return formatted_number

def getBitcointPrice():
    pricejson = json.loads(requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT').text)
    BTCUSDTprice = math.trunc(float(pricejson['price']))
    formattedBTCUSDTprice = add_zero_to_six_digits(BTCUSDTprice)
    dataList = list(str(formattedBTCUSDTprice))
    return dataList

def getBitcoinBlock():
    bitCoinBlockHeight = json.loads(requests.get('https://blockstream.info/api/blocks/tip/height').text)
    formattedBitCoinBlockHeight = add_zero_to_six_digits(bitCoinBlockHeight)
    dataList = list(str(formattedBitCoinBlockHeight))
    return dataList

def firstDisplayShow(toggle):
    toggleSwitch = int(toggle)
    if toggleSwitch == 1:
        epddisplay0 = epddriver.EPD(epdconfig.piPicoW(rst_pin[0], cs_pin[0], dc_pin[0], busy_pin[0]))
        epddisplay0.fill(0x00)
        wri = Writer(epddisplay0, bebasNeue50)
        Writer.set_textpos(epddisplay0, 98, 21)
        wri.printstring('BTC')
        epddisplay0.rect(5, 147, 118, 3, 0xff, True)
        Writer.set_textpos(epddisplay0, 155, 6)
        wri.printstring('USDT')
        epddisplay0.text(_program + ' ' + _version, 5, 285, 0xFF)
        epddisplay0.display(epddisplay0.buffer)
        epddisplay0.sleep()
        dataList = getBitcointPrice()
        return dataList
    elif toggleSwitch == 2:
        epddisplay0 = epddriver.EPD(epdconfig.piPicoW(rst_pin[0], cs_pin[0], dc_pin[0], busy_pin[0]))
        epddisplay0.fill(0x00)
        wri = Writer(epddisplay0, bebasNeue50)
        Writer.set_textpos(epddisplay0, 98, 21)
        wri.printstring('BTC')
        epddisplay0.rect(5, 147, 118, 3, 0xff, True)
        Writer.set_textpos(epddisplay0, 155, 6)
        wri.printstring('BLCK')
        epddisplay0.text(_program + ' ' + _version, 5, 285, 0xFF)
        epddisplay0.display(epddisplay0.buffer)
        epddisplay0.sleep()
        dataList = getBitcoinBlock()
        return dataList

if __name__=='__main__':
    try:
        toggleCase = 1
        while True:
            connect()
            if toggleCase % 2 == 1:
                dataList = firstDisplayShow(1)
            else:
                dataList = firstDisplayShow(2)
            toggleCase += 1
            print(*dataList)
            num = 0

            while True:
                displayNum = num+1
                epddisplay = epddriver.EPD(epdconfig.piPicoW(rst_pin[displayNum], cs_pin[displayNum], dc_pin[displayNum], busy_pin[displayNum]))
                cw = CenterWriter(epddisplay, bebasNeue229)
                print(dataList[num])
                if dataList[num] == " ":
                    epddisplay.Clear(0x00)
                    epddisplay.fill(0x00)
                    epddisplay.sleep()
                    num = num + 1
                else:
                    epddisplay.Clear(0x00)
                    epddisplay.fill(0x00)
                    cw.set_vertical_spacing(0)
                    cw.set_vertical_shift(0)
                    cw.write_lines(dataList[num])
                    epddisplay.display(epddisplay.buffer)
                    epddisplay.delay_ms(2)
                    epddisplay.sleep()
                    num = num + 1
                if(num == 6):
                    break
            sleep(300)

    except:
        machine.reset()
