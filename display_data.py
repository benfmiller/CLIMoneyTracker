import pandas as pd
import matplotlib.pyplot as plt
import main as mm
import work_wth_data as wd




def find_entry_date_range(filen):
    """input file or list, asks for descriptors, returns a list of lines"""
    
    date_lower = input("Please enter a date LOWER BOUND (ex. 1-2-20, 10-21-19)(xxx to ignore): ")
    date_higher = input("Please enter a date HIGHER BOUND (ex. 1-2-20, 10-21-19)(xxx to ignore): ")
    
    check_string = "\n\n\nIs this Correct?\n----------------\n"
    check_string += 'Date = "' + date_lower + '"\n'
    check_string += 'Date = "' + date_higher + '"\n'
    print(check_string)


    confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
    if confirmation == 'Y':
        list_of_lines = []

        if 'xxx' not in date_lower:
            year_lower = int(date_lower.split('-')[2])
            month_lower = int(date_lower.split('-')[0])
            day_lower = int(date_lower.split('-')[1])

        if 'xxx' not in date_higher:
            year_higher = int(date_higher.split('-')[2])
            month_higher = int(date_higher.split('-')[0])
            day_higher = int(date_higher.split('-')[1])

        for line in filen:
            line_orig = line
            line = line.split(',')
            line_year = int(line[0].split('-')[2])
            line_month = int(line[0].split('-')[0])
            line_day = int(line[0].split('-')[1])

            if 'xxx' not in date_lower:
                if line_year < year_lower:
                    continue
                if line_year == year_lower:
                    if line_month < month_lower:
                        continue
                    if line_month == month_lower:
                        if line_day < day_lower:
                            continue
            if 'xxx' not in date_higher:
                if line_year > year_higher:
                    continue
                if line_year == year_higher:
                    if line_month > month_higher:
                        continue
                    if line_month == month_higher:
                        if line_day > day_higher:
                            continue
            
            list_of_lines += [line_orig]
        return list_of_lines
    else:
        return find_entry_date_range(filen)

def total_for_date_range(s_or_r, first_time, listoas, old_listoas):
    """input 's' or 'r', first_time, list, and old list. Asks for date range, displays amount"""
    if s_or_r == 's':
        filepath = mm.get_user() + '/all.csv'
        string = '\n\n\n\n\n\n\nSearch for Spent Range'
        category_line = 'Date,Amount,Description,Category,Method of purchase'
    else:
        filepath = mm.get_user() + '/rec_all.csv'
        string = '\n\n\n\n\n\n\nSearch for Received Range'
        category_line = 'Date,Amount,Description,Category'
    if first_time == True:
    
        file = open(filepath, 'r')
        print(string)
        file.readline()
        list_of_lines = find_entry_date_range(file)
        print('\n|{:<6}'.format(0) + wd.display_line(category_line))
        print(wd.display_many_lines(list_of_lines))
        print('Total for Selection is ' + wd.format_dollars(wd.get_amount_for_list_of_lines(list_of_lines)) + '\n')
        file.close()
        choice = input('R)efine or D)one: ')
        if choice.lower() == 'r':
            return total_for_date_range(s_or_r, False, list_of_lines, list_of_lines)
        elif choice.lower() == 'd':
            print('Thanks!!\n\n\n\n\n')
            return list_of_lines
        else:
            return total_for_date_range(s_or_r, 'r', list_of_lines, list_of_lines)
    if first_time == 'r':
        choice = input('R)efine or D)one: ')
        if choice.lower() == 'r':
            return total_for_date_range(s_or_r, False, listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Thanks!!\n\n\n\n\n')
            return listoas
        else:
            return total_for_date_range(s_or_r, 'r', listoas, old_listoas)
    if first_time == False:
        if s_or_r == 's':
            string = '\n\n\n\n\n\n\nRefine Search for Spent Range'
        else:
            string = '\n\n\n\n\n\n\nRefine Search for Received Range'
        print(string)
        list_of_lines_new = find_entry_date_range(listoas)
        print('\n|{:<6}'.format(0) + wd.display_line(category_line))
        print(wd.display_many_lines(list_of_lines_new))
        print('Total for Selection is ' + wd.format_dollars(wd.get_amount_for_list_of_lines(list_of_lines_new)) + '\n')
        choice = input('R)efine, U)ndo, or D)one: ')
        if choice.lower() == 'r':
            return total_for_date_range(s_or_r, False, list_of_lines_new, listoas)
        elif choice.lower() == 'd':
            print('Thanks!!\n\n\n\n\n')
            return list_of_lines_new
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + wd.display_line(category_line))
            print(wd.display_many_lines(listoas))
            print('Total for Selection is ' + wd.format_dollars(wd.get_amount_for_list_of_lines(listoas)) + '\n')
            return total_for_date_range(s_or_r, False, listoas, old_listoas)
            
        else:
            return total_for_date_range(s_or_r, 're', list_of_lines_new, listoas)
    if first_time == 're':
        choice = input('R)efine, U)ndo, or D)one: ')
        if choice.lower() == 'r':
            return total_for_date_range(s_or_r, False, listoas, old_listoas)
        elif choice.lower() == 'd':
            print('Thanks!!\n\n\n\n\n')
            return listoas
        elif choice.lower() == 'u':
            print('\n|{:<6}'.format(0) + wd.display_line(category_line))
            print(wd.display_many_lines(old_listoas))
            print('Total for Selection is ' + wd.format_dollars(wd.get_amount_for_list_of_lines(old_listoas)) + '\n')
            return total_for_date_range(s_or_r, False, old_listoas, old_listoas)
        else:
            return total_for_date_range(s_or_r, 're', listoas, old_listoas)


