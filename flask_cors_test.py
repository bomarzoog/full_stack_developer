from flask_cors import CORS
from models import setup(db), Plant

def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	CORS(app)
	
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
	return reponse
	
	@app.route('/')
	def hello():
		return jsonify({'message': 'HELLO WORLD'})



	return app


