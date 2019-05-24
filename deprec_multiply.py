import pprint
import random
from timeit import default_timer as timer

def gradeschool_mult(x,y):
    '''Multiply two integers via gradeschool algorithm.'''
    x = str(x);  
    z = 0
    for i in range(len(x)):
        z += 10**i*int(x[len(x)-1-i])*y
   
    return z

def karatsuba_mult(x,y):
    '''Multiply two simlar length integers via karatsuba algorithm.'''
    if x<10 or y<10: return x*y
    x = str(x); y = str(y); 
    # convert to string of 0/1's, MSB first
    n = max(len(x),len(y))
    x = "0"*(n-len(x))+x; y = "0"*(n-len(y))+y # add leading zeroes if needed
    m = n//2
    xtop = int(x[:-m]); xbot = int(x[-m:])
    ytop = int(y[:-m]); ybot = int(y[-m:])
    return (10**(2*m)-10**m)*karatsuba_mult(xtop,ytop)+(10**m)*karatsuba_mult(xtop+xbot,ytop+ybot) +(1-10**m)*karatsuba_mult(xbot,ybot)

print(karatsuba_mult(20, 4))

input_lengths  = [2**i for i in range(5,14,2)]
gradeschool_times = []
karatsuba_times = []




for n in range(1, 9):

    sum_g = 0
    sum_k = 0

    for i in range(500):

        x = random.randrange(10**n)
        y = random.randrange(10**n)
        r = x*y
        #print(r)
        start = timer()
        gradeschool_mult(x,y)
        end=timer()
        sum_g += end - start

        start = timer()
        karatsuba_mult(x,y)
        end = timer()
        sum_k += end - start

    gradeschool_times.append(sum_k/500)
    karatsuba_times.append(sum_k/500)

for i in gradeschool_times:
    print(i)