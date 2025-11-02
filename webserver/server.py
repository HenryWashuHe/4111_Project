
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
# accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASE_USERNAME = "pme2111"
DATABASE_PASSWRD = "932856"
DATABASE_HOST = "34.139.8.30"
DATABASEURI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
with engine.connect() as conn:
	create_table_command = """
	CREATE TABLE IF NOT EXISTS test (
		id serial,
		name text
	)
	"""
	res = conn.execute(text(create_table_command))
	insert_table_command = """INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace')"""
	res = conn.execute(text(insert_table_command))
	# you need to commit for create, insert, update queries to reflect
	conn.commit()


@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request 
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print("uh oh, problem connecting to database")
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
	"""
	request is a special object that Flask provides to access web request information:

	request.method:   "GET" or "POST"
	request.form:     if the browser submitted a form, this contains the data in the form
	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

	See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
	"""

	# DEBUG: this is debugging code to see what request looks like
	print(request.args)


	#
	# example of a database query
	#
	select_query = "SELECT name from test"
	cursor = g.conn.execute(text(select_query))
	names = []
	for result in cursor:
		names.append(result[0])
	cursor.close()

	#
	# Flask uses Jinja templates, which is an extension to HTML where you can
	# pass data to a template and dynamically generate HTML based on the data
	# (you can think of it as simple PHP)
	# documentation: https://realpython.com/primer-on-jinja-templating/
	#
	# You can see an example template in templates/index.html
	#
	# context are the variables that are passed to the template.
	# for example, "data" key in the context variable defined below will be 
	# accessible as a variable in index.html:
	#
	#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
	#     <div>{{data}}</div>
	#     
	#     # creates a <div> tag for each element in data
	#     # will print: 
	#     #
	#     #   <div>grace hopper</div>
	#     #   <div>alan turing</div>
	#     #   <div>ada lovelace</div>
	#     #
	#     {% for n in data %}
	#     <div>{{n}}</div>
	#     {% endfor %}
	#
	context = dict(data = names)


	#
	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html
	#
	return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
	return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
	# accessing form inputs from user
	name = request.form['name']
	
	# passing params in for each variable into query
	params = {}
	params["new_name"] = name
	g.conn.execute(text('INSERT INTO test(name) VALUES (:new_name)'), params)
	g.conn.commit()
	return redirect('/')


@app.route('/login')
def login():
	abort(401)
	# Your IDE may highlight this as a problem - because no such function exists (intentionally).
	# This code is never executed because of abort().
	this_is_never_executed()


# ==================== ADDRESS VIEW ====================
@app.route('/address')
def address_view():
	"""
	Display all addresses with their neighborhoods
	"""
	addresses_query = """
		SELECT 
			a.address_id,
			a.street1,
			a.street2,
			a.postal_code,
			n.name as neighborhood_name
		FROM address a
		LEFT JOIN neighborhood n ON a.neighborhood_id = n.neighborhood_id
		ORDER BY n.name, a.street1
	"""
	cursor = g.conn.execute(text(addresses_query))
	addresses = []
	for row in cursor:
		addresses.append({
			"address_id": row[0],
			"street1": row[1],
			"street2": row[2],
			"postal_code": row[3],
			"neighborhood_name": row[4]
		})
	cursor.close()
	
	return render_template("address.html", addresses=addresses)


# ==================== DEFAULT HANDLERS VIEW ====================
@app.route('/default-handlers')
def default_handlers_view():
	"""
	Display the default agency mappings for complaint types
	"""
	mappings_query = """
		SELECT 
			ct.complaint_topic,
			a.agency_name
		FROM handle_by_default hbd
		JOIN complaint_type ct ON hbd.complaint_type_id = ct.complaint_type_id
		JOIN agency a ON hbd.agency_id = a.agency_id
		ORDER BY ct.complaint_topic
	"""
	cursor = g.conn.execute(text(mappings_query))
	mappings = []
	for row in cursor:
		mappings.append({
			"complaint_topic": row[0],
			"agency_name": row[1]
		})
	cursor.close()
	
	return render_template("default_handlers.html", mappings=mappings)


