import datetime
from gensim import corpora, models, similarities
from main.models import news
import nltk

dictionary = corpora.Dictionary.load('btp.dict')

corpus = corpora.MmCorpus('btp.mm')

lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary,num_topics=100,passes=5)
print lda.show_topics(topics=-1)
corpus_lda = lda[corpus]


i = 1
	
def extract_entity_names(t):
	entity_names = []
    
    	if hasattr(t, 'node') and t.node:
        	if t.node == 'NE':
            		entity_names.append(' '.join([child[0] for child in t]))
        	else:
            		for child in t:
                		entity_names.extend(extract_entity_names(child))
                
    	return entity_names
    
i=1 	
for doc in corpus_lda:
	if i<=4377:
		i=i+1
		continue
	
 	filename = str(i)
 	f = open('main/corpora/'+filename,'r')
 	x = unicode(f.read(),errors= 'ignore')
 	p = x[:10]
 	text = x[13:]
 	if(p[9]=='|'):
 		p=p[:8]
 		text=x[11:]
 	elif(p[9]==';'):
 		p=p[:9]
 		text = x[12:]
 	
 	entity_names = []
 	
 	sentences = nltk.word_tokenize(text)
 	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=True)
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))
	x =  list(set(entity_names))
	x = ';'.join(x)	
 	
 	d = datetime.datetime.strptime(p,"%d-%m-%Y")
 	obj = news.objects.create(doc_num=i,doc_text = text,doc_entity_set=x, date=d)
 	for entity in doc:
 		obj.__dict__['Topic'+str(entity[0])] =  entity[1]
 	obj.save()
 	i = i+1
