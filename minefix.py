import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import configparser

# Инициализация конфигурации
config = configparser.ConfigParser()

# Создание главного окна с темой
root = ThemedTk(theme="arc")
root.title("Менеджер модов")

# Переменные
folder_var = tk.StringVar()
version_var = tk.StringVar()
loader_var = tk.StringVar()

# Функция для загрузки настроек из файла
def load_settings():
    if os.path.exists('mods.ini'):
        config.read('mods.ini')
        if 'Settings' in config:
            folder_var.set(config['Settings'].get('download_folder', ''))
            version_var.set(config['Settings'].get('minecraft_version', '1.21.1'))
            loader_var.set(config['Settings'].get('loader', 'fabric'))
        if 'Mods' in config:
            return config['Mods'].values()
    return []

# Функция для сохранения настроек в файл
def save_settings():
    config['Settings'] = {
        'download_folder': folder_var.get(),
        'minecraft_version': version_var.get(),
        'loader': loader_var.get()
    }
    config['Mods'] = {f'mod_{i}': url for i, url in enumerate(mod_links)}
    with open('mods.ini', 'w') as configfile:
        config.write(configfile)

# Список ссылок на моды
mod_links = list(load_settings())

# Функция для получения последней версии мода
def get_latest_version(mod_url, game_version, loader):
    mod_id = mod_url.split('/')[-1]
    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json()
        for version in versions:
            if game_version in version["game_versions"] and loader in version["loaders"]:
                return version
    return None

# Функция для загрузки файла
def download_file(url, dest_folder, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(dest_folder, filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        log_message(f"Файл {filename} загружен в {dest_folder}", "success")
    else:
        log_message(f"Ошибка: Не удалось загрузить файл {filename}", "error")

# Функция для выбора папки
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)
        log_message(f"Выбрана папка: {folder}", "success")
        save_settings()

# Функция для обновления списка модов
def update_mod_list():
    mod_listbox.delete(0, tk.END)
    for mod in mod_links:
        mod_listbox.insert(tk.END, mod)
    log_message("Список модов обновлен", "success")

# Функция для добавления мода
def add_mod():
    mod_url = mod_entry.get()
    if mod_url:
        mod_links.append(mod_url)
        update_mod_list()
        log_message(f"Добавлен мод: {mod_url}", "success")
        save_settings()

# Функция для удаления выбранного мода
def remove_mod():
    selected_mod = mod_listbox.curselection()
    if selected_mod:
        mod_url = mod_links.pop(selected_mod[0])
        update_mod_list()
        log_message(f"Удален мод: {mod_url}", "success")
        save_settings()

import re

def download_mods():
    download_folder = folder_var.get()
    game_version = version_var.get()
    loader = loader_var.get()
    if not download_folder:
        messagebox.showerror("Ошибка", "Выберите папку для загрузки")
        return
    for mod_url in mod_links:
        version_info = get_latest_version(mod_url, game_version, loader)
        if version_info:
            version_number = version_info["version_number"]
            filename = version_info["files"][0]["filename"]
            download_url = version_info["files"][0]["url"]
            file_path = os.path.join(download_folder, filename)
            
            # Проверка, существует ли файл и соответствует ли он последней версии
            if os.path.exists(file_path):
                log_message(f"Мод {filename} уже установлен и соответствует последней версии.", "success")
                continue
            
            # Удаление старой версии, если она существует
            base_name = re.sub(r'-\d+(\.\d+)*', '', filename)  # Удаляем версию из имени файла
            for existing_file in os.listdir(download_folder):
                if existing_file.startswith(base_name) and existing_file != filename:
                    os.remove(os.path.join(download_folder, existing_file))
                    log_message(f"Удалена старая версия мода: {existing_file}", "success")
            
            # Загрузка новой версии
            download_file(download_url, download_folder, filename)
        else:
            log_message(f"Предупреждение: Мод {mod_url}, версия для {game_version} не найдена", "error")

# Функция для логирования сообщений в консоль
def log_message(message, tag):
    console_text.insert(tk.END, message + "\n", tag)
    console_text.see(tk.END)

# Настройка стиля
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")
style.map("TButton",
          foreground=[('pressed', 'red'), ('active', 'blue')],
          background=[('pressed', '!disabled', 'black'), ('active', 'white')])

# Основной фрейм
main_frame = ttk.Frame(root)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Интерфейс
ttk.Label(main_frame, text="Выберите папку для загрузки:").pack()
ttk.Entry(main_frame, textvariable=folder_var, width=50).pack()
ttk.Button(main_frame, text="Выбрать папку", command=select_folder).pack()

ttk.Label(main_frame, text="Список модов:").pack()
mod_listbox = tk.Listbox(main_frame, width=50, height=10)
mod_listbox.pack()

# Поле для ввода ссылки на мод
mod_entry = ttk.Entry(main_frame, width=50)
mod_entry.pack()

ttk.Button(main_frame, text="Добавить мод", command=add_mod).pack()
ttk.Button(main_frame, text="Удалить выбранный мод", command=remove_mod).pack()

ttk.Label(main_frame, text="Выберите версию Minecraft:").pack()
ttk.Entry(main_frame, textvariable=version_var, width=50).pack()

ttk.Label(main_frame, text="Выберите загрузчик:").pack()
loader_menu = ttk.OptionMenu(main_frame, loader_var, "fabric", "fabric", "forge", "quit", "neoforge")
loader_menu.pack()

ttk.Button(main_frame, text="Обновить список модов", command=update_mod_list).pack()
ttk.Button(main_frame, text="Загрузить моды", command=download_mods).pack()

# Консоль для вывода сообщений
console_frame = ttk.Frame(root)
console_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

console_text = tk.Text(console_frame, width=60, height=20, state='normal')
console_text.pack()

# Настройка тегов для изменения цвета текста
console_text.tag_config("success", foreground="green")
console_text.tag_config("error", foreground="red")

# Инициализация списка модов
update_mod_list()

# Запуск приложения
root.mainloop()