"""
This code comprises of banking system of new opened bank. It consists of facilities for customers such as opening 0 balance account, 
removing opened account, depositing or withdrawing money from account.
An admin can access the details from database present and view current customers and can also access the email ids of customers 
who removed their account from bank.

Database is in the format:

AccountNumber : Username, Name, Security Pin, Account Balance
"""
class BankingSystem:
	# initial data for convenience
	usernames = ['dmorgan', 'james', 'lThom', 'aubWit', 'HChen']
	customersNames = ['David Morgan', 'James Whitson', 'Lina Thomson', 'Aubrey Wit', 'Harley Chen']
	accountpins = ['2802', '0321', '9865', '7654', '4532'] # must be unique (no two accounts can have same pin)
	accountBalances = [10000, 54320, 12500, 4300, 3210]
	removedAccounts = []

	def __init__(self, accountsData, removedAccounts):
		self.accountsData = accountsData
		self.removedAccounts = removedAccounts

	# helper function to check whether entered username and pin is valid.
	def isValidUsernameAndPin(self, uname, pin):
		if uname in self.usernames:
			i = self.usernames.index(uname)
			if self.accountpins[i] == pin:
				return True
			else:
				print("Incorrect Pin!!")
				return False
		else:
			print("Username does not exist!")
			return False

	"""
	Details which can be accessed by customers.
	"""
	# Open a new account in bank
	def openAccount(self):
		uname = input("\nEnter username you want for account: ")
		if uname in self.usernames:
			print("Sorry! Account with this username already exists\n")
			return
		else:
			securityPin = input("Enter 4 digits security pin: ")
			try:
				pin_number = int(securityPin)
			except:
				print("Try again! Pin can only contains digits 0 to 9...")
				return

			firstName = input("Enter first name: ")
			lastName = input("Enter last name: ")
			name = firstName + " " + lastName
			depositAmount = eval(input("Enter deposit amount: "))
			if (depositAmount > 0):
				self.usernames.append(uname)
				self.customersNames.append(name)
				self.accountpins.append(securityPin)
				self.accountBalances.append(depositAmount)
				i = len(self.accountsData)
				while('A' + str(i) in self.accountsData):
					i = i+1
				self.accountsData['A' + str(i)] = [uname, name, securityPin, depositAmount]
				print("Congratulations!! Your account is now opened..\n")
			else:
				print("Deposit amount should be greater than 0\n")
				return

	# Account needs to be removed from bank
	def removeAccount(self):
		uname = input("Enter your username: ")
		securityPin = input("Enter account pin: ")

		# to check if security pin is valid 4 digit number
		try:
			pin_number = int(securityPin)
		except:
			print("Try again! Pin can only contains digits 0 to 9...")
			return
		if self.isValidUsernameAndPin(uname, securityPin) == True:
			accountNum = input("Enter account number: ")
			if accountNum in self.accountsData:
				if all(x in self.accountsData[accountNum] for x in [uname, securityPin]):
					email = input("Enter your email id: \n")
					i = self.usernames.index(uname)
					self.removedAccounts.append((self.usernames[i], email, self.customersNames[i]))
					self.usernames.pop(i)
					self.customersNames.pop(i)
					self.accountpins.pop(i)
					self.accountBalances.pop(i)
					del self.accountsData[accountNum]
				else:
					print("Account number, username and pin don't match. Please try again!!\n")
					return
			else:
				print("Incorrect account number.., try again!!\n")
				return
		else:
			print("Enter valid username and account pin\n")
			return

	# Amount that customer wants to withdraw from his/her account.
	def withdrawMoney(self, amount):
		uname = input("Enter your username: ")
		# check if username and corresponding account number exists and matches each other
		if uname in self.usernames:
			anum = input("Enter account number: ")
			if anum in self.accountsData:
				if uname in self.accountsData[anum]:
					i = self.usernames.index(uname)
					# withdraw if there is enough balance in account
					if (self.accountBalances[i] - amount) > 0:
						self.accountBalances[i] -= amount
						info = self.accountsData[anum]
						info[len(info)-1] -= amount
						print("Your current balance is updated to " + str(self.accountBalances[i]))
						print("\n")
					else:
						print("Insufficient balance, unable to withdraw\n")
						return
				else:
					print("Account Number doesn't match with username. Please try again.\n")
					return
			else:
				print("No such account exists. Please try again.\n")
				return
		else:
			print("Username doesn't exist")
			return

	# Amount that customer wants to deposit from his/her account.
	def depositMoney(self, amount):
		uname = input("Enter your username: ")
		# check if username and corresponding account number exists and matches each other
		if uname in self.usernames:
			anum = input("Enter account number: ")
			if anum in self.accountsData:
				if uname in self.accountsData[anum]:
					i = self.usernames.index(uname)
					self.accountBalances[i] += amount
					info = self.accountsData[anum]
					info[len(info)-1] += amount
					print("Your current balance is updated to " + str(self.accountBalances[i]))
					print("\n")
				else:
					print("Account Number doesn't match with username. Please try again.\n")
					return
			else:
				print("No such account exists. Please try again.\n")
				return
		else:
			print("Username doesn't exist\n")
			return
	"""
	Details which can be accessed by admin only.
	"""
	#details of customers who currently exists in bank in tabular form
	def currentCustomers(self):
		for k, v in self.accountsData.items():
			uname, name, pin, balance = v
			print ("{:<10} {:<10} {:<10} {:>10} {:>10}".format(k, uname, name, pin, balance))
		print("\n")

	#details of customers who removed their account from bank
	def deletedAccountsFromDB(self):
		if len(self.removedAccounts) == 0:
			print("No deleted accounts yet..\n")
		else:
			# printed deleted account using list comprehension
			deletedAccount = [x for x in self.removedAccounts]
			print(deletedAccount)
			print("\n")
	
	def choiceInput(self, userType, choice):
		if (userType == "Customer"):
			if choice == "1":
				# open account
				self.openAccount()
			elif choice == "2":
				# remove account
				self.removeAccount()
			elif choice == "3":
				# withdraw money
				amount = eval(input("Enter amount to withdraw: "))
				if amount > 0:
					self.withdrawMoney(amount)
				else:
					print("Invalid amount")
					return
			elif choice == "4":
				# deposit money
				amount = eval(input("Enter amount to deposit: "))
				if amount > 0:
					self.depositMoney(amount)
				else:
					print("Invalid amount")
					return
		else:
			if choice == "1":
				# bank customers database
				self.currentCustomers()
			elif choice == "2":
				# customer details of removed bank account
				self.deletedAccountsFromDB()

	#input from user
	def enterInput(self):
		while True:
			print("********** WELCOME TO Syracuse Bank **********")
			print("\n")
			userType = input("Enter your type (Customer/Admin): ")

			try:
				if userType == "Customer":
					print("*** SELECT YOUR CHOICE ***")
					print("--> 1. Open a new account")
					print("--> 2. Remove an account")
					print("--> 3. Withdraw Money")
					print("--> 4. Deposit Money")
					print("--> E. Exit/Quit")
					print("\n")
					
					choice = input("Enter choice from above:")

					if choice == "1" or choice == "2" or choice == "3" or choice == "4":
						self.choiceInput(userType, choice)
					elif choice == "E":
						print("Exit")
						break
					else:
						print("Invalid input. Try running program again!")
						break
					
				elif userType == "Admin":
					print("*** SELECT YOUR CHOICE ***")
					print("--> 1. View Current Database of Customers")
					print("--> 2. Customers who removed their account")
					print("--> E. Exit/Quit")
					print("\n")

					choice = input("Enter choice from above:")

					if choice == "1" or choice == "2":
						self.choiceInput(userType, choice)
					elif choice == "E":
						print("Exit")
						break
					else:
						print("Invalid input. Try running program again!")
						break
				else:
					raise BaseException('Invalid Input. Please Enter \"Customer\" or \"Admin\"')

			
			except BaseException as err:
				print(err)
				break


if __name__ == "__main__":
	accountsD = {}
	removedAccounts = []

	#created initial database dictionary using dictionary comprehension
	accountsD = {'A'+str(i):[BankingSystem.usernames[i], BankingSystem.customersNames[i], BankingSystem.accountpins[i], BankingSystem.accountBalances[i]] for i in range(len(BankingSystem.customersNames))}
	
	bankingSystemObject = BankingSystem(accountsD, removedAccounts)
	bankingSystemObject.enterInput()