import os
import tika 
from tika import parser


def parse_and_create_txt_file(path_to_PDF_file):
    tika.initVM()
    parsed_pdf = parser.from_file(path_to_PDF_file)
    parsed_content = parsed_pdf['content']
    
    pathToNewFile = os.path.splitext(path_to_PDF_file)[0] + '.txt'
    with open(pathToNewFile , 'w' , encoding= 'utf-8') as file:
        file.write(parsed_content)
       

# if __name__ == "__main__" :
#     main()     





