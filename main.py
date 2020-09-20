import work_wth_data as wd
import display_data as dd
import os
from os import path
from datetime import date



#------------------------------------------------------------------------------------

def get_yes_or_no(message):
    """Input a message, returns 'Y' or 'N'"""
    valid_input = False
    while not valid_input:
        answer = input(message)
        answer = answer.upper() # convert to upper case
        if answer == 'Y' or answer == 'N':
            valid_input = True
        else:
            print('Please enter Y for yes or N for no.')
    return answer

def list_to_string_with_comma(thing):
    """Input a list, returns every item in the list as a string with commas in between"""
    string = ""
    for item in thing:
        string += str(item) + ','
    return string[:-1]

#-----------------------------------------------------------------------------------

def get_year():
    """returns the year as a string"""
    file = open('settings.txt', 'r')
    year = file.readline()
    year = year[-5:-1]
    file.close()
    return year

def get_user():
    """returns the username as a string"""
    file = open('settings.txt', 'r')
    file.readline()
    user = file.readline()
    user = user[14:-1]
    file.close()
    return user

def get_users():
    """returns a list composed of usernames"""
    file = open('settings.txt', 'r')
    file.readline()
    file.readline()
    users = file.readline()
    users = users.split(',')
    file.close()
    users = users[1:]
    users[-1] = users[-1][:-1]
    return users

def get_curr_balance():
    """returns the current balance as a float"""
    file = open('settings.txt', 'r')
    for i in range(3):
        file.readline()
        j = i
        j += 1
    balance = file.readline()
    balance = float(balance[17:-1])
    file.close()
    return balance


def get_balances():
    """returns the balances as a list of strings"""
    file = open('settings.txt', 'r')
    for i in range(4):
        file.readline()
        j = i
        j += 1
    balances = file.readline()
    balances = balances.split(',')
    file.close()
    balances = balances[1:]
    balances[-1] = balances[-1][:-1]
    return balances

def check_user_year():
    """returns boolean if current year exists for current user"""
    path = get_user() + '/' + get_year() + '.csv'
    return os.path.exists(path)

#------------------------------------------------------------------------------------

def change_year(new_year):
    """Input year(xxxx)(str or int), changes current year"""
    file = open('settings.txt', 'r')
    outfile = open('tmpset.txt', 'w')
    file.readline()
    outfile.write('Year: ' + str(new_year) + '\n')
    for line in file:
        outfile.write(line)
    file.close()
    outfile.close()
    wd.rewrite_final('tmpset.txt', 'settings.txt')
    print("Done!")
    if not check_user_year():
        set_new_year()
    
def man_change_balance(new_amount):
    """updates balance ledger"""
    wd.man_balance_ledger_update(new_amount)
    change_balance(new_amount)


def change_balance(new_amount):
    """input new balance amount(any dtype), updates current balance, user balance"""
    file = open('settings.txt', 'r')
    outfile = open('tmpset.txt', 'w')
    for i in range(3):
        line = file.readline()
        outfile.write(line)
        j = i
        j += 1
    file.readline()
    outfile.write('Current balance: ' + '{:.2f}'.format(new_amount) + '\n')
    file.readline()
    balances = get_balances()
    balances[get_users().index(get_user())] = '{:.2f}'.format(new_amount)
    outfile.write('All balance:,' + list_to_string_with_comma(balances) + '\n')
    for line in file:
        outfile.write(line)
    file.close()
    outfile.close()
    wd.rewrite_final('tmpset.txt', 'settings.txt')
    
def change_curr_balance_to_user():
    """Used by change_user, title explains it"""
    file = open('settings.txt', 'r')
    outfile = open('tmpset.txt', 'w')
    for i in range(3):
        line = file.readline()
        outfile.write(line)
        j = i
        j += 1
    balance = get_balances()
    balance = balance[get_users().index(get_user())]
    file.readline()
    outfile.write('Current balance: ' + '{:.2f}'.format(float(balance)) + '\n')
    for line in file:
        outfile.write(line)
    file.close()
    outfile.close()
    wd.rewrite_final('tmpset.txt', 'settings.txt')

def change_user(username):
    """Input username, changes user, does nothing if user doesn't exist"""
    if username in get_users():
        file = open('settings.txt', 'r')
        outfile = open('tmpset.txt', 'w')
        outfile.write(file.readline())
        file.readline()
        outfile.write('Current User: ' + username + '\n')
        for line in file:
            outfile.write(line)
        file.close()
        outfile.close()
        wd.rewrite_final('tmpset.txt', 'settings.txt')
        change_curr_balance_to_user()
    else:
        print("User not found")





