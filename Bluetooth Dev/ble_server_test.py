#
# BLE Server Test
#
# import bluetooth
import uasyncio as asyncio
from ble_server import BLEServer

count = 0

def update_func():
    global count
    print(f'Update func, count = {count}')
    count += 1
    return str(count)

server = BLEServer(
    name='KevsRobots',
    update_func=update_func,
    update_interval_ms=2000)

asyncio.run(server.start())