#--------------------------------------------

def get_s_or_r():
    """Gets the user to enter 's' or 'p'"""
    answer = input("Please enter S)pent or R)eceived: ").lower()
    if answer == 's':
        return answer
    if answer == 'r':
        return answer
    else:
        print('Input not understood. Please try again.')
        return get_s_or_r()

def listify_list_of_lines(list_of_lines):
    """takes a list of entry lines and turns each entry in to a sublist"""
    final_list = []
    counter = 0
    for item in list_of_lines:
        final_line = []
        item = item[:-1]
        item = item.split(',')
        if counter != 0:
            item[1] = float(item[1][1:])
        for thing in item:
            final_line += [thing]
        final_list += [final_line]
        counter += 1
    return final_list

def get_entries_for_display():
    """Retrieves and reaffirms date range data"""
    s_or_r = get_s_or_r()

    if s_or_r == 's':
        category_line = 'Date,Amount,Description,Category,Method of purchase\n'
    else:
        category_line = 'Date,Amount,Description,Category\n'

    list_of_lines = total_for_date_range(s_or_r, True, [], [])

    check_string = "\n\n\nIs this Correct?\n----------------\n"
    check_string += '|{:<6}'.format(0) + wd.display_line(category_line)
    check_string += wd.display_many_lines(list_of_lines)
    print(check_string)
    print('Total for Selection is ' + wd.format_dollars(wd.get_amount_for_list_of_lines(list_of_lines)) + '\n')
    confirmation = mm.get_yes_or_no("Please enter Y)es or N)o: ")
    if confirmation == 'Y':
        list_of_lines = [category_line] + list_of_lines
        return listify_list_of_lines(list_of_lines)
    else:
        return get_entries_for_display()

def get_c_or_m():
    """Gets the user to enter 'c' or 'm'"""
    answer = input("Please enter C)ategory or M)ethod of Purchase (for spent): ").lower()
    if answer == 'c':
        return answer
    if answer == 'm':
        return answer
    else:
        print('Input not understood. Please try again.')
        return get_c_or_m()


def line_graph():
    print("\nShows Line Graph of Amounts over time\n")
    list_of_lines = get_entries_for_display()
    first_date = list_of_lines[1][0]
    last_date = list_of_lines[-1][0]
    df = pd.DataFrame(list_of_lines[1:], columns=list_of_lines[0])

    colors = ['green', 'red'] * len(list_of_lines)

    fig = plt.figure('Line Graph from ' + first_date + ' to ' + last_date)

    #-----------------------------------------------
    ax1 = fig.add_subplot(111)
    graph1 = df.groupby('Date', as_index=False, sort=False)['Amount'].sum()
    ax = graph1.plot.line(x='Date', legend=None, ax=ax1, color=colors)

    ax.set_xticks(range(len(graph1)))
    ax.set_xticklabels([graph1["Date"][item] for item in graph1.index.tolist()], rotation=60)
    
    plt.xlabel("Date")
    plt.ylabel("Total Spent ($)")
    plt.grid(axis='y')
    plt.show()
    
def get_explode(data_frame):
    listo = []
    for item in range(len(data_frame)):
        listo += [.2]
        j = item
        j += 1
    return listo

def pie_chart():
    """displays amounts by category, or methodofp in a pie chart"""
    print("\nShows Pie Chart of Category, or Method of Purchase over time\n")
    c_or_m = get_c_or_m()
    list_of_lines = get_entries_for_display()
    first_date = list_of_lines[1][0]
    last_date = list_of_lines[-1][0]
    df = pd.DataFrame(list_of_lines[1:], columns=list_of_lines[0])


    if c_or_m == 'c':
        fig_name = 'Categories'
        column = 'Category'
    else:
        fig_name = 'Method of Purchase'
        column = 'Method of purchase'

    plt.figure('Pie Chart of ' + fig_name + ' from ' + first_date + ' to ' + last_date)

    #-----------------------------------------------
    graph1 = df.groupby(column, as_index=False)['Amount'].sum()
    plt.pie(graph1['Amount'], labels=graph1[column],shadow=False,
    # with one slide exploded out
    explode=get_explode(graph1),
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    )
    plt.show()

def bar_graph():
    """displays amount by category or methodofp in a bar graph"""
    print("\nShows Bar Graph of Category, or Method of Purchase over time\n")
    c_or_m = get_c_or_m()
    list_of_lines = get_entries_for_display()
    first_date = list_of_lines[1][0]
    last_date = list_of_lines[-1][0]
    df = pd.DataFrame(list_of_lines[1:], columns=list_of_lines[0])


    if c_or_m == 'c':
        fig_name = 'Categories'
        columno = 'Category'
    else:
        fig_name = 'Method of Purchase'
        columno = 'Method of purchase'

    fig = plt.figure('Bar Graph of ' + fig_name + ' from ' + first_date + ' to ' + last_date)

    #-----------------------------------------------
    ax1 = fig.add_subplot(111)
    graph1 = df.groupby(columno, as_index=False, sort=False)['Amount'].sum()
    graph1.plot.bar(x=columno, legend=None, ax=ax1, color=['g'])
    plt.xlabel(columno)
    plt.ylabel("Total Spent ($)")
    plt.grid(axis='y')
    plt.show()
