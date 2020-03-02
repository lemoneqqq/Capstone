import csv
import emoji
import re
import pandas as pd
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['every','onto','whose','could'])
stop_words = set(stop_words)
def clean_syno(text)->pd:
    file = csv.reader(open(text)) # Here your csv file
    lines = list(file)
    for  movie_info in lines[1:]:
        #print(movie_info[-1])
        syno = movie_info[-1].lower()
        syno = syno.split()

        #['\ufeffrentrak_title_id', 'title_name', 'year', 'week', 'studio', 'genre', 'screen_number', 'sequel', 'gbo','opening', 'lead_actor', 'supporting_actor', 'producer', 'director', 'synopsis']
        #['809903', 'Daybreakers', '2010', '2', 'Other', 'Action', '2523', '0', '30101577', '15146692','Ethan Hawke,Willem Dafoe', '', 'Bryan Furst/Chris Brown/Sean Furst', 'Michael Spierig/Peter Spierig', " Fresh off the success of their inventive take on the zombie genre, Undead masterminds Michael and Peter Spierig direct Ethan Hawke in an ambitious tale of a futuristic Earth populated entirely by vampires, and the efforts made by the creatures to ensure that their food supply doesn't run out as humankind is faced with extinction. The year is 2017, and a vampire plague has turned most of the planet's human population into bloodsucking ghouls. As the population of mortals fast begins to dwindle, a vampiric corporation sets out to capture and farm every remaining human while simultaneously researching a consumable blood substitute, headed by undead hematologist Edward Dalton (Ethan Hawke). His work is interrupted after stumbling onto a pocket of human survivors lead by Elvis (Willem Dafoe), a former vampire, whose past reveals a cure that could reverse the tide and save the human race. With time running out, Dalton's only hope lies in outsmarting the security forces of his boss (Sam Neill), whose goal isn't just to find a substitute, but to repopulate humanity in order to sell its blood to the highest bidder. ~ Jason Buchanan, Rovimore "]
        without_c = look_for_C_in_syno(syno)
        delete_more = reduce_more(without_c)
        new = look_for_wave_in_syno(delete_more)
        if new == syno:
            pass
        else:
            new_syno = ''
            for letter in new:
                new_syno += ' '+letter
            new_syno = re.sub(r'[^\w\s]',' ',new_syno)
            movie_info[-1] = new_syno
        #print(movie_info[-1]) """ will print out every syno, without punction and all lower"""
    return lines
def look_for_wave_in_syno(synopisis:list)->list:
    try:
        return synopisis[:synopisis.index('~')]
    except:
        return synopisis

def look_for_C_in_syno(synopisis:list)->list:
    try:
        return synopisis[:synopisis.index('(c)')]
    except:
        return synopisis

def reduce_more(synopisis:list)->list:
    if 'more' in synopisis[-1]:
        return synopisis[:-1]
    else:
        return synopisis


def movie_classfier(movie_list:list)-> dict:
    genre_list = defaultdict()
    movie_genre = ['Action','Adventure','Animation','Comedy','Documentary','Drama','Family',
                   'Horror','Musical','Romantic Comedy','Science Fiction','Suspense','Western',]
    for element in movie_genre:
        genre_list[element]=[]
    for movie in movie_list[1:]:
        if movie[5] in genre_list.keys():
            genre_list[movie[5]].append(movie[0])
    return genre_list


def get_sgle_movie(genre_combo:list)->list:### get movie info based on genre.
    movies = []
    for ids in genre_combo:
        movies.append(total_movie_info[1])
    return movies

def nltk_token(movies:list)->list:
    words = []
    origianl_form = []
    movie_syno_str = ''
    tag = []
    result = []
    #syno_for_certain_genre = []
    for movie in movies:
        movie_syno_str += movie[-1] + ' '
    sentences = nltk.sent_tokenize(movie_syno_str,'english')
    for sentence in sentences:
        words.append(nltk.word_tokenize(sentence))
    for element in words:
        tag.append(nltk.pos_tag(element,lang = 'eng'))
    #print(tag)
    lemma = nltk.wordnet.WordNetLemmatizer()
    for word_type in tag:
        for word, type in word_type:
            if type.startswith('NN'):
                result.append(lemma.lemmatize(word, pos='n'))
            elif type.startswith('V'):
                result.append(lemma.lemmatize(word, pos='v'))
            elif type.startswith('JJ'):
                result.append(lemma.lemmatize(word, pos='a'))
            elif type.startswith('R'):
                result.append(lemma.lemmatize(word, pos='r'))
            else:
                result.append(word)
    return result


def remove_stop(text:list)->list:
    result= []
    for element in text:
        if element not in stop_words:
            result.append(element)
    return result





if __name__ == "__main__":
    total_movie_info = clean_syno('Capstone 2020 - Disney - Movie data.csv')
    #print(movie_info[0])
    genres = movie_classfier(total_movie_info)
    Action_ids,Adventure_ids,Animation_ids,Comedy_ids,Documentary_ids,Drama_ids,Family_ids,\
    Horror_ids,Musical_ids,Romantic_Comedy_ids,Science_Fiction_ids,Suspense_ids,Western_ids= genres['Action'],genres['Adventure'],\
                                                                                                   genres['Animation'],genres['Comedy'],\
                                                                                                   genres['Documentary'],genres['Drama'],genres['Family'],\
                                                                                                   genres['Horror'],genres['Musical'],genres['Romantic Comedy'],\
                                                                                                   genres['Science Fiction'],genres['Suspense'],genres['Western']
    Western_movie = get_sgle_movie(Western_ids)
    #print(action_movie)
    Western_movie_text = nltk_token(Western_movie)
    Western_movie__clean_text = remove_stop(Western_movie_text)
    print(Western_movie__clean_text)


