def f1(n):
    if n == 1:
        return n
    else:
        return n * f1(n - 1)

def f2(n):
    for i in range(1, n+1, +1):
        if i==n:
            print(i,end=" ")
        else:
            print(i, end="*")

if __name__ == '__main__':
    num = int(input("Enter a number: "))
    print("Factorial of",num,"is",end=" ")
    f2(num)
    print("=",end=" ")
    print(f1(num))
