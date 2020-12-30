from flask import Flask, url_for, session, request, redirect, render_template, flash
import mysql.connector

flag = 0

app = Flask(__name__)
app.secret_key = "hello"


@app.route("/", methods=["POST", "GET"])
def login():
	global flag
	if request.method == "POST":
	 	user = request.form["nm"]
	 	password = request.form["pwd"]

	 	if user == "admin" and password == "root":
	 		
	 		flag = 1
	 		
	 		return redirect(url_for("home"))
	 	else:
	 		return render_template("login.html")
	else:
	 	return render_template("login.html")


@app.route("/home", methods=["POST", "GET"])
def home():
	global flag
	if flag == 1:
			
		db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="root",
		database="prison_management"
		)

		mycursor = db.cursor()

		query = "SELECT pr.prisoner_id, name, ph_no, native_city, parole, cell, warden_id, block_id from prisoner pr, new_details nd where pr.prisoner_id=nd.prisoner_id;"
		

		mycursor.execute(query)
		rows = mycursor.fetchall()

		prisoner = []
		for x in rows:
			prisoner.append(x)
			
		return render_template("home.html", prisoner=prisoner)
		
	else:
		return redirect(url_for("login"))
	



@app.route("/addprisoner", methods=["POST", "GET"])
def addprisoner():
	global flag
	if request.method == "POST":
		prisoner_name = request.form["name"]
		native_city = request.form["city"]
		phone_no = request.form["phone"]
		parole = request.form["parole"]

		db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="root",
		database="prison_management"
		)

		mycursor = db.cursor()

		query = '''INSERT INTO prisoner(name, ph_no, native_city, parole) VALUES(%s, %s, %s, %s)'''
		val =  (prisoner_name, phone_no, native_city, parole)

		mycursor.execute(query,val)
		db.commit()

		return render_template("addPrisoner.html")
	else:
		if flag == 1:
			return render_template("addPrisoner.html")
		else:
			return redirect(url_for("login")) 
		

@app.route("/visiting", methods=["POST", "GET"])
def visit():
	if request.method == "POST":
		visitor = request.form["v_name"]
		phone = request.form["phone"]
		prisoner = request.form["p_name"]
		cell = request.form["cell"]
		relation = request.form["rel"]
		purpose = request.form["purpose"]

		db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="root",
		database="prison_management"
		)

		mycursor = db.cursor()

		query = "INSERT INTO visitor(visitor, ph_no, prisoner, cell, relation, purpose) VALUES (%s, %s, %s, %s, %s, %s)"
		val =  (visitor, phone, prisoner, cell, relation, purpose)

		mycursor.execute(query,val)
		db.commit()

		return render_template("visiting.html")

	else:
		if flag == 1:
			return render_template("visiting.html")
		else:
			return redirect(url_for("home"))


@app.route("/appointments", methods=["POST","GET"])
def appointment():
	global flag
	if flag == 1:
			
		db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="root",
		database="prison_management"
		)

		mycursor = db.cursor()

		query = "SELECT * FROM visitor"
		

		mycursor.execute(query)
		rows = mycursor.fetchall()

		visitor = []
		for x in rows:
			visitor.append(x)
			
		return render_template("appointments.html", visitor=visitor)
		
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	global flag
	flag = 0
	session.pop("user", None)
	return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
