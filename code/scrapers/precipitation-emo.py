import bs4
#import urllib3
import requests





def make_soup(markup):
    '''
    Take a string containing a html document and return a BeautifulSoup object.

    Inputs:
        markup (str): a string containing an html document received by a
            request object

    Returns:
        soup (soup): a BeautifulSoup object
    '''

    soup = bs4.BeautifulSoup(markup, 'html5lib')

    return soup


#url = 'http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=1709847&cs=rgb&format=CSV&width=360&height=180'

path = 'http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si='

data_id = '1709847'

fmt = '&cs=rgb&format=CSV&width=360&height=180'

url = path + data_id + fmt

rqst = requests.get(url)

markup = util.read_request(rqst)




'''
2016 Aug:  http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=1709847&cs=rgb&format=CSV&width=360&height=180
2016 Jul:  http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=1709848&cs=rgb&format=CSV&width=360&height=180
2016 Jun:  http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=1707079&cs=rgb&format=CSV&width=360&height=180
'''
