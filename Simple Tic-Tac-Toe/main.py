# Normal

status = True


def check(raw):
    global status
    list_o = [o for o in raw if o == "O"]
    list_x = [x for x in raw if x == "X"]
    list_all = [[raw[0], raw[1], raw[2]], [raw[3], raw[4], raw[5]], [raw[6], raw[7], raw[8]]]
    if abs(len(list_o) - len(list_x)) > 1:
        print("Impossible")
        return
    x = x_check(list_all)
    o = o_check(list_all)
    if x and o:
        print("Impossible")
        return
    elif x:
        print("X wins")
        status = False
        return
    elif o:
        print("O wins")
        status = False
        return
    elif not x and not o:
        game = game_check(raw)
        if game:
            print("Draw")
            status = False
            return


def game_check(raw) -> bool:
    """
    :return bool
        finished: True
        Unfinished: False
    """
    for item in raw:
        if item == " ":
            print("Game not finished")
            return False
    return True


def x_check(all) -> bool:
    x_column = 0
    x_row1 = 0
    x_row2 = 0
    x_row3 = 0
    for column in all:
        for idx, element in enumerate(column):
            if element == "X":
                x_column += 1
                if idx == 0:
                    x_row1 += 1
                elif idx == 1:
                    x_row2 += 1
                elif idx == 2:
                    x_row3 += 1
            else:
                continue
        if x_column == 3:
            return True
        x_column = 0
    if x_row1 == 3 or x_row2 == 3 or x_row3 == 3:
        return True
    if all[0][0] == "X" and all[1][1] == "X" and all[2][2] == "X":
        return True
    if all[0][2] == "X" and all[1][1] == "X" and all[2][0] == "X":
        return True
    return False


def o_check(all) -> bool:
    o_column = 0
    o_row1 = 0
    o_row2 = 0
    o_row3 = 0
    for column in all:
        for idx, element in enumerate(column):
            if element == "O":
                o_column += 1
                if idx == 0:
                    o_row1 += 1
                elif idx == 1:
                    o_row2 += 1
                elif idx == 2:
                    o_row3 += 1
            else:
                continue
        if o_column == 3:
            return True
        o_column = 0
    if o_row1 == 3 or o_row2 == 3 or o_row3 == 3:
        return True
    if all[0][0] == "O" and all[1][1] == "O" and all[2][2] == "O":
        return True
    if all[0][2] == "O" and all[1][1] == "O" and all[2][0] == "O":
        return True


def game_run(raw, player):
    raw = [x for x in raw]
    while True:
        pos = input("Enter the coordinates: ")
        inputs = pos.split()
        if inputs[0] in "123" and inputs[1] in "123":
            x = int(inputs[0])
            y = int(inputs[1])
            idx = (x - 1) * 3 + y - 1
            if raw[idx] == " ":
                if player == "X":
                    raw[idx] = "X"
                    break
                elif player == "O":
                    raw[idx] = "O"
                    break
            else:
                print("This cell is occupied! Choose another one!")
                continue
        elif inputs[0] in "0456789" or inputs[1] in "0456789":
            print("Coordinates should be from 1 to 3!")
        else:
            print("You should enter numbers!")
    print_now(raw)
    check(raw)
    if player == "X":
        player = "O"
    else:
        player = "X"
    return [raw, player]


def print_now(raw):
    print("---------")
    print("|", raw[0], raw[1], raw[2], "|")
    print("|", raw[3], raw[4], raw[5], "|")
    print("|", raw[6], raw[7], raw[8], "|")
    print("---------")


def game_init():
    print("""---------
|       |
|       |
|       |
---------""")
    params = ["         ", "X"]
    while status:
        params = game_run(params[0], params[1])


if __name__ == "__main__":
    game_init()
