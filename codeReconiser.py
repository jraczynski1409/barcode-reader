import cv2
import math

# Program rozczytujący kod kreskowy w formacie EAN13

def clean_binary_line(binary_line):
    # Znajdź indeksy pierwszej i ostatniej sekwencji zer
    first_zero_index = next((i for i, x in enumerate(binary_line) if x == 1), None)
    last_zero_index = len(binary_line) - next((i for i, x in enumerate(binary_line[::-1]) if x == 1), None)

    # Ustal granice sekwencji
    start_index = first_zero_index + 1 if first_zero_index is not None else 0
    end_index = last_zero_index - 1 if last_zero_index is not None else len(binary_line)

    # Wybierz tylko te elementy, które nie należą do pierwszej i ostatniej sekwencji zer
    cleaned_line = binary_line[start_index-1:end_index+1]

    return cleaned_line

def get_code_pattern(binary_line):
    counter = 0;
    code_pattern = []

    for i,x in enumerate(binary_line):
        if(i!=len(binary_line)-1):
            counter = counter + 1
            if(x!=binary_line[i+1]):
                code_pattern.append([counter,x])
                counter = 0;
        if(i==len(binary_line)-1):
            counter = counter + 1
            code_pattern.append([counter,x])
            counter = 0;
    print(len(code_pattern))
    return code_pattern

def get_width_line(barcode_width):
    return barcode_width/95

def create_binary_barcode_value(pattern_array, bit_width):
    binary_barcode = []
    binary_values = []
    for x in pattern_array:
        for i in range(0, round(x[0]/bit_width)):
            binary_barcode.append(x[1])
    
    if(len(binary_barcode)==95):
        if(binary_barcode[0:3]==[1,0,1] and binary_barcode[45:50]==[0,1,0,1,0] and binary_barcode[92:95]==[1,0,1]):
            del binary_barcode[92:95]
            del binary_barcode[45:50]
            del binary_barcode[0:3]
            
            for i in range(0,12):
                 binary_values.append(binary_barcode[i*7:i*7+7])
    else:
        print("dupa")
                
    
    return binary_values

def find_number(binary_number):
    A_codes = [[0, 0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 1], [0, 1, 1, 1, 1, 0, 1], [0, 1, 0, 0, 0, 1, 1], [0, 1, 1, 0, 0, 0, 1], [0, 1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1], [0, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 1]]
    B_codes = [[0, 1, 0, 0, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1, 1], [0, 1, 0, 0, 0, 0, 1], [0, 0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 0, 1], [0, 0, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 1, 1]]
    C_codes = [[1,1,1,0,0,1,0],[1,1,0,0,1,1,0],[1,1,0,1,1,0,0],[1,0,0,0,0,1,0],[1,0,1,1,1,0,0],[1,0,0,1,1,1,0],[1,0,1,0,0,0,0],[1,0,0,0,1,0,0],[1,0,0,1,0,0,0],[1,1,1,0,1,0,0]]
    try:
        index = A_codes.index(binary_number)
        return ([index,'A'])
    except ValueError:
        try:
            index = B_codes.index(binary_number)
            return ([index,'B'])
        except ValueError:
           try:
               index = C_codes.index(binary_number)
               return ([index,'C'])
           except ValueError:
               return([-1,'E'])

def find_first_number(binary_number):
    first_number_codes = [['A','A','A','A','A','A'],['A','A','B','A','B','B'],['A','A','B','B','A','B'],['A','A','B','B','B','A'],['A','B','A','A','B','B'],['A','B','B','A','A','B'],['A','B','B','B','A','A'],['A','B','A','B','A','B'],['A','B','A','B','B','A'],['A','B','B','A','B','A']]
    try:
        index = first_number_codes.index(binary_number)
        return (index)
    except ValueError:
        return(-1)


def decode_binary(binary_barcode):
    numbers = []
    for x in binary_barcode:
        numbers.append(find_number(x))

    return numbers

def get_code_value(values_barcode):
    letter_code = []
    for x in range(0,6):
        letter_code.append(values_barcode[x][1])
    return letter_code

# pobranie zdjęcia w skali szarosci
#barcode = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)
barcode = cv2.imread('6.png', cv2.IMREAD_GRAYSCALE)
# negatyw
barcode = cv2.bitwise_not(barcode)

# odczytywanie paska pikseli ze srodka obrazu
height, width = barcode.shape
row_index = round(height/2)
line = barcode[row_index, : ]

# binaryzacja zdjęcia
binaryLine = (line > 128).astype(int)

#usuwanie wszystkich pikseli poza barcodem
cleaned_line = clean_binary_line(binaryLine)

# obliczanie sredniej szerokosci w pikselach dla jednego bita
bit_width = get_width_line(len(cleaned_line))

# zamiana zestawu pikseli na zestaw bitow usuniecie bitow kontrolnych i podzial na przedzialy dla liczb
binary_barcode = create_binary_barcode_value(get_code_pattern(cleaned_line),bit_width)

#obliczanie wartosci liczbowej dla danej liczby oraz typu kodawania
values_barcode = decode_binary(binary_barcode)

code_array = []

code_array.append(find_first_number(get_code_value(values_barcode)))
for x in range(0,12):
    code_array.append(values_barcode[x][0])

code = ''.join([str(element) for element in code_array])

print(code)

# napisać funkcję która sprawdza poprawnoć kodu kreskowego za pomocą ostatniej cyfry


