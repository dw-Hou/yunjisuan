from flask import Flask,jsonify,request,render_template,send_from_directory
from flask_script import Manager
from darknet import load_para,detect
from utils import rectangle_detect_image
from werkzeug.utils import secure_filename
import os
import cv2
from flask_cors import CORS
import random
import string
app=Flask(__name__)
manager=Manager(app)
CORS(app,supports_credentials=True)
@app.route('/')
def index():
    return '<h1> Hello,world</h1>'

net,meta=load_para()
ALLOWED_EXTENSIONS=set(['png','jpg','JPG',"PNG",'bmp'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def return_random_string(filename):
	fmt= filename.rsplit('.',1)[1]
	return "".join(random.sample(string.ascii_letters+string.digits,20))+'.'+fmt

@app.route('/input',methods=['POST','GET'])
def input():
	if request.method=='POST':
		f=request.files['file']
		if not(f and allowed_file(f.filename)):
			return jsonify({"isvalid":1,"msg":"the format is error"})
		basepath=os.path.abspath(os.path.dirname(__file__))
		random_name=return_random_string(f.filename)
		print(basepath+'\n')
		print(random_name+'\n')
		upload_path=os.path.join(basepath,'IN_PATH',secure_filename(random_name))
		f.save(upload_path)
		return jsonify({"isvalid":0,"Path":'IN_PATH/'+random_name})
	return jsonify({"isvalid":1,"msg":"no POST"})

@app.route('/up_load',methods=['POST','GET'])
def upload():
	if request.method=='POST':
		content=request.get_json()
		upload_path=content['name']
		#print("debugqqq"+upload_path)
		basepath=os.path.abspath(os.path.dirname(__file__))
		img=cv2.imread(os.path.join(basepath,'IN_PATH',upload_path))
		random_name=return_random_string(upload_path)
		Img_outpath=os.path.join(basepath,'OUT_PATH',random_name)
		cv2.imwrite(os.path.join(basepath,'OUT_PATH','test.jpg'),img)
		print("debug\n")
		res=detect(net,meta,b'./OUT_PATH/test.jpg')
		print(res)
		rectangle_detect_image(img,res,Img_outpath)
		return jsonify({"isvalid":0,"Path":'OUT_PATH/'+random_name})
		#return render_template('upload_ok.html') 
	return jsonify({"isvalid":1,"msg":"no POST"})
	#return render_template('upload.html') 

@app.route("/OUT_PATH/<filename>")
def send_out_img(filename):
	basepath=os.path.abspath(os.path.dirname(__file__))
	return send_from_directory(os.path.join(basepath,'OUT_PATH'),filename)

@app.route("/IN_PATH/<filename>")
def send_in_img(filename):
	basepath=os.path.abspath(os.path.dirname(__file__))
	return send_from_directory(os.path.join(basepath,"IN_PATH"),filename)

if __name__=='__main__':
    manager.run()
