import datetime
import csv
def main():
    tasks = []

    while True:
        print("\n===== To-Do List =====")
        ascii_art ='''
            by Josè Renan Vita
      __...--~~~~~-._   _.-~~~~~--...__
    //               `V'               \\ 
   //                 |                 \\ 
  //__...--~~~~~~-._  |  _.-~~~~~~--...__\\ 
 //__.....----~~~~._\ | /_.~~~~----.....__\\
====================\\|//====================
                    `---`
'''
        print (ascii_art)
                    
        print("1. Aggiungi Task")
        print("2. Mostra Tasks")
        print("3. Segna Task come completate")
        print("4. Esci")
        print("5. Salva lista in CSV")
        print("6. Carica da lista in CSV")



        choice = input("Inserisci comando: ")

        if choice == '1':
            print()
            n_tasks = int(input("Quante scegli quante task vuoi aggiungere: "))

            for i in range(n_tasks):
                task = input("Inserisci testo Task: ")
                deadline_str = input("Inserisci la data di scadenza (AAAA-MM-GG HH:MM): ")
                try:
                    deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                    tasks.append({"task": task, "done": False, "deadline": deadline})
                    print("Task aggiunta!")
                except ValueError:
                    print("Formato data errato. Utilizzare AAAA-MM-GG HH:MM")
        elif choice == '2':
            print("\nTasks:")
            for index, task in enumerate(tasks):
                status = "Completata" if task["done"] else "Da completare"
                deadline = task.get("deadline", "Nessuna scadenza")
                print(f"{index + 1}. {task['task']} - {status} - Scadenza: {deadline:%Y-%m-%d %H:%M}")

        elif choice == '3':
            task_index = int(input("Inserisci il numero di task da segnare completate: ")) - 1
            if 0 <= task_index < len(tasks):
                tasks[task_index]["done"] = True
                print("Task segnata come  completata!")
            else:
                print("Numero invalido di task.")

        elif choice == '4':
            print("Esci dalla To-Do List.")
            break

        elif choice == '5':
            # Salva la lista delle task in un file CSV
            with open('tasks.csv', 'w', newline='') as csvfile:
                fieldnames = ['Task', 'Completata', 'Scadenza']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for task in tasks:
                    writer.writerow({'Task': task['task'],
                                     'Completata': task['done'],
                                     'Scadenza': task['deadline']})
                print("Lista delle task salvata in tasks.csv")
                

        elif choice == '6':
            file_path = input("Inserisci il percorso completo del file CSV: ")
            delimiter = ','  # Imposta il separatore di default
            date_format = '%Y-%m-%d %H:%M:%S'  # Imposta il formato della data di default

            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=delimiter)
                    for row in reader:
                        tasks.append({'task': row['Task'],
                                      'done': row['Completata'] == 'True',
                                      'deadline': datetime.datetime.strptime(row['Scadenza'], date_format)})
                    print("Lista delle task caricata da", file_path)
            except FileNotFoundError:
                print("File non trovato. Assicurati di aver inserito il percorso corretto.")
            except ValueError:
                print("Formato del file CSV non valido. Controlla i separatori, la codifica e il formato delle date.")
            except csv.Error as e:
                print("Errore durante la lettura del file CSV:", e)

        else:
            print("Scelta non valida. Prova di nuovo.")

if __name__ == "__main__":
    main()
