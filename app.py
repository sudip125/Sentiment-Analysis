from flask import Flask,render_template,request
from googletrans import Translator
import googletrans
import pickle

#load the model from disk
bb = pickle.load(open('ML_model\\nlp_model.pkl','rb'))
#Load count vector from disk
cv = pickle.load(open('ML_model\\transform.pkl','rb'))

# This is dictionary of all languages of googletrans API 
all_language = googletrans.LANGUAGES

Translater = Translator()

app_1 = Flask(__name__)

@app_1.route('/')
def home():
    return render_template('index.html')

@app_1.route('/predict',methods=['POST'])
def predict():
    
    if request.method=='POST':
        review = request.form["review"]

        # Any language which is type in the HTML form translate into english
        review = Translater.translate(review)

        # To find which language the user is typing in the HTML form
        language = all_language[review.src].capitalize()

        # Extract English sentences which is translated by google Translater API
        data = [review.text]

        # Convert the sentence into numerical
        sentence = cv.transform(data).toarray()
        
        # predict the sentence
        review_prediction = bb.predict(sentence)
        
        return render_template('result.html',prediction=review_prediction,language=language)
    
if __name__=='__main__':
    app_1.run(debug=False,port=1000)

print(all_language)