import time
import psutil

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'resizable', False)
Config.set("graphics", "width", 960)
Config.set("graphics", "height", 1017)

from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.lang import Builder
from MyLabel import MyLabel
from ListItemWithCheckbox import ListItemWithCheckbox
from RightCheckbox import RightCheckbox
from kivy.clock import Clock


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

    def build(self):
        return Builder.load_file('app.kv')

    """Function for sorting processes by name"""
    @staticmethod
    def sort_key(item):
        return str.lower(item.name())

    """It returns not existing processes pids collection or None."""
    def get_pid_collection_to_del(self):
        if len(self.root.ids.container.children) != 0:
            pid_collection = psutil.pids()
            my_collection = [int(item.text.split()[len(item.text.split()) - 4]) for item in
                             self.root.ids.container.children[:]]
            total_pid_collection = set(pid_collection)
            current_pid_collection = set(my_collection)
            old_pid_collection = current_pid_collection - total_pid_collection
            return list(old_pid_collection)
        else:
            return None

    """It returns not visible processes pids collection or None."""
    def get_pid_collection_to_add(self):
        if len(self.root.ids.container.children) != 0:
            pid_collection = psutil.pids()
            my_collection = [int(item.text.split()[len(item.text.split()) - 4]) for item in
                             self.root.ids.container.children[:]]
            total_pid_collection = set(pid_collection)
            current_pid_collection = set(my_collection)
            new_pid_collection = total_pid_collection - current_pid_collection
            return list(new_pid_collection)
        else:
            return None

    """This function adds new list items to gui list"""
    def append_new_processes_gui(self):
        pid_reminder = self.get_pid_collection_to_add()
        print('New pid collection: ', pid_reminder)
        if pid_reminder is not None:
            processes = [psutil.Process(pid) for pid in pid_reminder]
            for proc in processes:
                start_psutil = proc.create_time()
                cur_text = '{:<40}{:>45}{:>60}'.format(proc.name(),
                                                       str(proc.pid),
                                                       str(time.strftime("%e.%m.%Y --- %H:%M:%S",
                                                                         time.localtime(start_psutil)
                                                                         )
                                                           )
                                                       )
                self.root.ids.container.add_widget(ListItemWithCheckbox(text=cur_text))

    """This function clears not existing list items from gui list"""
    def remove_not_existing_processes_gui(self):
        not_existing_pid_collection = self.get_pid_collection_to_del()
        print('Not existing pid collection: ', not_existing_pid_collection)
        if not_existing_pid_collection is not None:
            my_collection = self.root.ids.container.children[:]
            for item in my_collection:
                split = item.text.split()
                if int(split[len(split) - 4]) in not_existing_pid_collection:
                    self.root.ids.container.remove_widget(item)

    """This function adds list items to gui processes list"""
    def fill_empty_gui_list(self):
        if len(self.root.ids.container.children) == 0:
            pid_collection = psutil.pids()
            processes = [psutil.Process(pid) for pid in pid_collection]
            processes.sort(key=self.sort_key)
            for proc in processes:
                start_psutil = proc.create_time()
                cur_text = '{:<40}{:>45}{:>60}'.format(proc.name(),
                                                       str(proc.pid),
                                                       str(time.strftime("%e.%m.%Y --- %H:%M:%S",
                                                                         time.localtime(start_psutil)
                                                                         )
                                                           )
                                                       )
                self.root.ids.container.add_widget(ListItemWithCheckbox(text=cur_text))

    def update_processes_gui(self):
        try:
            """If there are new processes which are not visible"""
            self.append_new_processes_gui()
            """If some processes have stoped but are still visible"""
            self.remove_not_existing_processes_gui()
            """If gui processes list is empty"""
            self.fill_empty_gui_list()
        except:
            self.update_processes_gui()

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
        path = f'D:\\System_programming\\TaskManager'
        self.file_manager.show(path)

    def add_process(self):
        try:
            psutil.Popen([self.file_manager_answer, '-c', 'while 1: pass'])
        except:
            print('Process adding error!')

    def remove_process(self):
        processes_to_remove_gui = [item for item in RightCheckbox.my_collection]
        for item in processes_to_remove_gui:
            self.root.ids.container.remove_widget(item)
        processes_to_terminate = [
                psutil.Process(int(item.text.split()[len(item.text.split()) - 4]))
                for item in RightCheckbox.my_collection
            ]
        try:
            for process in processes_to_terminate:
                process.terminate()
        except:
            pass
        alive = [1, 2]
        try:
            gone, alive = psutil.wait_procs(processes_to_terminate, timeout=3, callback=self.on_terminate)
        except:
            pass
        for proc in alive:
            try:
                proc.kill()
            except:
                pass
        RightCheckbox.my_collection.clear()

    """Each dt seconds the gui list will be updated."""
    def callback(self, dt):
        self.update_processes_gui()

    def on_start(self):
        self.update_processes_gui()
        Clock.schedule_interval(self.callback, 10)


if __name__ == '__main__':
    Myapp().run()
