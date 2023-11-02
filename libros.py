from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


# WebScraping
URL = 'https://cuspide.com/100-mas-vendidos/'
peticion= requests.get(URL)
html = peticion.text

soup = BeautifulSoup(html, 'html.parser')

libros = soup.find_all(class_=["woocommerce-loop-product__title"], string=re.compile(""))  
bdi = soup.find_all('bdi')

# Pandas
data = {'Libros': [], 'Precio': []}
df = pd.DataFrame(data)

# Iterar en el dataFrame
for i,j in zip(libros,bdi):
    libro = i.text
    precio = j.text 
    df = pd.concat([df, pd.DataFrame({'Libros': [libro], 'Precio': [precio]})], ignore_index=True)

# limipar strings 
def alphabets(element):
    return "".join(filter(str.isalpha, element))

df['Libros'] = df['Libros'].str.replace('\d+', '', regex=True)
df['Libros'] = [alphabets(x) for x in df['Libros']]
df['Precio'] = df['Precio'].str.replace('[^0-9]', '', regex=True)
df.to_csv('libros.csv', index= False)


print(df)