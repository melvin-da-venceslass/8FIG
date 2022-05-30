from pymodbus.client.sync import ModbusTcpClient

import json



class connect_machine:
    def read_regs(self,add,qty):
        try:
            return self.plccon.read_holding_registers(add,qty).registers
        except Exception as e:
            raise Exception("Machine Comm Error")

    def read_inpr(self,add,qty):
        try:
            self.create_conn()
            result = self.plccon.read_input_registers(add,qty).registers
            self.plccon.close()
            return result
        except Exception as e:
            raise Exception("Machine Comm Error")

    def write_regs(self,add,cmd,value):
        try:
            return self.plccon.write_register(add,cmd,unit=value)
        except Exception as e:

            raise Exception("Machine Comm Error")

    def create_conn(self):
         self.plccon = ModbusTcpClient(self.pipad,port=int(self.pport), timeout=3,auto_open=True)

    def __init__(self,settings_):
        try:
            self.setting = settings_
            self.pipad = settings_["machine_interface"]["machine_ip"]
            self.pport = settings_["machine_interface"]["machine_port"]
            self.p_int = settings_["machine_interface"]["ping_interval"]
            for each in settings_["machine_interface"]["registers"]:
                exec (f'self.{each["description"]}={each["regAddress"]}')
            self.plccon = ModbusTcpClient(self.pipad,port=int(self.pport), timeout=3,auto_open=True)
        except Exception as e:
            print(e)
            raise Exception("Machine Comm Error")

   


# if __name__ == "__main__":

#     settings_file = open("settings.conf")
#     settings_ = json.load(settings_file)
#     appObj =  connect_machine(settings_)

# import json

# class Struct:
#     def __init__(self, **entries):
#         self.__dict__.update(entries)


# class machine:
#     # def read_registers(self,address,quantity):
#     #     self.plccon.read_holding_registers(address,quantity)
#     #     return data.registers


#     def __init__(self,settings_):
#         self.pipad = settings_["machine_interface"]["machine_ip"]
#         self.pport = settings_["machine_interface"]["machine_port"]
#         print(self.pipad,self.pport)
#         self.plccon = ModbusTcpClient(self.pipad,port=int(self.pport), timeout=3)

#         # if self.plccon:
#         #     for each in settings_["machine_interface"]["registers"]:
#         #         exec(f"self.{each['description']} = Struct(each)")
            
# from pymodbus.client.sync import ModbusTcpClient
# import json







