import cs50
import sys
# "str." for isalpha, isspace, ex.: str.islower

def main():
    if len(sys.argv) != 2:
        print("python vigenere.py key")
        return 1
    key = sys.argv[1].lower()       #or key = str.lower(sys.argv[1])
    if str.isalpha(key) is False:
        print("key must be alphabetical chars")
        return 2
    print("Plaintext: ", end="")
    plain = cs50.get_string()
    print("Ciphertext: ", end="")
    i = 0   # a counter for key
    key_len = len(key)
    for c in plain:
        if str.isspace(c) or str.isdigit(c):
            print("{}".format(c), end="")
        elif str.islower(c):
            encipher = ((ord(c) - ord('a')) + ord(key[i % key_len]) - ord('a')) % 26
            c = chr(encipher + ord('a'))
            print(c, end="")
            i +=1
        else:
            encipher = ((ord(c) - ord('A')) + ord(key[i % key_len]) - ord('a')) % 26
            c = chr(encipher + ord('A'))
            print("{}".format(c), end="")
            i +=1
    print()
    return 0
    
if __name__=="__main__":
    main()