import main as mm
from datetime import date


def rewrite_final(input_file, output_file):
    """Input file to be rewritten to second input file"""
    infile = open(input_file, 'r')
    outfile = open(output_file, 'w')
    for line in infile:
        outfile.write(line)
    infile.close()
    outfile.close()

def format_dollars(amount):
    """Input float, Returns formatted dollars($x,xxx.xx)"""
    balance = '{:.2f}'.format(amount)
    balance = balance.split('.')
    bit = balance[0][::-1]
    new_thing = ''
    for i in range(1, len(bit) + 1):
        if (i-1) % 3 == 0 and i != 1:
            new_thing += ','
        new_thing += bit[i - 1]
    balance = '$' + new_thing[::-1] + '.' + balance[1]
    return balance

def get_amount_for_list_of_lines(list_of_lines):
    total = 0.0
    for item in list_of_lines:
        total += float(item.split(',')[1][1:])
    return total

def remove_line(line_rm, recospent):
    """Input line to be removed and 'rec' or 'spent', removes line. line must include '\\n', gets date from line"""
    line_split = line_rm.split(',')
    if 'rec' in recospent.lower():
        allpath = mm.get_user() + '/rec_all.csv'
        alltmppath = mm.get_user() + '/tmp/rec_all.csv'
        yearpath = mm.get_user() + '/20' + line_split[0][-2:] + 'rec.csv'
        yeartmppath = mm.get_user() + '/tmp/20' + line_split[0][-2:] + 'rec.csv'
    elif 'spent' in recospent.lower():
        allpath = mm.get_user() + '/all.csv'
        alltmppath = mm.get_user() + '/tmp/all.csv'
        yearpath = mm.get_user() + '/20' + line_split[0][-2:] + '.csv'
        yeartmppath = mm.get_user() + '/tmp/20' + line_split[0][-2:] + '.csv'
    else:
        print('recospent not provided')
        return
    allfilein = open(allpath, 'r')
    allfileout = open(alltmppath, 'w')
    yearfilein = open(yearpath, 'r')
    yearfileout = open(yeartmppath, 'w')

    for line in allfilein:
        if line != line_rm:
            allfileout.write(line)
    for line in yearfilein:
        if line != line_rm:
            yearfileout.write(line)
    
    allfilein.close()
    allfileout.close()
    yearfilein.close()
    yearfileout.close()

    rewrite_final(alltmppath, allpath)
    rewrite_final(yeartmppath, yearpath)

def display_line(line):
    """Input line, formats into columns and returns"""
    line = line.split(',')
    string = ''
    for i in range(len(line)):
        if i == len(line) -1:
            string += '|{}'.format(line[i])
        elif line[2][0] == '$' or line[2] == 'Amount':
            if i != 3:
                string += '|{:15}'.format(line[i])
            else:
                string += '|{:33}'.format(line[i])
        elif line[1][0] == '$' or line[1] == 'Amount':
            if i != 2:
                string += '|{:15}'.format(line[i])
            else:
                string += '|{:33}'.format(line[i])
        else:
            if i != 4:
                string += '|{:15}'.format(line[i])
            else:
                string += '|{:33}'.format(line[i])
    return string

def display_many_lines(list_of_lines):
    counter = 0
    string = ''
    if len(list_of_lines) <= 0:
        return 'There are no lines!!!'
    for item in list_of_lines:
        if counter != 0 and counter % 5 == 0:
            string += '\n'
        string += '|{:<6}'.format(counter + 1) + display_line(item)[:-1] + '\n'
        counter += 1
    return string

def get_last_spent():
    """Returns last spent line in ledger, not last entered"""
    infile = open(mm.get_user() + '/all.csv', 'r')
    for line in infile:
        new_line = line
    infile.close()
    return new_line

def get_last_received():
    """Returns last received line in ledger, not last entered"""
    infile = open(mm.get_user() + '/rec_all.csv', 'r')
    for line in infile:
        new_line = line
    infile.close()
    return new_line

def get_last_entry():
    """Returns last entry line"""
    infile = open(mm.get_user() + '/last_entry.csv', 'r')
    for line in infile:
        new_line = line
    infile.close()
    return new_line

