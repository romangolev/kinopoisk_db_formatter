
"""
kinopoisk.ru wached movies exporter


"""

from bs4 import BeautifulSoup
import json, csv

pages = ["files/page1.html","files/page2.html","files/page3.html","files/page4.html"]

movies_list = []
for page in pages:
     with open(page) as fp:
          soup = BeautifulSoup(fp, 'html.parser')


     profileFilmsList = soup.find_all(attrs={"class":"profileFilmsList"})
     items = profileFilmsList[0].find_all(attrs={"class":"item"})

     for item in items:
          movie_dict = dict()
          nameRus = item.find_all(attrs={'class':'nameRus'})
          # print(nameRus[0].string[-6:])
          movie_dict['nameRus'] = nameRus[0].string
          movie_dict['Year'] = nameRus[0].string[-6:][1:-1]
          nameEng = item.find_all(attrs={'class':'nameEng'})
          if nameEng[0].string != '\xa0':
               movie_dict['Title'] = nameEng[0].string 
          else :
               movie_dict['Title'] = nameRus[0].string
          date = item.find_all(attrs={'class':'date'})
          date_ = '-'.join((date[0].string[:-7].split('.'))[::-1])
          movie_dict['WatchedDate'] = date_
          movies_list.append(movie_dict)


with open("movies.json", "w") as fp:
    json.dump(movies_list,fp, ensure_ascii=False)#.encode('utf8')

fieldnames = ['nameRus','Year','Title','WatchedDate']

with open('movies.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(movies_list)
