import sys
import csv
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, 
                             QLineEdit, QFileDialog, QMessageBox, QInputDialog, QDateTimeEdit, QListView)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QDate, QDateTime, Qt
from PyQt5.QtWidgets import QListWidgetItem

class TaskList(dict):
    def __init__(self, task_list):
        self.task_list = task_list
        self.task_list.setStyleSheet("background-color: #330066; color: white;")

    def set_item_color(self, item):
        item.setForeground(QColor('gray'))

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.task_list = TaskList(QListWidget(self))
        self.initUI()

    def show_error(self, e):
        QMessageBox.critical(self, 'Errore', f'Si è verificato un errore: {e}')

    def initUI(self):
        self.setWindowTitle('To-Do List')

        # Layout
        layout = QVBoxLayout()

        # Input-Text per inserire task
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Inserisci una nuova task...')
        layout.addWidget(self.task_input)
        self.task_input.setStyleSheet("background-color: #330066; color: white;")

        # Seleziona data e ora per la scadenza
        self.datetime_input = QDateTimeEdit(self)
        self.datetime_input.setCalendarPopup(True)
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime_input)
        self.datetime_input.setStyleSheet("background-color: #330066; color: white;")

        # Bottone aggiungi task
        self.add_btn = QPushButton('Aggiungi Task', self)
        self.add_btn.clicked.connect(self.add_task)
        layout.addWidget(self.add_btn)

        # Bottone per salvare su CSV
        self.save_btn = QPushButton('Salva su CSV', self)
        self.save_btn.clicked.connect(self.save_to_csv)
        layout.addWidget(self.save_btn)

        # Bottone per caricare da CSV
        self.load_btn = QPushButton('Carica da CSV', self)
        self.load_btn.clicked.connect(self.load_from_csv)
        layout.addWidget(self.load_btn)

        # Bottone per segnare come completata
        self.complete_btn = QPushButton('Segna come completata', self)
        self.complete_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.complete_btn)

        # Bottone per rimuovere la task
        self.remove_btn = QPushButton('Rimuovi Task', self)
        self.remove_btn.clicked.connect(self.remove_task)
        layout.addWidget(self.remove_btn)

        # Stile
        self.setStyleSheet("background-color: #8c1aff;") 
        self.add_btn.setStyleSheet("background-color: #330066; color: white;") 
        self.save_btn.setStyleSheet("background-color: #330066; color: white;")
        self.load_btn.setStyleSheet("background-color: #330066; color: white;")
        self.complete_btn.setStyleSheet("background-color: #330066; color: white;")
        self.remove_btn.setStyleSheet("background-color: #330066; color: white;")

        # Task list display
        layout.addWidget(self.task_list.task_list)
        self.setLayout(layout)

    def add_task(self):
        task_name = self.task_input.text()
        task_deadline = self.datetime_input.dateTime()

        if task_name:
            item = QListWidgetItem(f"{task_name} - Scadenza: {task_deadline.toString()}")
            self.task_list.task_list.addItem(item)
            self.sort_tasks()
            self.task_input.clear()
        else:
            self.show_error("Inserisci un nome per la task.")

    def sort_tasks(self):
        tasks = []
        for index in range(self.task_list.task_list.count()):
            item = self.task_list.task_list.item(index)
            task_text = item.text()
            
            # Estrai la data di scadenza dal testo dell'item
            match = re.search(r'Scadenza: (.*)', task_text)
            if match:
                task_deadline_str = match.group(1)
                task_deadline = QDateTime.fromString(task_deadline_str)
                tasks.append((task_deadline, task_text))

        # Ordina le task in base alla scadenza
        tasks.sort(key=lambda x: x[0])

        # Cancella la lista attuale e aggiungi le task ordinate
        self.task_list.task_list.clear()
        for task_deadline, task_text in tasks:
            self.task_list.task_list.addItem(QListWidgetItem(task_text))

    def save_to_csv(self):
        # Salva le task in un file CSV
        file_path, _ = QFileDialog.getSaveFileName(self, "Salva CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Task", "Scadenza", "Completata"])
                    for index in range(self.task_list.task_list.count()):
                        item = self.task_list.task_list.item(index)
                        task_text = item.text()

                        # Estrai task e scadenza
                        task_parts = task_text.split(' - Scadenza: ')
                        task_name = task_parts[0]
                        task_deadline = f'"Scadenza: {task_parts[1]}"'
                        
                        # Stato completata
                        completed = "si" if item.foreground() == QColor('gray') else "no"
                        writer.writerow([task_name, task_deadline, completed])
            except Exception as e:
                self.show_error(e)

    def load_from_csv(self):
        # Carica le task da un file CSV
        file_path, _ = QFileDialog.getOpenFileName(self, "Apri CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Salta l'intestazione
                    self.task_list.task_list.clear()
                    for row in reader:
                        task_name = row[0]
                        task_deadline = row[1].strip('"')
                        completed = row[2]

                        item = QListWidgetItem(f"{task_name} - {task_deadline}")
                        if completed == "si":
                            self.task_list.set_item_color(item)
                        self.task_list.task_list.addItem(item)
            except Exception as e:
                self.show_error(e)

    def mark_completed(self):
        # Segna la task selezionata come completata
        selected_item = self.task_list.task_list.currentItem()
        if selected_item:
            selected_item.setText(f"{selected_item.text()} -X ")
            self.task_list.set_item_color(selected_item)

    def remove_task(self):
        # Rimuovi la task selezionata
        selected_item = self.task_list.task_list.currentItem()
        if selected_item:
            self.task_list.task_list.takeItem(self.task_list.task_list.row(selected_item))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo = ToDoApp()
    todo.show()
    sys.exit(app.exec_())
