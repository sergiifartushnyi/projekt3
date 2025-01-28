from flask import Flask , session , redirect , url_for , request , render_template , jsonify
from functools import wraps

app = Flask ( __name__ )
app.secret_key = 'your_secret_key'

USERS = {
    "admin": "password123" ,
    "user1": "pass1"
}


def login_required(f):
    @wraps ( f )
    def decorated_function(*args , **kwargs):
        if 'user' not in session:
            return redirect ( url_for ( 'login' ) )
        return f ( *args , **kwargs )

    return decorated_function


@app.route ( '/' )
@login_required
def index():
    return f"Привіт, {session['user']}! Ви залогінені."


@app.route ( '/login' , methods=['GET' , 'POST'] )
def login():
    if request.method == 'POST':
        username = request.form.get ( 'username' )
        password = request.form.get ( 'password' )

        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect ( url_for ( 'index' ) )
        else:
            return "Неправильне ім'я користувача або пароль" , 401

    return '''
        <form method="post">
            <p>Ім'я користувача: <input type="text" name="username"></p>
            <p>Пароль: <input type="password" name="password"></p>
            <p><input type="submit" value="Логін"></p>
        </form>
    '''


@app.route ( '/logout' )
@login_required
def logout():
    session.pop ( 'user' , None )
    return redirect ( url_for ( 'login' ) )


@app.route ( '/protected' )
@login_required
def protected():
    return f"Це захищений контент для користувача {session['user']}."


if __name__ == '__main__':
    app.run ( debug=True )