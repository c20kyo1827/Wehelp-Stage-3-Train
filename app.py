from flask import *
from flask_cors import CORS
from models import mydb_mgr
import boto3
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
# app.json.ensure_ascii = False
CORS(app)

mydb = mydb_mgr.mydb_mgr()
mydb.init()

s3 = boto3.client(
	"s3",
	"ap-southeast-2"
)

@app.route("/api/addMessage", endpoint="/api/addMessage")
def add_message():
	try:
		if request.args.get("image") and request.args.get("content"):
			print(request.args.get("image"))
			print(request.args.get("content"))
			mydb.add_message(request.args.get("message"), request.args.get("image"))
			return \
				jsonify({ \
					"ok": True
				}), 200
	except:
		return \
			jsonify({ \
				"error": True, \
				"message": "Server internal error" \
			}), 500

@app.route("/api/getMessage", endpoint="/api/getMessage")
def get_message():
	try:
		result = mydb.get_all_message()
		print(result)
		return jsonify({ \
				"data": result \
			})
	except:
		return \
			jsonify({ \
				"error": True, \
				"message": "Server internal error" \
			}), 500

# Pages
@app.route("/")
def index():
	return render_template("index.html")

app.config.from_object("config")
print(app.config)
app.run(host="0.0.0.0", port=5000)