from utils import generate_random_start, generate_from_seed
from keras.models import load_model
import tensorflow as tf
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField, DecimalField, IntegerField

# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = TextField("Please Enter a word, for example 'machine':", validators=[
                     validators.InputRequired()])

    # Number of words
    words = IntegerField('Enter number of words to generate:',
                         default=50, validators=[validators.InputRequired(),
                                                 validators.NumberRange(min=10, max=100, message='Number of words must be between 10 and 100')])
    # Submit button
    submit = SubmitField("Enter")


def load_keras_model():
    """Load in the pre-trained model"""
    global model
    model = load_model('../models/train-embeddings-rnn-2-layers.h5')
    # Required for model to work
    #global graph
    #graph = tf.compat.v1.get_default_graph()
    #graph = tf.get_default_graph()


# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        #diversity = float(request.form['diversity'])
        diversity=0.8
        words = int(request.form['words'])
        # Generate a random sequence

        #return render_template('seeded.html', input=generate_from_seed(model=model, graph=graph, seed=seed, new_words=words, diversity=diversity))
        return render_template('seeded.html',input=generate_from_seed(model=model, seed=seed, new_words=words,
                                                            diversity=diversity))
    # Send template information to index.html
    return render_template('index.html', form=form)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=80)
