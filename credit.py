import cs50
# 123456     second is 5 not 2
def main():
    digit_sum = 0   # sum of digits
    number = cs50.get_int()
    length = len(str(number))
    if length==15:
        if number//10**13 == 34 or number//10**13 == 37:
            tmp_sec_last = number // 10
            #number /= 10
            digit_sum = check(number, tmp_sec_last, digit_sum)
            if digit_sum % 10 == 0:
                print("AMEX")
            else:
                print("INVALID")
        else:
            print("INVALID")
    elif length == 16:
        if number//10**14 == 51 or number//10**14 == 52 or number//10**14 == 54 or number//10**14 == 54 or number//10**14 == 55:
            tmp_sec_last = number // 10
            digit_sum = check(number, tmp_sec_last, digit_sum)
            if digit_sum % 10 == 0:
                print("MASTERCARD")
            else:
                print("INVALID")
        elif number//10**15 == 4:
            tmp_sec_last = number // 10
            digit_sum = check(number, tmp_sec_last, digit_sum)
            if digit_sum % 10 == 0:
                print("VISA")
            else:
                print("INVALID1")
        else:
            print("INVALID")
    elif length == 13 and number//10**12 == 4:
        tmp_sec_last = number // 10
        check(number, tmp_sec_last, digit_sum)
        if digit_sum % 10 == 0:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")
    
def check(number, tmp_sec_last, digit_sum):
    while tmp_sec_last != 0:
        digit = (tmp_sec_last % 10) * 2
        digit_sum += digit // 10 + digit % 10
        tmp_sec_last //= 100
    while number != 0:
        digit_sum += number % 10
        number //= 100
    return digit_sum
if __name__=="__main__":
    main()