import numpy as np

class document:
    def __init__(self,txt,n):
        self.txt = txt
        self.plain_index = np.zeros(n)
        self.rand_p_1 = np.zeros(n)
        self.rand_p_2 = np.zeros(n)

    def create_final_index(self,m1,m2):
        #self.index_1 = np.dot(self.rand_p_1,m1)
        #self.index_2 = np.dot(self.rand_p_2,m2)
        self.index_1 = np.dot(np.transpose(m1),self.rand_p_1)
        self.index_2 = np.dot(np.transpose(m2),self.rand_p_2)
    

class Person:
    def __init__(self,n,m1,m3,s,vocab) -> None:
        self.m1 = np.random.randint(1,200,(n,n))
        self.m2 = np.random.randint(1,200,(n,n))
        self.s = s
        self.vocabs = vocab

class Owner(Person):
    def __init__(self,vocab,documents: list[document]) -> None:
        n= len(vocab)
        m1 = np.random.randint(1,10,(n,n))
        m2 = np.random.randint(1,10,(n,n))
        s = np.random.choice([0,1],n)
        self.documents = documents
        Person.__init__(self,n,m1,m2,s,vocab)

    def prepare_documents(self):
        #self.doc_vocab_pair = {}
        for doc in self.documents:
            #self.doc_vocab_pair[doc] = np.zeros(len(self.vocabs))
            for pos,vocab in enumerate(self.vocabs):
                if vocab in doc.txt:
                    #self.doc_vocab_pair[doc][pos] = 1
                    doc.plain_index[pos] = 1

    def create_documents_index(self):
        rand_p_1 = np.zeros(len(self.s)) 
        rand_p_2 = np.zeros(len(self.s))
        #print(self.s)
        for doc in self.documents:
            for pos,value in enumerate(self.s):
                if(value) == 0:
                    doc.rand_p_1[pos] = doc.plain_index[pos]
                    doc.rand_p_2[pos] = doc.plain_index[pos]
                else:
                    if doc.plain_index[pos] == 1:
                        rand = np.random.dirichlet(np.ones(2),size=1)
                        doc.rand_p_1[pos] = rand[0][0]
                        doc.rand_p_2[pos] = rand[0][1]
                    else:
                        doc.rand_p_1[pos] = np.random.randint(1,200)
                        doc.rand_p_2[pos] = -doc.rand_p_1[pos]

class User(Person):
    def __init__(self,vocab,m1,m2,s) -> None:
        self.m1 = m1
        self.m2 = m2
        self.q_1 = np.zeros(len(s))
        self.q_2 = np.zeros(len(s))
        self.s = s
        self.query_voab = vocab
        self.query_voab_index = np.zeros(len(s))

    def setup_query_vocab(self,desired_vocab):
        for desire in desired_vocab:
            self.query_voab[desire] =1

    def generate_query_index(self):
        for pos,value in enumerate(self.s):
                if(value) == 0:
                    self.q_1[pos] = self.query_voab_index[pos]
                    self.q_2[pos] = self.query_voab_index[pos]
                else:
                    if self.query_voab_index[pos] == 1:
                        rand = np.random.dirichlet(np.ones(2),size=1)
                        self.q_1[pos] = rand[0][0]
                        self.q_2[pos] = rand[1][1]
                    else:
                        self.q_1[pos] = np.random.randint(1,200)
                        self.q_2[pos] = -self.q_1[pos]

    def create_final_index(self):
        self.index_1 = np.dot(self.m1,self.q_1)
        self.index_2 = np.dot(self.m2,self.q_2)
    

                    
class Server:
    def __init__(self,documents: list[document]) -> None:
        self.documents = documents

    def search(self,index_1,index_2):
        score_dic = dict.fromkeys(self.documents,0)
        for doc in self.documents:
            score_dic[doc] = (np.dot(index_1,doc.index_1) + np.dot(index_2,doc.index_2))
        
        #for key in score_dic:
           #print(key.txt,score_dic[key])

        for k, v in sorted(score_dic.items(), key=lambda item: item[1]):
            print(k.txt,v)



        