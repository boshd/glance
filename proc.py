import psutil

class proc_monitor(object):

    # initializer
    def __init__(self):
        self.pointer = {}
        self.name = "proc"
        self.pointer['proc_info'] = { 
            'running_processes': 0,
            'running_threads': 0
        }
        self.pointer['grid'] = []

    # updates values
    def get_new_vals(self):
        proc_info_list = []
        for proc in psutil.process_iter():
            try:
                proc_info = {}
                proc_info['id'] = proc.pid
                proc_info['name'] = proc.name()
                proc_info['cpu'] = psutil.Process(proc.pid).cpu_percent()
                proc_info['memory'] = round(psutil.Process(proc.pid).memory_percent(),2)
                proc_info_list.append(proc_info)
            except:
                pass

        self.pointer['grid'] = []
        self.pointer['grid'].extend(proc_info_list)

proc = proc_monitor()