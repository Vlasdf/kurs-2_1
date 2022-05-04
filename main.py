from tkinter import *
from tkinter import messagebox
import pickle
import tkinter as tk
from tkinter import ttk
import sqlite3

root1 = Tk()
root1.geometry('500x500')
root1.title('Войти в систему')

def register():
    text = Label(text='Для входа в систему зарегистрируйтесь')
    text_log = Label(text='Введите ваш логин')
    register_login = Entry()
    text_pass1 = Label(text='Введите ваш пароль')
    register_pass1 = Entry()
    text_pass2 = Label(text='Повторите пароль')
    register_pass2 = Entry()
    btn_reg = Button(text='Зарегистрироваться', command=lambda:save())
    text.pack()
    text_log.pack()
    register_login.pack()
    text_pass1.pack()
    register_pass1.pack()
    text_pass2.pack()
    register_pass2.pack()
    btn_reg.pack()

    def save():
        login_pass_save = {}
        login_pass_save[register_login.get()]=register_pass1.get()
        f = open('login.txt', 'wb')
        pickle.dump(login_pass_save, f)
        f.close()
        login()

    def login():
        text_log = Label(text='Теперь вы можете войти в систему')
        text_enter_login = Label(text='Введите ваш логин')
        enter_login = Entry()
        text_enter_password = Label(text='Введите ваш пароль')
        enter_password = Entry(show='*')
        btn_enter = Button(text='Войти в систему', command=lambda: log_pass())
        text_log.pack()
        text_enter_login.pack()
        enter_login.pack()
        text_enter_password.pack()
        enter_password.pack()
        btn_enter.pack()

        def log_pass():
            f = open('login.txt', 'rb')
            a = pickle.load(f)
            f.close()
            if enter_login.get() in a:
                if enter_password.get() == a[enter_login.get()]:

                    class Main(tk.Frame):
                        def __init__(self, root):
                            super().__init__(root)
                            self.init_main()
                            self.db = db
                            self.view_records()

                        def init_main(self):
                            toolbar = tk.Frame(root, bg='#d7d8e0', bd=2)
                            toolbar.pack(side=tk.TOP, fill=tk.X)

                            btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog,
                                                        bg='#d7d8e0', bd=0,
                                                        compound=tk.TOP)
                            btn_open_dialog.pack(side=tk.LEFT)

                            btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0,
                                                        compound=tk.TOP, command=self.open_update_dialog)
                            btn_edit_dialog.pack(side=tk.LEFT)

                            btn_delete_records = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0,
                                                           compound=tk.TOP, command=self.delete_records)
                            btn_delete_records.pack(side=tk.LEFT)

                            btn_search_records = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, compound=tk.TOP,
                                                           command=self.open_search_dialog)
                            btn_search_records.pack(side=tk.LEFT)

                            btn_refresh_records = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0,
                                                            compound=tk.TOP,
                                                            command=self.view_records)
                            btn_refresh_records.pack(side=tk.LEFT)

                            self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15,
                                                     show='headings')

                            self.tree.column('ID', width=30, anchor=tk.CENTER)
                            self.tree.column('description', width=365, anchor=tk.CENTER)
                            self.tree.column('costs', width=150, anchor=tk.CENTER)
                            self.tree.column('total', width=100, anchor=tk.CENTER)

                            self.tree.heading('ID', text='ID')
                            self.tree.heading('description', text='Тип помещения')
                            self.tree.heading('costs', text='Покупка\Аренда')
                            self.tree.heading('total', text='Сумма')

                            self.tree.pack()
                            self.tree.bind("<<TreeviewSelect>>", self.select)
                            self.tree.bind("<Double-Button-1>", self.doubleClick_Info)




                        def select(self, event):
                            for selection in self.tree.selection():
                                item = self.tree.item(selection)
                                self.id = item["values"][0]


                        def description_info(self):
                            id = self.id
                            data = db.search_description(id)

                            descInfo_window = tk.Tk()
                            descInfo_window.title("Description Info")
                            descInfo_window.geometry("640x420+450+250")

                            square = data[0][1]
                            adress = data[0][2]
                            rooms = data[0][3]
                            lbl_sqr = tk.Label(descInfo_window, text=f"Площадь помещения: {square}",
                                                      font=("Ubuntu Mono", 32))


                            lbl_adress = tk.Label(descInfo_window, text=f"Расположена на {adress}",
                                                     font=("Ubuntu Mono", 16))
                            lbl_room = tk.Label(descInfo_window, text=f"Количество комнат: {rooms}",
                                                     font=("Ubuntu Mono", 16))

                            lbl_sqr.pack()
                            lbl_adress.pack()
                            lbl_room.pack()
                            frm_description = tk.Frame(descInfo_window)
                            frm_description.pack()

                            text = tk.Text(frm_description, width=65, height=12, wrap="word",
                                           highlightthickness=0,
                                           font=("Ubuntu Mono", 16))
                            text.pack(pady=15)
                            text["state"] = "disabled"
                            text["background"] = "#333232"

                            btn_close = tk.Button(descInfo_window, height=2, text="So interesting",
                                                  font=("Ubuntu Mono", 15),
                                                  command=descInfo_window.destroy)
                            btn_close.pack()
                            descInfo_window.mainloop()


                        def doubleClick_Info(self, event):
                            self.description_info()
                            self.tree.bind("<<TreeviewSelect>>", self.select)


                        def records(self, description, costs, total):
                            self.db.insert_data(description, costs, total)
                            self.view_records()

                            self.tree.pack(side=tk.LEFT)

                            scroll = tk.Scrollbar(self, command=self.tree.yview)
                            scroll.pack(side=tk.LEFT, fill=tk.Y)
                            self.tree.configure(yscrollcommand=scroll.set)

                        def update_record(self, description, costs, total):
                            self.db.c.execute('''UPDATE estate SET description=?, costs=?, total=? WHERE ID=?''',
                                              (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
                            self.db.conn.commit()
                            self.view_records()

                        def view_records(self):
                            self.db.c.execute('''SELECT * FROM estate''')
                            [self.tree.delete(i) for i in self.tree.get_children()]
                            [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


                        def delete_records(self):
                            for selection_item in self.tree.selection():
                                self.db.c.execute('''DELETE FROM estate WHERE ID=?''',
                                                  (self.tree.set(selection_item, '#1'),))
                            self.db.conn.commit()
                            self.view_records()

                        def search_records(self, description):
                            description = ('%' + description + '%',)  # для нахождения слова в любой позиции
                            self.db.c.execute('''SELECT * FROM estate WHERE description LIKE ?''',
                                              description)  # sql запрос \
                            [self.tree.delete(i) for i in
                             self.tree.get_children()]  # очищаем таблицу построчно при помощи цикла
                            [self.tree.insert('', 'end', values=row) for row in
                             self.db.c.fetchall()]  # отображаем результат

                        def open_dialog(self):
                            Child()

                        def open_update_dialog(self):
                            Update()

                        def open_search_dialog(self):
                            Search()


                    class Child(tk.Toplevel):
                        def __init__(self):
                            super().__init__(root)
                            self.init_child()
                            self.view = app

                        def init_child(self):
                            self.title('Добавление позиции')
                            self.geometry('400x220+400+300')
                            self.resizable(False, False)

                            label_description = tk.Label(self, text='Тип помещения:')
                            label_description.place(x=50, y=50)
                            label_select = tk.Label(self, text='Покупка/Аренда:')
                            label_select.place(x=50, y=80)
                            label_sum = tk.Label(self, text='Сумма:')
                            label_sum.place(x=50, y=110)

                            self.entry_description = ttk.Entry(self)
                            self.entry_description.place(x=200, y=50)

                            self.entry_money = ttk.Entry(self)
                            self.entry_money.place(x=200, y=110)

                            self.combobox = ttk.Combobox(self, values=[u'Покупка', u'Аренда'])
                            self.combobox.current(0)
                            self.combobox.place(x=200, y=80)

                            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
                            btn_cancel.place(x=300, y=170)

                            self.btn_ok = ttk.Button(self, text='Добавить')
                            self.btn_ok.place(x=300, y=170)
                            self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                                           self.combobox.get(),
                                                                                           self.entry_money.get()))

                            self.grab_set()
                            self.focus_set()

                    class Update(Child):
                        def __init__(self):
                            super().__init__()
                            self.init_edit()
                            self.view = app
                            self.db = db
                            self.default_data()

                        def init_edit(self):
                            self.title('Редактировать позицию')
                            btn_edit = ttk.Button(self, text='Редактировать')
                            btn_edit.place(x=205, y=170)
                            btn_edit.bind('<Button-1>',
                                          lambda event: self.view.update_record(self.entry_description.get(),
                                                                                self.combobox.get(),
                                                                                self.entry_money.get()))

                            self.btn_ok.destroy()

                        def default_data(self):
                            self.db.c.execute('''SELECT * FROM estate WHERE id=?''',
                                              (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
                            row = self.db.c.fetchone()
                            self.entry_description.insert(0, row[1])
                            if row[2] != 'Квартира':
                                self.combobox.current(1)
                            self.entry_money.insert(0, row[3])

                    class Search(tk.Toplevel):
                        def __init__(self):
                            super().__init__()
                            self.init_search()
                            self.view = app

                        def init_search(self):
                            self.title('Поиск')
                            self.geometry('300x100+400+300')  # размер окна
                            self.resizable(False, False)  # запретим изменять размеры окна

                            label_search = tk.Label(self, text='Поиск')  # виджет поиска
                            label_search.place(x=50, y=20)  # местонахождение виджета поиска

                            self.entry_search = ttk.Entry(self)  # поле ввода для поиска
                            self.entry_search.place(x=105, y=20, width=150)  # местонахождение поля ввода

                            btn_cancel = ttk.Button(self, text='Закрыть',
                                                    command=self.destroy)  # кнопка закрытия поля ввода
                            btn_cancel.place(x=185, y=50)  # местонахождение кнопки закрытия

                            btn_search = ttk.Button(self, text='Поиск')  # кнопка поиска
                            btn_search.place(x=105, y=50)  # местонахождение кнопки поиска
                            btn_search.bind('<Button-1>', lambda event: self.view.search_records(
                                self.entry_search.get()))  # бинд кнопки
                            btn_search.bind('<Button-1>', lambda event: self.destroy(),
                                            add='+')  # функция автоматического закрытия кнопки после нажания


                    class DB:
                        def __init__(self):
                            self.conn = sqlite3.connect('finance.db')
                            self.c = self.conn.cursor()
                            self.c.execute(
                                '''CREATE TABLE IF NOT EXISTS estate (id integer primary key, description text, costs text, total real)''')
                            self.conn.commit()

                        def insert_data(self, description, costs, total):
                            self.c.execute('''INSERT INTO estate(description, costs, total) VALUES (?, ?, ?)''',
                                           (description, costs, total))
                            self.conn.commit()

                        def search_description(self, id):
                            """Search authors biography"""
                            self.c.execute(f"SELECT * FROM place where id={id}")
                            response = self.c.fetchall()
                            return response



                    if __name__ == "__main__":
                        root = tk.Tk()
                        db = DB()
                        app = Main(root)
                        app.pack()
                        root.title("Estate")
                        root.geometry("665x450+300+200")
                        root.resizable(False, False)
                        root.mainloop()

                else:
                    messagebox.showinfo('Неверный логин или пароль')

register()
root1.mainloop()

