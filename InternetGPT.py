import requests
from googlesearch import search
from readability import Document
from bs4 import BeautifulSoup
from hugchat import hugchat
from hugchat.login import Login
from Url_text_extractor import *
from HuggingChat import huggingface_chatbot,huggingface_chatbot_2
import re
import html
import time

def extract_answer(text):
    # Utilise une expression régulière pour trouver toutes les chaînes entre ** et les stocker dans une liste
    matches = re.findall(r'\*\*(.*?)\*\*', text)
    
    # Rejoint les chaînes extraites en une seule chaîne
    extracted_text = ' '.join(matches)
    
    return extracted_text

def delete_spaces(texte):
    mots = texte.split()  # Divise le texte en mots
    texte_sans_espaces_inutiles = ' '.join(mots)  # Réassemble les mots sans espaces inutiles
    return texte_sans_espaces_inutiles

def web_GPT(query):
    # Étape 1: Prendre une question en entrée
    question = query

    # Étape 2: Transformer la question en mots-clés de recherche avec Hugging Face Chatbot
    #prompt1="Donne moi un unique groupe de mot clefs exhaustifs et en nombre suffisant, permettant de faire une recherche google qui me permettrait de répondre de la question: "
    prompt1="Please provide a comprehensive set of at most five keywords in french that would allow me to perform an internet search to answer the question: "
    #prompt2=" Répond en mettant ce groupe de mots clefs entre 2 double étoiles **."
    prompt2="Respond by placing this set of keywords between 2 double asterisks like this ** keywords **."
    response = huggingface_chatbot(prompt1+str(question)+prompt2,value=1)
    print("Keyword Response: ",response)
    keywords = extract_answer(response).split()
    print("Keywords extracted !")
    print(keywords)

    # Étape 3: Obtenir les URLs pertinantes
    relevant_urls = search_urls_by_keywords(keywords, num_results=3)
    print("Relevant Urls found !")
    print(relevant_urls)

    # Étape 4: Extraire le texte de chaque URL sélectionnée
    extracted_texts = []
    k=0
    for url in relevant_urls:
        extracted_text = extract_text_from_url(url)[0:10000]
        max_length = 5000  # Par exemple, vous pouvez ajuster cette valeur

        # Divisez le texte en morceaux de longueur maximale
        text_segments = [extracted_text[i:i + max_length] for i in range(0, len(extracted_text), max_length)]

        for i, segment in enumerate(text_segments):
            extracted_texts.append(delete_spaces(segment))
            print("SEGMENT:", delete_spaces(segment))

        #print("Segment " + str(i + 1) + ":")
        #print(segment)
        #extracted_texts.append(extracted_text)

            k+=1
            print("Extracted text "+str(k)+ " from url.")
        
    print("Length of extracted text lists:",len(extracted_texts))
    # Étape 5: Obtenir une réponse distincte à la question pour chaque texte extrait
    responses = []
    prompt3="Répond  de manière succinte et instructive à la question suivante: ** "
    prompt4="**. Tu répondra en te basant uniquement sur le contexte suivant, sans utiliser tes connaissances apprises: ** start of context: ** "  #sans utiliser tes connaissances apprises:
    complete_prompts=[prompt3+question+prompt4+text for text in extracted_texts]
    responses = huggingface_chatbot_2(complete_prompts,1)[0] #[0] car c'est un tuple !!
    print("Answers generated !")
    print("Responses 2:",responses)
    print("NOMPBRE DE REP:",len(responses))
    
       

    # Étape 6: Synthétiser les différentes réponses en une seule
    final_response = ''
    for index,j in enumerate(responses):
        final_response+=(' * REPONSE '+str(index)+': '+str(j))   #.replace('<|endoftext|>',''))
    print("SUM OF RESPONSES:",final_response)
    print("Lenght of final respo",len(final_response))
    prompt6="Répond à la question: "
    prompt5="** En synthétisant une réponse à partir des différentes réponses suivantes, sans utiliser tes connaissances apprises: ** "
    print("Synthétising final answer")
    try:
        synthesis = huggingface_chatbot(prompt6+query+prompt5+str(final_response)+ "**",1)
    except:
        time.sleep(3)
        try:
            synthesis = huggingface_chatbot(prompt6+query+prompt5+str(final_response)+ "**",1)
        except:
            return("Une erreur s'est produite, impossible de donner la réponse !")
    print("Réponse finale :")
    print(synthesis)
    return(synthesis)

if __name__ == "__main__":
    web_GPT("Qu'est ce que le modèle llama2-70b-hf ?")
