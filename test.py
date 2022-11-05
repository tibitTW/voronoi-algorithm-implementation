def f1():
    l1 = []

    def f2():
        l1.append(1)
        l1.append(2)
        l1.append(3)

    f2()
    return l1


print(f1())
