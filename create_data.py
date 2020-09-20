import os
import time
import datetime
import random

"""This file creates a txt file that can be used as input to the main.py file to create
a semi-random example user.

Run this file to generate a txt file that can be piped into main with the form

python main.py < input_creator.txt

This file will generate number_years years worth of data.
"""

new_user = "Jenny"
number_years = 5

current_year = datetime.datetime.now().year
working_year = current_year-number_years

rent = '1000'
purchases_description = ['hat', 'groceries','car','bills','gas','confetti','blanket','antifreeze','book']
purchase_category = ['food','rent','car','misc','gifts']
purchase_method = ['card','smiles','cash','check']

received_description = ['work','refund','gift']
received_category = ['work','other']


with open("input_creator.txt", "w") as file:
    #create new user
    file.write('5\n')
    file.write('5\n')
    file.write(new_user + '\n')
    file.write('y\n')
    file.write('6\n')

    for year in range(number_years):
        working_year += 1

        #change year

        file.write('5\n')
        file.write('3\n')
        file.write(str(working_year) + '\n')
        file.write('6\n')

        #go to add
        file.write('1\n')

        #pay rent, and income

        for i in range(1,13):
            #rent
            file.write('1\n')
            file.write(str(i) + '-1\n')
            file.write(str(rent) + '\n')
            file.write('rent\n')
            file.write('rent\n')
            file.write(str(purchase_method[random.randint(0,len(purchase_method)-1)]) + '\n')
            file.write('y\n')

            #work
            file.write('2\n')
            file.write(str(i) + '-11\n')
            file.write(str(random.randint(1500,3000)) + '\n')
            file.write('work\n')
            file.write('work\n')
            file.write('y\n')

        #random purchases

        for _ in range(90):
            file.write('1\n')
            file.write(str(random.randint(1,12)) + '-' + str(random.randint(1,28)) + '\n')
            file.write(str(random.randint(5,300)) + '\n')
            file.write(str(purchases_description[random.randint(0,len(purchases_description)-1)]) + '\n')
            file.write(str(purchase_category[random.randint(0,len(purchase_category)-1)]) + '\n')
            file.write(str(purchase_method[random.randint(0,len(purchase_method)-1)]) + '\n')
            file.write('y\n')

        #random received

        for _ in range(20):
            file.write('2\n')
            file.write(str(random.randint(1,12)) + '-' + str(random.randint(1,28)) + '\n')
            file.write(str(random.randint(50,500)) + '\n')
            file.write(str(received_description[random.randint(0,len(received_description)-1)]) + '\n')
            file.write(str(received_category[random.randint(0,len(received_category)-1)]) + '\n')
            file.write('y\n')

        file.write('5\n')



    #exit program
    file.write('6\n')


os.system("python main.py < input_creator.txt")


