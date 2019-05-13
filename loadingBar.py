def loadingBar(maximumNumber, currentNumber, startingNumber=0, message=''):
    p = ((currentNumber-startingNumber)/(maximumNumber-startingNumber))*100
    load = f"[{('█'*(round(p/100*20))).ljust(20, '.')}] {str(round(p, 2)).ljust(6)}% | {message}"
    print('\b'*len(load), end='', flush=True)
    print(load, end='')