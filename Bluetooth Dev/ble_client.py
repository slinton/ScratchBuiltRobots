#
# BLEClient
#
import aioble
import bluetooth
import machine
import uasyncio as asyncio

_GENERIC_SERVICE_UUID = bluetooth.UUID(0x1848) # data service UUID
_GENERIC_CHAR_UUID = bluetooth.UUID(0x2A6E) # char

# _REMOTE_UUID = bluetooth.UUID(0x1848)
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

class BLEClient:
    
    def __init__(self,
                 server_name:str,
                 service_uuid=_GENERIC_SERVICE_UUID,
                 char_uuid=_GENERIC_CHAR_UUID)->None:
        self.server_name = server_name
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.characteristic = None

        self.ready = False
        
    async def receive_message2(self)->None:
        while True:
            print('tick')
            await asyncio.sleep_ms(1000)
        
    async def receive_message(self)->None:
        print('receive message')
        while True:
            if self.ready:
                try:
                    command = await self.characteristic.read()
                    print(command)
                except TypeError:
                    print(f'something went wrong; remote disconnected?')
                    self.ready = False
                except asyncio.TimeoutError:
                    print(f'something went wrong; timeout error?')
                    self.ready = False
                except asyncio.GattError:
                    print(f'something went wrong; Gatt error - did the remote die?')
                    self.ready = False
                except Exception as e:
                    print(f'receive_message exception: {e}')
                    self.ready = False
            await asyncio.sleep_ms(1000)
        
    async def start_ble(self)->None:
        print('start_ble')
        while True:
            if not self.ready:
                print('attempting to start ble')
                try:
                    device = await self.find_server()
                    print(device)
                    connection = await device.connect()
                    print(connection)
                    service = await connection.service(self.service_uuid)
                    print(service)
                    self.characteristic = await service.characteristic(self.char_uuid)
                    print(self.characteristic)
                    if not self.characteristic == None:
                        self.ready = True
                        print(f'self.ready = {self.ready}')
                except asyncio.TimeoutError:
                    print("Timeout during connection")
                except Exception as e:
                    print(f'start_ble exception: {e}')
            await asyncio.sleep_ms(1000)
                
        
    async def find_server(self):
        while True:
            async with aioble.scan(5000, interval_us=30_000, window_us=30_000, active=True) as scanner:
                async for result in scanner:
                    if result.name() == self.server_name and self.service_uuid in result.services():
                        return result.device
    
    async def start(self)->None:
        print('start')
        tasks = [
            asyncio.create_task(self.start_ble()),
            asyncio.create_task(self.receive_message())
        ]
        await asyncio.gather(*tasks)

async def main():
    client = BLEClient("KevsRobots")
    await client.start()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print('End')