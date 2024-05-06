#
# BLEServer
#
import aioble
import bluetooth
from micropython import const
import uasyncio as asyncio

_GENERIC_SERVICE_UUID = bluetooth.UUID(0x1848)
_GENERIC_CHAR_UUID = bluetooth.UUID(0x2A6E)
_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

class BLEServer:
    def __init__(self,
                 name:str,
                 send_message_func=None,
                 send_interval_ms=1000,
                 service_uuid=_GENERIC_SERVICE_UUID,
                 char_uuid=_GENERIC_CHAR_UUID)->None:
        self.name = name
        self.send_message_func = send_message_func
        self.send_interval_ms = send_interval_ms
        print(f'update_func = {self.update_func}')
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.connected = False
        self.connection = None
        self.characteristic = None
        self.createService()
        
    def createService(self):
        print('createService')
        service = aioble.Service(self.service_uuid)
        self.characteristic = aioble.Characteristic(
            service,
            self.char_uuid,
            read = True,
            notify = True
        )
        aioble.register_services(service)
    
    async def advertise(self, interval_ms:int=250_000)->None:
        print('advertise')
        while True:
            print('start advertising')
            async with await aioble.advertise(
                interval_ms, 
                name=self.name, 
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[self.service_uuid]
            ) as self.connection:
                print("connection from", self.connection.device)
                self.connected = True

                await self.connection.disconnected()
                self.connected = False
                print(f'disconnected')
    
    async def send_message(self)->None:
        while True:
            if self.connected:
                print('send_message')
                message_str = ''
                if not self.send_message_func == None:
                    print('calling update_func')
                    message_str = self.send_message_func()
                message = bytearray(message_str, 'utf-8')
                self.characteristic.write(message)
                self.characteristic.notify(self.connection, message)
            await asyncio.sleep_ms(self.send_interval_ms)
    
            
    async def start(self)->None:
        print('start')
        tasks = [
            asyncio.create_task(self.advertise()),
            asyncio.create_task(self.send_message()),
        ]
        await asyncio.gather(*tasks)
    
    
    
async def main()->None:
    bleServer = BLEServer('BLE Test')
    await bleServer.start()
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print(f'End')
        
        
    