try:
    import getopt
    import sys

    # Handle xps files
    import fitz  # pip3 install PyMuPDF
    # Use matrix and arrays
    import numpy as np
    # Use Regex
    import re
    # write the excel output file
    import xlsxwriter
except ModuleNotFoundError as err:
    print(err)
    sys.exit()


class XpsToTable:
    """Class to read an XPS file produced by a gamma counter. Then to write an xlsx file with each experience separated and each replicate by line
    """

    def __init__(self):
        """Create the XpsToTable Class instance and initialize all attributes
        """        
        self.__input_file = None
        self.__output_file = None
        self.__replicates_format = []
        self.__data_final = np.empty([0, 3])
        self.__row = 0
        print("Xps Converter created")

    # Public methods
    def handle_arguments(self, argv: list):
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
                self.__fill_replicates_format(arg)
                
        if (self.__input_file == None) or (self.__output_file == None) or (self.__replicates_format == []):
            print("Inputfile, Outputfile and replicates parameters are mandatory")
            self.__print_usage()
            sys.exit(2)
        if not self.__check_inputfile():
            sys.exit()

    def read_xps_inputfile(self):
        doc = fitz.open(self.__input_file)
        for page in doc.pages(0, doc.page_count, 1):
            content = page.get_text("text")
            self.__get_data_from_content(content)
        doc.close()

    def write_exp_xls(self):
        workbook = xlsxwriter.Workbook(self.__output_file)
        worksheet = workbook.add_worksheet()
        for plate in self.__replicates_format:
            self.__write_one_table(plate, worksheet)
            self.__row += 2
        workbook.close()

    # Private methods
    def __write_one_table(self, plate: list, worksheet):
        data_table = self.__data_final[int(plate[0])-1:int(plate[1]), 2]
        col = 0
        for data in data_table:
            if col < int(plate[2]):
                worksheet.write(self.__row, col, data)
                col += 1
            else:
                self.__row += 1
                col = 0
                worksheet.write(self.__row, col, data)
                col += 1

    def __print_usage(self):
        print("Arguments:")
        print("-h \t\t\t\t\tShow help")
        print("-i \t --input <inputfile> \t\tPath of the input file. Look in data folder for a format example")
        print("-o \t --output <outputfile> \t\tPath and name of the desired CSV/XLS file produced")
        print("-r \t --replicates <replicatesfile> \tFile path to the replicates formats. One plate by line with start_pos end_pos nb_replicates\nThe number of replicates must be a multiple of end-start")

    def __check_inputfile(self):
        try:
            f = open(self.__input_file)
            f.close()
        except IOError:
            print("ERROR!\n{} file doesn't exist please check the file path".format(
                self.__input_file))
            return False
        return True

    def __fill_replicates_format(self, replicate_file: str):
        try:
            with open(replicate_file) as f:
                lines = f.read().splitlines()
                for line in lines:
                    self.__replicates_format.append(line.split())
        except:
            print("ERROR!\nReplicates file not found: {}".format(replicate_file))
            sys.exit()

        for replicate in self.__replicates_format:
            if len(replicate) != 3:
                raise Exception(
                    "ERROR!\nYou must give 3 values by line in format : start_pos, end_pos, nb_replicates\n Not : {}".format(replicate))
                sys.exit()
            else:
                if (int(replicate[1]) - int(replicate[0]) + 1) % int(replicate[2]) != 0:
                    raise Exception(
                        "ERROR!\nThe number of replicates must be a multiple of end_pos - start_pos")
                    sys.exit()

    def __get_data_from_content(self, content):
        content_list = content.splitlines()
        i = 0
        clean_list = []
        # Cursor move forward while the content is a whitespace
        while re.match('\s+', content_list[i]):
            i = i+1
        # Stop the process if the second table is detected
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
                self.__data_final = np.concatenate(
                    (self.__data_final, matrix), axis=0)


def main():
    converter = XpsToTable()
    converter.handle_arguments(sys.argv[1:])
    converter.read_xps_inputfile()
    converter.write_exp_xls()


# Check if the script is use as a main script if true then run the main function.
if __name__ == "__main__":
    main()
