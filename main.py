import re

search_engine = "http://www.assembly.ab.ca/documents/isysmenu.html"

def get_hansard_html(date) :    
    IW_DATABASE ='i_hansards';
    IW_FIELD_INPUT = 'Title';
    IW_FILTER_FNAME_LIKE = '20150326_1330_01_han.pdf'
    IW_FIELD_OK = 'Search+in+Hansard'
    
if __name__ == '__main__':