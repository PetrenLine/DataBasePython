import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from os.path import join

def register():
    # Получаем значения из полей ввода
    gender = gender_combobox.get()
    full_name = name_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()
    birth_date = dob_entry.get_date()

    # Сохраняем данные в базе данных
    save_to_database(gender, full_name, phone, password, birth_date)

def save_to_database(gender, full_name, phone, password, birth_date):
    # Подключаемся к базе данных (если файла нет, SQLite создаст новый)
    db_path = join(".", "registration_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            full_name TEXT,
            phone TEXT,
            password TEXT,
            birth_date DATE
        )
    ''')

    # Вставляем данные в таблицу
    cursor.execute('''
        INSERT INTO users (gender, full_name, phone, password, birth_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (gender, full_name, phone, password, str(birth_date)))  # Преобразуем дату в строку

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

    # Оповещаем пользователя об успешной регистрации
    messagebox.showinfo("Регистрация", "Регистрация успешно завершена!")

def show_table():
    # Открываем новое окно для отображения таблицы
    table_window = tk.Toplevel(window)
    table_window.title("Таблица пользователей")

    # Создаем Treeview для отображения таблицы
    tree = ttk.Treeview(table_window, columns=('ID', 'Пол', 'ФИО', 'Телефон', 'Пароль', 'Дата рождения'), show='headings')

    # Устанавливаем заголовки столбцов
    tree.heading('ID', text='ID')
    tree.heading('Пол', text='Пол')
    tree.heading('ФИО', text='ФИО')
    tree.heading('Телефон', text='Телефон')
    tree.heading('Пароль', text='Пароль')
    tree.heading('Дата рождения', text='Дата рождения')

    # Выбираем данные из базы данных и отображаем их в Treeview
    conn = sqlite3.connect(join(".", "registration_data.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Устанавливаем Treeview на окно
    tree.pack()

# Создаем главное окно
window = tk.Tk()
window.title("Регистрация")

# Создаем элементы управления на главном окне
gender_label = tk.Label(window, text="Пол:")
gender_label.pack()
gender_combobox = ttk.Combobox(window, values=["Мужской", "Женский"])
gender_combobox.pack()

name_label = tk.Label(window, text="ФИО:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

phone_label = tk.Label(window, text="Номер телефона:")
phone_label.pack()
phone_entry = tk.Entry(window)
phone_entry.pack()

password_label = tk.Label(window, text="Пароль:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

dob_label = tk.Label(window, text="Дата рождения:")
dob_label.pack()

dob_entry = DateEntry(window, width=12, background='darkblue',
                      foreground='white', borderwidth=2, date_pattern='dd.mm.y')
dob_entry.pack()

register_button = tk.Button(window, text="Зарегистрироваться", command=register)
register_button.pack()

# Кнопка для отображения таблицы
show_table_button = tk.Button(window, text="Отобразить таблицу", command=show_table)
show_table_button.pack()

# Запускаем главный цикл событий Tkinter
window.mainloop()
