from requests import get
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from contextlib import closing

def get_html_tables(Name):
    #the plan
    #to make it iterate the sites including the element
    #then when the webpage is shown where it outputs the links of different reactions
    #we will then list them in a table for them to iterate again and store these in an
    #external table 
    url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2=&Prod=&Prod2=&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI', Name.lower())

    #gets the html
    actualHtml = get_response(url)

    #beautifulsoup to parse
    html = BeautifulSoup(actualHtml, 'html.parser')

    link_iter = html.find()


    def get_response(url):
        #return html to parse, return none if it cant reach page
        with closing(get(url, stream=True)) as resp:
            if response(resp):
                return resp.content
            else:
                return None
    
    def response(resp):
        #if it is a functioning HTML
        content = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content is not None
                and content.fine('html') > -1)
    
