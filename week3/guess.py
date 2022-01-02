def guess():
    mi = 1
    ma = 2097151
    candidate = (mi+ma)//2
    resp = input(f'{candidate}: ')
    while resp != '=':
        if resp == '>':
            mi = candidate
        elif resp  == '<':
            ma = candidate
        candidate = (mi+ma)//2
        resp = input(f'{candidate}: ')
    print('Number is', candidate)

if __name__ == '__main__':
    guess()