def record_last_entry(new_line):
    """Input new_line, updates last entry(spent or rec)"""
    infile_path = mm.get_user() + '/last_entry.csv'
    infile = open(infile_path, 'r')
    outfile_path = mm.get_user() + '/tmp/last_entry.csv'
    outfile = open(outfile_path, 'w')
    today = date.today()
    today = today.strftime("%m-%d-%Y")

    for line in infile:
        outfile.write(line)
    outfile.write(today + ',' + new_line)
    infile.close()
    outfile.close()
    rewrite_final(outfile_path, infile_path)

def get_last_balance():
    """returns a float of last balance"""
    infile = open(mm.get_user() + '/balance.csv', 'r')
    for line in infile:
        balance = line.split(',')[1]
    infile.close()
    return float(balance)

def man_balance_ledger_update(new_amount):
    """Updates balance ledger when changed in settings/user menu"""
    today = date.today()
    today = today.strftime("%m-%d-%Y")
    difference = -(get_last_balance()-new_amount)
    new_line = '{},{:.2f},{:.2f},ManUpdate,ManUpdate\n'.format(today, new_amount, difference)
    balance_new_line(new_line)
    

def balance_new_line(new_line):
    """Input new balance line, inserts new balance line"""
    infile = open(mm.get_user() + '/balance.csv', 'r')
    outfile = open(mm.get_user() + '/tmp/balance.csv', 'w')
    for line in infile:
        outfile.write(line)
    outfile.write(new_line)
    infile.close()
    outfile.close()
    rewrite_final(mm.get_user() + '/tmp/balance.csv', mm.get_user() + '/balance.csv')

def update_bal_rid_spent():
    """Adds new line in balance, updates curr balance based on last spent"""
    allpath = mm.get_user() + '/all.csv'
    alllastpath = mm.get_user() + '/tmp/last/all.csv'
    allfile = open(allpath, 'r')
    alllastfile = open(alllastpath, 'r')
    fin_line = ''
    for line in allfile:
        last_line = alllastfile.readline()
        if last_line != line:
            fin_line = line.split(',')
            break
    allfile.close()
    alllastfile.close()
    new_amount = get_last_balance() - float(fin_line[1][1:])
    today = date.today()
    today = today.strftime("%m-%d-%Y")
    difference = float(fin_line[1][1:])
    new_line = '{},{:.2f},{:.2f},last rec removed, last rec removed\n'.format(today, new_amount, difference)
    mm.change_balance(new_amount)
    balance_new_line(new_line)

def update_bal_rid_received():
    """Adds new line in balance, updates curr balance based on last received"""
    allpath = mm.get_user() + '/rec_all.csv'
    alllastpath = mm.get_user() + '/tmp/last/rec_all.csv'
    allfile = open(allpath, 'r')
    alllastfile = open(alllastpath, 'r')
    fin_line = ''
    for line in allfile:
        last_line = alllastfile.readline()
        if last_line != line:
            fin_line = line.split(',')
            break
    allfile.close()
    alllastfile.close()
    new_amount = get_last_balance() - float(fin_line[1][1:])
    today = date.today()
    today = today.strftime("%m-%d-%Y")
    difference = -float(fin_line[1][1:])
    new_line = '{},{:.2f},{:.2f},last rec removed, last rec removed\n'.format(today, new_amount, difference)
    mm.change_balance(new_amount)
    balance_new_line(new_line)

