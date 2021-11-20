# Easy

import random


def main():
    print("Enter the number of friends joining (including you):")
    num = int(input())
    if num <= 0:
        print("No one is joining for the party")
        exit()
    friends = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for _ in range(num):
        friend = input()
        friends[friend] = 0
    print("Enter the total bill value:")
    total = int(input())
    price = round(total / num, 2)
    for name in friends.keys():
        friends[name] = price
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    result = input().lower()
    if result == "yes":
        luck = True
    else:
        luck = False
    if luck:
        lucky_dog = random.choice([x for x in friends.keys()])
        friends[lucky_dog] = 0
        price = round(total / (num - 1), 2)
        for name in friends.keys():
            if name != lucky_dog:
                friends[name] = price
        print(f"{lucky_dog} is the lucky one")
    else:
        print("No one is going to be lucky")
    print(friends)


if __name__ == "__main__":
    main()
