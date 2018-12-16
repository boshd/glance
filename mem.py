import psutil

class mem_monitor(object):
    
    # initializer
    def __init__(self):
        
        self.name = "mem"
        self.pointer = {}
        self.pointer['proc_info'] = { 
            'mem' : {}
        }

    # updates values (not really)
    def get_new_vals(self):
        pass

mem = mem_monitor()





