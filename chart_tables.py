import sys
import random

def karatsuba(x,y):
	"""Function to multiply 2 numbers in a more efficient manner than the grade school algorithm"""
	if len(str(x)) == 1 or len(str(y)) == 1:
		return x*y
	else:
		n = max(len(str(x)),len(str(y)))
		nby2 = n / 2
		
		a = x / 10**(nby2)
		b = x % 10**(nby2)
		c = y / 10**(nby2)
		d = y % 10**(nby2)
		
		ac = karatsuba(a,c)
		bd = karatsuba(b,d)
		ad_plus_bc = karatsuba(a+b,c+d) - ac - bd
        
        	# this little trick, writing n as 2*nby2 takes care of both even and odd n
		prod = ac * 10**(2*nby2) + (ad_plus_bc * 10**nby2) + bd

		return prod

def karatsuba_thresh(x,y):
	"""Function to multiply 2 numbers in a more efficient manner than the grade school algorithm"""
	if len(str(x)) <= 18 or len(str(y)) <= 18:
		return x*y
	else:
		n = max(len(str(x)),len(str(y)))
		nby2 = n / 2
		
		a = x / 10**(nby2)
		b = x % 10**(nby2)
		c = y / 10**(nby2)
		d = y % 10**(nby2)
		
		ac = karatsuba_thresh(a,c)
		bd = karatsuba_thresh(b,d)
		ad_plus_bc = karatsuba_thresh(a+b,c+d) - ac - bd
        
        	# this little trick, writing n as 2*nby2 takes care of both even and odd n
		prod = ac * 10**(2*nby2) + (ad_plus_bc * 10**nby2) + bd

		return prod        
    
def gradeMultSD(x,y):
    if (x == 0 or y == 0): return 0
    return x + gradeMultSD(x, y-1)

def gradeMultiply(x, y):
    if (x == 0 | y == 0): return 0
    xDiv10 = x/10
    yDiv10 = y/10
    xSD = xDiv10 == 0
    ySD = yDiv10 == 0
    if (xSD and ySD):
        return gradeMultSD(x,y)
    if xSD:
        return (gradeMultiply(x, yDiv10) * 10) + gradeMultiply(x, y % 10)
    if ySD:
        return (gradeMultiply(xDiv10, y) * 10) + gradeMultiply(x % 10, y)
    
    return (gradeMultiply(x, yDiv10) * 10 ) + gradeMultiply(x, y % 10)

n = int(sys.argv[1])
threshold = int(sys.argv[2])
k = open("outK.txt", "w+")
g = open("outG.txt", "w+")
if threshold == 0:
    for x in range(1,n):
        print(x)
        inputArray1 = []
        inputArray2 = []
        power = 1
        out1 = 0 
        out2 = 0
        for i in range(x):
            inputArray1.append(random.randint(0, 1))
            inputArray2.append(random.randint(0, 1))

        for i in range(len(inputArray1)):
            out1 += inputArray1[len(inputArray1)-1-i]*power
            power *= 2

        power = 1
        for i in range(len(inputArray2)):
            out2 += inputArray2[len(inputArray2)-1-i]*power
            power *=2

        import time as timeK
        start = timeK.time()
        karatsuba(out1,out2)
        end = timeK.time()
        k.write(str(end-start) + '\n')
        import time as timeG
        start = timeG.time()
        gradeMultiply(out1, out2)
        end = timeG.time()
        g.write(str(end-start) + '\n')

else:

    for x in range(1,n):
        print(x)
        inputArray1 = []
        inputArray2 = []
        power = 1
        out1 = 0 
        out2 = 0
        for i in range(x):
            inputArray1.append(random.randint(0, 1))
            inputArray2.append(random.randint(0, 1))

        for i in range(len(inputArray1)):
            out1 += inputArray1[len(inputArray1)-1-i]*power
            power *= 2

        power = 1
        for i in range(len(inputArray2)):
            out2 += inputArray2[len(inputArray2)-1-i]*power
            power *=2
        import time as timeK
        start = timeK.time()
        karatsuba_thresh(out1,out2)
        end = timeK.time()
        k.write(str(end-start) + '\n')
        import time as timeG
        start = timeG.time()
        gradeMultiply(out1, out2)
        end = timeG.time()
        g.write(str(end-start) + '\n')

    """
    threshold_count = n
    for x in range(1,n):
        print(x)
        inputArray1 = []
        inputArray2 = []
        power = 1
        out1 = 0 
        out2 = 0
        for i in range(x):
            inputArray1.append(random.randint(0, 1))
            inputArray2.append(random.randint(0, 1))

        for i in range(len(inputArray1)):
            out1 += inputArray1[len(inputArray1)-1-i]*power
            power *= 2

        power = 1
        for i in range(len(inputArray2)):
            out2 += inputArray2[len(inputArray2)-1-i]*power
            power *=2

        if threshold_count > threshold:
            import time as timeK
            start = timeK.time()
            karatsuba(out1,out2)
            end = timeK.time()
            #print(str(end-start) + '\n')
            threshold_count = threshold_count - 1
        else:
            
            print("Threshold exceeded")
            import time as timeN
            start = timeN.time()
            out1*out2
            end = timeN.time()
            print(str(end-start) + '\n')
    """
