import sys, npyscreen, psutil, drawille, math

class CreateInterface(npyscreen.NPSApp):

    def __init__(self,data,stop_event,srr):
        self.data            = data
        self.rr              = min(srr.values())
        self.stop_event      = stop_event
        self.window          = None 
        self.cpu_chart       = None
        self.pGrid           = None
        self.buttons         = None
        self.get_max_y       = None
        can_height           = None
        can_width            = None
        self.data_cpu        = None

    def while_waiting(self):
        memory_info    = self.data['mem']['proc_info']['mem']
        processes_info = self.data['proc']['proc_info']
        cpu_info       = self.data['cpu']['chart']
        cpcanv = drawille.Canvas()
        y = int(math.floor((float(cpu_info['percentage'])/100)*self.can_height*7))
        self.cpu_chart.value = (self.create_chart_for_cpu_using(y,cpcanv))
        self.cpu_chart.update(clear=True)
        self.proc_details = self.data['proc']['grid']
        sdata = self.proc_details
        cdata = []
        for proc in sdata: 
            cdata.append("{1: >5}  {0: <60}                                                       {2: >0.2f}%\
            ".format( (proc['name'][:60] + '...') if len(proc['name']) > 60 else proc['name'],
                       proc['id'],
                       proc['memory'],
                       " "*int(5*self.static_x))
            )
        self.pGrid.entry_widget.values =  cdata
        self.pGrid.entry_widget.comp_data(self.proc_details)
        self.pGrid.entry_widget.update(clear=True)
        self.window.display()

    def main(self):
        npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)

        self.keypress_timeout_default = 10
        if self.rr < 1000:
            self.keypress_timeout_default = int(self.rr / 100)

        self.window = WindowForm(parentApp = self, name="Glance")
        global last_height
        global last_width
        get_max_y, get_max_x = self.window.curses_pad.getmaxyx()
        last_height = get_max_y
        last_width = get_max_x
        self.static_y = float(get_max_y)/28
        self.static_x = float(get_max_x)/104
        self.cpu_chart = self.window.add(TheBox, name="CPU Usage History", relx=155, rely=5, max_height=int(get_max_y)-10, max_width=int(100*self.static_x*0.35))
        self.cpu_chart.value = ""
        self.pGrid = self.window.add(ButtonBox, name="Processes", relx=10, rely=5, max_height=int(get_max_y)-10, max_width=int((get_max_x-20)*0.65)-5)
        self.pGrid.entry_widget.values = []
        self.pGrid.entry_widget.scroll_exit = False
        self.buttons = self.window.add(npyscreen.FixedText, relx=10, rely=int(get_max_y)-5)
        self.buttons.value = "ctrl+n: Sort by Usage ^ctrl+k: Kill Processes"
        self.buttons.display()
        self.can_height = int(get_max_y)-10
        self.can_width = int((get_max_x-20)*0.65)-5
        self.data_cpu = [0]*self.can_width
        self.window.edit()

    def create_chart_for_cpu_using(self, height, canvas):
        data_arr = self.data_cpu
        for i in range(self.can_width):
            if i >= 2:
                data_arr[i-2] = data_arr[i]
        data_arr[self.can_width-1] = height
        data_arr[self.can_width-2] = height
        for x in range(0,self.can_width):
            for height in range(self.can_height,self.can_height-data_arr[x],-1):
                canvas.set(x,height)
        return canvas.frame(self.can_width-150,-182,self.can_width*2,self.can_height)

class ButtonControl(npyscreen.MultiLineAction):
    def __init__(self,*args,**kwargs):
        super(ButtonControl,self).__init__(*args,**kwargs)
        self.add_handlers({
            "^N" : self.sort_mem,
            "^K" : self.kill_proc,
        })
        self.comp_data_ = None
    def kill_proc():
        pid_to_kill = self._get_selected_process_pid()
        try:
            target = psutil.Process(int(pid_to_kill))
            target.terminate()
        except:
            pass
    def sort_mem():
        sort_mem  = True
        sort_main = False
    def comp_data(self, arr):
        self.comp_data_ = arr

class TheBox(npyscreen.BoxTitle):
    '''
    bbb
    '''
    box_str = ""
    boxx_str = ""
    _contained_widget = npyscreen.MultiLineEdit

class ButtonBox(npyscreen.BoxTitle):
    '''
    jj
    '''
    boxb_str = ""
    boxbb_str = ""
    _contained_widget = ButtonControl

class WindowForm(npyscreen.FormBaseNew):
    def create(self, *args, **kwargs):
        super(WindowForm, self).create(*args, **kwargs)
    def while_waiting(self):
        pass
