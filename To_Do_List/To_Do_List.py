# To-Do List
from os import system, name

choice = 0

# Function to clear terminal screen. Call with clear().
def clear():
  if name == "nt":
    _ = system("cls")
  else: 
    _ = system("clear")

def menu(option):
  clear()
  print("\nMenu:")
  print("0) Display menu")
  print("1) Display to-do list entries")
  print("2) Add new item to list")
  print("3) Mark item as complete")
  print("4) Exit")

  option = int(input("\nSelect option:\n"))
  return option

menu(choice)

print(choice)
'''
list = ["Dishes","Homework","PB"]

while 0 <= choice <= 4:
  counter = 1
  #choice = int(input("\nSelect option:\n"))
  
  # If option 0 is selected, display menu
  if choice == 0:
      menu(choice)
     # continue

  # If option 1 is selected, display current to-do list entries    
  elif choice == 1: 
      print("\nCurrent to-do list:")
      for i in list:
          print(str(counter) + ") " + i)
          counter += 1
      menu(choice)
     # continue

  # If option 2 is selected, prompt user for new to-do list entry and add it to list      
  elif choice == 2:
      new = input("\nWhat would you like to add to your to-do list?\n")
      list.append(new)
      menu(choice)
     # continue
  
  # If option 3 is selected, show current to-do list entries to user and remove the selected one from the list    
  elif choice == 3:
      print("")
      for i in list:
          print(str(counter) + ") " + i)
          counter += 1
      old = int(input("\nWhich entry would you like to remove?\n"))
      if 1 <= old <= len(list):
          del(list[old - 1])
          continue
      else:
          print("\nInvalid option. Please try again.\n")
          continue
  
  # If option 4 is selected, exit
  elif choice == 4:
    break
  
  # If no valid options are selected, repeat  
  else:
      print("\nInvalid option. Please try again.\n")
      menu(choice)

'''
