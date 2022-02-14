import pymongo
from flask import Flask, render_template, request, url_for, redirect, session

import bcrypt
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://ClaudioS:ProTech21!@studytogheterdb.dzubs.mongodb.net/StudyTogheterDB?retryWrites=true&w=majority")
db = client.get_database('StudyTogheterDB')
Utenti = pymongo.collection.Collection(db, 'Studenti')
Esami = pymongo.collection.Collection(db, 'Esami')
StudentiEsami = pymongo.collection.Collection(db, 'StudentiEsami')
StudentiIncontri = pymongo.collection.Collection(db, 'StudentiIncontri')
Incontridb = pymongo.collection.Collection(db, 'Incontri')
esame = []
incontro = []

@app.route('/')
def index():  # put application's code here
    return render_template('PaginaPrincipale.html')
@app.route('/Home')
def Home():  # put application's code here
    return render_template('PaginaPrincipale.html')
@app.route('/Chi Siamo')
def ChiSiamo():  # put application's code here
    return render_template('ChiSiamo.html')
@app.route('/Servizi')
def Servizi():  # put application's code here
    return render_template('Servizi.html')
@app.route('/Contatti')
def Contatti():  # put application's code here
    return render_template('Contatti.html')

@app.route('/Studiamo')
def Studiamo():  # put application's code here
    if "Username" in session:
        esame.clear()
        email = session["Username"]
        listaesami = StudentiEsami.find()
        for x in listaesami:
            if (x['Unito'] == True):
                if (x['Studente'] == email):
                    y = Esami.find_one({'Nome_esame': x['Esame']})
                    esame.append(y)
        return render_template('Studiamo.html', email=email, esame=esame)
    else:
        return redirect(url_for("Login"))


@app.route('/Unisciti')
def Unisciti():  # put application's code here
    if "Username" in session:
        esame.clear()
        email = session["Username"]
        listaesami = StudentiEsami.find()
        for x in listaesami:
            if (x['Unito'] == False):
                if (x['Studente'] == email):
                    y = Esami.find_one({'Nome_esame': x['Esame']})
                    esame.append(y)
        return render_template('Unisciti.html', email=email, esame=esame)
    else:
        return redirect(url_for("Login"))


@app.route('/Login', methods=['post','get'])
def Login():
        message = 'Please login to your account'
        if "Username" in session:
            return redirect(url_for("Studiamo"))

        if request.method == "POST":
            email = request.form.get("Username")
            password = request.form.get("password")

            email_found = Utenti.find_one({"_id": email})
            if email_found:
                email_val = email_found['_id']
                pwcheck = email_found['Password']
                if pwcheck == password:
                    session["Username"] = email_val
                    return redirect(url_for('Studiamo'))
                else:
                    if "Username" in session:
                        return redirect(url_for("Studiamo"))
                    message = 'Wrong password'
                    return render_template('Login.html', message=message)
            else:
                message = 'Email not found'
                return render_template('Login.html', message=message)
        return render_template('Login.html', message=message)

