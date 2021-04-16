# Allows arguments
import sys 

# Local Class import
from xps_to_table import XpsToTable


def main(): 
    converter = XpsToTable()
    converter.handle_arguments(sys.argv[1:])
    converter.read_xps_inputfile()
    

    


# Check if the script is use as a main script if true then run the main function.
if __name__ == "__main__":
    main()