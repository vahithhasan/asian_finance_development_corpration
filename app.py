from flask import Flask, render_template, request, flash
import smtplib
import ssl

app = Flask(__name__)
app.secret_key = "123"

@app.route("/")
def index():
    global username
    global email
    global phone
    global password
    username = request.form.get('username')
    email = request.form.get('useremail')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    return render_template("index.html")

@app.route('/Signin')
def Signin():
    return render_template('signin.html')

@app.route('/Forgot_password')
def Forgot_password():
    return render_template('forgot_password.html')

@app.route('/Forgot_fun', methods = ["POST", "GET"])
def Forgot_fun():
    from member_db import Member_DB
    db_m = Member_DB('member.db')
    username = request.form.get('email')

    for x in db_m.fetch_mail():
        print("Mail Round", x[0])
        if username == x[0]:
            print('IF X:', x[0])
            global num_otp_3
            import random
            num_otp = random.randint(2011, 99999)
            num_otp_3 = num_otp
            message = f"Hi {str(username)} Admin Key has {str(num_otp_3)}. This key will have expired in 8 minutes."

            from_mail = "vahithhasannorth@gmail.com"
            from_mail_password = "kmcbuunoqlfriqct"

            smtp_port = 587
            smtp_server = "smtp.gmail.com"
            simple_email_context = ssl.create_default_context()

            try:
                print("Connecting to server...")
                TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                TIE_server.starttls(context=simple_email_context)
                TIE_server.login(from_mail, from_mail_password)
                print("Connected to server.")

                print()
                print(f"Sendmail {username}")
                TIE_server.sendmail(from_mail, username, message)
                print(f"Email successfully sent to {username}")
            except Exception as e:
                print(e)
            finally:
                TIE_server.quit()
            return render_template('forgot_password_filed.html')

    flash("Unknown email. Try again", "warning")
    return render_template("signin.html")

@app.route('/Forgot_fun_check', methods = ["POST", 'GET'])
def Forgot_fun_check():
    otp = request.form.get('otp')
    num_otp_4 = str(num_otp_3)
    if otp == num_otp_4:
        return render_template('dashboard.html')
    else:
        flash("Wrong OTP", "warning")
        print("Forgot OTP: ", otp)
        return render_template('forgot_password_filed.html')


@app.route('/SignUp', methods = ["POST", "GET"])
def SignUp():
    from member_db import Member_DB
    db_m = Member_DB('member.db')
    if request.method == "POST":
        global username
        global email
        global phone
        global password
        username = request.form.get('username')
        email = request.form.get('useremail')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if confirm_password == password and password == confirm_password:
            if len(confirm_password) >= 6:
                for x in db_m.fetch_mail():
                    print("Mail Round", x[0])
                    if email == x[0]:
                        print('IF X:', x[0])
                        flash("This Email was already exist", "danger")
                        return render_template("signin.html")

                for x2 in db_m.fetch_phone():
                    x2_1 = str(x2[0])
                    print("Phone Round", x2[0], ' : Type DB: ', type(x2_1), " : Type Phone: ", type(phone))
                    if phone == x2_1:
                        print('IF X2: ', x2[0])
                        flash("This Phone Number was already exist", 'warning')
                        return render_template("signin.html")
                for x3 in db_m.fetch_password():
                    print("Password Round", x3[0])
                    if password == x3[0]:
                        print('IF x2: ', x3[0])
                        flash("This Password was already exist", 'danger')
                        return render_template("signin.html")
                if email and password and confirm_password:
                    print(username, email, phone, password, confirm_password)
                    import random
                    global num_otp_2
                    num_otp = random.randint(2011, 99999)
                    num_otp_2 = num_otp
                    message = f"Hi {str(username)} Admin Key has {str(num_otp_2)}. This key will have expired in 8 minutes."

                    from_mail = "vahithhasannorth@gmail.com"
                    from_mail_password = "kmcbuunoqlfriqct"

                    smtp_port = 587
                    smtp_server = "smtp.gmail.com"
                    simple_email_context = ssl.create_default_context()

                    try:
                        print("Connecting to server...")
                        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                        TIE_server.starttls(context=simple_email_context)
                        TIE_server.login(from_mail, from_mail_password)
                        print("Connected to server.")

                        print()
                        print(f"Sendmail {email}")
                        TIE_server.sendmail(from_mail, email, message)
                        print(f"Email successfully sent to {email}")
                    except Exception as e:
                        print(e)
                    finally:
                        TIE_server.quit()

                    return render_template('signup.html')
        else:
            flash("Please check password.", "danger")
            return render_template('signin.html')


@app.route('/SignUp_Confirmed', methods = ["POST", "GET"])
def SignUp_Confirmed():
    from member_db import Member_DB
    db_m = Member_DB('member.db')

    if request.method == "POST":
        position = request.form.get('position')
        admin_key = request.form.get('admin_key')
        confirm_admin_key = request.form.get('confirm_key')
        num_otp_3 = str(num_otp_2)
        if confirm_admin_key == admin_key and confirm_admin_key == num_otp_3:
            db_m.insert(username, email, phone, password, position)
            print(position, admin_key, confirm_admin_key, 'key', num_otp_3)
            print(db_m.fetch())
            flash("Account was created successfully", "success")
            return render_template('index.html')
        else:
            flash("Wrong Admin Key, Try Again.", "danger")
            return render_template('signup.html')


@app.route('/Login', methods = ["POST", "GET"])
def Login():
    from member_db import Member_DB
    db_m = Member_DB('member.db')
    for x in db_m.fetch_login():
        #print("USER X_1: ", x[0])

        username = request.form.get('username')
        email = request.form.get('useremail')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        x2 = x[0]
        x3 = x[1]
        print("Mail : ", x2, "\n", "Password: ", x3, "\n", "Type, Mail: ", type(email), type(x2), "Type Password: ", type(password), type(x3))
        print(email, password)
        if email == x2 and password == x3:
            print("Statement IF")
            return render_template('dashboard.html')
    flash("Wrong username or password", "danger")
    print('User: ', db_m.fetch_login())
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)



