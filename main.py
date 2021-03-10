import fitz #pip3 install PyMuPDF
import sys
import numpy as np
import pandas as pd

def check_arguments(argv):
    if len(argv) < 2:
        print("ERROR!\nYou must give an xps filepath as argument")
        return False
    else:
        try:
            f = open(argv[1])
            f.close()
        except IOError:
            print("{} file doesn't exist please check the file path".format(argv[1]))
            return False
        return True

def get_table_from_page_content(content):
    content_list = content.splitlines()
    i = 0
    clean_list = []
    while content_list[i] != "Unknown1":
        i = i + 1
    print(i)
    while content_list[i] != "Group":
        clean_list.append(content_list[i])
        i = i + 1
    matrix = np.array(clean_list)
    print(len(clean_list))
    matrix = np.reshape(matrix, (int(len(clean_list)/3), 3))
    return matrix

def main():
    if not check_arguments(sys.argv):
        exit()
    doc = fitz.open(sys.argv[1])
    for page in doc.pages(0,1,1):
        content = page.get_text("text")
        table = get_table_from_page_content(content)
    print(table)
    doc.close()

    


# Check if the script is use as a main script if true then run the main function.
if __name__ == "__main__":
    main()