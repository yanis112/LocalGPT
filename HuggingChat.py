from hugchat import hugchat
from hugchat.login import Login
import concurrent.futures
import time

def huggingface_chatbot(prompt_str,value=1):
    # Définissez vos variables ici (email, mot de passe, etc.)
    email = 'PUT YOUR HUGGING FACE EMAIL HERE'
    
    passwd = 'PUT YOUR HUGGING FACE PASSWORD HERE'

    # Log in to Hugging Face et accordez l'autorisation à HuggingChat
    sign = Login(email, passwd)
    cookies = sign.login()

    # Sauvegardez les cookies dans le répertoire local
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    # Créez un ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    chatbot.switch_llm(value) 

    # Vous pouvez maintenant utiliser chatbot pour interagir avec le modèle
    response = chatbot.chat(prompt_str)
    
    # Renvoyez la réponse au format str
    return str(response)



def huggingface_chatbot_2(prompts,value=1):
    # Définissez vos variables ici (email, mot de passe, etc.)
    email = 'PUT YOUR HUGGING FACE EMAIL HERE'
    
    passwd = 'YPUT YOUR HUGGING FACE PASSWORD HERE'

    # Log in to Hugging Face et accordez l'autorisation à HuggingChat
    sign = Login(email, passwd)
    cookies = sign.login()

    # Sauvegardez les cookies dans le répertoire local
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    # Créez un ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    chatbot.switch_llm(value)
    # Create a new conversation #RAJOUTE RECEMMENRT
    #id = chatbot.new_conversation()
    #chatbot.change_conversation(id)

    # Fonction pour interagir avec le modèle
    def chat_with_bot(prompt):
        response = chatbot.chat(prompt)
        return str(response)

    # Mesure du temps de début
    start_time = time.time()

    # Utilisez un ThreadPoolExecutor pour exécuter les requêtes en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Lancez les appels parallèles pour chaque prompt dans la liste
        results = list(executor.map(chat_with_bot, prompts))

    # Mesure du temps de fin
    end_time = time.time()

    # Calcul du temps total d'exécution
    total_time = end_time - start_time

    return results, total_time

# Exemple d'utilisation :
if __name__ == "__main__":
    prompts = ["Qui est Barack Obama ?", "Qui est Donald Trump ?", "Qui est Bill Clinton ?"]


    start_time=time.time()
    response = huggingface_chatbot(prompts[0])
    print(response)
    end_time=time.time()
    print("simple prompt time: "+str(end_time-start_time))
    # Mesure du temps pour répondre en parallèle
    responses_parallel, execution_time_parallel = huggingface_chatbot_2(prompts)
    print("Réponses en parallèle :", responses_parallel)
    print("Temps d'exécution en parallèle :", execution_time_parallel, "secondes")

    # Mesure du temps pour répondre l'un après l'autre
    responses_sequential = []
    start_time_sequential = time.time()
    for prompt in prompts:
        response = huggingface_chatbot(prompt)
        responses_sequential.append(response)
    end_time_sequential = time.time()
    execution_time_sequential = end_time_sequential - start_time_sequential

    #print("Réponses l'une après l'autre :", responses_sequential)
    print("Temps d'exécution l'un après l'autre :", execution_time_sequential, "secondes")


# Exemple d'utilisation de la fonction
#if __name__ == "__main__":
#    prompt = "Donne moi un unique groupe de mot clefs permettant de faire une recherche google qui me permettrait de répondre de la question: Quel est le bilan politique de Donlad Trump. Répond en mettant ce groupe de mots clefs entre 2 double étoiles ** "
    #response = huggingface_chatbot(prompt)
#    response=huggingface_chatbot_2(["Qui est BArack obama ?","Qui est donald trump ?", "Qui est Bill clinton ?"])
#    print(response)
