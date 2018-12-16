import psutil

class cpu_monitor(object):
    
    # initializer
    def __init__(self):
        self.pointer = {}
        self.name = "cpu"
        self.pointer['proc_info'] = {}
        self.pointer['chart'] = {
            'percentage' : ''
        }

    # updates values
    def get_new_vals(self):
        percent_usage = psutil.cpu_percent(percpu=True)
        sum_of_usage = sum(percent_usage)
        len_of_usage = len(percent_usage)

        self.pointer['chart']['percentage'] = sum_of_usage / len_of_usage

cpu = cpu_monitor()