def insert_line_spent_rec(new_line, inall, outall, inyear, outyear):
    """input new line, inall path, outall path, inyear path, outyear, updates all and year file with new line"""
    date = new_line.split(',')[0]
    this_year = int(date.split('-')[2])
    this_month = int(date.split('-')[0])
    this_day = int(date.split('-')[1])
    infile_all = open(inall, 'r')
    outfile_all = open(outall, 'w')
    infile_year = open(inyear, 'r')
    outfile_year = open(outyear, 'w')

    record_last_entry(new_line)

    for line in infile_all:
        new_date = line.split(',')[0]
        outfile_all.write(line)
    if new_date == 'Date':
        outfile_all.write(new_line)
        infile_all.close()
        outfile_all.close()
        rewrite_final(outall, inall)
    else:
        infile_all.close()
        outfile_all.close()
        infile_all = open(inall, 'r')
        outfile_all = open(outall, 'w')
        outfile_all.write(infile_all.readline())
        inserted = False

        counter = 1
        last_year = 50
        last_month = 50
        last_day = 50
        
        for line in infile_all:
            next_date = line.split(',')[0]
            next_year = int(next_date.split('-')[2])
            next_month = int(next_date.split('-')[0])
            next_day = int(next_date.split('-')[1])
            if this_year <= next_year and counter == 1:
                if this_month <= next_month and counter == 1:
                    if this_day < next_day and counter == 1:
                        if inserted == False:
                            outfile_all.write(new_line)
                            inserted = True
            if last_year < this_year and next_year > this_year:
                if inserted == False:
                    outfile_all.write(new_line)
                    inserted = True
            if last_year < this_year and next_year == this_year:
                if this_month < next_month:
                    if inserted == False:
                        outfile_all.write(new_line)
                        inserted = True
                if this_month == next_month:
                    if this_day < next_day:
                        if inserted == False:
                            outfile_all.write(new_line)
                            inserted = True
            if last_year == this_year and this_year == next_year:
                if last_month < this_month and this_month < next_month:
                    if inserted == False:
                        outfile_all.write(new_line)
                        inserted = True
                if last_month < this_month and this_month == next_month:
                    if this_day < next_day:
                        if inserted == False:
                            outfile_all.write(new_line)
                            inserted = True
                if last_month == this_month and this_month == next_month:
                    if last_day < this_day and this_day < next_day:
                        if inserted == False:
                            outfile_all.write(new_line)
                            inserted = True
                    if last_day == this_day and this_day < next_day:
                        if inserted == False:
                            outfile_all.write(new_line)
                            inserted = True
                if last_month == this_month and this_month < next_month:
                    if inserted == False:
                        outfile_all.write(new_line)
                        inserted = True
            if last_year == this_year and this_year < next_year:
                if inserted == False:
                    outfile_all.write(new_line)
                    inserted = True

            counter += 1    
            outfile_all.write(line)

            last_date = line.split(',')[0]
            last_year = int(last_date.split('-')[2])
            last_day = int(last_date.split('-')[1])
            last_month = int(last_date.split('-')[0])

        if inserted == False:
            outfile_all.write(new_line)

        infile_all.close()
        outfile_all.close()
        rewrite_final(outall, inall)


        #-----------------------------------------------------------------------------

        for line in infile_year:
            new_date = line.split(',')[0]
            outfile_year.write(line)
        if new_date == 'Date':
            outfile_year.write(new_line)
            infile_year.close()
            outfile_year.close()
            rewrite_final(outyear, inyear)
        else:
            infile_year.close()
            outfile_year.close()
            infile_year = open(inyear, 'r')
            outfile_year = open(outyear, 'w')
            outfile_year.write(infile_year.readline())

            inserted = False

            last_year = 50
            last_month = 50
            last_day = 50

            counter = 1
            
            for line in infile_year:
                next_date = line.split(',')[0]
                next_month = int(next_date.split('-')[0])
                next_day = int(next_date.split('-')[1])
                
                if this_month <= next_month and counter == 1:
                    if this_day < next_day and counter == 1:
                        if inserted == False:
                            outfile_year.write(new_line)
                            inserted = True
                if last_month < this_month and this_month < next_month:
                    if inserted == False:
                        outfile_year.write(new_line)
                        inserted = True
                if last_month < this_month and this_month == next_month:
                    if this_day < next_day:
                        if inserted == False:
                            outfile_year.write(new_line)
                            inserted = True
                if last_month == this_month and this_month == next_month:
                    if last_day < this_day and this_day < next_day:
                        if inserted == False:
                            outfile_year.write(new_line)
                            inserted = True
                    if last_day == this_day and this_day < next_day:
                        if inserted == False:
                            outfile_year.write(new_line)
                            inserted = True
                if last_month == this_month and this_month < next_month:
                    if inserted == False:
                        outfile_year.write(new_line)
                        inserted = True
                    
                counter += 1    
                outfile_year.write(line)

                last_date = line.split(',')[0]
                last_day = int(last_date.split('-')[1])
                last_month = int(last_date.split('-')[0])

            if inserted == False:
                outfile_year.write(new_line)

            infile_year.close()
            outfile_year.close()
            rewrite_final(outyear, inyear)


    

