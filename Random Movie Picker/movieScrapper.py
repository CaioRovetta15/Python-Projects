import requests 
from bs4 import BeautifulSoup
from PIL import Image
def getMediaInfo(num_pages=1):
    media_dict = {}
    for i in range(1, num_pages+1):
        URL = 'https://torrentools.com/'+str(i)+'/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        soup.prettify()
        results = soup.find(id="capas_pequenas")
        medias = results.find_all("div", class_="capa_lista")
        for media in medias:
            title = media.find('h3')
            movie_or_serie = media.find('span', class_="capa_categoria")
            url = media.find('a')
            cover_url = media.find('img')
            cover_image = cover_url# Image.open(requests.get(cover_url['src'], stream=True).raw)
            other_data = media.find('p')
            #make a list of the data (separated by line)
            other_data = other_data.text.splitlines()
            #remove the first element using list slicing
            other_data = other_data[1:]
            #remove the last 3 elements using list slicing
            other_data = other_data[:-3]
            #split the first element of the list by the / character
            #get the value between the () in the last element of the list
            last_element = other_data[-1]  # Get the last element of the list
            year_of_release = last_element[last_element.find("(")+1:last_element.find(")")]
            genre = other_data[0].split('/')
            #remove all the spaces from the list
            genre = [x.strip() for x in genre]
            IMDB_rating = media.find('span', class_="capa_imdb").text
            IMDB_rating = float(IMDB_rating.split(': ')[-1].replace(',', '.'))
            media_dict[title.text] = [movie_or_serie.text, url['href'], IMDB_rating , cover_url['src'],year_of_release, genre]
    return media_dict

if __name__ == '__main__':
    dic = getMediaInfo(1)
    for key in dic:
        print(dic[key])