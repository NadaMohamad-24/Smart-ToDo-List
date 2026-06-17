import ttkbootstrap as tb
from tkinter import ttk, messagebox

from database import (
    insert_task,
    get_tasks,
    delete_task,
    complete_task,
    update_task,
    search_tasks
)


class ToDoGUI(tb.Window):

    def __init__(self):

        super().__init__(themename="flatly")

        self.title("Smart To-Do List")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.current_theme = "flatly"
        self.selected_id = None

        # Title

        tb.Label(
            self,
            text="SMART TO-DO LIST",
            font=("Helvetica", 26, "bold")
        ).pack(pady=15)

        # Task

        tb.Label(
            self,
            text="Task"
        ).pack()

        self.task_entry = tb.Entry(
            self,
            width=40
        )

        self.task_entry.pack()

        # Priority

        tb.Label(
            self,
            text="Priority"
        ).pack()

        self.priority_box = tb.Combobox(
            self,
            values=["High", "Medium", "Low"],
            width=20
        )

        self.priority_box.pack()

        self.priority_box.current(0)

        # Due Date

        tb.Label(
            self,
            text="Due Date (YYYY-MM-DD)"
        ).pack()

        self.date_entry = tb.Entry(
            self,
            width=20
        )

        self.date_entry.pack(pady=5)

        # Search

        tb.Label(
            self,
            text="Search"
        ).pack()

        self.search_entry = tb.Entry(
            self,
            width=30
        )

        self.search_entry.pack()

        tb.Button(
            self,
            text="Search",
            bootstyle="info",
            command=self.search_task
        ).pack(pady=5)
                # Buttons Frame

        button_frame = tb.Frame(self)

        button_frame.pack(pady=10)


        tb.Button(
            button_frame,
            text="Add",
            bootstyle="success",
            command=self.add_task
        ).grid(row=0, column=0, padx=5)


        tb.Button(
            button_frame,
            text="Edit",
            bootstyle="warning",
            command=self.edit_selected
        ).grid(row=0, column=1, padx=5)


        tb.Button(
            button_frame,
            text="Update",
            bootstyle="info",
            command=self.update_selected
        ).grid(row=0, column=2, padx=5)


        tb.Button(
            button_frame,
            text="Delete",
            bootstyle="danger",
            command=self.delete_selected
        ).grid(row=0, column=3, padx=5)


        tb.Button(
            button_frame,
            text="Complete",
            bootstyle="primary",
            command=self.complete_selected
        ).grid(row=0, column=4, padx=5)


        # Dark / Light Mode

        tb.Button(
            self,
            text="🌙 Dark / ☀ Light",
            bootstyle="secondary",
            command=self.toggle_theme
        ).pack(pady=10)


        # Statistics

        self.stats_label = tb.Label(
            self,
            text=""
        )

        self.stats_label.pack(pady=10)


        # Table

        columns = (
            "ID",
            "Task",
            "Priority",
            "Due Date",
            "Status"
        )


        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )


        for col in columns:

            self.tree.heading(col, text=col)

            if col == "ID":

                self.tree.column(col, width=70)

            elif col == "Task":

                self.tree.column(col, width=300)

            else:

                self.tree.column(col, width=180)


        self.tree.pack(pady=20)


        self.tree.tag_configure(
            "completed",
            foreground="green"
        )


        self.load_tasks()
    def add_task(self):

        title = self.task_entry.get().strip()
        priority = self.priority_box.get()
        due_date = self.date_entry.get().strip()

        if title == "" or due_date == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return

        insert_task(
            title,
            priority,
            due_date
        )

        messagebox.showinfo(
            "Success",
            "Task Added Successfully!"
        )

        self.task_entry.delete(0, "end")
        self.date_entry.delete(0, "end")

        self.load_tasks()


    def load_tasks(self):

        for row in self.tree.get_children():

            self.tree.delete(row)

        tasks = get_tasks()

        completed = 0

        for task in tasks:

            if task[4] == "Completed":

                self.tree.insert(
                    "",
                    "end",
                    values=task,
                    tags=("completed",)
                )

                completed += 1

            else:

                self.tree.insert(
                    "",
                    "end",
                    values=task
                )

        total = len(tasks)

        pending = total - completed

        self.stats_label.config(
            text=f"Total: {total}    Completed: {completed}    Pending: {pending}"
        )


    def delete_selected(self):

        selected = self.tree.selection()

        if not selected:

            return

        item = self.tree.item(selected)

        task_id = item["values"][0]

        delete_task(task_id)

        messagebox.showinfo(
            "Deleted",
            "Task Deleted Successfully!"
        )

        self.load_tasks()


    def complete_selected(self):

        selected = self.tree.selection()

        if not selected:

            return

        item = self.tree.item(selected)

        task_id = item["values"][0]

        complete_task(task_id)

        messagebox.showinfo(
            "Completed",
            "Task Completed Successfully!"
        )

        self.load_tasks()


    def edit_selected(self):

        selected = self.tree.selection()

        if not selected:

            return

        item = self.tree.item(selected)

        values = item["values"]

        self.selected_id = values[0]

        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, values[1])

        self.priority_box.set(values[2])

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, values[3])


    def update_selected(self):

        if self.selected_id is None:

            return

        update_task(

            self.selected_id,

            self.task_entry.get(),

            self.priority_box.get(),

            self.date_entry.get()

        )

        messagebox.showinfo(
            "Updated",
            "Task Updated Successfully!"
        )

        self.selected_id = None

        self.load_tasks()


    def search_task(self):

        keyword = self.search_entry.get()

        results = search_tasks(keyword)

        for row in self.tree.get_children():

            self.tree.delete(row)

        for task in results:

            self.tree.insert(
                "",
                "end",
                values=task
            )


    def toggle_theme(self):

        if self.current_theme == "flatly":

            self.style.theme_use("darkly")

            self.current_theme = "darkly"

        else:

            self.style.theme_use("flatly")

            self.current_theme = "flatly"