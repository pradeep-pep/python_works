#ToDo List Application fetching user data via Input() & Not via sys.argv
#Run using Terminal command PS C:\Users\pepsara\Documents\PYTHON> python ToDoList2.py "ARGUMENTS"
#If file not found, it will create a new file
import sys
import os

#File Handling
def load_file():
    print(f"FILE REFERENCE:")
    TASK_FILE = "todotask2.txt"
    print(f"Looking for file at: {TASK_FILE}")
    print()
    if not os.path.exists(TASK_FILE):
        print("File does not exist : Creating a new file") 
        with open(TASK_FILE, "w") as f:
            pass   
        return []         
    with open(TASK_FILE, "r") as f:
        print("File does exist.")
        lines = f.readlines()
        print(lines)
        return [line.strip().split("-") for line in lines if line.strip()]

def save_file(tasks):
    TASK_FILE = "todotask2.txt"
    if not os.path.exists(TASK_FILE):
         print("File does not exist") 
         return []       
    with open(TASK_FILE, "w") as f:
        for task_name, task_desc, status in tasks:
            f.write(f"{task_name}-{task_desc}-{status}\n")

#Task Handling
def add_task(task_name, task_desc):
    tasks = load_file()
    tasks.append([task_name, task_desc, "pending"])
    save_file(tasks)
    print(f"Added: {task_name} - {task_desc} - pending")

def upd_task(task_num, status):
    tasks = load_file()
    tasks[task_num - 1][2] = status
    save_file(tasks)
    print(f"Updated: {tasks[task_num - 1][0]} - {tasks[task_num - 1][1]} - {status}")

def rem_task(remove_Item):
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty to attempt any remove item.")
        return
    removed = tasks.pop(remove_Item)
    save_file(tasks)
    print(f"Deleted: {removed[0]} - {removed[1]} - {removed[2]}")

#Main Menu
def ToDoMain():
    if len(sys.argv) < 2:
        ToDoWelcome()
        ToDoMainMenu()
        ToDoHelpMenu() 
        return
    ToDoAction()

def ToDoWelcome(): #1
    print()
    print("Welcome to the To-Do List Application!")
    print("You will be able to maintain a list of tasks where you can " \
          "\n'Add a new itenary, Update the status & Remove them from list'" \
          " as per need.")
    print()

def ToDoMainMenu(): #2
    print("Main Menu:")
    print("1. View Tasks")
    print("2. Add Task")        
    print("3. Update Task")
    print("4. Remove Task")
    print("5. Exit")
    print()
   
def ToDoHelpMenu(): #3
    print("Help Section:")
    print("You will have to enter the Action 'View, Add, Update, Remove' " \
          "followed by the Task Name & Task Description:'optional'")
    print()
    print("Samples: You can choose to enter any of the following methods:")
    print("*\t1 [OR] View")
    print("*\t2 [AND then] Add Study Python Programming")
    print("*\t2 [AND then] Add Finish Training Program")
    print("*\t3 [AND then] Update 2 Done [OR] Update 1 Cancelled [OR] Update 3 In Progress")
    print("*\t4 [AND then] Remove 2")
    print("*\t5 [OR] Exit")
    print()

def ToDoAction(): #4
    print("Action starts")
    ToDoAction = sys.argv[1]
    if ToDoAction == "1" or ToDoAction.lower() == "view":
        print("You have selected to view the tasks.")
        ToDoListTasks()
        print()
    elif ToDoAction.lower() == "add":
        print("You have selected to add a task [Format: Add Task_Name Task_Description] :")
        ToDoAddTasks()
        print()
        ToDoListTasks()
    elif ToDoAction.lower() == "update":
        print("You have selected to update a task [Format: Update Task_Number Task_Status] :")
        ToDoUpdTasks()
        print()
        ToDoListTasks() 
    elif ToDoAction == "4" or ToDoAction.lower() == "remove":
        print("You have selected to remove a task [Format: Remove Task_Number] :")
        ToDoRemoveTasks()
        print() 
        ToDoListTasks()     
    elif ToDoAction == "5"  or ToDoAction.lower() == "exit":
        ToDoExitMenu()
    else:
        print()
        print("Invalid input. Please try again.")
        ToDoMainMenu()

def ToDoListTasks(): #4a
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty.")
        return
    for i, (task_name, task_desc, status) in enumerate(tasks, 1):
        if status.lower() == "done":
           mark = "✔️"
           print(f"{i}. [{mark} ] {task_name} {task_desc}") 
        elif status.lower() == "in progress":
              mark = "⏳"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        elif status.lower() == "cancelled":
              mark = "❌"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        elif status.lower() == "pending":
              mark = "❌❌"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        else:
              print(f"{i}. Status of this item in To-Do list is any other than permitted.")

def ToDoAddTasks(): #4b
    tasks = load_file()
    if len(sys.argv) < 3 or sys.argv[1].lower() != "add":
        print("Wrong Input Format- [Please use: Add Task_Name Task_Description] : ")
        return   
    print(f"Task requested to add is: {sys.argv[2:]}")
    task_name, task_desc = sys.argv[2], " ".join(sys.argv[3:])
    add_task(task_name, task_desc)

def ToDoUpdTasks(): #4c
    tasks = load_file()
    if len(sys.argv) < 3 or sys.argv[1].lower() != "update" or sys.argv[2].isdigit() == False:
        print("Wrong Input Format- [Please use: Update Task_Number Task_Status] : ")       
        return  
    if int(sys.argv[2]) < 1 or int(sys.argv[2]) > len(tasks):
        print("Invalid task number.")
        return
    print(f"Task requested to update is: {sys.argv[2]}") 
    task_num, status = int(sys.argv[2]), " ".join(sys.argv[3:])
    upd_task(task_num, status)

def ToDoRemoveTasks(): #4d
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty to attempt any remove item.")
        return
    if len(sys.argv) != 3 or sys.argv[1].lower() != "remove" or sys.argv[2].isdigit() == False:
        print("Wrong Input Format- [Please use: Remove Task_Number] : ")
        return   
    if int(sys.argv[2]) < 1 or int(sys.argv[2]) > len(tasks):
        print(f"Invalid Task number to remove : {sys.argv[2]}")
        return
    print(f"Task requested to remove is: {sys.argv[2]}")
    remove_Item = int(sys.argv[2]) - 1
    rem_task(remove_Item)

def ToDoExitMenu(): #4c
    print()
    print("Thank you for using the To-Do List Application!")
    print("Goodbye!")   
    sys.exit()  

ToDoMain()
