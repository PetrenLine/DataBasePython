import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from os.path import join

def register():
    gender = gender_combobox.get()
    full_name = name_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()
    birth_date = dob_entry.get_date()

    save_to_database(gender, full_name, phone, password, birth_date)

def save_to_database(gender, full_name, phone, password, birth_date):
    db_path = join(".", "registration_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


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

    cursor.execute('''
        INSERT INTO users (gender, full_name, phone, password, birth_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (gender, full_name, phone, password, str(birth_date)))  

    conn.commit()
    conn.close()

    messagebox.showinfo("Регистрация", "Регистрация успешно завершена!")

def show_table():

    table_window = tk.Toplevel(window)
    table_window.title("Таблица пользователей")

    tree = ttk.Treeview(table_window, columns=('ID', 'Пол', 'ФИО', 'Телефон', 'Пароль', 'Дата рождения'), show='headings')

    tree.heading('ID', text='ID')
    tree.heading('Пол', text='Пол')
    tree.heading('ФИО', text='ФИО')
    tree.heading('Телефон', text='Телефон')
    tree.heading('Пароль', text='Пароль')
    tree.heading('Дата рождения', text='Дата рождения')


    conn = sqlite3.connect(join(".", "registration_data.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack()

    edit_button = tk.Button(table_window, text="Редактировать", command=lambda: edit_record(tree))
    edit_button.pack()

    delete_button = tk.Button(table_window, text="Удалить", command=lambda: delete_record(tree))
    delete_button.pack()

    search_entry = tk.Entry(table_window)
    search_entry.pack()

    search_button = tk.Button(table_window, text="Поиск", command=lambda: search_records(tree, search_entry.get()))
    search_button.pack()


def edit_record(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")
        return
    record_id, gender, full_name, phone, password, birth_date = tree.item(selected_item)['values']

    edit_window = tk.Toplevel(window)
    edit_window.title("Редактирование записи")

    gender_label = tk.Label(edit_window, text="Пол:")
    gender_label.grid(row=0, column=0)
    gender_entry = tk.Entry(edit_window)
    gender_entry.grid(row=0, column=1)
    gender_entry.insert(0, gender)

    name_label = tk.Label(edit_window, text="ФИО:")
    name_label.grid(row=1, column=0)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=1, column=1)
    name_entry.insert(0, full_name)

    phone_label = tk.Label(edit_window, text="Номер телефона:")
    phone_label.grid(row=2, column=0)
    phone_entry = tk.Entry(edit_window)
    phone_entry.grid(row=2, column=1)
    phone_entry.insert(0, phone)

    password_label = tk.Label(edit_window, text="Пароль:")
    password_label.grid(row=3, column=0)
    password_entry = tk.Entry(edit_window, show="*")
    password_entry.grid(row=3, column=1)
    password_entry.insert(0, password)

    dob_label = tk.Label(edit_window, text="Дата рождения:")
    dob_label.grid(row=4, column=0)
    dob_entry = DateEntry(edit_window, width=12, background='darkblue',
                          foreground='white', borderwidth=2, date_pattern='yyyy-MM-dd')
    dob_entry.grid(row=4, column=1)
    dob_entry.set_date(birth_date)
    
    def save_changes():
        updated_gender = gender_entry.get()
        updated_full_name = name_entry.get()
        updated_phone = phone_entry.get()
        updated_password = password_entry.get()
        updated_birth_date = dob_entry.get_date()

        update_record(record_id, updated_gender, updated_full_name, updated_phone, updated_password, updated_birth_date)

        update_record_in_table(tree, selected_item, record_id, updated_gender, updated_full_name, updated_phone, updated_password, updated_birth_date)

        edit_window.destroy()


    save_button = tk.Button(edit_window, text="Сохранить изменения", command=save_changes)
    save_button.grid(row=5, column=0, columnspan=2)


def update_record_in_table(tree, item, record_id, gender, full_name, phone, password, birth_date):
    tree.item(item, values=(record_id, gender, full_name, phone, password, birth_date))


def update_record(record_id, gender, full_name, phone, password, birth_date):
    conn = sqlite3.connect(join(".", "registration_data.db"))
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET gender=?, full_name=?, phone=?, password=?, birth_date=?
        WHERE id=?
    ''', (gender, full_name, phone, password, str(birth_date), record_id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Обновление", "Запись успешно обновлена.")

def delete_record(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
        return

    record_id = tree.item(selected_item)['values'][0]

    conn = sqlite3.connect(join(".", "registration_data.db"))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (record_id,))
    conn.commit()
    conn.close()

    show_table()

    messagebox.showinfo("Удаление", "Запись успешно удалена.")

def search_records(tree, search_text):
    conn = sqlite3.connect(join(".", "registration_data.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE full_name LIKE ?", ('%' + search_text + '%',))
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert("", tk.END, values=row)

window = tk.Tk()
window.title("Регистрация")

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

show_table_button = tk.Button(window, text="Отобразить таблицу", command=show_table)
show_table_button.pack()


window.mainloop()
