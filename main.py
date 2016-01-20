import time                           # For sleep
import yahooDataObject
import Pyro4
import slave
import master

# Init Master
masterObject = master.MasterProgram()
slaveObject = slave.SlaveProgram()

boot_time_slave = Pyro4.Proxy("PYRONAME:slave.boot.time")
boot_time_master = Pyro4.Proxy("PYRONAME:master.boot.time")
time_slave = boot_time_slave.getBootTime()
time_master = boot_time_master.getBootTime()

if (time_master<time_slave):
    masterObject.dataBase()
    masterObject.doWork()
else:
    slaveObject.dataBase()
    slaveObject.doWork()
