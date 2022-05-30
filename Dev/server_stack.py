from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

# Create an instance of ModbusServer
server = ModbusServer("192.168.7.251", 12345, no_block=True)

try:
    print("Start server...")
    server.start()
    print("Server is online")
    state = [0]
    while True:
        DataBank.set_words(0, [int(uniform(0, 100))])
        if state != DataBank.get_words(1):
            state = DataBank.get_words(1)
            print("Value of Register 1 has changed to " +str(state))
        sleep(0.5)

except Exception as e:
    print(e)
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")