def spent_money():
    print('\n\n\n\n\n\n\nNew Spent Entry')
    datee = input("Please enter a date (ex. 1-2, 10-21): ")
    amount = input("Please enter the $ amount (must be a float): $")
    description = input("Please enter a description (No Commas): ")
    category = input("Please enter a category (NA if none): ")
    methodofp = input("Please enter a method of purchase (NA if not available): ")

    check_string = "\n\n\nIs this Correct?\n----------------\n"
    check_string += 'Date = "' + datee + '"\n'
    check_string += 'Amount = "$' + amount + '"\n'
    check_string += 'Description = "' + description + '"\n'
    check_string += 'Category = "' + category + '"\n'
    check_string += 'Method of Purchase = "' + methodofp + '"\n'
    print(check_string)

    confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
    if confirmation == 'Y':
        rewrite_final(mm.get_user() + '/all.csv', mm.get_user() + '/tmp/last/all.csv')
        rewrite_final(mm.get_user() + '/' + mm.get_year() + '.csv', mm.get_user() + '/tmp/last/' + mm.get_year() + '.csv')
        line = datee + '-' + mm.get_year()[2:] + ',$' + '{:.2f}'.format(float(amount)) + ',' + description + ',' + category + ',' + methodofp + '\n'
        insert_line_spent_rec(line, mm.get_user() + '/all.csv', mm.get_user() + '/tmp/all.csv', mm.get_user() + '/' + mm.get_year() + '.csv', mm.get_user() + '/tmp/' + mm.get_year() + '.csv')
        
        today = date.today()
        today = today.strftime("%m-%d-%Y")
        new_amount = get_last_balance() - float(amount)
        new_date = datee + '-' + mm.get_year()[2:]
        new_line = '{},{:.2f},-{:.2f},{} for {},spent\n'.format(today, new_amount, float(amount),description,new_date)
        balance_new_line(new_line)

        mm.change_balance(mm.get_curr_balance() - float(amount))

        print("Entry Added!!")
    else:
        option = input('R)eenter or C)ancel:').upper()
        if option == 'R':
            spent_money()
        elif option == 'C':
            print('Back to Menu\n\n\n\n')
        else:
            print("Input not understood")


def received_money():
    print('\n\n\n\n\n\n\nNew Received Entry')
    datee = input("Please enter a date (ex. 1-2, 10-21): ")
    amount = input("Please enter the $ amount (must be a float): $")
    description = input("Please enter a description (No Commas): ")
    category = input("Please enter a category (NA if none): ")
    category = category.lower()

    check_string = "\n\n\nIs this Correct?\n----------------\n"
    check_string += 'Date = "' + datee + '"\n'
    check_string += 'Amount = "$' + amount + '"\n'
    check_string += 'Description = "' + description + '"\n'
    check_string += 'Category = "' + category + '"\n'
    print(check_string)

    confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
    if confirmation == 'Y':
        rewrite_final(mm.get_user() + '/rec_all.csv', mm.get_user() + '/tmp/last/rec_all.csv')
        rewrite_final(mm.get_user() + '/' + mm.get_year() + 'rec.csv', mm.get_user() + '/tmp/last/' + mm.get_year() + 'rec.csv')
        line = datee + '-' + mm.get_year()[2:] + ',$' + '{:.2f}'.format(float(amount)) + ',' + description + ',' + category + '\n'
        insert_line_spent_rec(line, mm.get_user() + '/rec_all.csv', mm.get_user() + '/tmp/rec_all.csv', mm.get_user() + '/' + mm.get_year() + 'rec.csv', mm.get_user() + '/tmp/' + mm.get_year() + 'rec.csv')
        
        today = date.today()
        today = today.strftime("%m-%d-%Y")
        new_amount = get_last_balance() + float(amount)
        new_date = datee + '-' + mm.get_year()[2:]
        new_line = '{},{:.2f},{:.2f},{} for {},received\n'.format(today, new_amount, float(amount),description,new_date)
        balance_new_line(new_line)

        mm.change_balance(mm.get_curr_balance() + float(amount))

        print("Entry Added!!")
    else:
        option = input('R)eenter or C)ancel:').upper()
        if option == 'R':
            received_money()
        elif option == 'C':
            print('Back to Menu\n\n\n\n')
        else:
            print("Input not understood")

