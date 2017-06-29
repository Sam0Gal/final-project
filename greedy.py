import cs50 as cs

def main():
    print("O hai! ", end="")
    while True:
        print("How much change is owed?")
        money = cs.get_float()
        if money >= 0:
            break
    money = round(money, 2)*100
    coins = money//25          #for quarters
    remainder = money % 25
    coins += remainder//10     #for dimes
    remainder = money % 10
    coins += remainder//5      #nickels
    remainder = money % 5
    coins += remainder//1       #pennies
    remainder = money % 1
    print(coins)

if __name__=="__main__":
    main()