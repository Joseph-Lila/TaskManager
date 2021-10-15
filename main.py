import time
import psutil

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'resizable', False)
Config.set("graphics", "width", 960)
Config.set("graphics", "height", 1017)
width_coefficient = .5

from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.lang import Builder
from MyLabel import MyLabel
from ListItemWithCheckbox import ListItemWithCheckbox
from RightCheckbox import RightCheckbox


class Myapp(MDApp):
    def __init__(self, **kwargs):
        self.title = 'P_r_o_k_o_p_e_n_k_o             IP-32         ------>             LAB2'
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.file_manager_answer = '?'

    def update_with_timer(self, seconds):
        while True:
            time.sleep(seconds)
            self.update_processes()

    def build(self):
        return Builder.load_file('app.kv')

    def update_processes(self):
        try:
            pid_collection = psutil.pids()
            processes = []

            #add lost elements
            if len(self.root.ids.container.children) != 0:
                my_collection = self.root.ids.container.children[:]
                for i in range(len(my_collection)):
                    split = my_collection[i].text.split()
                    my_collection[i] = int(split[len(split) - 4])
                total_pid_collection = set(pid_collection)
                current_pid_collection = set(my_collection)
                new_pid_collection = total_pid_collection - current_pid_collection
                old_pid_collection = current_pid_collection - total_pid_collection
                print('new_pid_collect = ', new_pid_collection)
                print('old_pid_collect = ', old_pid_collection)
                pid_reminder = list(new_pid_collection)
                pid_to_del = list(old_pid_collection)
                for i in range(len(pid_reminder)):
                    processes.append(psutil.Process(pid_reminder[i]))
                for i in range(len(processes)):
                    start_psutil = processes[i].create_time()
                    cur_text = '{:<40}{:>45}{:>60}'.format(processes[i].name(),
                                                           str(processes[i].pid),
                                                           str(time.strftime("%e.%m.%Y --- %H:%M:%S",
                                                                             time.localtime(start_psutil)
                                                                             )
                                                               )
                                                           )
                    self.root.ids.container.add_widget(ListItemWithCheckbox(text=cur_text))

            #clear gui
                if len(pid_to_del) != 0:
                    my_collection = self.root.ids.container.children[:]
                    for i in range(len(my_collection)):
                        split = my_collection[i].text.split()
                        if int(split[len(split) - 4]) in pid_to_del:
                            self.root.ids.container.remove_widget(my_collection[i])

            #fill gui
            if len(self.root.ids.container.children) == 0:
                for i in range(len(pid_collection)):
                    processes.append(psutil.Process(pid_collection[i]))
                for i in range(len(processes)):
                    start_psutil = processes[i].create_time()
                    cur_text = '{:<40}{:>45}{:>60}'.format(processes[i].name(),
                                                           str(processes[i].pid),
                                                           str(time.strftime("%e.%m.%Y --- %H:%M:%S",
                                                                             time.localtime(start_psutil)
                                                                             )
                                                               )
                                                           )
                    self.root.ids.container.add_widget(ListItemWithCheckbox(text=cur_text))

        except:
            self.update_processes()

    @staticmethod
    def on_terminate(proc):
        print('process {} terminated with exit code {}'.format(proc, proc.returncode))

    def file_manager_open(self, path):
        self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
        toast(path)
        self.file_manager_answer = path

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager_open = False
        self.file_manager.close()

    def get_file_manager_answer(self):
        path = f'D:\\System_programming\\lab2'
        self.file_manager.show(path)

    def add_process(self):
        try:
            psutil.Popen([self.file_manager_answer, '-c', 'while 1: pass'])
        except:
            print('Process adding error!')

    def remove_process(self):
            processes = []
            print(RightCheckbox.my_collection)
            for i in range(len(RightCheckbox.my_collection)):
                try:
                    self.root.ids.container.remove_widget(RightCheckbox.my_collection[i])
                    split = RightCheckbox.my_collection[i].text.split()
                    RightCheckbox.my_collection[i] = int(split[len(split) - 4])
                    processes.append(psutil.Process(RightCheckbox.my_collection[i]))
                    processes[-1].terminate()
                except:
                    pass
            alive = [1, 2]
            try:
                gone, alive = psutil.wait_procs(processes, timeout=3, callback=self.on_terminate)
            except:
                print('Недостаточно прав')
            for i in range(len(alive)):
                try:
                    alive[i].kill()
                except:
                    pass
            RightCheckbox.my_collection.clear()

    def on_start(self):
        self.update_processes()


if __name__ == '__main__':
    Myapp().run()
