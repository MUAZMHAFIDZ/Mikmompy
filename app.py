from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db import create_connection
from auth import fetchlogin, save_mikrotik, delete_mikrotik, update_myuser
from mikrotik import connect_to_router, create_hotspot_users, create_user_profile, get_all_hotspot_users, get_all_user_profiles, delete_hotspot_user, delete_hotspot_profile, get_print_user
import random
import string

app = Flask(__name__)
app.secret_key = 'supersecretkey'

web_title = "Mikmompy"

def check_login(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    return None

def generate_username_password(username_length=4, password_length=4):
    username_chars = string.ascii_lowercase + string.digits
    password_chars = string.digits
    
    username = ''.join(random.choices(username_chars, k=username_length))
    password = ''.join(random.choices(password_chars, k=password_length))
    
    return username, password

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = fetchlogin(username, password)
        if user:
            session['username'] = username
            session['pw_login'] = password
            session['id_login'] = user[0]
            return redirect(url_for('menu'))
        else:
            flash('Invalid login credentials!', 'error')

    return render_template('login.html', web_title=web_title)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'create_mikrotik' in request.form:
            ip_mikrotik = request.form['ip']
            rusername = request.form['rusername']
            rpassword = request.form['rpassword']
            hotspots = request.form['hotspot']
            dnsname = request.form['dns']
            save_mikrotik(ip_mikrotik, rusername, rpassword, hotspots, dnsname) 
            return redirect(url_for('menu'))  
        elif 'connect' in request.form:
            ip_mikrotik = request.form['ip']
            rusername = request.form['rusername']
            rpassword = request.form['rpassword']
            hotspots = request.form['hotspot']
            dnsname = request.form['dns']
            session['ip'] = ip_mikrotik
            session['rusername'] = rusername
            session['rpassword'] = rpassword
            session['hotspot'] = hotspots
            session['dns'] = dnsname
            return redirect(url_for('dashboard'))  
        elif 'delete_mikrotik' in request.form:
            id = request.form['id']
            delete_mikrotik(id)  
            return redirect(url_for('menu'))  
    connection = create_connection()
    cur = connection.cursor()
    cur.execute("SELECT * FROM mikrotik")
    mikrotiks = cur.fetchall()  
    return render_template('menu.html', mikrotiks=mikrotiks, web_title=web_title)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session or 'ip' not in session or 'rusername' not in session or 'rpassword' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    pw_login = session['pw_login']
    id_login = session['id_login']
    ip = session['ip']

    if request.method == 'POST':
        login_id = request.form['id_login']
        login_username = request.form['username_login']
        login_password = request.form['pw_login']
        update_myuser(login_id, login_username, login_password) 
        session.clear()
        return redirect(url_for('login'))  
    
    return render_template('dashboard.html', username=username, ip=ip, pw_login=pw_login, id_login=id_login, web_title=web_title)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    if 'username' not in session or 'ip' not in session or 'rusername' not in session or 'rpassword' not in session:
        return redirect(url_for('login'))
    
    rpassword = session['rpassword']
    rusername = session['rusername']
    pname = request.form.get('pname') 
    pharga = request.form.get('pharga')
    plimit = request.form.get('plimit')
    ip = session['ip']
    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)

    if request.method == 'POST':
        if 'create_profiles' in request.form:
            api_pool = connect_to_router(router_ip, username, password)
            api = api_pool.get_api()
            create_user_profile(api, pname+" Rp. "+pharga, plimit)
            api_pool.disconnect()
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        profiles = get_all_user_profiles(api)
        api_pool.disconnect()
        return render_template('profiles.html', profiles=profiles, web_title=web_title)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voucher', methods=['GET', 'POST'])
def voucher():
    if 'username' not in session or 'ip' not in session or 'rusername' not in session or 'rpassword' not in session:
        return redirect(url_for('login'))
    
    rpassword = session['rpassword']
    rusername = session['rusername']
    pwaktu = request.form.get("pwaktu") 
    profiless = request.form.get("profiless") 
    jumlah = request.form.get("jumlah") 
    ip = session['ip']

    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)
    pot = session['hotspot']
    pots = request.args.get('hotspot', pot)
    iddhapus = request.form.get('idhapus')

    if request.method == 'POST':
        if 'create_vouchers' in request.form:    
            if not profiless or not pwaktu:
                return jsonify({'error': 'Profil atau waktu tidak boleh kosong'})
            else:
                try:
                    api_pool = connect_to_router(router_ip, username, password)
                    api = api_pool.get_api()
                    for i in range(int(jumlah)):
                        print(i)
                        usernames, passwords = generate_username_password(6, 4)
                        create_hotspot_users(api, usernames, passwords, profiless, pwaktu, pots)
                    api_pool.disconnect()
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
        elif 'nnnnhapus' in request.form:
            try:
                api_pool = connect_to_router(router_ip, username, password)
                api = api_pool.get_api()
                delete_hotspot_user(api, iddhapus)
                api_pool.disconnect()
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        users = get_all_hotspot_users(api)
        users.reverse()
        profiles = get_all_user_profiles(api)
        api_pool.disconnect()
        return render_template('voucher.html', users=users, profiles=profiles, web_title=web_title)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/vouchermanual', methods=['GET', 'POST'])
def vouchermanual():
    if 'username' not in session or 'ip' not in session or 'rusername' not in session or 'rpassword' not in session:
        return redirect(url_for('login'))
    
    rpassword = session['rpassword']
    rusername = session['rusername']
    pwaktu = request.form.get("pwaktu") 
    profiless = request.form.get("profiless") 
    puserr = request.form.get("puserr") 
    pppw = request.form.get("ppw") 
    ip = session['ip']

    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)
    pot = session['hotspot']
    pots = request.args.get('hotspot', pot)

    if request.method == 'POST':
        if not profiless or not pwaktu:
            return jsonify({'error': 'Profil atau waktu tidak boleh kosong'})
        else:
            try:
                api_pool = connect_to_router(router_ip, username, password)
                api = api_pool.get_api()
                create_hotspot_users(api, puserr, pppw, profiless, pwaktu, pots)
                api_pool.disconnect()
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        users = get_all_hotspot_users(api)
        users.reverse()
        profiles = get_all_user_profiles(api)
        api_pool.disconnect()
        return render_template('vouchermanual.html', users=users, profiles=profiles, web_title=web_title)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/delete-user', methods=['POST'])
def delete_user():
    usernamer = request.form.get('idhapus')
    rpassword = session['rpassword']
    rusername = session['rusername']
    ip = session['ip']
    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)

    if not usernamer:
        return jsonify({'error': 'Username is required'}), 400
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        delete_hotspot_user(api, usernamer)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    usernamer = request.form.get('idhapus')
    rpassword = session['rpassword']
    rusername = session['rusername']
    ip = session['ip']
    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)

    if not usernamer:
        return jsonify({'error': 'Username is required'}), 400
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        delete_hotspot_profile(api, usernamer)
        return redirect(url_for('profiles'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/print-voucher', methods=['POST'])
def print_voucher():
    rpassword = session['rpassword']
    rusername = session['rusername']
    ip = session['ip']
    router_ip = request.args.get('router_ip', ip)
    username = request.args.get('username', rusername)
    password = request.args.get('password', rpassword)
    mydnst = session['dns']
    mydns = request.args.get('dns', mydnst)
    selected_users = request.form.getlist('selected_voucher')
    try:
        api_pool = connect_to_router(router_ip, username, password)
        api = api_pool.get_api()
        voucher = get_print_user(api, selected_users)
        return render_template('print_voucher.html', voucher=voucher, web_title=web_title, myUrl=mydns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
