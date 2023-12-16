max = 100; min = 200
arg = 0; ret = 0

def checkprime():

        i = 0

        ret = 1
        i = 2
        while (i < arg):
                if (arg % i == 0):
                        ret = 0
                        i = arg

                i = i + 1

def primes():

        arg = 2
        while (((arg + max)) % 2 != 0):
                checkprime()
                if (ret == 1):
                        print(arg)


                arg = arg + 1


primes()