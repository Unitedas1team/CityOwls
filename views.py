import logging
import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory, jsonify, \
    Response
from flask_login import current_user
from aquariusys import app, db
from forms import  LoginForm,DevicesForm
from flask_login import login_required, login_user, logout_user
from models import Admin,Weather,Devices,Light,Checkin,Inspection,Repair
from sqlalchemy.exc import IntegrityError

from initapp import csrf, camera

from datetime import datetime

import cv2

@app.route('/')    #根页面
def index():
    if current_user.is_authenticated:
        return redirect(url_for('patrol'))
    return render_template('base.html')  #把jinja2模板引擎集成到应用中


@app.route('/login', methods=['GET', 'POST'])  #管理员登录界面
def login():
    if current_user.is_authenticated:
        return redirect(url_for('patrol'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.pswd.data
        admin = Admin.query.first()
        if admin:
            if username == admin.account and admin.validate_password(password):
                login_user(admin, True)
                flash('Welcome !!')
                return redirect(url_for('patrol'))
        else:
            flash('No account!', 'error')
    return render_template('login.html', form=form)


@app.route('/patrol')
@login_required
def patrol():
    light = Light.query.first()
    state = light.state
    if state:
        bgcolor = 'bg-danger'
    else:
        bgcolor = 'bg-black'
    return render_template('patrol.html',bgcolor=bgcolor)


@app.route('/inspection',methods=['GET','POST'])
@login_required
def inspection():
    devices = Devices.query.first()
    form = DevicesForm()
    if form.validate_on_submit():
        thsensor = form.thsensor.data
        ilsensor = form.ilsensor.data
        wdsensor = form.wdsensor.data
        nosensor = form.nosensor.data
        pmsensor = form.pmsensor.data
        light    = form.light.data
        t = datetime.now()
        u = Admin.query.first()
        tstring = t.strftime('%Y-%m-%d-%H-%M-%S')
        if thsensor:
            devices.ths = False
        else:
            devices.ths = devices.ths
        if ilsensor:
            devices.ils =False
        else:
            devices.ilsensor =devices.ils
        if wdsensor:
            devices.wss = False
        else:
            devices.wss = devices.wss
        if nosensor:
            devices.nos = False
        else:
            devices.nos = devices.nos
        if pmsensor:
            devices.pms = False
        else:
            devices.pmsensor = devices.pms
        if light :
            devices.ltm = False
        else:
            devices.ltm = devices.ltm

        inspection = Inspection(
            timestamp=t,
            datestring=tstring,
            user=u,
            ths=thsensor,
            ils=ilsensor,
            wss=wdsensor,
            pms=pmsensor,
            nos=nosensor,
            ltm=light
        )
        db.session.add(inspection)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # 返回数据库添加前状态
        return redirect(url_for('patrol'))
    return render_template('inspection.html', form=form)


@app.route('/repair',methods=['GET','POST'])
@login_required
def repair():
    devices = Devices.query.first()
    form = DevicesForm()
    if form.validate_on_submit():
        thsensor = form.thsensor.data
        ilsensor = form.ilsensor.data
        wdsensor = form.wdsensor.data
        nosensor = form.nosensor.data
        pmsensor = form.pmsensor.data
        light = form.light.data
        t = datetime.now()
        u = Admin.query.first()
        tstring = t.strftime('%Y-%m-%d-%H-%M-%S')

        if thsensor:
            devices.ths = True
        else:
            devices.ths = devices.ths
        if ilsensor:
            devices.ils = True
        else:
            devices.ilsensor = devices.ils
        if wdsensor:
            devices.wss = True
        else:
            devices.wss = devices.wss
        if nosensor:
            devices.nos = True
        else:
            devices.nos = devices.nos
        if pmsensor:
            devices.pms = True
        else:
            devices.pmsensor = devices.pms
        if light:
            devices.ltm = True
        else:
            devices.ltm = devices.ltm

        repair = Repair(
            timestamp=t,
            datestring=tstring,
            user=u,
            ths=thsensor,
            ils=ilsensor,
            wss=wdsensor,
            pms=pmsensor,
            nos=nosensor,
            ltm=light
        )
        db.session.add(repair)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # 返回数据库添加前状态
        return redirect(url_for('patrol'))
    return render_template('repair.html', form=form)


@app.route('/selectrecords',methods=['GET','POST']) #查看经过条件过滤的记录页面
@login_required
def selectrecords():
    v = request.form.get('opvalue')
    if v == '1':
        records = Checkin.query.order_by(Checkin.timestamp.desc()).all()
        recordtype = '巡检'
    elif v == '2':
        records = Inspection.query.order_by(Inspection.timestamp.desc()).all()
        recordtype = '异常'
    else:
        records = Repair.query.order_by(Repair.timestamp.desc()).all()
        recordtype = '维修'
        v = '3'
    return render_template('records.html', records=records,recordtype=recordtype,rtype=v)


@app.route('/showrecord/<rtype>/<rid>')
@login_required
def showrecord(rtype,rid):

    if rtype == '1':
        return redirect(url_for('selectrecords'))
    elif rtype == '2':
        record = Inspection.query.get(int(rid))

    else :
        record = Repair.query.get(int(rid))

    return render_template('detail.html',record=record)

@app.route('/turnlight')
@login_required
def turnlight():
    light = Light.query.first()
    if light.state:
        light.state = False
    else:
        light.state = True
    db.session.commit()
    return redirect('patrol')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/monitor/<advtype>')
def monitor(advtype):
    return render_template('monitor.html',advtype=advtype)

@app.route('/advertise/<string:advtype>')
def advertise(advtype):
    return render_template('adv.html',advtype=advtype )


@app.route('/videomp4')
def videomp4():
    return send_from_directory(current_app.config['VIDEO_PATH'],'advertise.mp4')



@app.route('/logout')  #管理员退出返回
@login_required
def logout():
    logout_user()
    flash('Logout success!', 'info')
    return redirect(url_for('login'))



@csrf.exempt
@app.route('/update', methods=['GET', 'POST'])
def sensorsupdate():
    if request.method == 'POST':
        weather = Weather.query.first()
        light = Light.query.first()
        weather.temperature = request.form.get('temp')
        weather.humidity = request.form.get('humi')
        weather.illumination = request.form.get('illu')
        weather.windvelocity = request.form.get('wins')
        weather.pm2p5  = request.form.get('pm25')
        weather.noise = request.form.get('noise')
        db.session.commit()
        return jsonify(message='200 OK',state=light.state)
    return jsonify(message='404 ERR')



@app.route('/update-weather')
def update_weather():
    weather = Weather.query.first()
    humidity = weather.humidity
    temperature = weather.temperature
    illumination = weather.illumination
    windvelocity = weather.windvelocity
    pm2p5 = weather.pm2p5
    noise = weather.noise
    return jsonify(temperature = temperature,
                   humidity=humidity,
                   illumination=illumination,
                   windvelocity=windvelocity,
                   pm2p5=pm2p5,
                   noise=noise)


def gen(camera):
    """Video streaming generator function."""
    while True:
        sss, img = camera.read()
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