# ==================== NEIGHBORHOOD VIEW ====================
@app.route('/neighborhood')
def neighborhood_view():
	"""
	Display form to search neighborhoods with dynamic dropdowns
	"""
	# Get all neighborhoods from database
	neighborhoods = []
	complaint_types = []
	
	try:
		neighborhoods_query = """
			SELECT neighborhood_id, name 
			FROM neighborhood 
			ORDER BY name
		"""
		cursor = g.conn.execute(text(neighborhoods_query))
		for row in cursor:
			neighborhoods.append({"id": row[0], "name": row[1]})
		cursor.close()
		
		# Get all complaint types from database
		complaint_types_query = """
			SELECT complaint_type_id, complaint_topic 
			FROM complaint_type 
			ORDER BY complaint_topic
		"""
		cursor = g.conn.execute(text(complaint_types_query))
		for row in cursor:
			complaint_types.append({"id": row[0], "topic": row[1]})
		cursor.close()
	except Exception as e:
		print(f"Error loading dropdowns: {e}")
		import traceback
		traceback.print_exc()
	
	print(f"Loaded {len(neighborhoods)} neighborhoods and {len(complaint_types)} complaint types")
	
	return render_template("neighborhood.html", 
		neighborhoods=neighborhoods, 
		complaint_types=complaint_types)


@app.route('/neighborhood/search', methods=['GET'])
def neighborhood_search():
	"""
	Search for a neighborhood and display statistics:
	- Average completion speed (in days)
	- Complaint counts by type
	- Total complaints
	"""
	# Get neighborhoods and complaint types for dropdowns
	neighborhoods = []
	complaint_types_list = []
	
	try:
		neighborhoods_query = """
			SELECT neighborhood_id, name 
			FROM neighborhood 
			ORDER BY name
		"""
		cursor = g.conn.execute(text(neighborhoods_query))
		for row in cursor:
			neighborhoods.append({"id": row[0], "name": row[1]})
		cursor.close()
		
		complaint_types_query = """
			SELECT complaint_type_id, complaint_topic 
			FROM complaint_type 
			ORDER BY complaint_topic
		"""
		cursor = g.conn.execute(text(complaint_types_query))
		for row in cursor:
			complaint_types_list.append({"id": row[0], "topic": row[1]})
		cursor.close()
	except Exception as e:
		print(f"Error loading dropdown data in search: {e}")
		import traceback
		traceback.print_exc()
	
	# Get search parameters
	neighborhood_id = request.args.get('neighborhood_id', '').strip()
	neighborhood_name = request.args.get('neighborhood_name', '').strip().upper()
	filter_complaint_type = request.args.get('complaint_type_id', '').strip()
	
	# Determine which parameter to use (dropdown takes precedence)
	if neighborhood_id:
		# Using dropdown selection
		neighborhood_query = """
			SELECT neighborhood_id, name 
			FROM neighborhood 
			WHERE neighborhood_id = :id
		"""
		cursor = g.conn.execute(text(neighborhood_query), {"id": neighborhood_id})
		neighborhood_row = cursor.fetchone()
		cursor.close()
	elif neighborhood_name:
		# Using text search
		neighborhood_query = """
			SELECT neighborhood_id, name 
			FROM neighborhood 
			WHERE UPPER(name) = :name
		"""
		cursor = g.conn.execute(text(neighborhood_query), {"name": neighborhood_name})
		neighborhood_row = cursor.fetchone()
		cursor.close()
	else:
		return render_template("neighborhood.html", 
			neighborhoods=neighborhoods,
			complaint_types=complaint_types_list,
			error="Please select or enter a neighborhood name")
	
	if not neighborhood_row:
		return render_template("neighborhood.html", 
			neighborhoods=neighborhoods,
			complaint_types=complaint_types_list,
			error=f"Neighborhood not found")
	
	neighborhood_id = neighborhood_row[0]
	neighborhood_display_name = neighborhood_row[1]
	
	# Build query parameters based on filters
	query_params = {"neighborhood_id": neighborhood_id}
	complaint_type_filter = ""
	
	if filter_complaint_type:
		complaint_type_filter = "AND c.complaint_type_id = :complaint_type_id"
		query_params["complaint_type_id"] = filter_complaint_type
	
	# Get statistics: average completion speed
	avg_speed_query = f"""
		SELECT 
			AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days
		FROM complaint c
		JOIN address a ON c.address_id = a.address_id
		WHERE a.neighborhood_id = :neighborhood_id
		  {complaint_type_filter}
		  AND c.closed_at IS NOT NULL
		  AND c.created_at IS NOT NULL
	"""
	cursor = g.conn.execute(text(avg_speed_query), query_params)
	avg_speed_row = cursor.fetchone()
	cursor.close()
	avg_speed = round(avg_speed_row[0], 2) if avg_speed_row[0] else 0
	
	# Get complaint counts by type
	complaint_type_query = f"""
		SELECT 
			ct.complaint_topic,
			COUNT(*) as count
		FROM complaint c
		JOIN address a ON c.address_id = a.address_id
		JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
		WHERE a.neighborhood_id = :neighborhood_id
		  {complaint_type_filter}
		GROUP BY ct.complaint_topic
		ORDER BY count DESC
	"""
	cursor = g.conn.execute(text(complaint_type_query), query_params)
	complaint_types = []
	total_complaints = 0
	for row in cursor:
		complaint_types.append({"type": row[0], "count": row[1]})
		total_complaints += row[1]
	cursor.close()
	
	context = {
		"neighborhoods": neighborhoods,
		"complaint_types": complaint_types_list,
		"selected_neighborhood_id": neighborhood_id,
		"selected_complaint_type_id": filter_complaint_type,
		"neighborhood_name": neighborhood_display_name,
		"avg_speed": avg_speed,
		"complaint_type_breakdown": complaint_types,
		"total_complaints": total_complaints
	}
	
	return render_template("neighborhood.html", **context)


