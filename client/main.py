from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import sender

class MessangerApp(App):
    def build(self):
        self.main_layout = FloatLayout()
        self.main_layout_textinput = TextInput(hint_text ='enter text...',
                                               size_hint = (.8, .3),
                                               font_size = 25,
                                               pos_hint = {'x': .1, 'y': 0.6})
        self.main_layout_send_button = Button(text ='send to server',
                                              size_hint = (.8, .3),
                                              font_size = 25,
                                              pos_hint = {'x': .1, 'y': 0.1},
                                              on_release = self.send_data_to_server)
        self.main_layout.add_widget(self.main_layout_textinput)
        self.main_layout.add_widget(self.main_layout_send_button)
        return self.main_layout

    def send_data_to_server(self, instance):
        data = self.main_layout_textinput.text
        sender.send_to_server(data)

MessangerApp().run()





