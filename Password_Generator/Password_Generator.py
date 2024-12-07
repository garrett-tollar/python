# Password Generator
from os import system, name
import string
import secrets

def clear():
	if name == "nt":
		_ = system("cls")
	else: 
		_ = system("clear")

password = ""
letters = string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation
length = 8

def new_pass(password): # Add code snippet to ensure at least 2 of each character type for each option
	clear()
	print("Menu:")
	print("0) Display menu")
	print("1) Lowercase only")
	print("2) Uppercase only")
	print("3) Lowercase + Uppercase") 
	print("4) Lowercase + Uppercase + Numbers") 
	print("5) Lowercase + Uppercase + Numbers + Symbols")
	print("6) Exit\n")

	choice = int(input("Which character set would you like to use: "))
	length = int(input("Minimum password length (default = 8): "))
	
	if choice == 0:
		new_pass(password)
	elif choice == 1:
		for i in range(0,length):
			password += secrets.choice(string.ascii_lowercase)
		print(password)
		print("\n")
	elif choice == 2:
		for i in range(0,length):
			password += secrets.choice(string.ascii_uppercase)
		print(password)
		print("\n")
	elif choice == 3:
		for i in range(0,length):
			password += secrets.choice(string.ascii_lowercase + string.ascii_uppercase)
		print(password)
		print("\n")
	elif choice == 4:
		for i in range(0,length):
			password += secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
		print(password)
		print("\n")
	elif choice == 5:
		for i in range(0,length):
			password += secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
		print(password)
		print("\n")
	elif choice == 6:
		pass
	else:
		print("\nInvalid option. Please try again.\n")
		new_pass(password)

new_pass(password)
