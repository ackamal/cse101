# CSE101 HW5, #5:
# Thresholding and Multiplication Algorithms
import pprint
from bitstring import BitArray



# Binary multiplication function. Takes in
# two arrays of bits and returns their product.
def binary_multiply(bit_array_1, bit_array_2):

    return_length = len(bit_array_1) + len(bit_array_2) - 1

    output = [[0 for i in range(len(bit_array_1) + len(bit_array_2))] for j in range(len(bit_array_2))]
    #pprint.pprint(output)
    bit_array_2.reverse()

    for i in range(len(bit_array_2)):

        max_offset = len(bit_array_2) - 1
        incrmt = 0

        for j in range(len(bit_array_1)):
            
            #print("(" + str(i) + ", " + str(j) + ")" + ": " + str(bit_array_2[i]) + "*" + str(bit_array_1[j]))
            output[i][j + i + 1] = bit_array_2[i] * bit_array_1[j]

        incrmt = 0
    
    #pprint.pprint(output)

    return_list = [0 for i in range(len(bit_array_1) + len(bit_array_2))]


    carry = 0

    for i in range(len(return_list) - 1, -1, -1):
        for list in output: 

            return_list[i] = list[i] + return_list[i]

        return_list[i] = return_list[i] + carry

        carry = 0

        if (return_list[i] > 1):

            carry = 1

            if (return_list[i] % 2) == 0:
                return_list[i] = 0
            else:
                return_list[i] = 1

    while(len(return_list) > 1 and return_list[0] == 0):
        return_list.pop(0)

    pprint.pprint(return_list)
    return return_list

# Helper addition function for adding two
# binary numbers that might not have the
# same size.
def add_bits(bit_array_1, bit_array_2):

    
    while (len(bit_array_1) > len(bit_array_2)):
        bit_array_2.insert(0, 0)

    while len(bit_array_1) < len(bit_array_2):
        bit_array_1.insert(0, 0)

    sum = [0 for i in range(len(bit_array_1))]
    carry = 0

    for i in range(len(bit_array_1) - 1, -1, -1):
        sum[i] = bit_array_1[i] + bit_array_2[i] + carry

        if (sum[i] > 1):
            carry = 1

            if (sum[i] % 2) == 0:
                sum[i] = 0
            else:
                sum[i] = 1
        else:
            carry = 0

    if carry != 0 and i == 0:
        sum.insert(0, 1)

    return sum

# Helper subtraction function that subtracts
# the second bit array from the first.
def subtract_bits(bit_array_1, bit_array_2):

    b1 = "".join(map(str, bit_array_1))
    b2 = "".join(map(str, bit_array_2))
    diff = int(b1,2)-int(b2,2)

    if(diff >= 0):
        output = [int(i) for i in bin(diff)[2:]]
    else:
        output = [int(i) for i in bin(diff)[2:]]

    return output


def create_bit_array(input_data, bits, signed=False):
    if not isinstance(input_data, (int, long, str, unicode, BitArray)):
        raise TypeError("Input must be given as binary strings or integers.")
    elif isinstance(input_data, BitArray):
        return input_data 
    elif isinstance(input_data, (str, unicode)):
        input_data = input_data.replace("0b", "")
        if len(input_data) == 0:
            input_data = 0
        elif ("-" in input_data or input_data[0] == "0" or 
              (input_data[0] == "1" and not signed)):
            input_data = int(input_data, 2)
        else:
            mask = int(("1" * len(input_data)), 2)
            input_data = -1*((int(input_data, 2) ^ mask) + 1)
    return BitArray(int=input_data, length=bits)

class Multipliers(object):

    """
    This class implements various types of mulipliers using different algorithms used in study, analysis
    or practical implementation of ALU's in various Computer architectures.
    """
    @staticmethod
    def karatsuba_multiply(multiplier, multiplicand, bits = None, signed=False):

        # Use bit array only to calculate 2's complement of signed binaries.

        if bits is None:
            multiplier = multiplier.replace('0b','')
            if not signed:
                multiplier = multiplier.lstrip("0")

            multiplicand = multiplicand.replace('0b','')
            if not signed:
                multiplicand = multiplicand.lstrip("0")
            bits = max(len(multiplier), len(multiplicand)) + 1

        len_input = bits

        if (bits % 2) == 0:
            bits += 1

        multiplicand = create_bit_array(multiplicand, bits)
        multiplier = create_bit_array(multiplier, bits)

        sign_bit = None

        if ( signed or (multiplicand.int < 0) or (multiplier.int < 0)):
            # Calculating the sign of the product
            if ( ( multiplicand.bin[0] == "1" ) ^ ( multiplier.bin[0] == "1" ) ):
                sign_bit = 1
            else:
                sign_bit = 0

            # Strip off the sign bit
            multiplicand.int = abs(multiplicand.int)
            multiplier.int = abs(multiplier.int)

        # Binary without the sign bit
        multiplier_abs = multiplier.bin[1:]
        multiplicand_abs = multiplicand.bin[1:]

        if len(multiplier_abs) == 0 or len(multiplicand_abs) == 0:
            return "0"

        # Base case of 1 bit multiplication
        if len(multiplier_abs) == 1:
            return "1" if ( multiplier_abs == "1" and multiplicand_abs == "1" ) else "0"

        # Base case for 2 bit multiplication
        if len(multiplier_abs) == 2:
            return bin( multiplicand.int * multiplier.int ).replace("0b","")

        m = (bits-1) / 2

        # x = x1*(2**m) + x0
        # y = y1*(2**m) + y0

        x1 = multiplicand_abs[:m]
        x0 = multiplicand_abs[m:]

        y1 = multiplier_abs[:m]
        y0 = multiplier_abs[m:]

        #print x1, x0
        #print y1, y0
        #print "m ", m

        # Upper half of the bits
        z2 = Multipliers.karatsuba_multiply(x1, y1)
        # Lower half of the bits
        z0 = Multipliers.karatsuba_multiply(x0, y0)
        # ( x1 + x0 )( y1 + y0 )
        sum_term1 = int(x1,2) + int(x0,2)
        sum_term1 = bin(sum_term1)

        sum_term2 = int(y1,2) + int(y0,2)
        sum_term2 = bin(sum_term2)

        #print "sum terms: ", sum_term1.replace('0b',''), sum_term2.replace('0b','0')

        z1 = Multipliers.karatsuba_multiply(sum_term1, sum_term2)
        z1 = bin ( int(z1,2) - int(z2,2) - int(z0,2) )
        #print "z1: ", z1

        # The "0" padding at the right is binary equivalent of left shift or muliply with 2**bits
        abs_result = int((z2 + "0"*(2*m)),2) + int((z1 + "0"*(m)),2) + int(z0,2)

        # len_result = 2*length of multiplicand / multiplier

        len_result = 2*len_input

        # Converting to binary of 2ce the bit length of inputs
        abs_result = create_bit_array(abs_result, len_result)

        if sign_bit == 1:
            abs_result.int *= -1

        return abs_result.bin

def shift_left(bit_array_1, num_places):

    for i in range(num_places):
        bit_array_1.append(0)

    return bit_array_1

#binary_multiply([1, 1, 1, 1],[1, 0, 1])
#add_bits([1, 0, 0, 1, 0],[1, 1, 1, 0])
#pprint.pprint(ks_multiply([1, 0, 1],[1, 1]))

arr1 = [int(i) for i in create_bit_array(5, 4).bin]
arr2 = [int(i) for i in create_bit_array(3, 4).bin]

pprint.pprint(Multipliers.karatsuba_multiply(5, 3, 4))


        