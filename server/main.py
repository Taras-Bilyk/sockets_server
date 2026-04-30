from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from multiprocessing import Process
import subprocess
import socket
import config

class ServerApp(App):
    def build(self):
        self.my_ip_list = subprocess.check_output('hostname -I', shell=True, text=True).split(' ')
        if len(self.my_ip_list) > 1:
            self.my_ip = self.my_ip_list[len(self.my_ip_list) - 2]
        elif len(self.my_ip_list) == 1:
            self.my_ip = self.my_ip_list[0]
        else:
            self.my_ip = 'ip error'
            print("[CRITICAL] CAN'T FIND IP ADDRESS OF THIS SERVER !!!")
        config.ip_of_server = str(self.my_ip)
        self.port = int(config.port_of_server)
        self.counter_for_start_server_button = 1
        self.counter_for_disable_start_server_button = 0
        self.counter_for_disable_broadcast = 0
        self.main_layout = FloatLayout()
        self.start_server_button = Button(text = 'start server',
                                       size_hint = (.5, .15),
                                       font_size = 25,
                                       pos_hint = {'x': .02, 'y': .05},
                                       on_release = self.start_server)
        self.log_textinput = TextInput(hint_text = 'here will be more info...',
                                       text = 'd',
                                       size_hint = (.5, .5),
                                       font_size = 15,
                                       pos_hint = {'x': .02, 'y': .4})
        self.broadcast_textinput = TextInput(hint_text = 'broadcast...',
                                       size_hint = (.36, .2),
                                       font_size = 15,
                                       pos_hint = {'x': .6, 'y': .4})
        self.send_broadcast_button = Button(text = 'send broadcast (too all)',
                                       size_hint = (.36, .15),
                                       font_size = 15,
                                       pos_hint = {'x': .6, 'y': .05},
                                       on_release = self.send_broadcast,
                                       disabled = True)
        self.is_server_working_label = Label(text = 'to start server press "start server" button',
                                       color = (1, 0, 0, 1),
                                       size_hint = (.1, .01),
                                       font_size = 20,
                                       pos_hint = {'x': .2, 'y': .95})
        self.disable_start_and_stop_server_button = Button(text = 'enable / disable',
                                       size_hint = (.3, .1),
                                       font_size = 15,
                                       pos_hint = {'x': .02, 'y': .2},
                                       on_release = self.disable_start_server_button)
        self.disable_send_broadcast_button = Button(text = 'enable / disable',
                                       size_hint = (.2, .1),
                                       font_size = 15,
                                       pos_hint = {'x': .76, 'y': .2},
                                       on_release = self.disable_send_broadcast)
        self.server_ip_label = Label(text = 'server ip:\n####.####.#.#',
                                       size_hint = (.1, .01),
                                       font_size = 20,
                                       pos_hint = {'x': .65, 'y': .9})
        self.server_ip_label.text = 'server ip:\n' + str(self.my_ip)
        for widget in [
            self.start_server_button,
            self.log_textinput,
            self.broadcast_textinput,
            self.send_broadcast_button,
            self.is_server_working_label,
            self.disable_start_and_stop_server_button,
            self.disable_send_broadcast_button,
            self.server_ip_label
        ]:
            self.main_layout.add_widget(widget)
        Clock.schedule_interval(self.checking, 0.1)
        return self.main_layout

    def start_server(self, instance):
        if self.counter_for_start_server_button % 2 == 0:
            self.start_server_button.text = 'start server'
            self.is_server_working_label.text = 'server stopped'
            self.is_server_working_label.color = (1, 0, 0, 1)
            self.is_server_working_label.pos_hint = {'x': .08, 'y': .95}
            self.listening_process.kill()
            print('server stopped')
        else:
            self.start_server_button.text = 'stop server ...'
            self.is_server_working_label.text = 'server is working'
            self.is_server_working_label.color = (0, 1, 0, 1)
            self.is_server_working_label.pos_hint = {'x': .08, 'y': .95}
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.my_ip, self.port))
            print('server is listening ...')
            self.listening_process = Process(target=self.listen)
            self.listening_process.start()
        self.counter_for_start_server_button += 1
    def disable_start_server_button(self, instance):
        if self.counter_for_disable_start_server_button % 2 == 0:
            self.start_server_button.disabled = True
        else:
            self.start_server_button.disabled = False
        self.counter_for_disable_start_server_button += 1
    def disable_send_broadcast(self, instance):
        if self.counter_for_disable_broadcast % 2 == 0:
            self.send_broadcast_button.disabled = False
        else:
            self.send_broadcast_button.disabled = True
        self.counter_for_disable_broadcast += 1
    def listen(self):
        while 1:
            self.message = self.s.recvfrom(1024)
            self.file = open('log.txt', 'r')
            self.content = self.file.read()
            self.content_to_write = self.content + '\n' + str(self.message)
            self.file_to_wtite = open('log.txt', 'w')
            self.file_to_wtite.write(self.content_to_write)
            self.file_to_wtite.close()
    def checking(self, instance):
        self.text_from_log_file = open('log.txt', 'r').read()
        self.log_textinput.text = str(self.text_from_log_file)

    def send_broadcast(self, instance):
        print('send broadcast')

ServerApp().run()







