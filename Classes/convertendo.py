import binascii


def digito_para_array(numero):
    array = []
    for digito in numero:
        array.append(int(digito))

#     return array
#
#
# def convertToHEX(array2):
    array1 = []
    for digito in range(len(array)) :
        array1.append(hex(array[digito]))

    return array1

def convertToInteger(array3):
    array = []

    for num in range(len(array3)):
        array.append(int(array3[num],16))

#     return  array
#
# def convetToStringUnionInteger(array4):
    array1 = []

    for val in range(len(array)):
        array1.append(str(array[val]))


    aux = ""
    for v in range(len(array1)):
        string = str(aux) + str(array1[v])
        aux = string

    return  string

a = 528374123412

b = digito_para_array(a)
print(b)

c = convertToInteger(b)
print(c)

#
# d = convertToInteger(c)
# print(d)
#
# e = convetToStringUnionInteger(d)
# print(e)

# print( bytearray.fromhex("7061756c").decode())
