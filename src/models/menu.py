from src.common.database import Database
from src.models.loanees import Loanee
from src.models.loans import Loan
from tabulate import tabulate

Database.initialize()

while True:
    # choose initial action to take
    action = input("\nWelcome to your LoanShark App. Choose an action:\n1)View loanees\n2)View loans\n"
                   "3)create loan\n4)Exit\n\n=>")

    # convert user input to lower case int without white spaces
    action = str(action).strip().lower()

    if action == "1":
        i = 0
        # create new list to be used to add serial number
        new_list = []

        # Get a dict of all loanees from database
        loanee_list = Loanee.view_loanees()

        # iterate through dict to form new list with serial number
        for element in loanee_list:
            i += 1
            element["S/N"] = i
            new_list.append([element["S/N"], element['name'], element['phone_number'], element["_id"]])

        # output new_list using tabulate library
        print(tabulate(new_list, headers=["S/N", "Name", "PhoneNumber", "id"], tablefmt="rst"))

        # ask user to select a particular loanee from list
        answer = input("Enter serial number to select a particular loanee or 0 to exit: ")
        answer = str(answer).strip().lower()

        # if answer is 0, exit to main menu
        if answer == '0':
            continue

        try:
            loanee_id = ""

            # iterate through new_list to get id from serial number
            for element in new_list:
                # element[0] = Serial number column
                if element[0] == int(answer):
                    # element[3] = loanee_id column
                    loanee_id = element[3]

            # get loanee from database using id, output is dict
            selected_loanee = Loanee.get_loanee(id=loanee_id)

            # create a new Loanee object using selected_loanee dict
            selected_loanee = Loanee(name=selected_loanee['name'], phone_number=selected_loanee['phone_number'],
                                     email_address=selected_loanee['email_address'], _id=selected_loanee['_id'])
        except:
            print("invalid input")
            continue

        while True:
            # get user action for selected loanee
            answer = input("Loanee: {}\nChoose an action:\n1)View loans\n2)Create loans\n"
                           "3)Delete loanee\n4)Exit\n\n =>".format(selected_loanee.name))
            answer = str(answer).strip().lower()

            ####################################################
            if answer == "1":
                # get all loans with loanee's id from database
                # create new loan_list for keeping loans
                loan_list = []
                for loan in Loan.view_loans():
                    if loan["loanee_id"] == loanee_id:
                        loan_list.append([loan["loanee_name"], loan["amount_collected"], loan["amount_due"],
                                          loan["date_collected"], loan["date_due"], loan["interest_rate"]])

                # if loan_list is not empty, output using tabulate
                if loan_list:
                    print(tabulate(loan_list, headers=["loanee_name", "amount_collected", "amount_due",
                                                       "date_collected", "date_due", "interest_rate(%)"],
                                   tablefmt="rst"))
                else:
                    print("No data available")

            elif answer == '2':
                # create new loan
                amount = int(input("Amount to be loaned: "))
                due_date = input("Due date(DD/MM/YYYY): ")
                interest_rate = input("interest rate(%): ")

                selected_loanee.create_loan(amount=amount, date_due=due_date, interest_rate=interest_rate)
                print("loan created\n\n")

            elif answer == '3':
                # delete loan using id
                try:
                    Loanee.delete_loanee(id=loanee_id)
                    print("{} was successfully deleted".format(selected_loanee.name))
                    break
                except:
                    print("loanee could not be deleted")

            elif answer == '4':
                # exit while loop of selected loanee, back to main menu
                print("Exiting")
                break
            else:
                # invalid input, repeat while loop
                print("invalid input")
                continue

    elif action == "2":
        # num to be used for serial number
        num = 1
        # loan_list to be displayed to user
        loan_list = []
        # loan_list2, which contains id to be used for selecting user
        loan_list2 = []
        # delete_query to get id, used for deleting
        delete_query = None

        for loan in Loan.view_loans():
            # create loan_list and loan_list2 from all loans in database
            loan["S/N"] = num
            loan_list.append([loan["S/N"], loan["loanee_name"], loan["amount_collected"], loan["amount_due"],
                              loan["date_collected"], loan["date_due"], loan["interest_rate"]])
            loan_list2.append([loan["S/N"], loan["loanee_name"], loan["amount_collected"], loan["amount_due"],
                               loan["date_collected"], loan["date_due"], loan["interest_rate"], loan["_id"]])
            num += 1

        # output loan_list
        print(tabulate(loan_list, headers=["S/N", "Loanee Name", "amount collected", "amount due", "date collected",
                                           "date due", "interest_rate"], tablefmt="rst"))

        # get user input for serial number to delete
        answer = input("Enter serial number of loan to delete or 0 to exit: ")
        answer = str(answer).strip().lower()

        if answer != '0':
            # use loan_list2 to get id of the serial number selected
            for loan in loan_list2:
                if loan[0] == int(answer):
                    print("you have selected: ")
                    loan_temp_list = [loan]
                    print(tabulate(loan_temp_list, headers=["S/N", "Loanee Name", "amount collected", "amount due",
                                                            "date collected", "date due", "interest rate", "id"],
                                   tablefmt="rst"))
                    # id is last item in loan_list2
                    delete_query = loan[-1]
                    ans = input("\nProceed with delete?(Y/N): ")
                    if str(ans).strip().lower() == 'y':
                        Loan.delete_loan(id=delete_query)
                        print("Successfully deleted")
                    else:
                        pass
        elif answer == '0':
            print("exiting")
        else:
            print("invalid input")

    elif action == "3":

        name = input("name of loanee: ")
        phone_number = input("phone number of loanee: ")
        email_address = input("email address of loanee: ")

        # create new loanee and save to database
        loanee = Loanee(name=name, phone_number=phone_number, email_address=email_address)
        loanee.save_to_mongo()

        amount = int(input("Amount to be loaned: "))
        due_date = input("Due date(DD/MM/YYYY): ")
        interest_rate = input("Interest rate(%): ")

        # create new loan and save to database
        loanee.create_loan(amount=amount, date_due=due_date, interest_rate=interest_rate)
        print("loan created")

    elif action == '4':
        # exit application
        print("Thank you for using this application\n\nGood bye!!")
        break

    else:
        # invalid input, output main menu
        print("Invalid input\nPlease select one of the options\n")
        continue
