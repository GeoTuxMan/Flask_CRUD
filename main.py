# /new_user displaying a view for add a new record
# /add save input into db

# pymysql.cursors.DictCursor dictionary(key/value), column name/column value
# /update

import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/new_user')
def add_user_view():
	return render_template('add.html', title="Add User - Python Flask MySQL CRUD")
	
@app.route('/add', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try: 
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO users(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User added successfully!')
			return redirect('/')
		else:
			flash('Error while adding user')
			return redirect('/')
	except Exception as e:
		print(e)
		flash('an error occurred')
		return redirect('/')
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/')
def users():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		return render_template('users.html', title="Users - Python Flask MySQL CRUD", table=table)
	except Exception as e:
		print(e)
		return render_template('error.html', title="Eroare",message='An error occurred.')
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()
		
@app.route('/edit/<int:id>',methods=['GET', 'POST'])
def edit_view(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE user_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', title="Edit User", row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
		
@app.route('/update', methods=['POST'])
def update_user():
	conn = None
	cursor = None
	try: 
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_id = request.form['id']
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			print(_hashed_password)
			# save edits
			sql = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/delete/<int:id>')
def delete_user(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

if __name__ == "__main__":
	#app.run()
	app.run(host='127.0.0.1',port=8000,debug=True)