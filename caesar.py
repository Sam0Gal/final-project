import cs50
import sys
# "str." for isalpha, isspace, ex.: str.islower

def main():
    if len(sys.argv) != 2:
        print("python caesar.py key")
        return 1
    key = int(sys.argv[1])
    if key < 0:
        print("key must be non-negative int")
        return 2
    print("Plaintext: ", end="")
    plain = cs50.get_string()
    print("Ciphertext: ", end="")
    for c in plain:
        if str.isspace(c) or str.isdigit(c):
            print("{}".format(c), end="")
        elif str.islower(c):
            encipher = ((ord(c) - ord('a')) + key) % 26
            c = chr(encipher + ord('a'))
            print(c, end="")
        else:
            encipher = ((ord(c) - ord('A')) + key) % 26
            c = chr(encipher + ord('A'))
            print("{}".format(c), end="")
    print()
    return 0

if __name__=="__main__":
    main()