#--------------------------------------------------------------------------------------------------

def set_new_year():
    """sets up new year if it doesn't exist for user"""
    path = get_user() + '/' + 'all.csv'
    allfile = open(path, 'r')
    spend_default = allfile.readline()
    newyear_path = get_user() + '/' + get_year() + '.csv'
    new_year_file = open(newyear_path, 'w')
    new_year_file.write(spend_default)
    allfile.close()
    new_year_file.close()

    path = get_user() + '/' + 'rec_all.csv'
    allfile = open(path, 'r')
    rec_default = allfile.readline()
    newyear_path = get_user() + '/' + get_year() + 'rec.csv'
    new_year_file = open(newyear_path, 'w')
    new_year_file.write(rec_default)
    allfile.close()
    new_year_file.close()
    print("Congratulations on making it to the new year!!!")

def add_new_user(username):
    """Input new username, sets up files and stuff"""
    if username in get_users():
        print("User already exists!")
        return
    file = open('settings.txt', 'r')
    outfile = open('tmpset.txt', 'w')
    outfile.write(file.readline())
    file.readline()
    outfile.write('Current User: ' + username + '\n')
    outfile.write(file.readline()[:-1] + ',' + username + '\n')
    file.readline()
    outfile.write('Current balance: 0.00\n')
    outfile.write(file.readline()[:-1] + ',0.00' + '\n')
    for line in file:
        outfile.write(line)
    file.close()
    outfile.close()
    wd.rewrite_final('tmpset.txt', 'settings.txt')

    os.mkdir(get_user())
    os.mkdir((get_user() + '/' + 'tmp'))
    os.mkdir((get_user() + '/' + 'tmp' + '/' + 'last'))

    new_all_path = get_user() + '/' + 'all.csv'
    spend_default = 'Date,Amount,Description,Category,Method of purchase\n'
    newyear_path = get_user() + '/' + get_year() + '.csv'
    new_year_file = open(newyear_path, 'w')
    new_year_file.write(spend_default)
    new_all_file = open(new_all_path, 'w')
    new_all_file.write(spend_default)
    new_all_file.close()
    new_year_file.close()

    new_balancesheet = open(get_user() + '/' + 'balance.csv', 'w')
    new_balancesheet.write('Date,Amount,Change Amount,Description,Category\n')
    today = date.today()
    today = today.strftime("%m-%d-%Y")
    new_balancesheet.write(today + ',0.00,0.00,Init,Init')
    new_balancesheet.close()

    new_recall = open(get_user() + '/' + 'rec_all.csv', 'w')
    new_recall.write('Date,Amount,Description,Category\n')
    new_balancesheet.close()

    new_rec_year = open(get_user() + '/' + get_year() + 'rec.csv', 'w')
    new_rec_year.write('Date,Amount,Description,Category\n')
    new_rec_year.close()

    new_last_entry = open(get_user() + '/last_entry.csv', 'w')
    new_last_entry.write('Date Recorded,Date,Amount,Description,Category,(method of purchase)\n')
    new_last_entry.close()

    print("Welcome!! User added")


def get_format_balance():
    """Returns formatted curr balance($x,xxx.xx)"""
    balance = '{:.2f}'.format(get_curr_balance())
    balance = balance.split('.')
    bit = balance[0][::-1]
    new_thing = ''
    for i in range(1, len(bit) + 1):
        if (i-1) % 3 == 0 and i != 1:
            new_thing += ','
        new_thing += bit[i - 1]
    balance = '$' + new_thing[::-1] + '.' + balance[1]
    return balance

#--------------------------------------------------------------------------------------------------

