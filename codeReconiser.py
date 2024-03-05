import cv2
import matplotlib.pyplot as plt

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

def find_sequence_length(binary_line, sequence):
    # Konwertuj listę binarną na ciąg znaków
    binary_string = ''.join(map(str, binary_line))

    # Znajdź indeksy początku i końca sekwencji
    start_index = binary_string.find(sequence)
    end_index = binary_string.rfind(sequence)

    # Oblicz długość sekwencji
    if start_index != -1 and end_index != -1:
        sequence_length = end_index - start_index + len(sequence)
    else:
        sequence_length = 0

    return sequence_length
    

barcode = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)

barcode = cv2.bitwise_not(barcode)

height, width = barcode.shape

row_index = round(height/2)

line = barcode[row_index, : ]

binaryLine = (line > 128).astype(int)

cleaned_line = clean_binary_line(binaryLine)
print(cleaned_line)