@app.route('/Registrazione', methods=['post','get'])
def Registrazione():
        if "Username" in session:
            return redirect(url_for("Studiamo"))
        if request.method == "POST":
            user = request.form.get("Username")
            email = request.form.get("email")

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            user_found = Utenti.find_one({"_id": user})
            email_found = Utenti.find_one({"Email": email})
            if user_found:
                message = 'Username già utilizzato'
                return render_template('Registrazione.html', message=message)
            if email_found:
                message = 'Email già utilizzata'
                return render_template('Registrazione.html', message=message)
            if password1 != password2:
                message = 'Le password non corrispondono!'
                return render_template('Registrazione.html', message=message)
            else:
                user_input = {'_id': user, 'Email': email, 'Password': password1}
                Utenti.insert_one(user_input)

                user_data = Utenti.find_one({"_id": user})
                new_user = user_data['_id']
                session['Username'] = new_user

                listaEsami = Esami.find()
                for x in listaEsami:
                    NewStudenteEsame = {'Studente': new_user, 'Esame': x['Nome_esame'], 'Unito': False}
                    StudentiEsami.insert_one(NewStudenteEsame)

                listaIncontri = Incontridb.find()
                for x in listaIncontri:
                    NewStudenteIncontro = {'Studente': new_user, 'Incontro': x['_id'], 'Unito': False}
                    StudentiIncontri.insert_one(NewStudenteIncontro)

                return render_template('Studiamo.html', email=new_user)
        return render_template('Registrazione.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
     session.pop("Username", None)
     return render_template("PaginaPrincipale.html")

@app.route("/Esame/<string:esame>")
def Esame(esame):
    if "Username" in session:
        incontro.clear()
        email = session["Username"]
        listaincontro = StudentiIncontri.find()
        for x in listaincontro:
            if (x['Unito'] == True):
                if (x['Studente'] == email):
                    y = Incontridb.find_one({'_id': x['Incontro']})
                    if (y['EsameApp'] == esame):
                        incontro.append(y)
        return render_template('Esame.html', esame=esame, email=email, incontro=incontro)
    else:
        return redirect(url_for("Login"))

@app.route('/Incontri/<string:esame>', methods=["POST", "GET"])
def Incontri(esame):
    if "Username" in session:
        incontro.clear()
        email = session["Username"]
        listaincontro = StudentiIncontri.find()
        for x in listaincontro:
            if (x['Unito'] == False):
                if (x['Studente'] == email):
                    y = Incontridb.find_one({'_id': x['Incontro']})
                    if(y['EsameApp'] == esame):
                        incontro.append(y)
        return render_template('Incontri.html', esame=esame, email=email, incontro=incontro)
    else:
        return redirect(url_for("Login"))

@app.route("/Materiale/<string:esame>")
def Materiale(esame):
    return render_template('Materiale.html', esame=esame)

@app.route("/Unisci/<string:esame>", methods=["POST", "GET"])
def Unisci(esame):
    email = session["Username"]
    db.StudentiEsami.update_one({"Esame": esame, "Studente": email}, {"$set": {"Unito": True}})
    return redirect(url_for("Unisciti"))

@app.route("/Elimina/<string:esame>", methods=["POST", "GET"])
def Elimina(esame):
    email = session["Username"]
    db.StudentiEsami.update_one({"Esame": esame, "Studente": email}, {"$set": {"Unito": False}})
    return redirect(url_for("Studiamo"))

@app.route("/Partecipa/<string:esame>/<string:id>/<incontro>", methods=["POST", "GET"])
def Partecipa(esame,id,incontro):
    email = session["Username"]
    db.StudentiIncontri.update_one({"Incontro": id, "Studente": email}, {"$set": {"Unito": True}})
    return redirect(url_for("Incontri", esame=esame, email=email, incontro=incontro))

@app.route("/Abbandona/<string:esame>/<string:id>/<incontro>", methods=["POST", "GET"])
def Abbandona(esame,id,incontro):
    email = session["Username"]
    db.StudentiIncontri.update_one({"Incontro": id, "Studente": email}, {"$set": {"Unito": False}})
    return redirect(url_for("Esame", esame=esame, email=email, incontro=incontro))

@app.route("/CreaIncontro/<string:esame>/<incontro>", methods=["POST", "GET"])
def CreaIncontro(esame,incontro):
    email = session["Username"]
    count = 0
    messaggio = ''
    if request.method == "POST":
        Luogo = request.form.get("Luogo")
        Orario = request.form.get("Orario")
        Descrizione = request.form.get("Descrizione")
        if (Luogo == "" or Orario == "" or Descrizione == ""):
            messaggio = "Attenzione, devi compilare tutti i campi!"
            return render_template('CreaIncontro.html', esame=esame, incontro=incontro, messaggio=messaggio)
        else:
            contatore = Incontridb.find()
            for x in contatore:
                count = count + 1
            NuovoIncontro = {'_id': str(count), 'Luogo': Luogo, 'Orario': Orario, 'Descrizione': Descrizione, 'NPartecipanti': 0, 'EsameApp': esame}
            Incontridb.insert_one(NuovoIncontro)
            listaStudenti = Utenti.find()
            for x in listaStudenti:
                NewStudenteIncontro = {'Studente': x['_id'], 'Incontro': NuovoIncontro['_id'], 'Unito': False}
                StudentiIncontri.insert_one(NewStudenteIncontro)
            return redirect(url_for("Incontri", esame=esame, email=email, incontro=incontro))
    return render_template('CreaIncontro.html', esame=esame, incontro=incontro, messaggio=messaggio)


if __name__ == '__main__':
    app.run()
