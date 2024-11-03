import os
import requests
import configparser
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.listview import ListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.animation import Animation

config = configparser.ConfigParser()

class ModManagerApp(App):
    def build(self):
        self.title = "Менеджер модов"
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.folder_input = TextInput(hint_text="Выберите папку для загрузки", multiline=False)
        self.layout.add_widget(self.folder_input)

        self.select_folder_button = Button(text="Выбрать папку", on_press=self.select_folder)
        self.layout.add_widget(self.select_folder_button)

        self.mod_list = ListView()
        self.layout.add_widget(ScrollView(size_hint=(1, 0.5), do_scroll_x=False, do_scroll_y=True))

        self.mod_input = TextInput(hint_text="Введите URL мода", multiline=False)
        self.layout.add_widget(self.mod_input)

        self.add_mod_button = Button(text="Добавить мод", on_press=self.add_mod)
        self.layout.add_widget(self.add_mod_button)

        self.remove_mod_button = Button(text="Удалить выбранный мод", on_press=self.remove_mod)
        self.layout.add_widget(self.remove_mod_button)

        self.download_button = Button(text="Загрузить моды", on_press=self.download_mods)
        self.layout.add_widget(self.download_button)

        self.console = Label(size_hint_y=None, height=44)
        self.layout.add_widget(self.console)

        self.load_settings()
        return self.layout

    def load_settings(self):
        if os.path.exists('mods.ini'):
            config.read('mods.ini')
            if 'Settings' in config:
                self.folder_input.text = config['Settings'].get('download_folder', '')

    def select_folder(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title="Выберите папку", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=self.on_folder_selected)
        popup.open()

    def on_folder_selected(self, chooser, selection, touch):
        if selection:
            self.folder_input.text = selection[0]
            self.save_settings()

    def save_settings(self):
        config['Settings'] = {'download_folder': self.folder_input.text}
        with open('mods.ini', 'w') as configfile:
            config.write(configfile)

    def add_mod(self, instance):
        mod_url = self.mod_input.text
        if mod_url:
            self.mod_list.adapter.data.extend([mod_url])
            self.mod_list._trigger_reset_populate()
            self.console.text += f"Добавлен мод: {mod_url}\n"
            self.save_settings()

    def remove_mod(self, instance):
        selected_mod = self.mod_list.adapter.get_data()
        if selected_mod:
            self.mod_list.adapter.data.remove(selected_mod[0])
            self.mod_list._trigger_reset_populate()
            self.console.text += f"Удален мод: {selected_mod[0]}\n"
            self.save_settings()

    def download_mods(self, instance):
        download_folder = self.folder_input.text
        if not download_folder:
            self.console.text += "Ошибка: Выберите папку для загрузки\n"
            return
        for mod_url in self.mod_list.adapter.get_data():
            version_info = self.get_latest_version(mod_url)
            if version_info:
                filename = version_info["files"][0]["filename"]
                download_url = version_info["files"][0]["url"]
                self.download_file(download_url, download_folder, filename)
            else:
                self.console.text += f"Предупреждение: Мод {mod_url} не найден\n"

    def get_latest_version(self, mod_url):
        mod_id = mod_url.split('/')[-1]
        url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
        response = requests.get(url)
        if response.status_code == 200:
            versions = response.json()
            return next((version for version in versions if "1.21.1" in version["game_versions"]), None)
        return None

    def download_file(self, url, dest_folder, filename):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(dest_folder, filename)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            self.console.text += f"Файл {filename} загружен в {dest_folder}\n"
        else:
            self.console.text += f"Ошибка: Не удалось загрузить файл {filename}\n"

if __name__ == '__main__':
    ModManagerApp().run()