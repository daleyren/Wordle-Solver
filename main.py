from urllib import response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import pdb
import time
import random

# PUSH GUESS TO WEBSITE
def upload(guess):
    for i in range(5):
        ActionChains(browser)\
        .send_keys(guess[i])\
        .perform()
        time.sleep(0.1)
    ActionChains(browser)\
        .send_keys(Keys.ENTER)\
        .perform()

# TAKE IN PROSPECTIVE LIST
prospectives = []
with open('words.txt') as file:
    prospectives = file.readlines()

for i in range(len(prospectives)):
    prospectives[i] = prospectives[i][:5]

# OPEN WORDLE WEBSITE
url = 'https://www.nytimes.com/games/wordle/index.html'
browser = webdriver.Chrome('/Users/daler/Computer Science/Personal Projects/Tools/chromedriver')
browser.get(url)

# GET RID OF TUTORIAL POP-UP
browser.find_element_by_class_name('Modal-module_closeIcon__b4z74').click()

# GUESSING THE WORD

filled = set() # set of correct indexes
contains = set() # set of present and correct letters
valids = dict() # index: set of possible letters
invalids = set() # absent letters

for i in range(5):
    valids[i] = set()

currBox = 0
grid = browser.find_elements_by_class_name('Tile-module_tile__3ayIZ')


guess = 'SLATE'
solved = False

# upload(guess)
# print(grid[0].text)

while not solved:
    if currBox >= 30:
        print("FAILED")
        break
    upload(guess)
    time.sleep(7)
    # PROCESS WORD
    for i in range(5):
        index = currBox%5
        letter = grid[currBox].text
        state = grid[currBox].get_attribute('data-state')

        print(str(index) + ' ' + letter + ' ' + state)

        if state == 'absent':
            if letter not in contains:
                invalids.add(letter)
        elif state == 'correct':
            valids[index].add(letter)
            temp = set()
            temp.add(letter)
            valids[index] = temp
            for j in range(5):
                if index != j and letter in valids[j]:
                    valids[j].remove(letter)

            contains.add(letter)
            filled.add(index)

        elif state == "present":
            if letter not in contains:
                for j in range(5):
                    if j not in filled:
                        valids[j].add(letter)

            if letter in valids[index]:
                valids[index].remove(letter)
            contains.add(letter)

            num = 0
            temp = -1
            for j in range(5):
                if letter in valids[j]:
                    num += 1
                    temp = j
            if num == 1:
                filled.add(temp)
        else:
            print('ERROR!')
            pdb.set_trace()

        currBox += 1
    
        
    
    # FIND NEXT WORD IF UNSOLVED
    
    i = 0
    while i < len(prospectives):
        prospect = prospectives[i]
        for j in range(5):
            currChar = str(prospect[j].upper())
            if currChar in invalids\
                or (j in filled and currChar not in valids[j]):
                prospectives.pop(i)
                i -= 1
                break
        i += 1
        
    # super jank
    i = 0
    while i < len(prospectives):
        prospect = prospectives[i]
        for present in contains:
            # WORD MUST CONTAIN PRESENT (OR ELSE POP)
            count = 0
            for j in range(5):
                currChar = str(prospect[j].upper())
                if currChar != present:
                    count += 1
            if count == 5:
                prospectives.pop(i)
                i -= 1
                break
        i += 1
        
    print(contains)
    print(filled)
    print(valids)
    print(invalids)

    print(len(prospectives))
    print(prospectives)
    print()

    # PICK NEXT GUESS
    guess = random.choice(prospectives)

    if len(prospectives) == 1:
        upload(guess)
        solved = True

print("SOLVED")


    

