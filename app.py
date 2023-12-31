from flask import *
from flask_cors import CORS
from models import mydb_mgr
import boto3
import uuid
import logging
import sys
import os
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
# app.json.ensure_ascii = False
CORS(app)

mydb = mydb_mgr.mydb_mgr()
mydb.init()

s3 = boto3.resource("s3",
		aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
		aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY")
	)
bucket_name = "stage3bucket"

logging.root.name = "Test API"
logging.basicConfig(level=logging.INFO,
                format="[%(levelname)-7s] %(name)s - %(message)s",
                stream=sys.stdout)

@app.route("/api/addMessage", endpoint="/api/addMessage" ,methods=["POST"])
def add_message():
	try:
		ALLOWED_EXTENSIONS = {'png', 'jpg', 'bmp', 'tiff', 'tif', 'gif', 'jpeg'}
		def allowed_file(filename):
			return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

		original_filename = request.files["image"].filename
		if not allowed_file(original_filename):
			return \
				jsonify({ \
					"error": True, \
					"message": "Image format is not allowed" \
				}), 400

		image_uuid = uuid.uuid4().hex
		new_filename = image_uuid + '.' + \
			original_filename.rsplit('.', 1)[1].lower()
		print(original_filename)
		print(new_filename)
		s3.Bucket(bucket_name).upload_fileobj(request.files["image"], new_filename)

		mydb.add_message(request.form.get("message"), new_filename)
		return \
			jsonify({ \
				"ok": True
			}), 200
	except Exception as e:
		exc_type, _, exc_tb = sys.exc_info()
		logging.error("Error : {error}, type : {type} at line : {line}".format(error=e, type=exc_type, line=exc_tb.tb_lineno))
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
		files = []
		bucket = s3.Bucket(bucket_name)
		for obj in bucket.objects.all():
			files.append(obj.key)
		print(files)
		return jsonify({
				"data": {
					"message": result,
					"image": files
				}
			})
	except Exception as e:
		exc_type, _, exc_tb = sys.exc_info()
		logging.error("Error : {error}, type : {type} at line : {line}".format(error=e, type=exc_type, line=exc_tb.tb_lineno))
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