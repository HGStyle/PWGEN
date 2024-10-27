import flask
import json
import random
import os

app = flask.Flask('')

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def pwgen(gentype):
    password = ""

    # Get the language names
    langnames_path = os.path.join("data", "langnames.json")
    with open(langnames_path, 'r', encoding='utf-8') as file:
        langnames = json.load(file)

    if gentype in langnames:
        # Get a random order of words
        orders_path = os.path.join("data", "orders.json")
        with open(orders_path, 'r', encoding='utf-8') as file:
            orders = json.load(file)
        order = random.choice(orders)

        # Get a random word of each word type
        for wordtype in order:
            if wordtype == "pron":
                pron = load_data(os.path.join("data", gentype, "pron.txt"))
                password += random.choice(pron) + " "
            elif wordtype == "noun":
                noun = load_data(os.path.join("data", gentype, "noun.txt"))
                password += random.choice(noun) + " "
            elif wordtype == "adj":
                adj = load_data(os.path.join("data", gentype, "adj.txt"))
                password += random.choice(adj) + " "
            elif wordtype == "verb":
                verb = load_data(os.path.join("data", gentype, "verb.txt"))
                password += random.choice(verb) + " "

    elif gentype == "syllab":
        # Load the syllabs
        syllabs = load_data(os.path.join("data", "syllabs.txt"))

        # Generate the password
        iterations = random.randint(4, 8)
        password = ''.join(random.choice(syllabs) for _ in range(iterations))

    return password.strip()

@app.route('/')
def index():
    gentype = flask.request.args.get('type')
    dynamichtml = '<h1>PWGEN by HGStyle</h1><br><h2>Select the type of password to generate</h2>'
    if gentype:
        dynamichtml = '''
                                <h1>''' + pwgen(gentype) + '''</h1>
                                <h2>might be your new password... <a href="?type=''' + gentype + '''">Or not?</a></h2>
                                <br><h3>Change password type</h3>'''
    return '''<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>PWGEN - Generate a random, secure and easy-to-remember password!</title>
            </head>
            <body>
                ''' + dynamichtml + '''
                <a href="?type=english">Passphrase in English</a><br>
                <a href="?type=french">Phrase de passe en Français</a><br>
                <a href="?type=german">Passphrase auf Deutsch</a><br>
                <a href="?type=polish">Hasło w języku polskim</a><br>
                <a href="?type=spanish">Frase de paso en Español</a><br>
                <a href="?type=syllab">Password made out of syllabs (beta)</a><br>
            </body>
            <style>
                body {
                    margin-left: 20%;
                    margin-top: 5%;
                    font-family: sans-serif;
                    font-size: 125%;
                    color: dimgray;
                    background-color: whitesmoke;
                }
            </style>
        </html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
