import machine_interface,json,time
settings_file = open("settings.conf")
settings_ = json.load(settings_file)
x = machine_interface.connect_machine(settings_)
# print(x.read_inpr(1,10),end="\r")
print(x.write_regs(0,10,10),end="\r")



