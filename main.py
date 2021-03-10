import fitz #pip3 install PyMuPDF
import sys

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


def main():
    if not check_arguments(sys.argv):
        exit()
    doc = fitz.open(sys.argv[1])
    for page in doc:
        print(page.get_text("text"))

    


# Check if the script is use as a main script if true then run the main function.
if __name__ == "__main__":
    main()