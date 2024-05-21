#
# BLEClient
#
import aioble
import bluetooth
import uasyncio as asyncio

_GENERIC_SERVICE_UUID = bluetooth.UUID(0x1848) # data service UUID
_GENERIC_CHAR_UUID = bluetooth.UUID(0x2A6E) # characteristic UUID
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

class BLEClient:
    """Class to create a BLE client that connects to a server and receives messages.
    """
    
    def __init__(self,
                 server_name:str,
                 receive_message_func = None,
                 receive_interval_ms:int = 1000,
                 service_uuid:bluetooth.UUID = _GENERIC_SERVICE_UUID,
                 char_uuid:bluetooth.UUID = _GENERIC_CHAR_UUID)-> None:
        """Initialize the BLEClient object.

        Args:
            server_name (str): Name of server to connect to.
            receive_message_func (_type_, optional): User provided function called when the client receives a message. 
                Defaults to None.
            receive_interval_ms (int, optional): Interval between receives, ms. Defaults to 1000.
            service_uuid (UUID, optional): Service UUID. Defaults to _GENERIC_SERVICE_UUID.
            char_uuid (UUID, optional): Characteristic UUID. Defaults to _GENERIC_CHAR_UUID.
        """
        self.server_name = server_name
        self.receive_message_func = receive_message_func
        self.receive_interval_ms = receive_interval_ms
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.connection = None
        self.characteristic = None
        
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        while True:
            await self.update()
            await asyncio.sleep_ms(self.receive_interval_ms)
                
    async def update(self)-> None:
        try:
            if self.is_connected():
                self.show_connected(True)
                await self.receive_message()
            else:
                self.show_connected(False)
                await self.connect_to_server()
        except Exception as e:
            print(f'Exception: {e}')
            self.connection = None
                    
    def show_connected(self, connected: bool)-> None:
        """Subclasses over ride this to show state of connecton"""
        pass
               
    def is_connected(self)->bool:
        return not self.connection == None and self.connection.is_connected() 

    async def receive_message(self)-> None:
        message = await self.characteristic.read()
        message_str = message.decode('utf-8')
        
        if self.receive_message_func:
            self.receive_message_func(message_str)
                
    async def connect_to_server(self)-> None:
        device = await self.find_server()
                    
        self.connection = await device.connect()
        print(f'Connection: {self.connection}')
                    
        service = await self.connection.service(self.service_uuid)
        print(f'Service: {service}')
                    
        self.characteristic = await service.characteristic(self.char_uuid)
        print(f'Characteristic: {self.characteristic}')
        
    async def find_server(self):
        """Find the server with the name server_name and service_uuid.

        Returns:
            device: server
        """
        while True:
            print('Scanning for server...', end='')
            async with aioble.scan(5000, interval_us=30_000, window_us=30_000, active=True) as scanner:
                async for result in scanner:
                    if result.name() == self.server_name and self.service_uuid in result.services():
                        print(f'found: {result.name()}')
                        return result.device
            await asyncio.sleep_ms(100)
    

if __name__ == "__main__":
    client = BLEClient("BLE Test")
    client.start()

