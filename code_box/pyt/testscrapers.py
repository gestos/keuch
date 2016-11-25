from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen("/home/keuch/Arrays.html").read()
souppe = BeautifulSoup(r)
print souppe.prettify()
