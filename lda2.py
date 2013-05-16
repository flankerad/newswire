from gensim import corpora, models, similarities
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#get the dictionary which we created earlier
dictionary = corpora.Dictionary.load('../generated/btp.dict')

# load the corpus we stored in matrix market format earlier
corpus = corpora.MmCorpus('../generated/btp.mm')

# apply LDA and extract topics out of it.

lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary,num_topics=100,passes=2)
#array = lda.show_topics(200)
#for i in range(0,200):
#	print "topic "+str(i)+" "+array[i]

print lda.show_topics(topics=-1)

corpus_lda = lda[corpus]
for doc in corpus_lda:
	print doc