# ==================== AGENCY VIEW ====================
@app.route('/agency')
def agency_view():
	"""
	Display form to search agencies with dynamic dropdowns
	"""
	# Get all agencies from database
	agencies = []
	complaint_types = []
	
	try:
		agencies_query = """
			SELECT agency_id, agency_name 
			FROM agency 
			ORDER BY agency_name
		"""
		cursor = g.conn.execute(text(agencies_query))
		for row in cursor:
			agencies.append({"id": row[0], "name": row[1]})
		cursor.close()
		
		# Get all complaint types from database
		complaint_types_query = """
			SELECT complaint_type_id, complaint_topic 
			FROM complaint_type 
			ORDER BY complaint_topic
		"""
		cursor = g.conn.execute(text(complaint_types_query))
		for row in cursor:
			complaint_types.append({"id": row[0], "topic": row[1]})
		cursor.close()
	except Exception as e:
		print(f"Error loading agency dropdowns: {e}")
		import traceback
		traceback.print_exc()
	
	print(f"Loaded {len(agencies)} agencies and {len(complaint_types)} complaint types")
	
	return render_template("agency.html", 
		agencies=agencies, 
		complaint_types=complaint_types)


@app.route('/agency/search', methods=['GET'])
def agency_search():
	"""
	Search for an agency and display:
	- Average completion speed (in days)
	- City-wide benchmark for comparison
	- Total complaints handled
	"""
	# Get agencies and complaint types for dropdowns
	agencies = []
	complaint_types = []
	
	try:
		agencies_query = """
			SELECT agency_id, agency_name 
			FROM agency 
			ORDER BY agency_name
		"""
		cursor = g.conn.execute(text(agencies_query))
		for row in cursor:
			agencies.append({"id": row[0], "name": row[1]})
		cursor.close()
		
		complaint_types_query = """
			SELECT complaint_type_id, complaint_topic 
			FROM complaint_type 
			ORDER BY complaint_topic
		"""
		cursor = g.conn.execute(text(complaint_types_query))
		for row in cursor:
			complaint_types.append({"id": row[0], "topic": row[1]})
		cursor.close()
	except Exception as e:
		print(f"Error loading agency dropdown data in search: {e}")
		import traceback
		traceback.print_exc()
	
	# Get search parameters
	agency_id = request.args.get('agency_id', '').strip()
	agency_name = request.args.get('agency_name', '').strip()
	filter_complaint_type = request.args.get('complaint_type_id', '').strip()
	
	# Determine which parameter to use (dropdown takes precedence)
	if agency_id:
		# Using dropdown selection
		agency_query = """
			SELECT agency_id, agency_name 
			FROM agency 
			WHERE agency_id = :id
		"""
		cursor = g.conn.execute(text(agency_query), {"id": agency_id})
		agency_row = cursor.fetchone()
		cursor.close()
	elif agency_name:
		# Using text search (case-insensitive partial match)
		agency_query = """
			SELECT agency_id, agency_name 
			FROM agency 
			WHERE UPPER(agency_name) LIKE UPPER(:name)
			LIMIT 1
		"""
		cursor = g.conn.execute(text(agency_query), {"name": f"%{agency_name}%"})
		agency_row = cursor.fetchone()
		cursor.close()
	else:
		return render_template("agency.html", 
			agencies=agencies,
			complaint_types=complaint_types,
			error="Please select or enter an agency name")
	
	if not agency_row:
		return render_template("agency.html", 
			agencies=agencies,
			complaint_types=complaint_types,
			error=f"Agency not found")
	
	agency_id = agency_row[0]
	agency_display_name = agency_row[1]
	
	# Build query parameters based on filters
	query_params = {"agency_id": agency_id}
	complaint_type_filter = ""
	
	if filter_complaint_type:
		complaint_type_filter = "AND c.complaint_type_id = :complaint_type_id"
		query_params["complaint_type_id"] = filter_complaint_type
	
	# Get agency's average completion speed
	agency_speed_query = f"""
		SELECT 
			AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days,
			COUNT(*) as total_complaints
		FROM complaint c
		WHERE c.agency_id = :agency_id
		  {complaint_type_filter}
		  AND c.closed_at IS NOT NULL
		  AND c.created_at IS NOT NULL
	"""
	cursor = g.conn.execute(text(agency_speed_query), query_params)
	agency_row = cursor.fetchone()
	cursor.close()
	
	agency_avg_speed = round(agency_row[0], 2) if agency_row[0] else 0
	agency_total_complaints = agency_row[1] if agency_row[1] else 0
	
	# Get city-wide benchmark (average across all agencies) with same filter
	citywide_query_params = {}
	if filter_complaint_type:
		citywide_query_params["complaint_type_id"] = filter_complaint_type
	
	citywide_query = f"""
		SELECT 
			AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days
		FROM complaint c
		WHERE c.closed_at IS NOT NULL
		  AND c.created_at IS NOT NULL
		  {complaint_type_filter.replace(':agency_id', ':complaint_type_id') if filter_complaint_type else ''}
	"""
	cursor = g.conn.execute(text(citywide_query), citywide_query_params)
	citywide_row = cursor.fetchone()
	cursor.close()
	
	citywide_avg_speed = round(citywide_row[0], 2) if citywide_row[0] else 0
	
	# Calculate performance comparison
	if citywide_avg_speed > 0:
		performance_diff = agency_avg_speed - citywide_avg_speed
		if performance_diff < 0:
			performance_text = f"{abs(performance_diff):.2f} days faster than city average"
		elif performance_diff > 0:
			performance_text = f"{performance_diff:.2f} days slower than city average"
		else:
			performance_text = "Matches city average"
	else:
		performance_text = "N/A"
	
	# Get complaint breakdown by type for this agency
	complaint_breakdown_query = f"""
		SELECT 
			ct.complaint_topic,
			COUNT(*) as count
		FROM complaint c
		JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
		WHERE c.agency_id = :agency_id
		  {complaint_type_filter}
		GROUP BY ct.complaint_topic
		ORDER BY count DESC
		LIMIT 10
	"""
	cursor = g.conn.execute(text(complaint_breakdown_query), query_params)
	complaint_breakdown = []
	for row in cursor:
		complaint_breakdown.append({"type": row[0], "count": row[1]})
	cursor.close()
	
	context = {
		"agencies": agencies,
		"complaint_types": complaint_types,
		"selected_agency_id": agency_id,
		"selected_complaint_type_id": filter_complaint_type,
		"agency_name": agency_display_name,
		"agency_avg_speed": agency_avg_speed,
		"citywide_avg_speed": citywide_avg_speed,
		"performance_text": performance_text,
		"total_complaints": agency_total_complaints,
		"complaint_breakdown": complaint_breakdown
	}
	
	return render_template("agency.html", **context)


