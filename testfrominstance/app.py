from chalice import Chalice
from chalicelib.util import get_session
from chalice import CORSConfig

from chalicelib.db import db, base

app = Chalice(app_name='testfrominstance')
base.metadata.create_all(db)

cors_config = CORSConfig(
allow_origin='*',
allow_headers=['X-Special-Header'],
max_age=600,
expose_headers=['X-Special-Header'],
allow_credentials=True
)

@app.route('/')
def index():	
	return {'hello': 'world'}

@app.route('/print', cors=cors_config)
def get_earned_by_id():
	with get_session() as session:
		x = session.execute("select * from testing where name='miku';").fetchone()[0]
		return str(x)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