def add_entry_menu():
    """Add entry meny"""
    entry_menu = "Add Entry Menu:\nYear is: " + get_year() + '\n---------------\n'
    entry_menu += "1: Spent Money\n"
    entry_menu += "2: Received Money\n"
    entry_menu += "3: Change Year\n"
    entry_menu += "4: Show Last Entry\n"
    entry_menu += "5: Back to Main Menu\n"
    print(entry_menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        wd.spent_money()
    elif menu_select == '2':
        wd.received_money()
    elif menu_select == '3':
        change_year(input('Please enter a year(yyyy): '))
    elif menu_select == '4':
        print(wd.display_line("Date Recorded,Date,Amount,Description,Category,(method of purchase)"))
        print(wd.display_line(wd.get_last_entry()))
    elif menu_select == '5':
        main_menu()
        return
    else:
        print("Input not understood. Please try again.")
    add_entry_menu()


def editor_menu():
    """Edit entry menu"""
    edit_menu = "Edit Entry Menu:\n----------------\n"
    edit_menu += "1: Reenter last spent entry\n"
    edit_menu += "2: Remove older spent entry\n"
    edit_menu += "3: Reenter last received entry\n"
    edit_menu += "4: Remove older received entry\n\n"
    edit_menu += "5: Display last SPENT entry\n"
    edit_menu += "6: Display last RECEIVED entry\n"
    edit_menu += "7: Back to Main Menu\n"
    print(edit_menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        wd.edit_last_spent()
    elif menu_select == '2':
        wd.edit_older_spent(True,'','')
    elif menu_select == '3':
        wd.edit_last_rec()
    elif menu_select == '4':
        wd.edit_older_rec(True,'','')
    elif menu_select == '5':
        print(wd.display_line('Date,Amount,Description,Category,Method of purchase'))
        print(wd.display_line(wd.get_last_spent()))
    elif menu_select == '6':
        print(wd.display_line('Date,Amount,Description,Category'))
        print(wd.display_line(wd.get_last_received()))
    elif menu_select == '7':
        main_menu()
        return
    else:
        print("Input not understood. Please try again.")
    editor_menu()

def entry_search():
    search_menu = "Entry search menu:\n------------------\n"
    search_menu += "1: Search Spent\n"
    search_menu += "2: Search Received\n"
    search_menu += "3: Back to Main Menu\n"
    print(search_menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        wd.search_spent_all(True,'','')
    elif menu_select == '2':
        wd.search_received_all(True,'','')
    elif menu_select == '3':
        main_menu()
        return
    else:
        print("Input not understood. Please try again.")
    entry_search()

def stat_display_menu():
    display_menu = "Stat Display Menu:\n------------------\n"
    display_menu += "1: Total SPENT for Date Range\n"
    display_menu += "2: Total RECEIVED for Date Range\n\n"
    display_menu += "3: Line graph\n"
    display_menu += "4: Pie chart\n"
    display_menu += "5: Bar graph\n"
    display_menu += "6: Back to Main Menu\n"
    print(display_menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        dd.total_for_date_range('s', True,'','')
    elif menu_select == '2':
        dd.total_for_date_range('r', True,'','')
    elif menu_select == '3':
        dd.line_graph()
    elif menu_select == '4':
        dd.pie_chart()
    elif menu_select == '5':
        dd.bar_graph()
    elif menu_select == '6':
        main_menu()
        return
    else:
        print("Input not understood. Please try again.")
    stat_display_menu()



def settings_menu():
    set_menu = "Settings and User Menu:\n-----------------------\n"
    set_menu += "1: Change user\n"
    set_menu += "2: Manually set balance\n"
    set_menu += "3: Change year\n"
    set_menu += "4: View users and balances\n"
    set_menu += "5: Add new User\n"
    set_menu += "6: Back to Main Menu\n"
    print(set_menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        change_user(input("Please enter a username: "))
    elif menu_select == '2':
        man_change_balance(float(input('Please enter a new balance(xxxx.xx): ')))
    elif menu_select == '3':
        change_year(input('Please enter a year(yyyy): '))
    elif menu_select == '4':
        print('Users and Balances')
        [print(values) for values in zip(get_users(), get_balances())]
        print('')
    elif menu_select == '5':
        new_user = input('Please enter a new username: ')
        if get_yes_or_no('Is this correct? (y or n) "' + new_user + '"') == 'Y':
            add_new_user(new_user)
        else:
            print('You declined the username!')
    elif menu_select == '6':
        main_menu()
        return
    else:
        print("Input not understood. Please try again.")
    settings_menu()




def main_menu():
    string = "Current User is: "
    string += get_user() + "\n"
    string += "Year is: " + get_year() + '\n'
    string += "Current balance is: " + get_format_balance()
    print(string)
    menu = "\nAcct Menu \n---------\n"
    menu += "1: Add Entry\n"
    menu += "2: Open Editor\n"
    menu += "3: Entry Search\n"
    menu += "4: Display Stats\n"
    menu += "5: Settings/User\n"
    menu += "6: Exit Program\n"
    print(menu)
    menu_select = input("Please select an option: ")
    print('\n\n\n\n\n\n\n')

    if menu_select == '1':
        add_entry_menu()
        return
    elif menu_select == '2':
        editor_menu()
        return
    elif menu_select == '3':
        entry_search()
        return
    elif menu_select == '4':
        stat_display_menu()
        return
    elif menu_select == '5':
        settings_menu()
        return
    elif menu_select == '6':
        print("Have a good day!!!")
        return
    else:
        print("Input not understood. Please try again!")
    main_menu()
    
    
if __name__ == "__main__":
    main_menu()