# ==================== USER PROFILE VIEW ====================
@app.route('/user')
def user_list():
	"""
	Display list of all users
	"""
	users_query = """
		SELECT user_id, name, email_address, created_at
		FROM app_user
		ORDER BY name
	"""
	cursor = g.conn.execute(text(users_query))
	users = []
	for row in cursor:
		users.append({
			"user_id": row[0],
			"name": row[1],
			"email_address": row[2],
			"created_at": row[3]
		})
	cursor.close()
	
	return render_template("user_list.html", users=users)


@app.route('/user/<user_id>')
def user_profile(user_id):
	"""
	Display user profile with tracked complaints
	"""
	# Get user info
	user_query = """
		SELECT user_id, name, email_address, created_at
		FROM app_user
		WHERE user_id = :user_id
	"""
	cursor = g.conn.execute(text(user_query), {"user_id": user_id})
	user_row = cursor.fetchone()
	cursor.close()
	
	if not user_row:
		return "User not found", 404
	
	user_info = {
		"user_id": user_row[0],
		"name": user_row[1],
		"email_address": user_row[2],
		"created_at": user_row[3]
	}
	
	# Get tracked complaints
	tracked_query = """
		SELECT 
			c.complaint_id,
			c.description,
			c.created_at,
			c.closed_at,
			ct.complaint_topic,
			a.agency_name,
			s.name as status_name,
			tb.added_at,
			tb.note
		FROM tracked_by tb
		JOIN complaint c ON tb.complaint_id = c.complaint_id
		JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
		JOIN agency a ON c.agency_id = a.agency_id
		JOIN status s ON c.status_id = s.status_id
		WHERE tb.user_id = :user_id
		ORDER BY tb.added_at DESC
	"""
	cursor = g.conn.execute(text(tracked_query), {"user_id": user_id})
	tracked_complaints = []
	for row in cursor:
		tracked_complaints.append({
			"complaint_id": row[0],
			"description": row[1],
			"created_at": row[2],
			"closed_at": row[3],
			"complaint_topic": row[4],
			"agency_name": row[5],
			"status_name": row[6],
			"added_at": row[7],
			"note": row[8]
		})
	cursor.close()
	
	return render_template("user_profile.html", user=user_info, tracked_complaints=tracked_complaints)


