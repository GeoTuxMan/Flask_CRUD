from flask_table import Table, Col, LinkCol, ButtonCol

class Results(Table):
	classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
	user_id = Col('Id', show=False)
	user_name = Col('Name')
	user_email = Col('Email')
	user_password = Col('Password', show=False)
	edit_button_with_link = ButtonCol('Edit', 'edit_view', url_kwargs=dict(id='user_id'),button_attrs={'class': 'btn btn-primary', 'method': 'GET'})
	delete_button_with_link = ButtonCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'),button_attrs={'class': 'btn btn-danger', 'method': 'GET'})