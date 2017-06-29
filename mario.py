import cs50


def main():
    while True:
        print("Height:", end="")
        h = cs50.get_int()
        if h > 0 and h < 23:
         break
    width = h
    for i in range(h):
        print(" " * (h - i - 1), end="")
        print("#" * (i + 2), end="")    # "i + 2": +1 because i starts from 0 and +1 for pyramid
        print("  ", end="")
        print("#" * (i+2))
        print()

if __name__=="__main__":
    main()