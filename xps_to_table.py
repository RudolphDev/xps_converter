import getopt
import sys

# Handle xps files
import fitz #pip3 install PyMuPDF
# Use matrix and arrays
import numpy as np
# Use Regex
import re


class XpsToTable:
    
    def __init__(self):
        self.__input_file = None
        self.__output_file = None
        self.__nb_replicates = None
        self.__list_len_exps = []
        self.__data_final = np.empty([0,3])
        print("Converter created")

    def handle_arguments(self, argv):
        try:
            opts, args = getopt.getopt(
                argv, "hi:o:r:s:", ["input=", "output=", "replicates=", "sequences="])
        except getopt.GetoptError as err:
            print(err)
            self.__print_usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt == "-h":
                self.__print_usage()
                sys.exit()
            elif opt in ("-i", "--input"):
                self.__input_file = arg
            elif opt in ("-o", "--output"):
                self.__output_file = arg
            elif opt in ("-r", "--replicates"):
                self.__replicates = arg
            elif opt in ("-s", "--sequences"):
                self.__list_len_exps = arg
                
        # Uncomment to check all the parameters
        # if (self.__input_file == None) or (self.__output_file == None) or (len(self.__list_len_exps) == 0):
        #     print("Inputfile, outputfile and sequences parameters are mandatory")
        #     self.__print_usage()
        #     sys.exit(2)
        if not self.__check_inputfile():
            sys.exit()

    def read_xps_inputfile(self):
        doc = fitz.open(self.__input_file)
        for page in doc.pages(0,doc.page_count,1):
            content = page.get_text("text")
            self.__get_data_from_content(content)
        doc.close()

    def __print_usage(self):
        print("Arguments:")
        print("-h \t\t\t\t\tShow help")
        print("-i \t --input <inputfile> \t\tPath of the input file. Look in data folder for a format example")
        print("-o \t --output <outputfile> \t\tPath and name of the desired CSV/XLS file produced")
        print("-r \t --replicates <nb_replicates> \tNumber of replicates for each experience Default value = 1")
        print("-s \t --sequences <list> \t\tA list of int representing the number of ... in the expercience. Format = \"6 4 5\"")

    def __check_inputfile(self):
        try:
            f = open(self.__input_file)
            f.close()
        except IOError:
            print("{} file doesn't exist please check the file path".format(self.__input_file))
            return False
        return True
    
    def __get_data_from_content(self, content):
        content_list = content.splitlines()
        i = 0
        clean_list = []
        #Cursor move forward while the content is a whitespace
        while re.match('\s+', content_list[i]):
            i = i+1
        #Stop the process if the second table is detected
        if re.match('^[A-Z]{1}$', content_list[i]):
            return
        else:
            pattern = '^Unknown[0-9]+'
            while not re.match(pattern, content_list[i]):
                i = i + 1
            while content_list[i] != "Group":
                clean_list.append(content_list[i])
                i = i + 1
            matrix = np.array(clean_list)
            matrix = np.reshape(matrix, (int(len(clean_list)/3), 3))
            if np.shape(self.__data_final)[0] == 0:
                self.__data_final = matrix
            else:
                self.__data_final =np.concatenate((self.__data_final, matrix), axis=0)