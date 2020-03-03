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
from yellowbrick.text import PosTagVisualizer


def clean_syno(text)->pd:
    ###load the csv file and then turn them into lower cases, clean some noise like ~ xxx.more, (c) disney offical etc.
    file = csv.reader(open(text)) # Here your csv file
    lines = list(file) #read into list.
    for  movie_info in lines[1:]:#disregard the first line --> column title
        syno = movie_info[-1].lower()
        syno = syno.split()
        #what each line looks like:
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
            #############new_syno = re.sub(r'[^\w\s]',' ',new_syno)
            movie_info[-1] = new_syno
        #print(movie_info[-1]) """ will print out every syno, without punction and all lower"""
    return lines


def look_for_wave_in_syno(synopisis:list)->list:
    ### look to ~ and delete all leters after this symbol
    try:
        return synopisis[:synopisis.index('~')]
    except:
        return synopisis

def look_for_C_in_syno(synopisis:list)->list:
    """look for (c) then delete everything after it."""
    try:
        return synopisis[:synopisis.index('(c)')]
    except:
        return synopisis

def reduce_more(synopisis:list)->list:
    """in some syno, read.more is the last word, we need to delete it."""
    if 'more' in synopisis[-1]:
        return synopisis[:-1]
    else:
        return synopisis


def movie_classfier(movie_list:list)-> dict:
    ### classfy movies by genre, store into ids.
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
    ### for synopisis, clean up into sentence token- then work token, return word into orgianl form(lemmatize)

    origianl_form = []
    movie_syno_str = []
    result = []
    #syno_for_certain_genre = []
    total_tag = []
    for movie in movies:
        movie_tag = []
        cleaned = []
        movie_syno_str = movie[-1]
        words = []
        syno_sentences = nltk.sent_tokenize(movie_syno_str,'english') ### tokenize the word.
        # sentences.append(syno_sentences)
        # #print(sentences)
        for sentence in syno_sentences:
            words.append(nltk.word_tokenize(sentence))
            for element in words:
                sentence_tag = []
                sentence_tag = nltk.pos_tag(element,lang = 'eng') ## give each word a tag. so that we know which word is noun, adj etc.
                movie_tag.append(sentence_tag)
            lemma = nltk.wordnet.WordNetLemmatizer()
            for word, type in sentence_tag:
                if type.startswith('NN'):#### currently we only keep n, verb, adj, and return these words into it's origianl form:
                # likes -> like    leaves -> leaf
                ### here's what it means: https://zhuanlan.zhihu.com/p/38231514
                    cleaned.append(lemma.lemmatize(word, pos='n'))
                elif type.startswith('V'):
                    cleaned.append(lemma.lemmatize(word, pos='v'))
                elif type.startswith('JJ'):
                    cleaned.append(lemma.lemmatize(word, pos='a'))
                elif type.startswith('R'):
                    cleaned.append(lemma.lemmatize(word, pos='r'))
                else:
                        # it is other form, disregard it.
                    cleaned.append(word)
        result.append(cleaned)
        total_tag.append(movie_tag)
    viz = PosTagVisualizer()
    viz.fit(total_tag)
    viz.show()
    return result


def remove_stop(text:list)->list:
    result= []
    for movie_syno in text:
        clean_syno = []
        #print(element)
        for sentence in movie_syno:
            sentence = re.sub(r'[^\w\s]', '', sentence)
            if sentence != '':
                if sentence not in stop_words:
                    clean_syno.append(sentence)
        result.append(clean_syno)
    return result





if __name__ == "__main__":
    total_movie_info = clean_syno('Capstone 2020 - Disney - Movie data.csv')
    #print(movie_info[0])
    genres = movie_classfier(total_movie_info)
    #seperaete movies into different genre with their ids.
    Action_ids,Adventure_ids,Animation_ids,Comedy_ids,Documentary_ids,Drama_ids,Family_ids,\
    Horror_ids,Musical_ids,Romantic_Comedy_ids,Science_Fiction_ids,Suspense_ids,Western_ids   =    genres['Action'],genres['Adventure'],\
                                                                                                   genres['Animation'],genres['Comedy'],\
                                                                                                   genres['Documentary'],genres['Drama'],genres['Family'],\
                                                                                                   genres['Horror'],genres['Musical'],genres['Romantic Comedy'],\
                                                                                                   genres['Science Fiction'],genres['Suspense'],genres['Western']
    Science_Fiction_movies = get_sgle_movie(Science_Fiction_ids)
    #print(action_movie)
    Science_Fiction_text = nltk_token(Science_Fiction_movies)
    print(Science_Fiction_text)
    Science_Fiction_text = remove_stop(Science_Fiction_text)
    #print(Science_Fiction_text)


