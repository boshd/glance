# Reduce plz
import interface, threading, sys, os, run

# monitors
from cpu import cpu
from mem import mem
from proc import proc

def main():
    srr = {[cpu,proc,mem][i]: [1000, 1000, 1000][i] for i in range(3)}
    some_EXTRENAL_event = threading.Event()
    dataGenerator = GenerateDataWith([cpu,proc,mem], some_EXTRENAL_event, srr)
    interfaje = interface.CreateInterface(dataGenerator.data, some_EXTRENAL_event, srr)
    dataGenerator.make()
    interfaje.run()

# Helper Classes
# Threader using threading library which runs "live" updates on background thread
class Threader(threading.Thread):
    def __init__(self,cb, event, interval):
        self.cb = cb
        self.interval = interval
        self.event = event
        super(Threader,self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            self.cb()

# Generates the actual data using the monitors "list"
class GenerateDataWith:
    def __init__(self,monitors_,stop_event, srr):
        self.srr = srr
        self.monitors = monitors_
        self.data = {}
        for monitor in self.monitors:
            self.data[monitor.name] = monitor.pointer
        self.stop_event = stop_event
    def make(self):
        for monitor in self.monitors:
            sho3lana = Threader(monitor.get_new_vals,self.stop_event, self.srr[monitor]/1000)
            sho3lana.start()

# Calls main function when app begins running
if __name__ == '__main__':
    main()