@app.route('/complaint/search')
def complaint_search():
	"""
	Search for complaints to track
	"""
	query = request.args.get('query', '').strip()
	
	if not query:
		return render_template("complaint_search.html", complaints=[])
	
	# Search complaints by description or complaint type
	search_query = """
		SELECT 
			c.complaint_id,
			c.description,
			ct.complaint_topic,
			a.agency_name,
			s.name as status_name,
			c.created_at
		FROM complaint c
		JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
		JOIN agency a ON c.agency_id = a.agency_id
		JOIN status s ON c.status_id = s.status_id
		WHERE UPPER(c.description) LIKE UPPER(:query)
		   OR UPPER(ct.complaint_topic) LIKE UPPER(:query)
		ORDER BY c.created_at DESC
		LIMIT 50
	"""
	cursor = g.conn.execute(text(search_query), {"query": f"%{query}%"})
	complaints = []
	for row in cursor:
		complaints.append({
			"complaint_id": row[0],
			"description": row[1],
			"complaint_topic": row[2],
			"agency_name": row[3],
			"status_name": row[4],
			"created_at": row[5]
		})
	cursor.close()
	
	return render_template("complaint_search.html", complaints=complaints, query=query)


@app.route('/user/<user_id>/track/<complaint_id>', methods=['POST'])
def track_complaint(user_id, complaint_id):
	"""
	Add a complaint to user's tracked list
	"""
	note = request.form.get('note', '').strip()
	
	# Check if already tracking
	check_query = """
		SELECT 1 FROM tracked_by 
		WHERE user_id = :user_id AND complaint_id = :complaint_id
	"""
	cursor = g.conn.execute(text(check_query), {"user_id": user_id, "complaint_id": complaint_id})
	exists = cursor.fetchone()
	cursor.close()
	
	if exists:
		return redirect(f'/user/{user_id}')
	
	# Insert tracking record
	insert_query = """
		INSERT INTO tracked_by (user_id, complaint_id, added_at, note)
		VALUES (:user_id, :complaint_id, CURRENT_TIMESTAMP, :note)
	"""
	g.conn.execute(text(insert_query), {
		"user_id": user_id,
		"complaint_id": complaint_id,
		"note": note if note else None
	})
	g.conn.commit()
	
	return redirect(f'/user/{user_id}')


@app.route('/user/<user_id>/untrack/<complaint_id>', methods=['POST'])
def untrack_complaint(user_id, complaint_id):
	"""
	Remove a complaint from user's tracked list
	"""
	delete_query = """
		DELETE FROM tracked_by 
		WHERE user_id = :user_id AND complaint_id = :complaint_id
	"""
	g.conn.execute(text(delete_query), {"user_id": user_id, "complaint_id": complaint_id})
	g.conn.commit()
	
	return redirect(f'/user/{user_id}')


if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

			python server.py

		Show the help text using:

			python server.py --help

		"""

		HOST, PORT = host, port
		print("running on %s:%d" % (HOST, PORT))
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

run()
