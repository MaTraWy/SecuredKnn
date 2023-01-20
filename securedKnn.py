import numpy as np
"""
    Code Author: @Mahmoud Srewa
    PhD student,  Computer Science Departement, the university of Alabama.
    Written in Alsharif Labs - the university of Alabama
"""
class document:
    """
    A class that represents the documents that are assumed to be hosted on a server
    So it will have the encrypted index (a vector that represents the vocabulary in this document).
    """ 
    def __init__(self,txt,n):
        self.txt = txt
        # the plain index of a given document that is not encrypted, assume it not with server 🤣
        self.plain_index = np.zeros(n)

        # the splited two index of document , assume also it is not with the server 🤣🤣
        self.rand_p_1 = np.zeros(n)
        self.rand_p_2 = np.zeros(n)

    def create_final_index(self,m1,m2):
        """
        this method calculate final encrypted indexs 👩‍💻
        arguments:
            m1,m2: secret key of the owner that used to create the encrypted index
        return:
           No-Return, only create a new two encrypted index   encrypted_index_1 & 2
        """
        #self.index_1 = np.dot(self.rand_p_1,m1)
        #self.index_2 = np.dot(self.rand_p_2,m2)

        # here the splited index that is with the server
        self.encrypted_index_1 = np.dot(np.transpose(m1),self.rand_p_1)
        self.encrypted_index_2 = np.dot(np.transpose(m2),self.rand_p_2)
    

class Person:
    """
    a parent class that represents both trusted entities (a user and owner),
    Create this class to avoid duplicating code, as they both share some functions and attributes.
    """ 
    def __init__(self,n,m1,m3,s,vocab) -> None:
        self.m1 = np.random.randint(1,200,(n,n))
        self.m2 = np.random.randint(1,200,(n,n))
        self.s = s
        self.vocabs = vocab

class Owner(Person):
    """
    Owner class contains methods that only used by an owner of a docuemnts (Admin)
    """ 
    def __init__(self,vocab,documents: list[document]) -> None:
        """
        arguments:
           vocab: set of vocab that we do search with, we only can search through
           documents: set of documents that are going to be uploaded to a server
        """
        n= len(vocab)
        
        #here generating both random key matrix m1,m2.
        m1 = np.random.randint(1,10,(n,n))
        m2 = np.random.randint(1,10,(n,n))
        #here generating the S binary matrix which is used as a spliting index.
        s = np.random.choice([0,1],n)
        self.documents = documents
        Person.__init__(self,n,m1,m2,s,vocab)

    def prepare_documents(self):
        """
        this method calculate plain index for each document
        return:
           No-Return, only generate the plain index in each document.
        """
        
        #loop over every doc
        for doc in self.documents:
            #here we loop over enumerated vocab, to have index of each vocab
            for pos,vocab in enumerate(self.vocabs):
                if vocab in doc.txt:
                    #If a match occurs with vocabulary, update the corresponding plain text index. 
                    doc.plain_index[pos] = 1

    def create_documents_index(self):
        """
        this method calculate the splited two index for each document
        for each document:
            1- loop over enumerated
                - if s[i] =0 then the two value of splited index at i is eqall to value of 
                    plain index at i
                - if s[i] =1 then we check the value of plain index at i
                    - if plainIndex[i] == 1
                        then generate two random number for both splited index where their sum is 1
                    - if plainIndex[i] == 0
                        then generate two random number for both splited index where their sum is 0  
        return:
           No-Return, only generate the splited index of each document.
        """
        #looping over each document
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
    """
    The User class contains methods that are only used by users, such as initiating query indexes. 
    """ 
    def __init__(self,vocab,m1,m2,s) -> None:
        """
        arguments:
            Vocabulary: a collection of words that we can only search through.
            s:          the splitting factor, which must be the same as the admin person.
            m1, m2:     This is the inverse transposition of the admin person's m1 and m2. 
        """
        self.m1 = m1
        self.m2 = m2

        #intializaing the split index for the query
        self.q_1 = np.zeros(len(s))
        self.q_2 = np.zeros(len(s))
        self.s = s
        self.query_voab = vocab

        #plain query index
        self.query_voab_plain_index = np.zeros(len(s))

    def setup_query_vocab(self,desired_vocab):
        """
        this method construct the query index
        arguments:
            desired_vocab: the query's search vocabulary 
        return:
           No-Return, only generate the query index
        """
        for desire in desired_vocab:
            self.query_voab_plain_index[desire] =1

    def generate_query_index(self):
        """
        this method calculate the splited two index for query

        loop over enumerated s
                - if s[i] = 1 then the two value of splited index at i is eqall to value of 
                    plain index at i
                - if s[i] = 0 then we check the value of plain index at i
                    - if plainIndex[i] == 1
                        then generate two random number for both splited index where their sum is 1
                    - if plainIndex[i] == 0
                        then generate two random number for both splited index where their sum is 0  
        return:
           No-Return, only generate the splited index for the query
        """
        for pos,value in enumerate(self.s):
                if(value) == 1:
                    self.q_1[pos] = self.query_voab_plain_index[pos]
                    self.q_2[pos] = self.query_voab_plain_index[pos]
                else:
                    if self.query_voab_plain_index[pos] == 1:
                        rand = np.random.dirichlet(np.ones(2),size=1)
                        self.q_1[pos] = rand[0][0]
                        self.q_2[pos] = rand[0][1]
                    else:
                        self.q_1[pos] = np.random.randint(1,200)
                        self.q_2[pos] = -self.q_1[pos]

    def create_final_index(self):
        """
        this method calculate final encrypted indexs 👩‍💻
        return:
           No-Return, only create a new two encrypted index   encrypted_index_1 & 2
        """
        self.encrypted_index_1 = np.dot(self.m1,self.q_1)
        self.encrypted_index_2 = np.dot(self.m2,self.q_2)
    

                    
class Server:
    """
    The Server class contains the query processing method, and return the matched documents
    """ 
    def __init__(self,documents: list[document]) -> None:
        self.documents = documents

    def search(self,index_1,index_2):
        """
            This method constructs a dictionary where a key is a document and a value is the score from applying the search, then returns the high score.

        arguments:
            index_1,index_2: the query search splited index
        return:
           No-Return, only return the matched documents
        """
        score_dic = dict.fromkeys(self.documents,0)
        for doc in self.documents:
            #score calcualtion from multiplaying the the splited index of query with splited index of query
            score_dic[doc] = (np.dot(index_1,doc.encrypted_index_1) + np.dot(index_2,doc.encrypted_index_2))
        
        #for key in score_dic:
           #print(key.txt,score_dic[key])

        for k, v in sorted(score_dic.items(), key=lambda item: item[1],reverse=True):
            print(k.txt,np.round(v, 2))



        