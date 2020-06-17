import random
import os
import copy


# Defines cls() to clear the screen of prints
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


arr = []
for i in range(4):
    arr.append(random.randint(1, 5))


def guess(arr, turn):
    temp_arr=arr.copy()
    done = False
    guess_arr = []
    while not done:
        print('turn', turn)
        select = input("Pick a number between 1 and 6")
        cls()
        try:
            if int(select) < 7 and int(select) > 0:
                guess_arr.append(select)

            else:
                print('Invalid Number')
        except ValueError:
            print("Invalid Number")

        if len(guess_arr) == 4:
            sub = 0
            matches = [0, 0, 0, 0]
            half_matches = []
            for n, i in enumerate(guess_arr):
                if int(i) == temp_arr[n-sub]:
                    matches[n] = int(i)
                    temp_arr.remove(temp_arr[n-sub])
                    sub += 1
                elif int(i) in temp_arr:
                    half_matches.append(int(i))
            done = True

    winnings = 0
    for i in matches:
        if i:
            winnings += 1
    print("Your guesses - ", guess_arr)
    print("You guessed %s correctly" % winnings)
    print("You guessed %s correctly, but not in the right place" % len(half_matches))
    if winnings == 4:
        return True

turn = 0
for i in range(5):
    turn += 1
    if guess(arr, turn):
        print('correct = ', arr)
        break