def edit_last_spent():
    """Rewrites last spent last files to main files, option to reenter entry"""
    print('\n\n\n\n\n\n\n')
    answer = input("Remove, Reenter, or leave alone LAST SPENT entry? (remove, reenter, nevermind): ").lower()
    if answer == "remove":
        print(display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_line(get_last_spent()))
        update_bal_rid_spent()
        rewrite_final(mm.get_user() + '/tmp/last/all.csv', mm.get_user() + '/all.csv')
        rewrite_final(mm.get_user() + '/tmp/last/' + mm.get_year() + '.csv', mm.get_user() + '/' + mm.get_year() + '.csv')
        print("LAST SPENT entry removed\n")
        return
    elif answer == "reenter":
        print(display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_line(get_last_spent()))
        update_bal_rid_spent()
        rewrite_final(mm.get_user() + '/tmp/last/all.csv', mm.get_user() + '/all.csv')
        rewrite_final(mm.get_user() + '/tmp/last/' + mm.get_year() + '.csv', mm.get_user() + '/' + mm.get_year() + '.csv')
        print("LAST SPENT entry removed\n")
        spent_money()
        return
    elif answer == "nevermind":
        print("Nothing done, going back to edit menu")
        return
    else:
        print("Input not understood. Please try again.")
    edit_last_spent()

