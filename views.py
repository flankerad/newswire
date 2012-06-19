from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from newswire.main.models import news, tnews
import datetime
from gensim import corpora, models, similarities
from djangosphinx import SphinxSearch  

def home(request):
    '''
    displays the home page of website
    '''
    if request.method == 'POST':
        query = request.POST.get('query')
        print query
        query_set = tnews.search.query(query)
        for i in query_set:
            print i.id,i._sphinx
        my_result = query_set[3].doc_text
        date_of_myresult = news.objects.get(id=query_set[3].id).date
        print date_of_myresult
        data = {'result':my_result,'datestamp':date_of_myresult,'id':query_set[3].id}
        return render_to_response('base.html',data,RequestContext(request))
    return render_to_response('base.html',RequestContext(request))


def get_similar(request,doc_id):
    topic_distribution = []
    document_relevance = []
    days_range = 162
    day_const = 500
    #fetch the topic list for the news doc
    news_object = news.objects.get(id=doc_id)
    news_date = news_object.date
    
    for i in range(0,100):
        Topic_weight = news_object.__dict__['Topic'+str(i)]
        if(Topic_weight):
            topic_distribution.append((i,Topic_weight))        
    #print topic_distribution
    # sort topic distribution on the basis of weight
    topic_distribution.sort(key=lambda tup: tup[1])
    topic_distribution.reverse()
    #print topic_distribution                                                            ( checked)
    # topic distribution contains the sorted list of topics in the required document
    
    #define constants******************************************
    subtraction_factor = 0
    multiplication_factor = 1000*len(topic_distribution)
    
    #topic_distribution = topic_distribution[:1]
    #print topic_distribution
    for topic in topic_distribution:
        fetch_doc_limit = len(topic_distribution)*2-subtraction_factor
        news_list = get_news_for_topic(topic[0],doc_id, fetch_doc_limit)
        for temp in news_list:
            #print temp.doc_num
            #print temp.__dict__['Topic'+str(topic[0])]
            
            date_diff =abs(( news_date - temp.date).days)
            date_factor = day_const*(days_range/(date_diff+100))
            
            doc_does_not_exist = True
            try:
                for newsitem in document_relevance:
                    if(newsitem[0]==temp.doc_num):
                        newsitem[2]+=temp.__dict__['Topic'+str(topic[0])]*multiplication_factor
                        doc_does_not_exist = False   
            except:
                document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic[0])]*multiplication_factor + date_factor))
            if(doc_does_not_exist==True):  
                document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic[0])]*multiplication_factor + date_factor))            
               
            #if((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic)]*multiplication_factor) not in news_list):
            #    document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic)]*multiplication_factor))
        subtraction_factor+=2
        multiplication_factor-=1000
    document_relevance.sort(key=lambda tup: int(tup[2]))
    document_relevance.reverse()
    #print document_relevance    
    similarity_list = get_final_similarity(news_object ,document_relevance)
    similarity_decision_matrix = []
    #print similarity_list
    for item in similarity_list:
        similarity_decision_matrix.append((document_relevance[item[0]][0],document_relevance[item[0]][1],(document_relevance[item[0]][2]*100*item[1])/1000))
    similarity_decision_matrix.sort(key=lambda tup: int(tup[2]))
    similarity_decision_matrix.reverse()
    print similarity_decision_matrix
    articles = []
    for i in similarity_decision_matrix:
        filename = str(i[0])
        f = open('main/corpora/'+filename,'r')
        x = unicode(f.read(),errors='ignore')
        articles.append(x)
    data= { 'articles':articles}
    return render_to_response('my.html',data,RequestContext(request)) 
    # new document relevance list created
    #print topic_distribution
        
def get_final_similarity(original,source_list):
    original_entity_list = original.doc_entity_set.replace(';',' ')
    #print original_entity_list
    entity_corpus = []
    for i in source_list:
        entity_corpus.append(news.objects.get(id=i[0]).doc_entity_set)
        
    texts = [[word for word in document.lower().split(';')] for document in entity_corpus]
    
    all_tokens = sum(texts, [])
    #print all_named_entity_set
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]
    dictionary = corpora.Dictionary(texts)
    
    
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    vec_bow = dictionary.doc2bow(original_entity_list.lower().split())
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sims 
    

    
        
    
    

