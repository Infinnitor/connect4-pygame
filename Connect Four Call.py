# cool
import CFourText as c

while True:
    thing = c.take_turn(int(input("Where da piece go???? ")) - 1)
    if thing[0]:
        c.os.system("cls")
        print(c.return_matrix(thing[1]))
    else:
        print("wrong")
