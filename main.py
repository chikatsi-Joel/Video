import threading
from flask import Flask, send_file, request, redirect, url_for, jsonify
import mimetypes, database, requests, whisper_proxu, config

app = Flask(__name__)

@app.route('/srt/<name>', methods = ['GET'])
def send_srt(name) :
    return send_file(f'Transcribe/{name}.srt', mimetype= mimetypes.guess_type(url= f'Transcribe/{name}.srt')[0])
    
@app.route('/get_all_video')
def get_video() :
    all_video = database.Video.get_all_video()
    video = [
        {
            'id' : video.id,
            'beta_mode' : video.beta_mode,
            'price' : video.price,
            'id_user' : video.id_user,
            'model_type' : video.model_type
        } for video in all_video
    ]
    return jsonify(video)

@app.route('/add_user', methods = ['POST'])
def add_user() :
    data = request.form
    name = data['name']
    mail = data['mail']
    password = data['password']
    age = data['age']
    try :
        database.User.addUser(name, mail, password, int(age))
    except AttributeError:
        info = {"Echec de l'enregistremement" : "Email déjà utilisée", "status" : False}
        return info
    except :
        info = {"Echec de l'enregistremement" : "Email déjà utilisée", "status" : False}
        return info
    info = {"Enregistrement reussie." : 'Utilisateur ajouté avec succès', "status" : True}
    return info

@app.route("/authentification", methods = ['POST'])
def auth() :
    data = request.form
    mail = data['email']
    passw = data['password']
    user = database.User.get_user_by_mail(mail)
    if user :
        sd = {"find" : True, "correct" : (passw == user.password  and user.mail == mail)}
        return sd
    else :
        sd = {"find" : False, "correct" : False}
        return sd
    
@app.route('/upload_compte', methods = ['POST'])
def charge_compte() :
    data = request.form
    id_user = data['id']
    compte = data['montant']
    database.User.charger_compte(id_user, float(compte))
    return {"success" : 'Compte charger avec succès..'}
    
@app.route('/upload_password', methods = ['POST'])
def change_password() :
    data = request.form
    id_user = data['id']
    last_password = data['last_password']
    password = data['password']
    try :
       database.User.change_password(id_user, password, last_password)
    except InterruptedError :
        return {'success' : "Mot de Passe Non correspondant.."}
    return {"sreceive_videuccess" : 'Mot de passe changé avec succès..'}
    
@app.route('/get_db', methods = ['POST', 'GET'])
def getdb() :
    return send_file('Database/database.db', mimetype='application/octet-stream')


@app.route('/video', methods=['POST'])
def receive_video():
    video = request.files['file']
    if video:
        video.save("Video/" + video.filename)
        data = request.form
        typ = data['type']
        database.Video.add_video(
            config.get_price(typ) > 0,
            config.get_price(typ),
            typ,
            data['id']
        )
        thread = threading.Thread(target = whisper_proxu.transcribe_audio, args = (
            "Video/" + video.filename,
            data['lang_dep'],
            data['lang_cible'],
            typ,
            name := data['name']
        ))
        thread.start()
        thread.join()
        return redirect(url_for('send_srt', name = name))

@app.route('/get_user', methods = ['POST'])
def get_user() :
    data = request.form
    email = data['mail']
    print(email)
    user = database.User.get_user_by_mail(email = email)
    data = {
        'name' : user.name,
        'age' : user.age,
        'compte' : user.compte,
        'mail' : user.mail,
        'id' : user.id
    }
    return data

@app.route('/get_all_user', methods = ['POST', "GET"])
def get_all_user() :
    all_user = database.User.get_all_user()
    all_user = [
        {
            "id" : user.id,
            "name" : user.name,
            "age" : user.age,
            'mail' : user.mail,
            "is_delete" : user.is_delete,
            "compte" : user.compte
        } for user in all_user
    ]
    return jsonify(all_user)


@app.route("/delete_compte", methods = ['GET', 'POST'])
def delete_compte() :
    data = request.form
    email = data['mail']
    
app.run(host=config.host, port=config.port, debug=True)