import cv2

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
            code_pattern.append([counter,x])
            counter = 0;

    return code_pattern


barcode = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)

barcode = cv2.bitwise_not(barcode)

height, width = barcode.shape

row_index = round(height/2)

line = barcode[row_index, : ]

binaryLine = (line > 128).astype(int)

cleaned_line = clean_binary_line(binaryLine)

print(len(cleaned_line))
print(get_code_pattern(cleaned_line))