def edit_older_spent(first_time, listoas, old_listoas):
    """input first time (True or False), input list, searches spent, removes one line"""
    if first_time == True:
        string = '\n\n\n\n\n\n\nSearch for Spent'
        filepath = mm.get_user() + '/all.csv'
        file = open(filepath, 'r')
        print(string)
        file.readline()
        list_of_lines = find_entry(file, 's')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_many_lines(list_of_lines))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
        file.close()
        choice = input('R)efine or C)ancel (If only one line left, D)elete: ')
        if choice.lower() == 'r':
            edit_older_spent(False, list_of_lines, list_of_lines)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(list_of_lines))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(list_of_lines) == 1:
                    remove_line(list_of_lines[0], 'spent')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add spent entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
                    print(display_many_lines(list_of_lines))
                else:
                    print("Improper number of lines")
                    edit_older_spent('r', list_of_lines, list_of_lines)
            else:
                edit_older_spent('r', list_of_lines, list_of_lines)
        else:
            edit_older_spent('r', list_of_lines, list_of_lines)
    if first_time == 'r':
        choice = input('R)efine or C)ancel (If only one line left, D)elete: ')
        if choice.lower() == 'r':
            edit_older_spent(False, listoas, old_listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(listoas) == 1:
                    remove_line(listoas[0], 'spent')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add spent entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
                    print(display_many_lines(listoas))
                else:
                    print("Improper number of lines")
                    edit_older_spent('r', listoas, old_listoas)
            else:
                edit_older_spent('r', listoas, old_listoas)
        else:
            edit_older_spent('r', listoas, old_listoas)
    if first_time == False:
        string = '\n\n\n\n\n\n\nRefine Search for Spent Remover'
        print(string)
        list_of_lines_new = find_entry(listoas, 's')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_many_lines(list_of_lines_new))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
        choice = input('R)efine, U)ndo, C)ancel, or (if only one left) D)elete: ')
        if choice.lower() == 'r':
            edit_older_spent(False, list_of_lines_new, listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            edit_older_spent(False, listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(list_of_lines_new))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(list_of_lines_new) == 1:
                    remove_line(list_of_lines_new[0], 'spent')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add spent entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
                    print(display_many_lines(list_of_lines_new))
                else:
                    print("Improper number of lines")
                    edit_older_spent('re', list_of_lines_new, listoas)
            else:
                edit_older_spent('re', list_of_lines_new, listoas)
        else:
            edit_older_spent('re', list_of_lines_new, listoas)
    if first_time == 're':
        choice = input('R)efine, U)ndo, C)ancel, or (if only one left) D)elete: ')
        if choice.lower() == 'r':
            edit_older_spent(False, listoas, old_listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(old_listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(old_listoas)) + '\n')
            edit_older_spent(False, old_listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(listoas) == 1:
                    remove_line(listoas[0], 'spent')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add spent entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
                    print(display_many_lines(listoas))
                else:
                    print("Improper number of lines")
                    edit_older_spent('re', listoas, old_listoas)
            else:
                edit_older_spent('re', listoas, old_listoas)
        else:
            edit_older_spent('re', listoas, old_listoas)

def edit_last_rec():
    """Rewrites last rec last files to main files, option to reenter entry"""
    print('\n\n\n\n\n\n\n')
    answer = input("Remove, Reenter, or leave alone LAST RECEIVED entry? (remove, reenter, nevermind): ").lower()
    if answer == "remove":
        print(display_line('Date,Amount,Description,Category'))
        print(display_line(get_last_received()))
        update_bal_rid_received()
        rewrite_final(mm.get_user() + '/tmp/last/rec_all.csv', mm.get_user() + '/rec_all.csv')
        rewrite_final(mm.get_user() + '/tmp/last/' + mm.get_year() + 'rec.csv', mm.get_user() + '/' + mm.get_year() + 'rec.csv')
        print("LAST RECEIVED entry removed\n")
        return
    elif answer == "reenter":
        print(display_line('Date,Amount,Description,Category'))
        print(display_line(get_last_received()))
        update_bal_rid_received()
        rewrite_final(mm.get_user() + '/tmp/last/rec_all.csv', mm.get_user() + '/rec_all.csv')
        rewrite_final(mm.get_user() + '/tmp/last/' + mm.get_year() + 'rec.csv', mm.get_user() + '/' + mm.get_year() + 'rec.csv')
        print("LAST RECEIVED entry removed\n")
        received_money()
        return
    elif answer == "nevermind":
        print("Nothing done, going back to edit menu")
        return
    else:
        print("Input not understood. Please try again.")
    edit_last_rec()

def edit_older_rec(first_time, listoas, old_listoas):
    """input first time (True or False), input list, searches rec, removes one line"""
    if first_time == True:
        string = '\n\n\n\n\n\n\nSearch for Received'
        filepath = mm.get_user() + '/rec_all.csv'
        file = open(filepath, 'r')
        print(string)
        file.readline()
        list_of_lines = find_entry(file, 'r')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
        print(display_many_lines(list_of_lines))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
        file.close()
        choice = input('R)efine or C)ancel (If only one line left, D)elete: ')
        if choice.lower() == 'r':
            edit_older_rec(False, list_of_lines, list_of_lines)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(list_of_lines))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(list_of_lines) == 1:
                    remove_line(list_of_lines[0], 'rec')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add received entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
                    print(display_many_lines(list_of_lines))
                else:
                    print("Improper number of lines")
                    edit_older_rec('r', list_of_lines, list_of_lines)
            else:
                edit_older_rec('r', list_of_lines, list_of_lines)
        else:
            edit_older_rec('r', list_of_lines, list_of_lines)
    if first_time == 'r':
        choice = input('R)efine or C)ancel (If only one line left, D)elete: ')
        if choice.lower() == 'r':
            edit_older_rec(False, listoas, old_listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(listoas) == 1:
                    remove_line(listoas[0], 'rec')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add received entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
                    print(display_many_lines(listoas))
                else:
                    print("Improper number of lines")
                    edit_older_rec('r', listoas, old_listoas)
            else:
                edit_older_rec('r', listoas, old_listoas)
        else:
            edit_older_rec('r', listoas, old_listoas)
    if first_time == False:
        string = '\n\n\n\n\n\n\nRefine Search for Received Remover'
        print(string)
        list_of_lines_new = find_entry(listoas, 'r')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
        print(display_many_lines(list_of_lines_new))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
        choice = input('R)efine, U)ndo, C)ancel, or (if only one left) D)elete: ')
        if choice.lower() == 'r':
            edit_older_rec(False, list_of_lines_new, listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            edit_older_rec(False, listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(list_of_lines_new))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(list_of_lines_new) == 1:
                    remove_line(list_of_lines_new[0], 'rec')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add received entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
                    print(display_many_lines(list_of_lines_new))
                else:
                    print("Improper number of lines")
                    edit_older_rec('re', list_of_lines_new, listoas)
            else:
                edit_older_rec('re', list_of_lines_new, listoas)
        else:
            edit_older_rec('re', list_of_lines_new, listoas)
    if first_time == 're':
        choice = input('R)efine, U)ndo, C)ancel, or (if only one left) D)elete: ')
        if choice.lower() == 'r':
            edit_older_rec(False, listoas, old_listoas)
        elif choice.lower() == 'c':
            print('Thanks!!\n\n\n\n\n')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(old_listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(old_listoas)) + '\n')
            edit_older_rec(False, old_listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Is this Correct???\n------------------')
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
            if confirmation == 'Y':
                if len(listoas) == 1:
                    remove_line(listoas[0], 'rec')
                    print('\n\n\n\n\n\n\nLine Removed!!!\n')
                    print('To reenter line, go to add received entry (change to appropriate year):')
                    print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
                    print(display_many_lines(listoas))
                else:
                    print("Improper number of lines")
                    edit_older_rec('re', listoas, old_listoas)
            else:
                edit_older_rec('re', listoas, old_listoas)
        else:
            edit_older_rec('re', listoas, old_listoas)

def find_entry(filen, r_or_s):
    """input file or list, asks for descriptors, returns a list of lines"""
    
    datee = input("Please enter a date (ex. 1-2-20, 10-21-19) (enter x's to ignore (1-x-22) or xxx(x...)): ")
    amount_range_lower = input("Please enter the $ range LOWER (must be a float) (enter xxx(x...) to ignore): $")
    amount_range_higher = input("Please enter the $ range UPPER (must be a float) (enter xxx(x...) to ignore): $")
    description = input("Please enter a description (No Commas) (enter xxx(x...) to ignore): ")
    category = input("Please enter a category (enter xxx(x...) to ignore): ")
    methodofp = 'xxx'
    if r_or_s == 's':
        methodofp = input("Please enter a method of purchase (enter x's to ignore): ")
    
    check_string = "\n\n\nIs this Correct?\n----------------\n"
    check_string += 'Date = "' + datee + '"\n'
    check_string += 'Amount range lower = "$' + amount_range_lower + '"\n'
    check_string += 'Amount range higher = "$' + amount_range_higher + '"\n'
    check_string += 'Description = "' + description + '"\n'
    check_string += 'Category = "' + category + '"\n'
    check_string += '(method of purchase) = "' + methodofp + '"\n'
    print(check_string)

    confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
    if confirmation == 'Y':
        list_of_lines = []
        find_date = False
        if 'xxx' not in datee:
            find_date = True
            find_year = datee.split('-')[2]
            find_month = datee.split('-')[1]
            find_day = datee.split('-')[0]

        for line in filen:
            line_orig = line
            line = line.split(',')
            line_year = line[0].split('-')[2]
            line_month = line[0].split('-')[1]
            line_day = line[0].split('-')[0]

            if find_date == True:
                if 'x' not in find_year:
                    if line_year != find_year:
                        continue
                if 'x' not in find_month:
                    if line_month != find_month:
                        continue
                if 'x' not in find_day:
                    if line_day != find_day:
                        continue
            if 'xxx' not in amount_range_lower:
                if float(line[1][1:]) < float(amount_range_lower):
                    continue
            if 'xxx' not in amount_range_higher:
                if float(line[1][1:]) > float(amount_range_higher):
                    continue
            if 'xxx' not in description.lower():
                if description.lower() not in line[2].lower():
                    continue
            if 'xxx' not in category.lower():
                if category.lower() not in line[3].lower():
                    continue
            if 'xxx' not in methodofp.lower():
                if methodofp.lower() not in line[-1].lower():
                    continue

            list_of_lines += [line_orig]
        return list_of_lines
    else:
        return find_entry(filen, r_or_s)


def search_spent_all(first_time, listoas, old_listoas):
    """input first time (True or False), input list, searches spent"""
    if first_time == True:
        string = '\n\n\n\n\n\n\nSearch for Spent'
        filepath = mm.get_user() + '/all.csv'
        file = open(filepath, 'r')
        print(string)
        file.readline()
        list_of_lines = find_entry(file, 's')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_many_lines(list_of_lines))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
        file.close()
        choice = input('R)efine or S)top: ')
        if choice.lower() == 'r':
            search_spent_all(False, list_of_lines, list_of_lines)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        else:
            search_spent_all('r', list_of_lines, list_of_lines)
    if first_time == 'r':
        choice = input('R)efine or S)top: ')
        if choice.lower() == 'r':
            search_spent_all(False, listoas, old_listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        else:
            search_spent_all('r', listoas, old_listoas)
    if first_time == False:
        string = '\n\n\n\n\n\n\nRefine Search for Spent'
        print(string)
        list_of_lines_new = find_entry(listoas, 's')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
        print(display_many_lines(list_of_lines_new))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
        choice = input('R)efine, U)ndo, or S)top: ')
        if choice.lower() == 'r':
            search_spent_all(False, list_of_lines_new, listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            search_spent_all(False, listoas, old_listoas)
            
        else:
            search_spent_all('re', list_of_lines_new, listoas)
    if first_time == 're':
        choice = input('R)efine, U)ndo, or S)top: ')
        if choice.lower() == 'r':
            search_spent_all(False, listoas, old_listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category,Method of purchase'))
            print(display_many_lines(old_listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(old_listoas)) + '\n')
            search_spent_all(False, old_listoas, old_listoas)
        else:
            search_spent_all('re', listoas, old_listoas)

def search_received_all(first_time, listoas, old_listoas):
    """input first time (True or False), input list, input old list, searches spent"""
    if first_time == True:
        string = '\n\n\n\n\n\n\nSearch for Received'
        filepath = mm.get_user() + '/rec_all.csv'
        file = open(filepath, 'r')
        print(string)
        file.readline()
        list_of_lines = find_entry(file, 'r')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
        print(display_many_lines(list_of_lines))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines)) + '\n')
        file.close()
        choice = input('R)efine or S)top: ')
        if choice.lower() == 'r':
            search_received_all(False, list_of_lines, list_of_lines)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        else:
            search_received_all('r', list_of_lines, list_of_lines)
    if first_time == 'r':
        choice = input('R)efine or S)top: ')
        if choice.lower() == 'r':
            search_received_all(False, listoas, old_listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        else:
            search_received_all('r', listoas, old_listoas)
    if first_time == False:
        string = '\n\n\n\n\n\n\nRefine Search for Spent'
        print(string)
        list_of_lines_new = find_entry(listoas, 'r')
        print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
        print(display_many_lines(list_of_lines_new))
        print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
        choice = input('R)efine, U)ndo, or S)top: ')
        if choice.lower() == 'r':
            search_received_all(False, list_of_lines_new, listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(listoas)) + '\n')
            search_received_all(False, listoas, old_listoas)
            
        else:
            search_received_all('re', list_of_lines_new, listoas)
    if first_time == 're':
        choice = input('R)efine, U)ndo, or S)top: ')
        if choice.lower() == 'r':
            search_received_all(False, listoas, old_listoas)
        elif choice.lower() == 's':
            print('Thanks!!\n\n\n\n\n!')
            return
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + display_line('Date,Amount,Description,Category'))
            print(display_many_lines(old_listoas))
            print('Total for Selection is ' + format_dollars(get_amount_for_list_of_lines(old_listoas)) + '\n')
            search_received_all(False, old_listoas, old_listoas)
        else:
            search_received_all('re', listoas, old_listoas)
