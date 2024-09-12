import csv
import os
import tempfile
from contextlib import closing
from requests import get

def response(resp):
    #if it is a functioning HTML
    content = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content is not None
            and content.find('html') > -1)


def get_response(url):
    #return html to parse, return none if it cant reach page
    with closing(get(url, stream=True)) as resp:
        if response(resp):
            return resp.content
        else:
            return None

def save_csv(file_location, name, headers, rows):
        if file_location == None:
            file_location = os.path.join(tempfile.gettempdir(), 'temprawdata.txt')
        else:
            file_location = os.path.join(file_location, f"Ouput_Data_{name}.csv")

        print("\n Saving file")
        with open(file_location, 'w', newline = '') as file:
            write_csv = csv.writer(file)
            write_csv.writerow(headers)
            write_csv.writerows(rows)
