import logging
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import re

documents = []
# read the news articles from corpus
for i in range(1,8975):
	filename = str(i)
	f = open('../corpora/'+filename,'r')
	x = unicode(f.read(),errors='ignore')
	p= x.replace('[','').replace(']','').replace('.',' ').replace(',','').replace('(','').replace(')','').replace('\'','')
	p = p.replace(':','').replace('-',' ').replace('\"',' ').replace(';','')
	p = p[10:]
	p = re.sub("\d+", "", p)
	documents.append(p)
# // read files 


# stoplist  .. TODO : how are we deciding the stoplist is good or bad for us

stoplist = set(', " 2008 2009 2010 2012 2011 a asked as b c d e f g h i j K L m n o p q r s t u v w x y z mr ms mrs able about above according accordingly across actually shri dr after afterwards again against aint all allow allows almost alone along already also although always am among amongst an and another any anybody anyhow anyone anything anyway anyways anywhere apart appear appreciate appropriate are arent around as aside ask asking associated at available away awfully b be became because become becomes becoming been before beforehand behind being believe below beside besides best better between beyond both brief but by c cmon cs came can cant cannot cant cause causes certain certainly changes clearly co com come comes concerning consequently consider considering contain containing contains corresponding could couldnt course currently d definitely described despite did didnt different do does doesnt doing dont done down downwards during e each edu eg eight either else elsewhere enough entirely especially et etc even ever every everybody everyone everything everywhere ex exactly example except f far few fifth first five followed following follows for former formerly forth four from further furthermore g get gets getting given gives go goes going gone got gotten greetings h had hadnt happens hardly has hasnt have havent having he hes hello help hence her here heres hereafter hereby herein hereupon hers herself hi him himself his hither hopefully how howbeit however i id ill im ive ie if ignored immediate in inasmuch inc indeed indicate indicated indicates inner insofar instead into inward is isnt it itd itll its its itself j just k keep keeps kept know knows known l last lately later latter latterly least less lest let lets like liked likely little look looking looks ltd m mainly many may maybe me mean meanwhile merely might more moreover most mostly much must my myself n name namely nd near nearly necessary need needs neither never nevertheless new next nine no nobody non none noone nor normally not nothing novel now nowhere o obviously of off often oh ok okay old on once one ones only onto or other others otherwise ought our ours ourselves out outside over overall own p particular particularly per perhaps placed please plus possible presumably probably provides q que quite qv r rather rd re really reasonably regarding regardless regards relatively respectively right s said same saw say saying says second secondly see seeing seem seemed seeming seems seen self selves sensible sent serious seriously seven several shall she should shouldnt since six so some somebody somehow someone something sometime sometimes somewhat somewhere soon sorry specified specify specifying still sub such sup sure t ts take taken tell tends th than thank thanks thanx that thats thats the their theirs them themselves then thence there theres thereafter thereby therefore therein theres thereupon these they theyd theyll theyre theyve think third this thorough thoroughly those though three through throughout thru thus to together too took toward towards tried tries truly try trying twice two u un under unfortunately unless unlikely until unto up upon us use used useful uses using usually uucp v value various very via viz vs w want wants was wasnt way we wed well were weve welcome well went were werent what whats whatever when whence whenever where wheres whereafter whereas whereby wherein whereupon wherever whether which while whither who whos whoever whole whom whose why will willing wish with within without wont wonder would would wouldnt x y yes yet you youd youll youre youve your yours yourself yourselves z zero'.split())


#/**************************************** PROCESSING STARTS ***********************************************************************


# remove all the stopwords from the news articles

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
all_tokens = sum(texts,[])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
#print tokens_once
texts = [[word for word in text if word not in tokens_once] for text in texts]
#print texts
# texts contains the array of tokens out of all the news articles.. 

dictionary = corpora.Dictionary(texts)
dictionary.save('../generated/btp.dict')
#print dictionary.token2id

corpus = [dictionary.doc2bow(text) for text in texts]
# store corpus in a serialized manner in matrix market format 
corpora.MmCorpus.serialize('../generated/btp.mm',corpus)
