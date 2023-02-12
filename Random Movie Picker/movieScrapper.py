import requests 
from bs4 import BeautifulSoup

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
            other_data = media.find('p')
            IMDB_rating = media.find('span', class_="capa_imdb")
            media_dict[title.text] = [movie_or_serie.text, url['href'], IMDB_rating.text, other_data.text, cover_url['src']]
    return media_dict

if __name__ == '__main__':
    dic = getMediaInfo(1)
    print(dic.keys())
