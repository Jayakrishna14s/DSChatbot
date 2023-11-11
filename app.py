from flask import Flask, render_template, request, jsonify
import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')
# app = Flask(__name__, template_folder='html/templates')

def response(user_input):
  robo_response = ''
  sent_tokens.append(user_input)
  TfidfVec = TfidfVectorizer(tokenizer = LemNormalize,stop_words='english')
  tfidf = TfidfVec.fit_transform(sent_tokens)
  
  vals = cosine_similarity(tfidf[-1],tfidf)
  idx = vals.argsort()[0][-2]
  """ numpy.argsort() function is used to perform an indirect sort along the 
  given axis using the algorithm specified by the kind keyword. It returns an 
  array of indices of the same shape as arr that that would sort the array."""

  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]

  if(req_tfidf == 0):
    robo_response = robo_response + "I am sorry! I don't understand you"
    return robo_response
  else:
    robo_response = robo_response + sent_tokens[idx]
    return robo_response
f = open('chatbot.txt','r',errors='ignore')

raw = f.read()
# raw = raw.lower() # convert all characters to lower case

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw) # converts raw to a list of sentences
word_tokens = nltk.word_tokenize(raw) # converts raw to a list of words

# WordNetLemmatizer is a semantically-oriented dictionary of english included in NLTK
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation) # string.punctuation will give the all sets of punctuation.(see code below)
"""The ord() function in Python accepts a string of length 1 as an argument 
and returns the unicode code point representation of the passed argument. 
For example ord('B') returns 66 which is a unicode code point value of 
character 'B'."""
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

Greeting_input = ("hello", "hi", "greetings", "sup", "what's up","hey",)
Greeting_response = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
  for word in sentence.split():
    if word.lower() in Greeting_input:
      return random.choice(Greeting_response)
# flag = True
# print("ROBO: My name is ROBO. I will answer your queries about Chatbots. If you want to exit, type Bye!")

# while(flag == True):
#   user_response = input()
#   user_response = user_response.lower()
#   if(user_response != 'bye!'):
#     if user_response == 'thanks' or user_response == 'thank you':
#       flag = False
#       print("ROBO: You are welcome...!")
#     else:
#       if greeting(user_response) != None:
#         print("ROBO: ",greeting(user_response))
#       else:
#         print("ROBO: ",end="")
#         print(response(user_response))
#         sent_tokens.remove(user_response)
#   else:
#     flag = False
#     print("ROBO: Bye! Take Care ...")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    chatbot_response = response(user_input) 
    return jsonify({'response': chatbot_response})  

if __name__ == '__main__':
    app.run(debug=True)