def get_news_for_topic(topic_number,doc_id,number_of_results): 
    if(topic_number==0):
        list_of_news =  news.objects.exclude( Topic0 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==1):
        list_of_news =  news.objects.exclude( Topic1 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==2):
        list_of_news =  news.objects.exclude( Topic2 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==3):
        list_of_news =  news.objects.exclude( Topic3 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==4):
        list_of_news =  news.objects.exclude( Topic4 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==5):
        list_of_news =  news.objects.exclude( Topic5 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==6):
        list_of_news =  news.objects.exclude( Topic6 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==7):
        list_of_news =  news.objects.exclude( Topic7 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==8):
        list_of_news =  news.objects.exclude( Topic8 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==9):
        list_of_news =  news.objects.exclude( Topic9 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==10):
        list_of_news =  news.objects.exclude( Topic10 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==11):
        list_of_news =  news.objects.exclude( Topic11 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==12):
        list_of_news =  news.objects.exclude( Topic12 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==13):
        list_of_news =  news.objects.exclude( Topic13 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==14):
        list_of_news =  news.objects.exclude( Topic14 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==15):
        list_of_news =  news.objects.exclude( Topic15 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==16):
        list_of_news =  news.objects.exclude( Topic16 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==17):
        list_of_news =  news.objects.exclude( Topic17 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==18):
        list_of_news =  news.objects.exclude( Topic18 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==19):
        list_of_news =  news.objects.exclude( Topic19 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))        
    elif(topic_number==20):
        list_of_news =  news.objects.exclude( Topic20 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==21):
        list_of_news =  news.objects.exclude( Topic21 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==22):
        list_of_news =  news.objects.exclude( Topic22 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==23):
        list_of_news =  news.objects.exclude( Topic23 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==24):
        list_of_news =  news.objects.exclude( Topic24 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==25):
        list_of_news =  news.objects.exclude( Topic25 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==26):
        list_of_news =  news.objects.exclude( Topic26 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==27):
        list_of_news =  news.objects.exclude( Topic27 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==28):
        list_of_news =  news.objects.exclude( Topic28 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==29):
        list_of_news =  news.objects.exclude( Topic29 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==30):
        list_of_news =  news.objects.exclude( Topic30 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==31):
        list_of_news =  news.objects.exclude( Topic31 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==32):
        list_of_news =  news.objects.exclude( Topic32 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==33):
        list_of_news =  news.objects.exclude( Topic33 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==34):
        list_of_news =  news.objects.exclude( Topic34 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==35):
        list_of_news =  news.objects.exclude( Topic35 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==36):
        list_of_news =  news.objects.exclude( Topic36 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==37):
        list_of_news =  news.objects.exclude( Topic37 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==38):
        list_of_news =  news.objects.exclude( Topic38 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==39):
        list_of_news =  news.objects.exclude( Topic39 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==40):
        list_of_news =  news.objects.exclude( Topic40 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==41):
        list_of_news =  news.objects.exclude( Topic41 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==42):
        list_of_news =  news.objects.exclude( Topic42 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==43):
        list_of_news =  news.objects.exclude( Topic43 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==44):
        list_of_news =  news.objects.exclude( Topic44 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==45):
        list_of_news =  news.objects.exclude( Topic45 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==46):
        list_of_news =  news.objects.exclude( Topic46 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==47):
        list_of_news =  news.objects.exclude( Topic47 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==48):
        list_of_news =  news.objects.exclude( Topic48 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==49):
        list_of_news =  news.objects.exclude( Topic49 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==50):
        list_of_news =  news.objects.exclude( Topic50 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==51):
        list_of_news =  news.objects.exclude( Topic51 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==52):
        list_of_news =  news.objects.exclude( Topic52 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==53):
        list_of_news =  news.objects.exclude( Topic53 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==54):
        list_of_news =  news.objects.exclude( Topic54 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==55):
        list_of_news =  news.objects.exclude( Topic55 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==56):
        list_of_news =  news.objects.exclude( Topic56 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==57):
        list_of_news =  news.objects.exclude( Topic57 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==58):
        list_of_news =  news.objects.exclude( Topic58 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==59):
        list_of_news =  news.objects.exclude( Topic59 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==60):
        list_of_news =  news.objects.exclude( Topic60 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==61):
        list_of_news =  news.objects.exclude( Topic61 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==62):
        list_of_news =  news.objects.exclude( Topic62 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==63):
        list_of_news =  news.objects.exclude( Topic63 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==64):
        list_of_news =  news.objects.exclude( Topic64 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==65):
        list_of_news =  news.objects.exclude( Topic65 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==66):
        list_of_news =  news.objects.exclude( Topic66= None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==67):
        list_of_news =  news.objects.exclude( Topic67 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==68):
        list_of_news =  news.objects.exclude( Topic68 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==69):
        list_of_news =  news.objects.exclude( Topic69 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==70):
        list_of_news =  news.objects.exclude( Topic70 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==71):
        list_of_news =  news.objects.exclude( Topic71 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==72):
        list_of_news =  news.objects.exclude( Topic72 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==73):
        list_of_news =  news.objects.exclude( Topic73 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==74):
        list_of_news =  news.objects.exclude( Topic74 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==75):
        list_of_news =  news.objects.exclude( Topic75 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==76):
        list_of_news =  news.objects.exclude( Topic76= None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==77):
        list_of_news =  news.objects.exclude( Topic77 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==78):
        list_of_news =  news.objects.exclude( Topic78 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==79):
        list_of_news =  news.objects.exclude( Topic79 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))            
    elif(topic_number==80):
        list_of_news =  news.objects.exclude( Topic80 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==81):
        list_of_news =  news.objects.exclude( Topic81 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==82):
        list_of_news =  news.objects.exclude( Topic82 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==83):
        list_of_news =  news.objects.exclude( Topic83 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==84):
        list_of_news =  news.objects.exclude( Topic84 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==85):
        list_of_news =  news.objects.exclude( Topic85 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==86):
        list_of_news =  news.objects.exclude( Topic86= None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==87):
        list_of_news =  news.objects.exclude( Topic87 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==88):
        list_of_news =  news.objects.exclude( Topic88 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==89):
        list_of_news =  news.objects.exclude( Topic89 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==90):
        list_of_news =  news.objects.exclude( Topic90 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==91):
        list_of_news =  news.objects.exclude( Topic91 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==92):
        list_of_news =  news.objects.exclude( Topic92 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==93):
        list_of_news =  news.objects.exclude( Topic93 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==94):
        list_of_news =  news.objects.exclude( Topic94 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==95):
        list_of_news =  news.objects.exclude( Topic95 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==96):
        list_of_news =  news.objects.exclude( Topic96= None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==97):
        list_of_news =  news.objects.exclude( Topic97 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==98):
        list_of_news =  news.objects.exclude( Topic98 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    elif(topic_number==99):
        list_of_news =  news.objects.exclude( Topic99 = None ).exclude(doc_num=doc_id).order_by('Topic'+str(topic_number))
    
    listelem = list(list_of_news)
    listelem.reverse()
    #listlem contains the weight sorted list of news which describe given topic 
    if(len(listelem)<=number_of_results):
        listelem = listelem[:len(listelem)]
    else:
        listelem = listelem[:number_of_results]
    #test code***************************************
    #for i in listelem:
        #print i.__dict__['Topic62']
        #print i.doc_num
    #test code ends**********************************
    return listelem
          
            
def get_similar2(doc_id):
    topic_distribution = []
    document_relevance = []
    days_range = 162
    day_const = 500
    #fetch the topic list for the news doc
    news_object = news.objects.get(id=doc_id)
    news_date = news_object.date
    
    for i in range(0,100):
        Topic_weight = news_object.__dict__['Topic'+str(i)]
        if(Topic_weight):
            topic_distribution.append((i,Topic_weight))        
    #print topic_distribution
    # sort topic distribution on the basis of weight
    topic_distribution.sort(key=lambda tup: tup[1])
    topic_distribution.reverse()
    #print topic_distribution                                                            ( checked)
    # topic distribution contains the sorted list of topics in the required document
    
    #define constants******************************************
    subtraction_factor = 0
    multiplication_factor = 1000*len(topic_distribution)
    
    #topic_distribution = topic_distribution[:1]
    #print topic_distribution
    for topic in topic_distribution:
        fetch_doc_limit = len(topic_distribution)*2-subtraction_factor
        news_list = get_news_for_topic(topic[0],doc_id, fetch_doc_limit)
        for temp in news_list:
            #print temp.doc_num
            #print temp.__dict__['Topic'+str(topic[0])]
            
            date_diff =abs(( news_date - temp.date).days)
            date_factor = day_const*(days_range/(date_diff+100))
            
            doc_does_not_exist = True
            try:
                for newsitem in document_relevance:
                    if(newsitem[0]==temp.doc_num):
                        newsitem[2]+=temp.__dict__['Topic'+str(topic[0])]*multiplication_factor
                        doc_does_not_exist = False   
            except:
                document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic[0])]*multiplication_factor + date_factor))
            if(doc_does_not_exist==True):  
                document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic[0])]*multiplication_factor + date_factor))            
               
            #if((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic)]*multiplication_factor) not in news_list):
            #    document_relevance.append((temp.doc_num,temp.date,temp.__dict__['Topic'+str(topic)]*multiplication_factor))
        subtraction_factor+=2
        multiplication_factor-=1000
    document_relevance.sort(key=lambda tup: int(tup[2]))
    document_relevance.reverse()
    #print document_relevance    
    similarity_list = get_final_similarity(news_object ,document_relevance)
    similarity_decision_matrix = []
    #print similarity_list
    for item in similarity_list:
        similarity_decision_matrix.append((document_relevance[item[0]][0],document_relevance[item[0]][1],(document_relevance[item[0]][2]*100*item[1])/1000))
    similarity_decision_matrix.sort(key=lambda tup: int(tup[2]))
    similarity_decision_matrix.reverse()
    print similarity_decision_matrix
    articles = []
    for i in similarity_decision_matrix:
        filename = str(i[0])
        f = open('main/corpora/'+filename,'r')
        x = unicode(f.read(),errors='ignore')
        articles.append(x)
    data= { 'articles':articles} 
    # new document relevance list created
    #print topic_distribution
