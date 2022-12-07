import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from lxml import etree
from math import sqrt
import tkinter as tk
#traitement de requete
def traitement_requete(r):
    # Tokenization
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    keywords_with_stoplist = tokenizer.tokenize(r)
    tokens = [w.lower() for w in keywords_with_stoplist]

    # Elimination des mots vides
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in tokens if not w in stop_words]
    print('Keywords: ', keywords)

    # Normalisation
    lemmatizer = WordNetLemmatizer()
    lemmatised = [lemmatizer.lemmatize(word) for word in keywords]
    print('Lemmatised: ', lemmatised)

    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in lemmatised]
    print('Stemmed: ', stemmed)

    return stemmed

#vecteur dictionnairee : transoforme les mots cles de dictionnaire
# en un dict , avec les  keys = mots dict , key = 0
def vecteur_dictionnaire(chemin_dict):
    file = etree.parse(chemin_dict)
    root = file.getroot()
    final_dict = {}

    for child in root:
        final_dict[child.get('name')] = 0

    print("Vecteur dicionniare: \n", final_dict)
    return final_dict

#Cette fonction retourne le vecteur requête : les valeurs
#des mots clés de la requête sera modifié à 1
def vecteur_requete(vect_req, r):
    for k in vect_req.keys():
        if k in r:
            #modification du valeur si la condition est verifié
            vect_req[k] = 1

    print("Vecteur de la requete: \n", vect_req)
    return vect_req

#question5
def sim_req_docs(chemin_fichier_inverse, chemin_fichier_docs, vecteur_req):
    # Extraction des différents vecteurs à partir du fichier inverse dans une liste: vect_list
    vect_list = []
    root = etree.parse(chemin_fichier_inverse).getroot()
    docs_root = etree.parse(chemin_fichier_docs).getroot()
    doc_names = [w.get("name") for w in docs_root]
    for doc in doc_names:
        d = {}
        for child in root:
            name = child.get("name")
            for child1 in child:
                if child1.get("name") == doc:
                    d[name] = float(child1.text)
            if name not in d.keys():
                d[name] = 0
        vect_list.append(d)

    print("Liste des vecteurs: ")
    for v in vect_list:
        print(v)

    # Calcul de similarité entre les vecteurs documents et la requête
    sim_dict = {}
    for i in range(len(vect_list)):
        dic = vect_list[i]
        dv = list(dic.values())
        rv = list(vecteur_req.values())
        nom = sum([dv[i] * rv[i] for i in range(len(dic))])
        den = sqrt(sum([x ** 2 for x in dv]) * sum([y ** 2 for y in rv]))
        if den == 0:
            return False
        sim_dict["doc" + str(i + 1)] = nom / den

    print("Dicionnaire de similarite: ", sim_dict)
    return sim_dict

#question 6 tri selon les valeurs
def trie_documents(doc_sim):
    for k, v in sorted(doc_sim.items(), key=lambda x: x[1], reverse=True):
        print(k)
    return  sorted(doc_sim.items(), key=lambda x: x[1], reverse=True)


#main_function()

def main():
    # creation de  Top level window
    frame = tk.Tk()
    frame.title("indexation gui")
    #le choix du fentre et les dimensions
    frame.geometry('640x480')


    def printInput():
         #input de requete
        inp = inputtxt.get(1.0, "end-1c")
        lbl = tk.Label(frame, text="results are :")
        lbl.config(text="Provided Input: provided " + inp)
         #traitement de requete
        normalized = traitement_requete(inp)
        vect_dict = vecteur_dictionnaire("dictionnaire.xml")
        vect_req = vecteur_requete(vect_dict, normalized)
        doc_sim = sim_req_docs("inverse_final.xml", "docs.xml", vect_req)
        if not doc_sim:
            lbl.config(text="pas de resultat  "  + inp)
            lbl.pack()
        else:
            ls = trie_documents(doc_sim)
            lbx = tk.Listbox(frame)
            for i in  range(len(ls)) :
                lbx.insert(i,ls[i])
            lbx.pack()
            lbl.pack()
    inputtxt = tk.Text(frame, height=3)
    inputtxt.pack()
    printButton = tk.Button(frame, text="search", command=printInput)
    printButton.pack()
    frame.mainloop()
main()

                                                                                     

                                                                                     



























