import math, cmath, flask
from flask import Flask, render_template, request, session, flash, redirect, make_response
from wtforms import Form, FloatField, validators, SelectField, SubmitField, StringField, SelectMultipleField, widgets, PasswordField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import pandas.io.json
import os, webbrowser, pycountry, glob, requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from socket import gethostname

app = Flask(__name__, template_folder=u'/home/sapphirenitro/mysite')
app.secret_key = 'invigourenergy'

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="sapphirenitro",
    password="iyzadsyammil00",
    hostname="sapphirenitro.mysql.pythonanywhere-services.com",
    databasename="sapphirenitro$pvt",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#table for calculation
class Calc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)
    rmk = db.Column(db.String(100))

    gor = db.Column(db.Float(20))
    og = db.Column(db.Float(20))
    gg = db.Column(db.Float(20))
    temp = db.Column(db.Float(20))
    press = db.Column(db.Float(20))
    h2s = db.Column(db.Float(20))
    co2 = db.Column(db.Float(20))
    n2 = db.Column(db.Float(20))
    ppm = db.Column(db.Float(20))
    cor1 = db.Column(db.String(100))
    cor2 = db.Column(db.String(100))
    cor3 = db.Column(db.String(100))
    cor4 = db.Column(db.String(100))

    pb = db.Column(db.Float(20))
    rs = db.Column(db.Float(20))
    bo = db.Column(db.Float(20))
    co = db.Column(db.Float(20))
    uo = db.Column(db.Float(20))
    po = db.Column(db.Float(20))
    z = db.Column(db.Float(20))
    bg = db.Column(db.Float(20))
    pg = db.Column(db.Float(20))
    ug = db.Column(db.Float(20))
    bw = db.Column(db.Float(20))
    uw = db.Column(db.Float(20))
    pw = db.Column(db.Float(20))
    cw = db.Column(db.Float(20))
    iow = db.Column(db.Float(20))
    iog = db.Column(db.Float(20))
    iwg = db.Column(db.Float(20))

#table for pvt table input data
class TblIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)
    rmk = db.Column(db.String(100))
    cor1 = db.Column(db.String(100))
    cor2 = db.Column(db.String(100))
    cor3 = db.Column(db.String(100))
    cor4 = db.Column(db.String(100))
    stemp = db.Column(db.Float(20))
    etemp = db.Column(db.Float(20))
    stp1 = db.Column(db.Float(20))
    spress = db.Column(db.Float(20))
    epress = db.Column(db.Float(20))
    stp2 = db.Column(db.Float(20))

#table for basic lookup output
class BasicTblOut(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)

    temp = db.Column(db.Float(20))
    press = db.Column(db.Float(20))
    pb = db.Column(db.Float(20))
    rs = db.Column(db.Float(20))
    po = db.Column(db.Float(20))
    uo = db.Column(db.Float(20))
    bo = db.Column(db.Float(20))
    co = db.Column(db.Float(20))
    pg = db.Column(db.Float(20))
    ug = db.Column(db.Float(20))
    bg = db.Column(db.Float(20))
    z = db.Column(db.Float(20))
    pw = db.Column(db.Float(20))
    uw = db.Column(db.Float(20))
    bw = db.Column(db.Float(20))
    cw = db.Column(db.Float(20))
    iog = db.Column(db.Float(20))
    iwg = db.Column(db.Float(20))
    iow = db.Column(db.Float(20))

#table for lab lookup output
class LabTblOut(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)

    temp = db.Column(db.Float(20))
    press = db.Column(db.Float(20))
    pb = db.Column(db.Float(20))
    rs = db.Column(db.Float(20))
    po = db.Column(db.Float(20))
    uo = db.Column(db.Float(20))
    bo = db.Column(db.Float(20))
    co = db.Column(db.Float(20))
    pg = db.Column(db.Float(20))
    ug = db.Column(db.Float(20))
    bg = db.Column(db.Float(20))
    z = db.Column(db.Float(20))
    pw = db.Column(db.Float(20))
    uw = db.Column(db.Float(20))
    bw = db.Column(db.Float(20))
    cw = db.Column(db.Float(20))
    iog = db.Column(db.Float(20))
    iwg = db.Column(db.Float(20))
    iow = db.Column(db.Float(20))

#table for match input&output
class Matching(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)

    temp = db.Column(db.Float(20))
    pb = db.Column(db.Float(20))
    press = db.Column(db.Float(20))
    rs = db.Column(db.Float(20))
    bo = db.Column(db.Float(20))
    uo = db.Column(db.Float(20))

    pbG1 = db.Column(db.Float(20))
    pbG2 = db.Column(db.Float(20))
    pbS1 = db.Column(db.Float(20))
    pbS2 = db.Column(db.Float(20))
    pbVB1 = db.Column(db.Float(20))
    pbVB2 = db.Column(db.Float(20))
    pbP1 = db.Column(db.Float(20))
    pbP2 = db.Column(db.Float(20))
    pbAM1 = db.Column(db.Float(20))
    pbAM2 = db.Column(db.Float(20))

    rsG1 = db.Column(db.Float(20))
    rsG2 = db.Column(db.Float(20))
    rsS1 = db.Column(db.Float(20))
    rsS2 = db.Column(db.Float(20))
    rsVB1 = db.Column(db.Float(20))
    rsVB2 = db.Column(db.Float(20))
    rsP1 = db.Column(db.Float(20))
    rsP2 = db.Column(db.Float(20))
    rsAM1 = db.Column(db.Float(20))
    rsAM2 = db.Column(db.Float(20))

    boG1 = db.Column(db.Float(20))
    boG2 = db.Column(db.Float(20))
    boS1 = db.Column(db.Float(20))
    boS2 = db.Column(db.Float(20))
    boVB1 = db.Column(db.Float(20))
    boVB2 = db.Column(db.Float(20))
    boP1 = db.Column(db.Float(20))
    boP2 = db.Column(db.Float(20))
    boAM1 = db.Column(db.Float(20))
    boAM2 = db.Column(db.Float(20))

    uoBG1 = db.Column(db.Float(20))
    uoBG2 = db.Column(db.Float(20))
    uoBL1 = db.Column(db.Float(20))
    uoBL2 = db.Column(db.Float(20))

#table for chart
class Chart(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pjt = db.Column(db.String(100))
    cse = db.Column(db.Integer)

    temp = db.Column(db.Float(20))
    press = db.Column(db.Float(20))
    pb = db.Column(db.Float(20))
    rs = db.Column(db.Float(20))
    bo = db.Column(db.Float(20))
    co = db.Column(db.Float(20))
    uo = db.Column(db.Float(20))
    po = db.Column(db.Float(20))
    zf = db.Column(db.Float(20))
    bg = db.Column(db.Float(20))
    pg = db.Column(db.Float(20))
    ug = db.Column(db.Float(20))
    bw = db.Column(db.Float(20))
    uw = db.Column(db.Float(20))
    pw = db.Column(db.Float(20))
    cw = db.Column(db.Float(20))
    iow = db.Column(db.Float(20))
    iog = db.Column(db.Float(20))
    iwg = db.Column(db.Float(20))

#table for list of project&case
class pjt_cse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pjt = db.Column(db.String(100))
    cse = db.Column(db.String(100))

#table for list of project for local database only
class pjt_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    pjt = db.Column(db.String(100))

def allpjt():
    return db.session.query(pjt_cse).group_by(pjt_cse.pjt)
def allcse():
    return db.session.query(pjt_cse).group_by(pjt_cse.cse).filter((pjt_cse.pjt == session['xpjtx']) | (pjt_cse.pjt == 'Add New'))

def allpjt2():
    return db.session.query(pjt_user).group_by(pjt_user.pjt).filter((pjt_user.user == session['usern']) | (pjt_user.user == None))

#table for user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    reserv_type = db.Column(db.String(100))
    reserv_depth = db.Column(db.Float(20))
    country = db.Column(db.String(100))

    process = db.relationship('BasicTblOut', backref='case', lazy='dynamic')
    process2 = db.relationship('LabTblOut', backref='case', lazy='dynamic')
    process3 = db.relationship('Chart', backref='case', lazy='dynamic')
    process4 = db.relationship('Matching', backref='case', lazy='dynamic')
    process5 = db.relationship('Calc', backref='case', lazy='dynamic')
    process6 = db.relationship('TblIn', backref='case', lazy='dynamic')

# Model
class InputForm(Form):
    igor = FloatField(id='gor', validators=[validators.InputRequired()])
    iog = FloatField(id='og',validators=[validators.InputRequired()])
    igg = FloatField(id='gg',validators=[validators.InputRequired()])
    itemp = FloatField(id='temp',validators=[validators.InputRequired()])
    ipress = FloatField(id='press',validators=[validators.InputRequired()])
    ih2s = FloatField(id='h2s',validators=[validators.InputRequired()])
    ico2 = FloatField(id='co2',validators=[validators.InputRequired()])
    in2 = FloatField(id='n2',validators=[validators.InputRequired()])
    ippm = FloatField(id='ppm',validators=[validators.InputRequired()])

    ipb = SelectField('cpb', id='cor1', choices=[('VB','Vasquez and Beggs'),('AM','Al-Marhoun'),('G','Glaso'),
        ('PF','Petrosky and Farshasd'),('S','Standing')])
    irs = SelectField('crs', id='cor2', choices=[('VB', 'Vasquez and Beggs'), ('AM', 'Al-Marhoun'), ('G', 'Glaso'),
                                      ('PF', 'Petrosky and Farshasd'), ('S', 'Standing')])
    ibo = SelectField('cbo', id='cor3', choices=[('VB', 'Vasquez and Beggs'), ('AM', 'Al-Marhoun'), ('G', 'Glaso'),
                                      ('PF', 'Petrosky and Farshasd'), ('S', 'Standing')])
    iuo = SelectField('cuo', id='cor4', choices=[('B', 'Beal'), ('BR', 'Beggs Robinson')])
    sub = SubmitField('Calculate')
    sv = SubmitField(' ')
    cont = SubmitField('Continue')
    pjt = QuerySelectField(get_label='pjt',query_factory=allpjt,allow_blank=True,blank_text='Select Project..',default='nothing')
    cse = QuerySelectField(get_label='cse',query_factory=allcse,allow_blank=True,blank_text='Select Case..',default='nothing')
    rmk = StringField()
    pjt2 = QuerySelectField(get_label='pjt',query_factory=allpjt2,allow_blank=True,blank_text='Select Project..',default='nothing')
    cse2 = SelectField(choices=[('0','Select Case..')])
    filesub = FileField()
    subf = SubmitField('Submit')
    exp = SubmitField('Export CSV File')
    rmk2 = StringField()

# Model2
class InputForm2(Form):
    istemp = FloatField(_name='stemp', id='stemp', validators=[validators.InputRequired()])
    ietemp = FloatField(id='etemp', validators=[validators.InputRequired()])
    istp1 = FloatField(id='stp1', validators=[validators.InputRequired()])
    ispress = FloatField(id='spress', validators=[validators.InputRequired()])
    iepress = FloatField(id='epress', validators=[validators.InputRequired()])
    istp2 = FloatField(id='stp2', validators=[validators.InputRequired()])

    ipb = SelectField('cpb', id='cor1', choices=[('VB','Vasquez and Beggs'),('AM','Al-Marhoun'),('G','Glaso'),
        ('PF','Petrosky and Farshasd'),('S','Standing')])
    irs = SelectField('crs', id='cor2', choices=[('VB', 'Vasquez and Beggs'), ('AM', 'Al-Marhoun'), ('G', 'Glaso'),
                                      ('PF', 'Petrosky and Farshasd'), ('S', 'Standing')])
    ibo = SelectField('cbo', id='cor3', choices=[('VB', 'Vasquez and Beggs'), ('AM', 'Al-Marhoun'), ('G', 'Glaso'),
                                      ('PF', 'Petrosky and Farshasd'), ('S', 'Standing')])
    iuo = SelectField('cuo', id='cor4', choices=[('B', 'Beal'), ('BR', 'Beggs Robinson')])
    sv = SubmitField(' ')
    rec = SubmitField('PVT Chart')
    ree = SubmitField('PVT Eclipse')
    getmo = SubmitField('Match Data')
    getout = SubmitField('Get Output')

#Model3
class InputForm3(Form):
    newT = FloatField(id='newT', validators=[validators.InputRequired()])
    param = SelectField('prm', id='para', choices=[('pb','Pb'),('rs','Rs'),('bo','Bo'),('co','Co'),('uo','µo'),
                    ('po','ρo'),('zf','Z Factor'),('bg','Bg'),('pg','ρg'),('ug','µg'),('bw','Bw'),('uw','µw'),
                    ('pw','ρw'),('cw','Cw'),('iow','IFT oil-water'),('iwg','IFT water-gas'),('iog','IFT oil-gas')])
    sub4 = SubmitField('Generate Chart')
    sv = SubmitField(' ')
    ret = SubmitField('PVT Table')
    ree = SubmitField('PVT Eclipse')

#Model4
class InputForm4(Form):
    restemp = FloatField(id='restemp', validators=[validators.InputRequired()])
    wrefpress = FloatField(id='wrefpress', validators=[validators.InputRequired()])
    sub2 = SubmitField('Export Text File')
    sv = SubmitField(' ')
    rec = SubmitField('PVT Chart')
    ret = SubmitField('PVT Table')

#Model5
class InputForm5(Form):
    mtemp = FloatField(id='mtemp', validators=[validators.InputRequired()])
    mbppress = FloatField(id='mbppress', validators=[validators.InputRequired()])
    mpress = FloatField(id='mpress', validators=[validators.InputRequired()])
    mrrs = FloatField(id='mrrs', validators=[validators.InputRequired()])
    mbbo = FloatField(id='mbbo', validators=[validators.InputRequired()])
    muo = FloatField(id='muo', validators=[validators.InputRequired()])
    sub3 = SubmitField('Match Data')
    sv = SubmitField(' ')
    cont = SubmitField('Get Output')

#Overriding SelectMultipleField into list of checkboxes
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Model7
class InputForm7(Form):
    usern = StringField(id='usern', validators=[validators.InputRequired()])
    passw = PasswordField(id='passw', validators=[validators.InputRequired()])
    log = SubmitField('Login')
    logout = SubmitField('Logout')

#Override selectfield to get dropdown list of country
class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(c.alpha_3, c.name) for c in pycountry.countries]

#Model8
class InputForm8(Form):
    gname = StringField(id='gname', validators=[validators.InputRequired()])
    email = StringField(id='email', validators=[validators.InputRequired()])
    rt = SelectField('rt', id='rt', choices=[('SS', 'Sandstone'), ('CN', 'Carbonate')])
    rd = FloatField(id='rd', validators=[validators.InputRequired()])
    ctry = CountrySelectField()
    log = SubmitField('Login')

#Model9
class InputForm9(Form):
    fn = StringField(id='fn')
    sub = SubmitField('Submit')
    t1 = FileField()
    t2 = FileField()
    t3 = FileField()
    t4 = FileField()
    t5 = FileField()
    t6 = FileField()

@app.route('/Menu',methods=['GET', 'POST'])
def showmenu():
    exf2 = InputForm7(request.form)
    user_right_now = session['type']

    if exf2.logout.data:
        session.clear()
        flash('Log out Successful!')
        return redirect('/')

    return render_template('index.html',user_right_now = user_right_now,exf2=exf2)

@app.route('/',methods=['GET', 'POST'])
def showlogin():
    form = InputForm7(request.form)

    if request.method == 'POST' and form.validate():

        if form.usern.data == 'admin':
            if form.passw.data == 'admin':
                session['type'] = 'Admin'
                session['usern'] = form.usern.data

                flash('Log in Successful!')
                return redirect('/PVT Menu')
            else:
                flash('Wrong Password!')
        else:
            flash('Wrong Username and Password!')

    return render_template('login.html',form=form)

@app.route('/Guest',methods=['GET', 'POST'])
def showguest():
    form = InputForm8(request.form)
    session['type'] = 'Guest'

    if request.method == 'POST' and form.validate():
        user = User(type=session['type'],name=form.gname.data,email=form.email.data,reserv_type=form.rt.data,
                            reserv_depth=form.rd.data,country=form.ctry.data)
        db.session.add(user)
        db.session.flush()
        session['pid'] = user.id
        db.session.commit()
        flash('Information Saved')
        return redirect('/PVT Menu')

    return render_template('guest.html',form=form)

@app.route('/PVT Menu',methods=['GET', 'POST'])
def showpvtmenu():
    exf2 = InputForm7(request.form)

    session['mpb1'] = 1
    session['mpb2'] = 1
    session['mpb3'] = 1
    session['mpb4'] = 1
    session['mpb5'] = 1
    session['cpb1'] = 0
    session['cpb2'] = 0
    session['cpb3'] = 0
    session['cpb4'] = 0
    session['cpb5'] = 0

    session['mrs1'] = 1
    session['mrs2'] = 1
    session['mrs3'] = 1
    session['mrs4'] = 1
    session['mrs5'] = 1
    session['crs1'] = 0
    session['crs2'] = 0
    session['crs3'] = 0
    session['crs4'] = 0
    session['crs5'] = 0

    session['mbo1'] = 1
    session['mbo2'] = 1
    session['mbo3'] = 1
    session['mbo4'] = 1
    session['mbo5'] = 1
    session['cbo1'] = 0
    session['cbo2'] = 0
    session['cbo3'] = 0
    session['cbo4'] = 0
    session['cbo5'] = 0

    session['muo1'] = 1
    session['muo2'] = 1
    session['cuo1'] = 0
    session['cuo2'] = 0

    session['mtemp'] = None
    session['mbppress'] = None
    session['mpress'] = None
    session['mrrs'] = None
    session['mbbo'] = None
    session['muo'] = None

    session['pss'] = 0

    return render_template('pvtmenu.html',exf2=exf2)

#display sensitivity analysis
@app.route('/SenS',methods=['GET', 'POST'])
def showsens():

    if session['type'] == 'Admin':
        # Extra model for local database sensitivity
        class InputForm66(Form):
            #file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(session['xpjtx'])
            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(session['xpjtx']) + '.csv'
            rawlist = pd.read_csv(file_name)
            cslist = rawlist[rawlist.chartprm == str(session['chtchoice'])]
            intcslist = cslist['cse'].tolist()
            intcslist = [int(i) for i in intcslist]
            cslists = [(x, x) for x in intcslist]
            cscheck = MultiCheckboxField(choices=cslists, default=intcslist)
            plot = SubmitField('Plot')
        form = InputForm66(request.form)

    elif session['type'] == 'Guest':
        #Model6  <--- put here instead of outside route for getting the session data
        class InputForm6(Form):
            db.session.close()
            try:
                senpjt = session['senpjt']
                cslist = pd.read_sql_query("SELECT cse FROM chart WHERE pjt = '%s' " % (senpjt), app.config['SQLALCHEMY_DATABASE_URI'])
                cslists = [(x, x) for x in cslist['cse'].drop_duplicates().tolist()]
                cscheck = MultiCheckboxField(choices=cslists,default=cslist['cse'].drop_duplicates().tolist())
            finally:
                db.session.close()
            plot = SubmitField('Plot')
        form = InputForm6(request.form)

    #the start of code for this route
    exf2 = InputForm7(request.form)
    senchoice = session['chtchoice']

    plt.rcParams.update({'font.size': 13})
    fig, ax = plt.subplots()
    ax.set_ylabel('Parameter')
    ax.set_xlabel('Pressure')
    html = mpld3.fig_to_html(fig)

    if exf2.logout.data:
        session.clear()
        flash('Log out Successful!')
        return redirect('/')

    if request.method == 'POST':

        lbl = []
        pl = []
        i = 0

        if session['type'] == 'Admin':

            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(session['xpjtx']) + '.csv'
            try:
                plotdf = pd.read_csv(file_name)
                sensdf = pd.DataFrame(data=[],columns=['cse','temp','press','pb','rs','bo','co','uo','po','zf','bg'
                                                   ,'pg','ug','bw','uw','pw','cw','iow','iog','iwg'])

                for k in range(len(plotdf.index)):
                    finalpb = 0
                    ingor = plotdf.loc[int(k), 'gor']
                    inog = plotdf.loc[int(k), 'og']
                    ingg = plotdf.loc[int(k), 'gg']
                    inh2s = plotdf.loc[int(k), 'h2s']
                    inco2 = plotdf.loc[int(k), 'co2']
                    inn2 = plotdf.loc[int(k), 'n2']
                    inppm = plotdf.loc[int(k), 'ppm']
                    pss = pd.Series(np.linspace(plotdf.loc[int(k), 'spress'],plotdf.loc[int(k), 'epress'],
                            plotdf.loc[int(k), 'step2']+1,(plotdf.loc[int(k), 'epress'] - plotdf.loc[int(k), 'spress'])
                            / plotdf.loc[int(k), 'step2'])).to_json(orient='values')
                    ps = pandas.io.json.read_json(pss)
                    cor1 = plotdf.loc[int(k), 'calcor1']
                    cor2 = plotdf.loc[int(k), 'calcor2']
                    cor3 = plotdf.loc[int(k), 'calcor3']
                    cor4 = plotdf.loc[int(k), 'calcor4']

                    mgpb = plotdf.loc[int(k), 'p1gpb']
                    mspb = plotdf.loc[int(k), 'p1spb']
                    mvbpb = plotdf.loc[int(k), 'p1vbpb']
                    mpfpb = plotdf.loc[int(k), 'p1pfpb']
                    mampb = plotdf.loc[int(k), 'p1ampb']
                    cgpb = plotdf.loc[int(k), 'p2gpb']
                    cspb = plotdf.loc[int(k), 'p2spb']
                    cvbpb = plotdf.loc[int(k), 'p2vbpb']
                    cpfpb = plotdf.loc[int(k), 'p2pfpb']
                    campb = plotdf.loc[int(k), 'p2ampb']

                    mgrs = plotdf.loc[int(k), 'p1grs']
                    msrs = plotdf.loc[int(k), 'p1srs']
                    mvbrs = plotdf.loc[int(k), 'p1vbrs']
                    mpfrs = plotdf.loc[int(k), 'p1pfrs']
                    mamrs = plotdf.loc[int(k), 'p1amrs']
                    cgrs = plotdf.loc[int(k), 'p2grs']
                    csrs = plotdf.loc[int(k), 'p2srs']
                    cvbrs = plotdf.loc[int(k), 'p2vbrs']
                    cpfrs = plotdf.loc[int(k), 'p2pfrs']
                    camrs = plotdf.loc[int(k), 'p2amrs']

                    mgbo = plotdf.loc[int(k), 'p1gbo']
                    msbo = plotdf.loc[int(k), 'p1sbo']
                    mvbbo = plotdf.loc[int(k), 'p1vbbo']
                    mpfbo = plotdf.loc[int(k), 'p1pfbo']
                    mambo = plotdf.loc[int(k), 'p1ambo']
                    cgbo = plotdf.loc[int(k), 'p2gbo']
                    csbo = plotdf.loc[int(k), 'p2sbo']
                    cvbbo = plotdf.loc[int(k), 'p2vbbo']
                    cpfbo = plotdf.loc[int(k), 'p2pfbo']
                    cambo = plotdf.loc[int(k), 'p2ambo']

                    mbguo = plotdf.loc[int(k), 'p1bguo']
                    mbluo = plotdf.loc[int(k), 'p1bluo']
                    cbguo = plotdf.loc[int(k), 'p2bguo']
                    cbluo = plotdf.loc[int(k), 'p2bluo']

                    ntemp = plotdf.loc[int(k), 'charttemp']

                    pf = pd.Index(ps)
                    inws = inppm / 1000000 * 100

                    data = np.zeros_like(pf)
                    data = data.astype(float)
                    px = np.array(data).ravel()
                    px = pd.Series(px)
                    tx = np.array(data).ravel()
                    tx = pd.Series(tx)
                    xfinalpb = np.array(data).ravel()
                    xfinalpb = pd.Series(xfinalpb)
                    xfinalrs = np.array(data).ravel()
                    xfinalrs = pd.Series(xfinalrs)
                    xfinalco = np.array(data).ravel()
                    xfinalco = pd.Series(xfinalco)
                    xfinalbw = np.array(data).ravel()
                    xfinalbw = pd.Series(xfinalbw)
                    xfinalbo = np.array(data).ravel()
                    xfinalbo = pd.Series(xfinalbo)
                    xfinaluo = np.array(data).ravel()
                    xfinaluo = pd.Series(xfinaluo)
                    finalpo = np.array(data).ravel()
                    finalpo = pd.Series(finalpo)
                    finalz = np.array(data).ravel()
                    finalz = pd.Series(finalz)
                    gfvf = np.array(data).ravel()
                    gfvf = pd.Series(gfvf)
                    gd = np.array(data).ravel()
                    gd = pd.Series(gd)
                    gv = np.array(data).ravel()
                    gv = pd.Series(gv)
                    finaluw = np.array(data).ravel()
                    finaluw = pd.Series(finaluw)
                    finalpw = np.array(data).ravel()
                    finalpw = pd.Series(finalpw)
                    finalcw = np.array(data).ravel()
                    finalcw = pd.Series(finalcw)
                    fiow = np.array(data).ravel()
                    fiow = pd.Series(fiow)
                    fiog = np.array(data).ravel()
                    fiog = pd.Series(fiog)
                    fiwg = np.array(data).ravel()
                    fiwg = pd.Series(fiwg)

                    for i in range(len(ps)):
                        if cor1 == "VB":
                            if inog <= 30:
                                xfinalpb[i] = ((27.64 * ingor / ingg) * 10 ** ((-11.172 * inog) / (ntemp + 460))) ** (
                                1 / 1.0937)
                            else:
                                xfinalpb[i] = ((56.06 * ingor / ingg) * 10 ** ((-10.393 * inog) / (ntemp + 460))) ** (
                                1 / 1.187)
                            xfinalpb[i] = mvbpb * xfinalpb[i] + cvbpb
                        elif cor1 == "AM":
                            xfinalpb[i] = 0.00538088 * ingor ** 0.715082 * ingg ** -1.87784 * (141.5 / (
                            inog + 131.5)) ** 3.1437 * \
                                          (ntemp + 460) ** 1.32657
                            xfinalpb[i] = mampb * xfinalpb[i] + campb
                        elif cor1 == "G":
                            x = (ingor / ingg) ** 0.816 * ((ntemp ** 0.172) / (inog ** 0.989))
                            logpb = 1.7669 + 1.7447 * math.log10(x) - (0.30218 * (math.log10(x) ** 2))
                            xfinalpb[i] = 10 ** logpb
                            xfinalpb[i] = mgpb * xfinalpb[i] + cgpb
                        elif cor1 == "PF":
                            x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * ntemp ** 1.3911)
                            xfinalpb[i] = ((112.727 * ingor ** 0.577421) / (ingg ** 0.8439 * 10 ** x)) - 1391.051
                            xfinalpb[i] = mpfpb * xfinalpb[i] + cpfpb
                        elif cor1 == "S":
                            xfinalpb[i] = 18.2 * (
                            (ingor / ingg) ** 0.83 * 10 ** (0.00091 * ntemp - 0.0125 * inog) - 1.4)
                            xfinalpb[i] = mspb * xfinalpb[i] + cspb

                        if pf[i] <= 14.7:
                            xfinalrs[i] = 0
                        else:
                            if pf[i] < xfinalpb[i]:
                                if cor2 == "VB":
                                    if inog <= 30:
                                        xfinalrs[i] = 0.0362 * ingg * pf[i] ** 1.0937 * (math.exp(25.724 * inog / (ntemp + 460)))
                                    else:
                                        xfinalrs[i] = 0.0178 * ingg * pf[i] ** 1.187 * (math.exp(23.931 * inog / (ntemp + 460)))
                                    xfinalrs[i] = mvbrs * xfinalrs[i] + cvbrs
                                elif cor2 == "AM":
                                    xfinalrs[i] = ((185.8432 * ingg ** 1.87784) * (
                                    (141.5 / (inog + 131.5)) ** -3.1437) * ((ntemp + 460) ** -1.32657) * pf[i]) ** 1.398441
                                    xfinalrs[i] = mamrs * xfinalrs[i] + camrs
                                elif cor2 == "G":
                                    x = 2.8869 - (14.1811 - 3.3093 * np.log10(pf[i])) ** 0.5
                                    logrs = 10 ** x
                                    xfinalrs[i] = ingg * (((inog ** 0.989) / (ntemp ** 0.172)) * logrs) ** 1.2255
                                    xfinalrs[i] = mgrs * xfinalrs[i] + cgrs
                                elif cor2 == "PF":
                                    x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * ntemp ** 1.3911)
                                    xfinalrs[i] = ((((pf[i] / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** x) ** 1.73184)
                                    xfinalrs[i] = mpfrs * xfinalrs[i] + cpfrs
                                elif cor2 == "S":
                                    x = 0.0125 * inog - 0.00091 * ntemp
                                    xfinalrs[i] = ingg * (((pf[i] / 18.2) + 1.4) * 10 ** x) ** 1.2048
                                    xfinalrs[i] = msrs * xfinalrs[i] + csrs
                            else:
                                xfinalrs[i] = ingor

                        if pf[i] > xfinalpb[i]:
                            # VB
                            xfinalco[i] = ((-1433) + (5 * xfinalrs[i]) + (17.2 * ntemp) - (1180 * ingg) + (
                            12.61 * inog)) / ((10 ** 5) * pf[i])
                        elif pf[i] < xfinalpb[i]:
                            # Mcain
                            xfinalco[i] = np.exp(-7.573 - (1.45 * np.log(pf[i])) - (0.383 * np.log(xfinalpb[i]))
                                            + (1.402 * math.log((ntemp + 460)) + (0.256 * math.log(inog)) + (0.449 * np.log(ingor))))

                        # water fvf
                        A1 = 0.9911 + (6.35 * 10 ** -5) * ntemp + (8.5 * 10 ** -7 * ntemp ** 2)
                        A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * ntemp + (
                            4.57 * 10 ** -12 * ntemp ** 2)
                        A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * ntemp + (
                            -1.43 * 10 ** -15 * ntemp ** 2)
                        xfinalbw[i] = A1 + A2 * pf[i] + A3 * pf[i] ** 2

                        if cor3 == "VB":
                            if pf[i] <= 14.7 and ntemp == 60:
                                xfinalbo[i] = 1
                            elif pf[i] <= xfinalpb[i]:
                                if inog <= 30:
                                    xfinalbo[i] = 1 + 0.0004677 * xfinalrs[i] + (ntemp - 60) * (inog / ingg) * (
                                    0.00001751 + (-1.811 * 10 ** -8) * xfinalrs[i])
                                else:
                                    xfinalbo[i] = 1 + 0.000467 * xfinalrs[i] + (ntemp - 60) * (inog / ingg) * (
                                        0.000011 + (1.337 * 10 ** -9) * xfinalrs[i])
                                xfinalbo[i] = mvbbo * xfinalbo[i] + cvbbo
                            elif pf[i] > xfinalpb[i]:
                                if inog <= 30:
                                    xfinalbo[i] = 1 + 0.0004677 * xfinalrs[i] + (ntemp - 60) * (inog / ingg) * (
                                    0.00001751 + (-1.811 * 10 ** -8) * xfinalrs[i])
                                else:
                                    xfinalbo[i] = 1 + 0.000467 * xfinalrs[i] + (ntemp - 60) * (inog / ingg) * (
                                        0.000011 + (1.337 * 10 ** -9) * xfinalrs[i])
                                xfinalbo[i] = xfinalbo[i] * (1 - float(xfinalco[i]) * (pf[i] - xfinalpb[i]))
                                xfinalbo[i] = mvbbo * xfinalbo[i] + cvbbo
                        elif cor3 == "AM":
                            if pf[i] <= 14.7 and ntemp == 60:
                                xfinalbo[i] = 1
                            elif pf[i] <= xfinalpb[i]:
                                bob = xfinalrs[i] ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                                xfinalbo[i] = 0.497069 + (0.862963 * 10 ** -3 * (ntemp + 460)) + (
                                0.182594 * 10 ** -2 * bob) + (0.318099 * 10 ** -5 * bob ** 2)
                                xfinalbo[i] = mambo * xfinalbo[i] + cambo
                            elif pf[i] > xfinalpb[i]:
                                bob = xfinalrs[i] ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                                xfinalbo[i] = 0.497069 + (0.862963 * 10 ** -3 * (ntemp + 460)) + (
                                0.182594 * 10 ** -2 * bob) + (0.318099 * 10 ** -5 * bob ** 2)
                                xfinalbo[i] = xfinalbo[i] * (1 - float(xfinalco[i]) * (pf[i] - xfinalpb[i]))
                                xfinalbo[i] = mambo * xfinalbo[i] + cambo
                        elif cor3 == "G":
                            if pf[i] <= 14.7 and ntemp == 60:
                                xfinalbo[i] = 1
                            elif pf[i] <= xfinalpb[i]:
                                bob = (xfinalrs[i] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * ntemp)
                                A = -6.58511 + 2.91329 * np.log10(bob) - 0.27683 * (np.log10(bob) ** 2)
                                xfinalbo[i] = 1 + 10 ** A
                                xfinalbo[i] = mgbo * xfinalbo[i] + cgbo
                            elif pf[i] > xfinalpb[i]:
                                bob = (xfinalrs[i] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * ntemp)
                                A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                                xfinalbo[i] = 1 + 10 ** A
                                xfinalbo[i] = xfinalbo[i] * (1 - float(xfinalco[i]) * (pf[i] - xfinalpb[i]))
                                xfinalbo[i] = mgbo * xfinalbo[i] + cgbo
                        elif cor3 == "PF":
                            if pf[i] <= 14.7 and ntemp == 60:
                                xfinalbo[i] = 1
                            elif pf[i] <= xfinalpb[i]:
                                xfinalbo[i] = 1.0113 + 7.2046 * (10 ** -5) * (xfinalrs[i] ** 0.3738 * (
                                    ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                    ntemp) ** 0.5371) ** 3.0936
                                xfinalbo[i] = mpfbo * xfinalbo[i] + cpfbo
                            elif pf[i] > xfinalpb[i]:
                                xfinalbo[i] = 1.0113 + 7.2046 * (10 ** -5) * (xfinalrs[i] ** 0.3738 * (
                                    ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                                                              ntemp) ** 0.5371) ** 3.0936
                                xfinalbo[i] = xfinalbo[i] * (1 - float(xfinalco[i]) * (pf[i] - xfinalpb[i]))
                                xfinalbo[i] = mpfbo * xfinalbo[i] + cpfbo
                        elif cor3 == "S":
                            if pf[i] <= 14.7 and ntemp == 60:
                                xfinalbo[i] = 1
                            elif pf[i] <= xfinalpb[i]:
                                xfinalbo[i] = 0.9759 + 0.00012 * (xfinalrs[i] * (
                                    ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * ntemp) ** 1.2
                                xfinalbo[i] = msbo * xfinalbo[i] + csbo
                            elif pf[i] > xfinalpb[i]:
                                xfinalbo[i] = 0.9759 + 0.00012 * (xfinalrs[i] * (ingg / (141.5 / (inog + 131.5)))
                                                                  ** 0.5 + 1.25 * ntemp) ** 1.2
                                xfinalbo[i] = xfinalbo[i] * (1 - float(xfinalco[i]) * (pf[i] - xfinalpb[i]))
                                xfinalbo[i] = msbo * xfinalbo[i] + csbo

                        if cor4 == "B":
                            aa = 10 ** (0.43 + (8.33 / inog))
                            deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (ntemp + 200)) ** aa

                            if pf[i] < xfinalpb[i]:
                                aaa = 10.715 * (xfinalrs[i] + 100) ** -0.515
                                bbb = 5.44 * (xfinalrs[i] + 150) ** -0.338
                                xfinaluo[i] = aaa * deadoil ** bbb
                            elif pf[i] > xfinalpb[i]:
                                aaa = 10.715 * (xfinalrs[i] + 100) ** -0.515
                                bbb = 5.44 * (xfinalrs[i] + 150) ** -0.338
                                xfinaluo[i] = aaa * deadoil ** bbb
                                ass = (-3.9 * (10 ** -5) * pf[i]) - 5
                                m = 2.6 * pf[i] ** 1.187 * 10 ** ass
                                xfinaluo[i] = xfinaluo[i] * (pf[i] / xfinalpb[i]) ** m
                            xfinaluo[i] = mbluo * xfinaluo[i] + cbluo
                        elif cor4 == "BR":
                            zz = 3.0324 - 0.02023 * inog
                            yy = 10 ** zz
                            xx = yy * (ntemp) ** -1.163
                            deadoil = (3.141 * (10 ** 10)) * (ntemp ** -3.444) * (math.log10(inog)) ** (
                                10.313 * (math.log10(ntemp)) - 36.447)

                            if pf[i] < xfinalpb[i]:
                                aaa = 10.715 * (xfinalrs[i] + 100) ** -0.515
                                bbb = 5.44 * (xfinalrs[i] + 150) ** -0.338
                                xfinaluo[i] = aaa * deadoil ** bbb
                            elif pf[i] > xfinalpb[i]:
                                aaa = 10.715 * (xfinalrs[i] + 100) ** -0.515
                                bbb = 5.44 * (xfinalrs[i] + 150) ** -0.338
                                xfinaluo[i] = aaa * deadoil ** bbb
                                ass = (-3.9 * (10 ** -5) * pf[i]) - 5
                                m = 2.6 * pf[i] ** 1.187 * 10 ** ass
                                xfinaluo[i] = xfinaluo[i] * (pf[i] / xfinalpb[i]) ** m
                            xfinaluo[i] = mbguo * xfinaluo[i] + cbguo

                        finalpo[i] = ((62.4 * (141.5 / (inog + 131.5))) + (0.0136 * xfinalrs[i] * ingg)) / xfinalbo[i]

                        xg = 1 - inn2 - inco2 - inh2s
                        gamghc = (ingg - 0.967 * inn2 - 1.52 * inco2 - 1.18 * inh2s) / xg
                        tpchc = 168 + 325 * gamghc - 12.5 * gamghc ** 2
                        ppchc = 677 + gamghc * (15 - 37.5 * gamghc)
                        tpcm = xg * tpchc + 227 * inn2 + 548 * inco2 * 672 * inh2s
                        ppcm = xg * ppchc + 493 * inn2 + 1071 * inco2 + 1036 * inh2s
                        epslon = 120 * (xg ** 0.9 - xg ** 1.6) + 15 * (inco2 ** 0.5 - inh2s ** 4)
                        tpc = tpcm - epslon
                        ppc = ppcm * (tpc / (tpcm + inh2s * (1 - inh2s) * epslon))
                        tpr = (ntemp + 460) / tpc

                        ppr = pf[i] / ppc
                        AA = 1.39 * (tpr - 0.92) ** 0.5 - 0.36 * tpr - 0.101
                        BB = (0.62 - 0.23 * tpr) * ppr + (0.066 / (tpr - 0.86) - 0.037) * ppr ** 2 + 0.32 / 10 ** (
                            9 * (tpr - 1)) * ppr ** 6
                        CC = 0.132 - 0.32 * np.log10(tpr)
                        DD = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
                        finalz[i] = AA + ((1 - AA) / np.exp(BB)) + (CC * ppr ** DD)

                        ppr = pf[i] / ppc

                        E = 35.37 * pf[i] / (finalz[i] * (ntemp + 460))
                        gfvf[i] = 1 / E

                        gd[i] = (28.97 * pf[i] * ingg) / (finalz[i] * 10.7316 * (ntemp + 460))

                        ugas1 = 0.001 * (8.1888 - 6.15 * math.log10(ingg) + (0.01709 - 0.002062 * ingg) * ntemp)
                        gv[i] = math.exp(
                            -2.4621182 + ppr * (2.97054714 + ppr * (-0.286264054 + ppr * 0.00805420522)) + tpr * (
                                2.80860949 + ppr * (-3.49803305 + ppr * (0.36037302 + ppr * -0.0104432413)) + tpr * (
                                    -0.793385684 + ppr * (
                                    1.39643306 + ppr * (-0.149144925 + ppr * 0.00441015512)) + tpr *
                                    (0.0839387178 + ppr * (
                                    -0.186408848 + ppr * (0.0203367881 + ppr * -0.000609579263)))))) / tpr * ugas1

                        finaluw[i] = math.exp(1.003 - (1.479 * 10 ** -2 * ntemp) + (1.982 * 10 ** -5 * ntemp ** 2))

                        pwsc = 62.368 + (0.438603 * inws) + (1.60074 * 10 ** -3 * inws)
                        finalpw[i] = pwsc / xfinalbw[i]

                        C1 = 3.8546 - 0.000134 * pf[i]
                        C2 = -0.01052 + 4.77 * 10 ** -7 * pf[i]
                        C3 = (3.9267 * 10 ** -5) - (8.8 * 10 ** -10 * pf[i])
                        finalcw[i] = (C1 + C2 * ntemp + C3 * ntemp ** 2) * 10 ** -6

                        fiow[i] = 30

                        ido = (1.17013 - (1.694 * 10 ** -3 * ntemp)) * (38.085 - 0.259 * inog)
                        fiog[i] = ido * (0.056379 + (0.94362 * np.exp(-3.8491 * 10 ** -3 * xfinalrs[i])))

                        Wdens = finalpw[i] * 0.0160185
                        Gdens = gd[i] * 0.0160185
                        fiwg[i] = ((1.53988 * (Wdens - Gdens) + 2.08339) / (((ntemp + 460) / 302.881) ** (0.821976 - 1.83785 *
                        10 ** -3 * (ntemp + 460) + 1.34016 * 10 ** -6 * (ntemp + 460) ** 2))) ** 3.6667
                        px[i] = pf[i]

                        sensdf = sensdf.append(pd.Series([k+1,ntemp,px[i],xfinalpb[i],xfinalrs[i],xfinalbo[i],
                                            xfinalco[i],xfinaluo[i],finalpo[i],finalz[i],gfvf[i],gd[i],
                                            gv[i],xfinalbw[i],finaluw[i],finalpw[i],finalcw[i],fiow[i],
                                            fiog[i],fiwg[i]],index=['cse','temp','press','pb','rs','bo','co','uo','po','zf','bg'
                                            ,'pg','ug','bw','uw','pw','cw','iow','iog','iwg']),ignore_index=True)

            except FileNotFoundError:
                pass

            i = 0
            while i in range(len("".join(form.cscheck.data)) - 1):
                pt = ax.plot(sensdf[sensdf.cse==i+1]['press'], sensdf[sensdf.cse==i+1][str(senchoice)], '-o')
                pl.append(pt)
                lbl.append('Case ' + str(int("".join(form.cscheck.data)[i])))
                print(True)
                i = i + 1

            i = int("".join(form.cscheck.data)[-1])
            pt = ax.plot(sensdf[sensdf.cse==i]['press'], sensdf[sensdf.cse==i][str(senchoice)], '-o')
            pl.append(pt)
            lbl.append('Case ' + str(i))
            plugins.connect(fig, plugins.InteractiveLegendPlugin(pl, lbl))
            html = mpld3.fig_to_html(fig)

        elif session['type'] == 'Guest':
            while i in range(len("".join(form.cscheck.data)) - 1):
                rd1 = pd.read_sql_query("SELECT press, "+str(senchoice)+" FROM chart WHERE cse = " + str(int("".join(form.cscheck.data)[i])),
                                        app.config['SQLALCHEMY_DATABASE_URI'])
                pt = ax.plot(rd1['press'], rd1[str(senchoice)], '-o')
                pl.append(pt)
                lbl.append('Case ' + str(int("".join(form.cscheck.data)[i])))
                i = i + 1

            i = int("".join(form.cscheck.data)[-1])
            rd1 = pd.read_sql_query("SELECT press, "+str(senchoice)+" FROM chart WHERE cse = " + str(i),
                                    app.config['SQLALCHEMY_DATABASE_URI'])
            pt = ax.plot(rd1['press'], rd1[str(senchoice)], '-o')
            pl.append(pt)
            lbl.append('Case ' + str(i))
            plugins.connect(fig, plugins.InteractiveLegendPlugin(pl, lbl))
            html = mpld3.fig_to_html(fig)

    return render_template('sens.html',html=html,form=form,exf2=exf2)

@app.route("/gdbview",methods=['GET', 'POST'])
def viewgdb():
    t1 = pd.read_sql(db.session.query(Calc).statement,db.session.bind)
    t1.set_index('id',inplace=True)
    t1 = t1.rename_axis(None)
    t2 = pd.read_sql(db.session.query(TblIn).statement, db.session.bind)
    t2.set_index('id', inplace=True)
    t2 = t2.rename_axis(None)
    t3 = pd.read_sql(db.session.query(BasicTblOut).statement, db.session.bind)
    t3.set_index('id', inplace=True)
    t3 = t3.rename_axis(None)
    t4 = pd.read_sql(db.session.query(LabTblOut).statement, db.session.bind)
    t4.set_index('id', inplace=True)
    t4 = t4.rename_axis(None)
    t5 = pd.read_sql(db.session.query(Matching).statement, db.session.bind)
    t5.set_index('id', inplace=True)
    t5 = t5.rename_axis(None)
    t6 = pd.read_sql(db.session.query(Chart).statement, db.session.bind)
    t6.set_index('id', inplace=True)
    t6 = t6.rename_axis(None)

    return render_template('guestdb.html',tables=[t1.to_html(classes='t1'),t2.to_html(classes='t2'),t3.to_html(classes='t3'),
                            t4.to_html(classes='t4'),t5.to_html(classes='t5'),t6.to_html(classes='t6')],
                           titles=['','1. Calculation Input and Output', '2. Input Used for PVT Table Data','3. PVT Table Data without Lab Data',
                            '4. PVT Table Data with Lab Data', '5. Matching Input and Output', '6. PVT Chart Data'])

@app.route('/NewApp',methods=['GET', 'POST'])
def shownewapp():
    #declaration/initilize which form to use
    form = InputForm(request.form)
    form2 = InputForm2(request.form)
    form3 = InputForm3(request.form)
    form4 = InputForm4(request.form)
    form5 = InputForm5(request.form)
    exf2 = InputForm7(request.form)

    # declaration/initilization of variables used
    html=''
    session['check'] = ''
    session['saved'] = ''
    xfinalpb = ""
    xfinalrs = ""
    xfinalbo = ""
    xfinalco = ""
    xfinaluo = ""
    xfinalpo = ""
    xfinalz = ""
    xgfvf = ""
    xgd = ""
    xgv = ""
    xfinalbw = ""
    xfinaluw = ""
    xfinalpw = ""
    xfinalcw = ""
    fiow = ""
    xfiog = ""
    xfiwg = ""
    session['xpjtx'] = ''

    if form.subf.data:
        file = request.files[form.filesub.name]
        filedata = pd.read_csv(file)
        filedata.to_csv('/home/sapphirenitro/mysite/pvtcsv/' + str(file.filename),index=False)
        flash('Load CSV File Completed!')
        return redirect('/NewApp')

    #conditional statement to enable pop up for adding new project/case when 'Add New' is selected
    if request.method == 'POST':

        if session['type'] == 'Admin':

            if form.pjt2.data == None:
                pass
            # conditional statement for loading input data
            elif form.pjt2.data.pjt != None and form.pjt2.data.pjt != 'Add New':
                def allcse2():
                    filecs = []
                    try:
                        filecs.append('Select Case..')
                        filecs.append('Add New')
                        readcs = pd.read_csv('/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv')
                        intcs = readcs['cse'].tolist()
                        intcs = [int(i) for i in intcs]
                        filecs.extend(intcs)
                        filecs = [(y, y) for y in filecs]
                        filecs[0] = ('0', 'Select Case..')
                    except FileNotFoundError:
                        pass
                    return filecs
                form.cse2.choices = allcse2()
                session['xpjtx'] = form.pjt2.data.pjt

            if form.cse2.data == '0':
                pass
            elif form.cse2.data != None and form.cse2.data != 'Add New':
                #file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data)
                file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
                # will load input fields for the selected case if it exists
                try:
                    lodf = pd.read_csv(file_name)
                    if pd.isnull(lodf.loc[int(form.cse2.data) - 1, 'gor']):
                        pass
                    else:
                        form.igor.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'gor'])]
                        form.iog.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'og'])]
                        form.igg.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'gg'])]
                        form.itemp.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'temp'])]
                        form.ipress.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'press'])]
                        form.ih2s.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'h2s'])]
                        form.ico2.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'co2'])]
                        form.in2.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'n2'])]
                        form.ippm.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'ppm'])]

                    if pd.isnull(lodf.loc[int(form.cse2.data) - 1, 'mtemp']):
                        pass
                    else:
                        form5.mtemp.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mtemp'])]
                        form5.mbppress.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mbppress'])]
                        form5.mpress.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mpress'])]
                        form5.mrrs.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mrs'])]
                        form5.mbbo.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mbo'])]
                        form5.muo.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'muo'])]

                    if pd.isnull(lodf.loc[int(form.cse2.data) - 1, 'charttemp']):
                        pass
                    else:
                        form3.newT.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'charttemp'])]

                except FileNotFoundError:
                    pass

            if request.form['npjt'] == '':
                pass
            elif request.form['npjt'] != None:
                #file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(request.form['npjt']) + '.csv'
                file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(request.form['npjt']) + '.csv'
                newdf = pd.DataFrame(data=[],columns=['pjt','cse','rmk','gor','og','gg','temp','press','h2s','co2','n2','ppm','calcor1','calcor2','calcor3',
                                                      'calcor4','mbo','mbppress','mpress','mrs','mtemp','muo','p1ambo','p1ampb','p1amrs','p1bguo','p1bluo',
                                                      'p1gbo','p1gpb','p1grs','p1pfbo','p1pfpb','p1pfrs','p1sbo','p1spb','p1srs','p1vbbo','p1vbpb','p1vbrs',
                                                      'p2ambo','p2ampb','p2amrs','p2bguo','p2bluo','p2gbo','p2gpb','p2grs','p2pfbo','p2pfpb','p2pfrs','p2sbo',
                                                      'p2spb','p2srs','p2vbbo','p2vbpb','p2vbrs','epress','etemp','spress','stemp','step1','step2','chartprm','charttemp'])
                newdf.to_csv(file_name,index=False)
                add_new = pjt_user(user=session['usern'], pjt=request.form['npjt'])
                db.session.add(add_new)
                db.session.commit()
                form.pjt2.choices = allpjt2()
                return redirect('NewApp')

            if request.form['ncse'] == '':
                pass
            elif request.form['ncse'] != None:
                #read csv file and save the new case number
                #file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data)
                file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
                upcs = pd.read_csv(file_name)
                upcs.loc[int(request.form['ncse'])-1,'cse'] = request.form['ncse']
                upcs.loc[int(request.form['ncse']) - 1, 'pjt'] = form.pjt2.data.pjt#os.path.splitext(form.pjt2.data)[0]
                upcs.to_csv(file_name,index=False)
                #unable to call the def for case list so need to copy and past here
                newcs = []
                newcs.append('Select Case..')
                newcs.append('Add New')
                rnewcs = pd.read_csv(file_name)
                #the case number are read as float in dataframe so need to change to int
                intcs = rnewcs['cse'].tolist()
                intcs = [int(i) for i in intcs]
                #put the list of int case number into choices
                newcs.extend(intcs)
                newcs = [(y, y) for y in newcs]
                newcs[0] = ('0', 'Select Case..')
                form.cse2.choices = newcs
                form.cse2.data = request.form['ncse']

        elif session['type'] == 'Guest':
            # try and except to prevent error when load case based on project
            try:
                session['xpjtx'] = form.pjt.data.pjt
                print(session['xpjtx'])
            except AttributeError:
                pass

            if form.pjt.data == None:
                pass

            #conditional statement for loading input data
            elif form.pjt.data.pjt != None and form.pjt.data.pjt != 'Add New':
                if form.cse.data == None:
                    pass
                elif form.cse.data.cse != None and form.cse.data.cse != 'Add New':
                    #check if project/case is new or already exists
                    if db.session.query(Calc.id).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).scalar() != None:
                        #load the data into form field for calculation
                        form.igor.raw_data = [str(db.session.query(Calc.gor).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.iog.raw_data = [str(db.session.query(Calc.og).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.igg.raw_data = [str(db.session.query(Calc.gg).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.itemp.raw_data = [str(db.session.query(Calc.temp).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.ipress.raw_data = [str(db.session.query(Calc.press).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.ih2s.raw_data = [str(db.session.query(Calc.h2s).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.ico2.raw_data = [str(db.session.query(Calc.co2).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.in2.raw_data = [str(db.session.query(Calc.n2).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form.ippm.raw_data = [str(db.session.query(Calc.ppm).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]

                    if db.session.query(Matching.id).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).scalar() != None:
                        # load the data into form field for matching
                        form5.mtemp.raw_data = [str(db.session.query(Matching.temp).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form5.mbppress.raw_data = [str(db.session.query(Matching.pb).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form5.mpress.raw_data = [str(db.session.query(Matching.press).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form5.mrrs.raw_data = [str(db.session.query(Matching.rs).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form5.mbbo.raw_data = [str(db.session.query(Matching.bo).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]
                        form5.muo.raw_data = [str(db.session.query(Matching.uo).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).first()[0])]

                    else:
                        pass

            if request.form['npjt'] == '':
                pass
            elif request.form['npjt'] != None:
                add_new = pjt_cse(pjt=request.form['npjt'])
                db.session.add(add_new)
                db.session.commit()
                return redirect('NewApp')

            if form.cse.data == None:
                pass

            if request.form['ncse'] == '':
                pass
            elif request.form['ncse'] != None:
                add_new = pjt_cse(pjt=form.pjt.data.pjt,cse=request.form['ncse'])
                db.session.add(add_new)
                db.session.commit()
                return redirect('NewApp')

    ingor = form.igor.data
    inog = form.iog.data
    ingg = form.igg.data
    intemp = form.itemp.data
    inpress = form.ipress.data
    inh2s = form.ih2s.data
    inco2 = form.ico2.data
    inn2 = form.in2.data
    inppm = form.ippm.data

    cor1 = form.ipb.data
    cor2 = form.irs.data
    cor3 = form.ibo.data
    cor4 = form.iuo.data

    if form.sub.data:
        try:
            inws = inppm / 1000000 * 100

            if cor1 == "VB":
                if inog <= 30:
                    finalpb = ((27.64 * ingor / ingg) * 10 ** ((-11.172 * inog) / (intemp + 460))) ** (1 / 1.0937)
                else:
                    finalpb = ((56.06 * ingor / ingg) * 10 ** ((-10.393 * inog) / (intemp + 460))) ** (1 / 1.187)
            elif cor1 == "AM":
                finalpb = 0.00538088 * ingor ** 0.715082 * ingg ** -1.87784 * (141.5 / (inog + 131.5)) ** 3.1437 * \
                          (intemp + 460) ** 1.32657
            elif cor1 == "G":
                x = (ingor / ingg) ** 0.816 * ((intemp ** 0.172) / (inog ** 0.989))
                logpb = 1.7669 + 1.7447 * math.log10(x) - (0.30218 * (math.log10(x) ** 2))
                finalpb = 10 ** logpb
            elif cor1 == "PF":
                x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * intemp ** 1.3911)
                finalpb = ((112.727 * ingor ** 0.577421) / (ingg ** 0.8439 * 10 ** x)) - 1391.051
            elif cor1 == "S":
                finalpb = 18.2 * ((ingor / ingg) ** 0.83 * 10 ** (0.00091 * intemp - 0.0125 * inog) - 1.4)
            else:
                finalpb = "Invalid Correlation!!"
            xfinalpb = "{:.2f}".format(finalpb)

            if inpress <= 14.7:
                finalrs = 0
            else:
                if inpress < finalpb:
                    if cor2 == "VB":
                        if inog <= 30:
                            finalrs = 0.0362 * ingg * inpress ** 1.0937 * (math.exp(25.724 * inog / (intemp + 460)))
                        else:
                            finalrs = 0.0178 * ingg * inpress ** 1.187 * (math.exp(23.931 * inog / (intemp + 460)))
                    elif cor2 == "AM":
                        finalrs = (
                                  (185.8432 * ingg ** 1.87784) * ((141.5 / (inog + 131.5)) ** -3.1437) * ((intemp + 460)
                                                                                                          ** -1.32657) * inpress) ** 1.398441
                    elif cor2 == "G":
                        x = 2.8869 - (14.1811 - 3.3093 * math.log10(inpress)) ** 0.5
                        logrs = 10 ** x
                        finalrs = ingg * (((inog ** 0.989) / (intemp ** 0.172)) * logrs) ** 1.2255
                    elif cor2 == "PF":
                        x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * intemp ** 1.3911)
                        finalrs = ((((inpress / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** x) ** 1.73184)
                    elif cor2 == "S":
                        x = 0.0125 * inog - 0.00091 * intemp
                        finalrs = ingg * (((inpress / 18.2) + 1.4) * 10 ** x) ** 1.2048
                    else:
                        finalrs = "Invalid Correlation!!"
                else:
                    finalrs = ingor
            xfinalrs = round(finalrs, 2)

            if inpress > finalpb:
                # VB
                finalco = ((-1433) + (5 * finalrs) + (17.2 * intemp) - (1180 * ingg) + (12.61 * inog)) / (
                (10 ** 5) * inpress)
            elif inpress < finalpb:
                # Mcain
                finalco = math.exp(-7.573 - (1.45 * math.log(inpress)) - (0.383 * math.log(finalpb)) +
                                   (1.402 * math.log((intemp + 460)) + (0.256 * math.log(inog)) + (
                                   0.449 * math.log(ingor))))

            # water fvf
            A1 = 0.9911 + (6.35 * 10 ** -5) * intemp + (8.5 * 10 ** -7 * intemp ** 2)
            A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * intemp + (
                4.57 * 10 ** -12 * intemp ** 2)
            A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * intemp + (
                -1.43 * 10 ** -15 * intemp ** 2)
            finalbw = A1 + A2 * inpress + A3 * inpress ** 2

            xfinalco = "{:.2E}".format(finalco)
            xfinalbw = round(finalbw, 2)

            if cor3 == "VB":
                if inpress <= 14.7 and intemp == 60:
                    finalbo = 1
                elif inpress <= finalpb:
                    if inog <= 30:
                        finalbo = 1 + 0.0004677 * finalrs + (intemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                             (
                                                                                             -1.811 * 10 ** -8) * finalrs)
                    else:
                        finalbo = 1 + 0.000467 * finalrs + (intemp - 60) * (inog / ingg) * (
                        0.000011 + (1.337 * 10 ** -9)
                        * finalrs)
                elif inpress > finalpb:
                    if inog <= 30:
                        finalbox = 1 + 0.0004677 * finalrs + (intemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                              (
                                                                                              -1.811 * 10 ** -8) * finalrs)
                    else:
                        finalbox = 1 + 0.000467 * finalrs + (intemp - 60) * (inog / ingg) * (
                        0.000011 + (1.337 * 10 ** -9)
                        * finalrs)
                    finalbo = finalbox * (1 - float(finalco) * (inpress - finalpb))
            elif cor3 == "AM":
                if inpress <= 14.7 and intemp == 60:
                    finalbo = 1
                elif inpress <= finalpb:
                    F = finalrs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                    finalbo = 0.497069 + (0.862963 * 10 ** -3 * (intemp + 460)) + (0.182594 * 10 ** -2 * F) + \
                              (0.318099 * 10 ** -5 * F ** 2)
                elif inpress > finalpb:
                    F = finalrs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                    finalbox = 0.497069 + (0.862963 * 10 ** -3 * (intemp + 460)) + (0.182594 * 10 ** -2 * F) + \
                               (0.318099 * 10 ** -5 * F ** 2)
                    finalbo = finalbox * (1 - float(finalco) * (inpress - finalpb))
            elif cor3 == "G":
                if inpress <= 14.7 and intemp == 60:
                    finalbo = 1
                elif inpress <= finalpb:
                    bob = (finalrs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * intemp)
                    A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                    finalbo = 1 + 10 ** A
                elif inpress > finalpb:
                    bob = (finalrs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * intemp)
                    A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                    finalbox = 1 + 10 ** A
                    finalbo = finalbox * (1 - float(finalco) * (inpress - finalpb))
            elif cor3 == "PF":
                if inpress <= 14.7 and intemp == 60:
                    finalbo = 1
                elif inpress <= finalpb:
                    finalbo = 1.0113 + 7.2046 * (10 ** -5) * (finalrs ** 0.3738 * (
                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (intemp) ** 0.5371) ** 3.0936
                elif inpress > finalpb:
                    finalbox = 1.0113 + 7.2046 * (10 ** -5) * (finalrs ** 0.3738 * (
                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (intemp) ** 0.5371) ** 3.0936
                    finalbo = finalbox * (1 - float(finalco) * (inpress - finalpb))
            elif cor3 == "S":
                if inpress <= 14.7 and intemp == 60:
                    finalbo = 1
                elif inpress <= finalpb:
                    finalbo = 0.9759 + 0.00012 * (
                                                     finalrs * (
                                                     ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * intemp) ** 1.2
                elif inpress > finalpb:
                    finalbox = 0.9759 + 0.00012 * (finalrs * (ingg / (141.5 / (inog + 131.5)))
                                                   ** 0.5 + 1.25 * intemp) ** 1.2
                    finalbo = finalbox * (1 - float(finalco) * (inpress - finalpb))
            else:
                finalbo = "Invalid Correlation!!"
            xfinalbo = round(finalbo, 2)

            if cor4 == "B":
                aa = 10 ** (0.43 + (8.33 / inog))
                deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (intemp + 200)) ** aa
                if inpress < finalpb:
                    aaa = 10.715 * (finalrs + 100) ** -0.515
                    bbb = 5.44 * (finalrs + 150) ** -0.338
                    uos = aaa * deadoil ** bbb
                    finaluo = uos
                elif inpress > finalpb:
                    aaa = 10.715 * (finalrs + 100) ** -0.515
                    bbb = 5.44 * (finalrs + 150) ** -0.338
                    uos = aaa * deadoil ** bbb
                    ass = (-3.9 * (10 ** -5) * inpress) - 5
                    m = 2.6 * inpress ** 1.187 * 10 ** ass
                    finaluo = uos * (inpress / finalpb) ** m
                xfinaluo = round(finaluo, 2)

            elif cor4 == "BR":
                zz = 3.0324 - 0.02023 * inog
                yy = 10 ** zz
                xx = yy * (intemp) ** -1.163
                deadoil = (3.141 * (10 ** 10)) * (intemp ** -3.444) * (math.log10(inog)) ** (
                10.313 * (math.log10(intemp)) - 36.447)

                if inpress < finalpb:
                    aaa = 10.715 * (finalrs + 100) ** -0.515
                    bbb = 5.44 * (finalrs + 150) ** -0.338
                    uos = aaa * deadoil ** bbb
                    finaluo = uos
                elif inpress > finalpb:
                    aaa = 10.715 * (finalrs + 100) ** -0.515
                    bbb = 5.44 * (finalrs + 150) ** -0.338
                    uos = aaa * deadoil ** bbb
                    ass = (-3.9 * (10 ** -5) * inpress) - 5
                    m = 2.6 * inpress ** 1.187 * 10 ** ass
                    finaluo = uos * (inpress / finalpb) ** m
                xfinaluo = "{:.2E}".format(finaluo, 2)

            else:
                xfinaluo = "Invalid Correlation!!"

            finalpo = ((62.4 * (141.5 / (inog + 131.5))) + (0.0136 * finalrs * ingg)) / finalbo
            xfinalpo = round(finalpo, 2)

            xg = 1 - inn2 - inco2 - inh2s
            gamghc = (ingg - 0.967 * inn2 - 1.52 * inco2 - 1.18 * inh2s) / xg
            tpchc = 168 + 325 * gamghc - 12.5 * gamghc ** 2
            ppchc = 677 + gamghc * (15 - 37.5 * gamghc)
            tpcm = xg * tpchc + 227 * inn2 + 548 * inco2 * 672 * inh2s
            ppcm = xg * ppchc + 493 * inn2 + 1071 * inco2 + 1036 * inh2s
            epslon = 120 * (xg ** 0.9 - xg ** 1.6) + 15 * (inco2 ** 0.5 - inh2s ** 4)
            tpc = tpcm - epslon
            ppc = ppcm * (tpc / (tpcm + inh2s * (1 - inh2s) * epslon))
            tpr = (intemp + 460) / tpc
            ppr = inpress / ppc
            AA = 1.39 * (tpr - 0.92) ** 0.5 - 0.36 * tpr - 0.101
            BB = (0.62 - 0.23 * tpr) * ppr + (0.066 / (tpr - 0.86) - 0.037) * ppr ** 2 + 0.32 / 10 ** (
                9 * (tpr - 1)) * ppr ** 6
            CC = 0.132 - 0.32 * math.log10(tpr)
            DD = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
            finalz = AA + ((1 - AA) / cmath.exp(BB)) + (CC * ppr ** DD)
            xfinalz = round(finalz.real, 2)

            E = 35.37 * inpress / (finalz * (intemp + 460))
            gfvf = 1 / E
            xgfvf = "{:.2f}".format(gfvf.real)

            gd = (28.97 * inpress * ingg) / (finalz * 10.7316 * (intemp + 460))
            xgd = "{:.2f}".format(gd.real)

            ugas1 = 0.001 * (8.1888 - 6.15 * math.log10(ingg) + (0.01709 - 0.002062 * ingg) * intemp)
            gv = cmath.exp(-2.4621182 + ppr * (2.97054714 + ppr * (-0.286264054 + ppr * 0.00805420522)) + tpr * (
                2.80860949 + ppr * (-3.49803305 + ppr * (0.36037302 + ppr * -0.0104432413)) + tpr * (
                    -0.793385684 + ppr * (1.39643306 + ppr * (-0.149144925 + ppr * 0.00441015512)) + tpr *
                    (
                    0.0839387178 + ppr * (-0.186408848 + ppr * (0.0203367881 + ppr * -0.000609579263)))))) / tpr * ugas1
            xgv = "{:.2f}".format(gv.real)

            finaluw = math.exp(1.003 - (1.479 * 10 ** -2 * intemp) + (1.982 * 10 ** -5 * intemp ** 2))
            xfinaluw = round(finaluw, 2)

            pwsc = 62.368 + (0.438603 * inws) + (1.60074 * 10 ** -3 * inws)
            finalpw = pwsc / finalbw
            xfinalpw = round(finalpw, 2)

            C1 = 3.8546 - 0.000134 * inpress
            C2 = -0.01052 + 4.77 * 10 ** -7 * inpress
            C3 = (3.9267 * 10 ** -5) - (8.8 * 10 ** -10 * inpress)
            finalcw = (C1 + C2 * intemp + C3 * intemp ** 2) * 10 ** -6
            xfinalcw = "{:.2E}".format(finalcw)

            fiow = "{:.2f}".format(30)

            ido = (1.17013 - (1.694 * 10 ** -3 * intemp)) * (38.085 - 0.259 * inog)
            fiog = ido * (0.056379 + (0.94362 * math.exp(-3.8491 * 10 ** -3 * finalrs)))
            xfiog = round(fiog, 2)

            Wdens = finalpw * 0.0160185
            Gdens = gd * 0.0160185
            fiwg = ((1.53988 * (Wdens - Gdens) + 2.08339) / (((intemp + 460) / 302.881) ** (0.821976 - 1.83785
                                                                                            * 10 ** -3 * (
                                                                                            intemp + 460) + 1.34016 * 10 ** -6 * (
                                                                                            intemp + 460) ** 2))) ** 3.6667
            xfiwg = "{:.2f}".format(fiwg.real)

            ingorr = ingor
            inogg = inog
            inggg = ingg

            inh2ss = inh2s
            inco22 = inco2
            inn22 = inn2
            inppmm = inppm

            session['ingorr'] = ingorr
            session['inogg'] = inogg
            session['inggg'] = inggg

            session['inh2ss'] = inh2ss
            session['inco22'] = inco22
            session['inn22'] = inn22
            session['inppmm'] = inppmm

            session['cor1'] = cor1
            session['cor2'] = cor2
            session['cor3'] = cor3
            session['cor4'] = cor4

            session['xpb'] = xfinalpb
            session['xrs'] = xfinalrs
            session['xbo'] = xfinalbo
            session['xco'] = xfinalco
            session['xuo'] = xfinaluo
            session['xpo'] = xfinalpo
            session['xz'] = xfinalz
            session['xbg'] = xgfvf
            session['xpg'] = xgd
            session['xug'] = xgv
            session['xbw'] = xfinalbw
            session['xuw'] = xfinaluw
            session['xpw'] = xfinalpw
            session['xcw'] = xfinalcw
            session['xiow'] = fiow
            session['xiog'] = xfiog
            session['xiwg'] = xfiwg

            # pass choices to other flask
            if session['type'] == 'Guest':
                session['cschoice'] = form.cse.data.cse
                session['pjchoice'] = form.pjt.data.pjt
            # pass temp and press to be appended in db
            session['uptemp'] = intemp
            session['uppress'] = inpress

        except ValueError:
            xfinalpb = 'ERROR!!'

        session['tabtype'] = 'normal'
        session['gtnc'] = 'no'

        session['mpb1'] = 1
        session['mpb2'] = 1
        session['mpb3'] = 1
        session['mpb4'] = 1
        session['mpb5'] = 1
        session['cpb1'] = 0
        session['cpb2'] = 0
        session['cpb3'] = 0
        session['cpb4'] = 0
        session['cpb5'] = 0

        session['mrs1'] = 1
        session['mrs2'] = 1
        session['mrs3'] = 1
        session['mrs4'] = 1
        session['mrs5'] = 1
        session['crs1'] = 0
        session['crs2'] = 0
        session['crs3'] = 0
        session['crs4'] = 0
        session['crs5'] = 0

        session['mbo1'] = 1
        session['mbo2'] = 1
        session['mbo3'] = 1
        session['mbo4'] = 1
        session['mbo5'] = 1
        session['cbo1'] = 0
        session['cbo2'] = 0
        session['cbo3'] = 0
        session['cbo4'] = 0
        session['cbo5'] = 0

        session['muo1'] = 1
        session['muo2'] = 1
        session['cuo1'] = 0
        session['cuo2'] = 0

        # pass the input of match
        session['mtemp'] = None
        session['mbppress'] = None
        session['mpress'] = None
        session['mrrs'] = None
        session['mbbo'] = None
        session['muo'] = None

        flash('Calculation completed!')
        # after calculation change input in form field according to input entered before this
        form.igor.raw_data = [str(session['ingorr'])]
        form.iog.raw_data = [str(session['inogg'])]
        form.igg.raw_data = [str(session['inggg'])]
        form.itemp.raw_data = [str(session['uptemp'])]
        form.ipress.raw_data = [str(session['uppress'])]
        form.ih2s.raw_data = [str(session['inh2ss'])]
        form.ico2.raw_data = [str(session['inco22'])]
        form.in2.raw_data = [str(session['inn22'])]
        form.ippm.raw_data = [str(session['inppmm'])]

    if form.exp.data:
        file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
        try:
            updf = pd.read_csv(file_name)
            # enable download the csv file as projects
            resp = make_response(updf.to_csv(index=False))
            resp.headers["Content-Disposition"] = "attachment; filename=" + str(form.pjt2.data.pjt) + '.csv'
            resp.headers["Content-Type"] = "text/csv"
            return resp
        # this code is for file not exists yet
        except FileNotFoundError:
            pass

    mtemp = form5.mtemp.data
    mbppress = form5.mbppress.data
    mpress = form5.mpress.data
    mrrs = form5.mrrs.data
    mbbo = form5.mbbo.data
    muo = form5.muo.data

    err = 1.00
    prevest = 0
    co = 0

    if form5.sub3.data:

        mgpb = 1
        mspb = 1
        mvbpb = 1
        mpfpb = 1
        mampb = 1
        cgpb = 0
        cspb = 0
        cvbpb = 0
        cpfpb = 0
        campb = 0

        mgrs = 1
        msrs = 1
        mvbrs = 1
        mpfrs = 1
        mamrs = 1
        cgrs = 0
        csrs = 0
        cvbrs = 0
        cpfrs = 0
        camrs = 0

        mgbo = 1
        msbo = 1
        mvbbo = 1
        mpfbo = 1
        mambo = 1
        cgbo = 0
        csbo = 0
        cvbbo = 0
        cpfbo = 0
        cambo = 0

        mbguo = 1
        mbluo = 1
        cbguo = 0
        cbluo = 0

        Gx = (mrrs / ingg) ** 0.816 * ((mtemp ** 0.172) / (inog ** 0.989))
        Glogpb = 1.7669 + 1.7447 * math.log10(Gx) - (0.30218 * (math.log10(Gx) ** 2))
        Gpb = 10 ** Glogpb

        while err > 0.05:
            diff = mbppress - (mgpb * Gpb) - cgpb
            dm = diff / Gpb
            dc = diff / 2
            mgpb = mgpb + dm
            cgpb = cgpb + dc
            est = mgpb * Gpb + cgpb
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        Spb = 18.2 * ((ingor / ingg) ** 0.83 * 10 ** (0.00091 * mtemp - 0.0125 * inog) - 1.4)

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbppress - (mspb * Spb) - cspb
            dm = diff / Spb
            dc = diff / 2
            mspb = mspb + dm
            cspb = cspb + dc
            est = mspb * Spb + cspb
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        if inog <= 30:
            VBpb = ((27.64 * ingor / ingg) * 10 ** ((-11.172 * inog) / (mtemp + 460))) ** (1 / 1.0937)
        else:
            VBpb = ((56.06 * ingor / ingg) * 10 ** ((-10.393 * inog) / (mtemp + 460))) ** (1 / 1.187)

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbppress - (mvbpb * VBpb) - cvbpb
            dm = diff / VBpb
            dc = diff / 2
            mvbpb = mvbpb + dm
            cvbpb = cvbpb + dc
            est = mvbpb * VBpb + cvbpb
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        PFx = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * mtemp ** 1.3911)
        PFpb = ((112.727 * ingor ** 0.577421) / (ingg ** 0.8439 * 10 ** PFx)) - 1391.051

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbppress - (mpfpb * PFpb) - cpfpb
            dm = diff / PFpb
            dc = diff / 2
            mpfpb = mpfpb + dm
            cpfpb = cpfpb + dc
            est = mpfpb * PFpb + cpfpb
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        AMpb = 0.00538088 * ingor ** 0.715082 * ingg ** -1.87784 * (141.5 / (inog + 131.5)) ** 3.1437 * \
               (mtemp + 460) ** 1.32657

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbppress - (mampb * AMpb) - campb
            dm = diff / AMpb
            dc = diff / 2
            mampb = mampb + dm
            campb = campb + dc
            est = mampb * AMpb + campb
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        Gx = 2.8869 - (14.1811 - 3.3093 * math.log10(mpress)) ** 0.5
        Glogrs = 10 ** Gx
        Grs = ingg * (((inog ** 0.989) / (mtemp ** 0.172)) * Glogrs) ** 1.2255

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mrrs - (mgrs * Grs) - cgrs
            dm = diff / Grs
            dc = diff / 2
            mgrs = mgrs + dm
            cgrs = cgrs + dc
            est = mgrs * Grs + cgrs
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        Sx = 0.0125 * inog - 0.00091 * mtemp
        Srs = ingg * (((mpress / 18.2) + 1.4) * 10 ** Sx) ** 1.2048

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mrrs - (msrs * Srs) - csrs
            dm = diff / Srs
            dc = diff / 2
            msrs = msrs + dm
            csrs = csrs + dc
            est = msrs * Srs + csrs
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        if inog <= 30:
            VBrs = 0.0362 * ingg * mpress ** 1.0937 * (math.exp(25.724 * inog / (mtemp + 460)))
        else:
            VBrs = 0.0178 * ingg * mpress ** 1.187 * (math.exp(23.931 * inog / (mtemp + 460)))

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mrrs - (mvbrs * VBrs) - cvbrs
            dm = diff / VBrs
            dc = diff / 2
            mvbrs = mvbrs + dm
            cvbrs = cvbrs + dc
            est = mvbrs * VBrs + cvbrs
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        PFx = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * mtemp ** 1.3911)
        PFrs = ((((mpress / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** PFx) ** 1.73184)

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mrrs - (mpfrs * PFrs) - cpfrs
            dm = diff / PFrs
            dc = diff / 2
            mpfrs = mpfrs + dm
            cpfrs = cpfrs + dc
            est = mpfrs * PFrs + cpfrs
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        AMrs = ((185.8432 * ingg ** 1.87784) * ((141.5 / (inog + 131.5)) ** -3.1437) * ((mtemp + 460)
                                                                                        ** -1.32657) * mpress) ** 1.398441

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mrrs - (mamrs * AMrs) - camrs
            dm = diff / AMrs
            dc = diff / 2
            mamrs = mamrs + dm
            camrs = camrs + dc
            est = mamrs * AMrs + camrs
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        if mrrs > 0:
            if mrrs > mbppress:
                # VB
                co = ((-1433) + (5 * mrrs) + (17.2 * mtemp) - (1180 * ingg) + (12.61 * inog)) / ((10 ** 5) * mrrs)
            elif mrrs < mbppress:
                # Mcain
                co = math.exp(-7.573 - (1.45 * math.log(mrrs)) - (0.383 * math.log(mbppress)) +
                              (1.402 * math.log((mtemp + 460)) + (0.256 * math.log(inog)) + (
                                  0.449 * math.log(ingor))))
        else:
            co = None

        if mrrs <= 14.7 and mtemp == 60:
            Gbo = 1
            Sbo = 1
            VBbo = 1
            PFbo = 1
            AMbo = 1
        elif mrrs <= mbppress:
            Gbob = (mrrs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * mtemp)
            GA = -6.58511 + 2.91329 * math.log10(Gbob) - 0.27683 * (math.log10(Gbob) ** 2)
            Gbo = 1 + 10 ** GA
            Sbo = 0.9759 + 0.00012 * (mrrs * (ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * mtemp) ** 1.2
            if inog <= 30:
                VBbo = 1 + 0.0004677 * mrrs + (mtemp - 60) * (inog / ingg) * (0.00001751 +
                                                                              (-1.811 * 10 ** -8) * mrrs)
            else:
                VBbo = 1 + 0.000467 * mrrs + (mtemp - 60) * (inog / ingg) * (0.000011 + (1.337 * 10 ** -9) * mrrs)
            AMF = mrrs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
            AMbo = 0.497069 + (0.862963 * 10 ** -3 * (mtemp + 460)) + (0.182594 * 10 ** -2 * AMF) + (
            0.318099 * 10 ** -5 * AMF ** 2)
            PFbo = 1.0113 + 7.2046 * (10 ** -5) * (mrrs ** 0.3738 * (
                ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (mtemp) ** 0.5371) ** 3.0936
        elif mrrs > mbppress:
            Gbob = (mrrs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * mtemp)
            GA = -6.58511 + 2.91329 * math.log10(Gbob) - 0.27683 * (math.log10(Gbob) ** 2)
            Gbox = 1 + 10 ** GA
            Gbo = Gbox * (1 - float(co) * (mrrs - mbppress))
            Sbox = 0.9759 + 0.00012 * (mrrs * (ingg / (141.5 / (inog + 131.5)))
                                       ** 0.5 + 1.25 * mtemp) ** 1.2
            Sbo = Sbox * (1 - float(co) * (mrrs - mbppress))
            if inog <= 30:
                VBbox = 1 + 0.0004677 * mrrs + (mtemp - 60) * (inog / ingg) * (0.00001751 +
                                                                               (-1.811 * 10 ** -8) * mrrs)
            else:
                VBbox = 1 + 0.000467 * mrrs + (mtemp - 60) * (inog / ingg) * (0.000011 + (1.337 * 10 ** -9)
                                                                              * mrrs)
            VBbo = VBbox * (1 - float(co) * (mrrs - mbppress))
            AMF = mrrs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
            AMbox = 0.497069 + (0.862963 * 10 ** -3 * (mtemp + 460)) + (0.182594 * 10 ** -2 * AMF) + \
                    (0.318099 * 10 ** -5 * AMF ** 2)
            AMbo = AMbox * (1 - float(co) * (mrrs - mbppress))
            PFbox = 1.0113 + 7.2046 * (10 ** -5) * (mrrs ** 0.3738 * (
                ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (mtemp) ** 0.5371) ** 3.0936
            PFbo = PFbox * (1 - float(co) * (mrrs - mbppress))

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbbo - (mgbo * Gbo) - cgbo
            dm = diff / Gbo
            dc = diff / 2
            mgbo = mgbo + dm
            cgbo = cgbo + dc
            est = mgbo * Gbo + cgbo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        err = 1.00

        while err > 0.05:
            diff = mbbo - (msbo * Sbo) - csbo
            dm = diff / Sbo
            dc = diff / 2
            msbo = msbo + dm
            csbo = csbo + dc
            est = msbo * Sbo + csbo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbbo - (mvbbo * VBbo) - cvbbo
            dm = diff / VBbo
            dc = diff / 2
            mvbbo = mvbbo + dm
            cvbbo = cvbbo + dc
            est = mvbbo * VBbo + cvbbo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbbo - (mpfbo * PFbo) - cpfbo
            dm = diff / PFbo
            dc = diff / 2
            mpfbo = mpfbo + dm
            cpfbo = cpfbo + dc
            est = mpfbo * PFbo + cpfbo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        err = 1.00
        prevest = 0

        while err > 0.05:
            diff = mbbo - (mambo * AMbo) - cambo
            dm = diff / AMbo
            dc = diff / 2
            mambo = mambo + dm
            cambo = cambo + dc
            est = mambo * AMbo + cambo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        aa = 10 ** (0.43 + (8.33 / inog))
        deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (mtemp + 200)) ** aa

        zz = 3.0324 - 0.02023 * inog
        yy = 10 ** zz
        xx = yy * (mtemp) ** -1.163
        deadoil2 = (3.141 * (10 ** 10)) * (mtemp ** -3.444) * (math.log10(inog)) ** (
        10.313 * (math.log10(mtemp)) - 36.447)  # 10 ** xx - 1

        if mrrs < mbppress:
            aaa = 10.715 * (mrrs + 100) ** -0.515
            bbb = 5.44 * (mrrs + 150) ** -0.338
            uos = aaa * deadoil ** bbb
            BLuo = uos

            aaa2 = 10.715 * (mrrs + 100) ** -0.515
            bbb2 = 5.44 * (mrrs + 150) ** -0.338
            uos2 = aaa2 * deadoil2 ** bbb2
            BGuo = uos2

        elif mrrs > mbppress:
            aaa = 10.715 * (mrrs + 100) ** -0.515
            bbb = 5.44 * (mrrs + 150) ** -0.338
            uos = aaa * deadoil ** bbb
            ass = (-3.9 * (10 ** -5) * mrrs) - 5
            m = 2.6 * mrrs ** 1.187 * 10 ** ass
            BLuo = uos * (mrrs / mbppress) ** m

            aaa2 = 10.715 * (mrrs + 100) ** -0.515
            bbb2 = 5.44 * (mrrs + 150) ** -0.338
            uos2 = aaa2 * deadoil2 ** bbb2
            ass2 = (-3.9 * (10 ** -5) * mrrs) - 5
            m2 = 2.6 * mrrs ** 1.187 * 10 ** ass2
            BGuo = uos2 * (mrrs / mbppress) ** m2

        err = 1.00

        while err > 0.05:
            diff = muo - (mbguo * BGuo) - cbguo
            dm = diff / BGuo
            dc = diff / 2
            mbguo = mbguo + dm
            cbguo = cbguo + dc
            est = mbguo * BGuo + cbguo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        err = 1.00

        while err > 0.05:
            diff = muo - (mbluo * BLuo) - cbluo
            dm = diff / BLuo
            dc = diff / 2
            mbluo = mbluo + dm
            cbluo = cbluo + dc
            est = mbluo * BLuo + cbluo
            err = math.fabs(((est - prevest) / est)) * 100
            prevest = est

        session['tabtype'] = 'matched'

        session['mpb1'] = mgpb
        session['mpb2'] = mspb
        session['mpb3'] = mvbpb
        session['mpb4'] = mpfpb
        session['mpb5'] = mampb
        session['cpb1'] = cgpb
        session['cpb2'] = cspb
        session['cpb3'] = cvbpb
        session['cpb4'] = cpfpb
        session['cpb5'] = campb

        session['mrs1'] = mgrs
        session['mrs2'] = msrs
        session['mrs3'] = mvbrs
        session['mrs4'] = mpfrs
        session['mrs5'] = mamrs
        session['crs1'] = cgrs
        session['crs2'] = csrs
        session['crs3'] = cvbrs
        session['crs4'] = cpfrs
        session['crs5'] = camrs

        session['mbo1'] = mgbo
        session['mbo2'] = msbo
        session['mbo3'] = mvbbo
        session['mbo4'] = mpfbo
        session['mbo5'] = mambo
        session['cbo1'] = cgbo
        session['cbo2'] = csbo
        session['cbo3'] = cvbbo
        session['cbo4'] = cpfbo
        session['cbo5'] = cambo

        session['muo1'] = mbguo
        session['muo2'] = mbluo
        session['cuo1'] = cbguo
        session['cuo2'] = cbluo

        session['check'] = 'checked'

        flash('Calculation Completed!')
        # after calculation change input in form field according to input entered before this
        form5.mtemp.raw_data = [str(mtemp)]
        form5.mbppress.raw_data = [str(mbppress)]
        form5.mpress.raw_data = [str(mpress)]
        form5.mrrs.raw_data = [str(mrrs)]
        form5.mbbo.raw_data = [str(mbbo)]
        form5.muo.raw_data = [str(muo)]
        #pass the input of match
        session['mtemp'] = mtemp
        session['mbppress'] = mbppress
        session['mpress'] = mpress
        session['mrrs'] = mrrs
        session['mbbo'] = mbbo
        session['muo'] = muo

    incr1 = ''
    incr2 = ''
    tp = ''
    ps = ''
    i = ''
    ii = ''
    ingorr = ''
    inogg = ''
    inggg = ''
    inh2ss = ''
    inco22 = ''
    inn22 = ''
    inppmm = ''
    pss = ''
    cor1 = ''
    cor2 = ''
    cor3 = ''
    cor4 = ''

    stemp = form2.istemp.data
    etemp = form2.ietemp.data
    stp1 = form2.istp1.data
    spress = form2.ispress.data
    epress = form2.iepress.data
    stp2 = form2.istp2.data

    session['stemp'] = stemp
    session['etemp'] = etemp
    session['stp1'] = stp1
    session['spress'] = spress
    session['epress'] = epress
    session['stp2'] = stp2

    if form2.getout.data:
        incr1 = (etemp - stemp) / stp1
        incr2 = (epress - spress) / stp2
        tp = np.linspace(stemp, etemp, stp1 + 1, incr1)
        ps = np.linspace(spress, epress, stp2 + 1, incr2)
        i = pd.Series(tp).to_json(orient='values')
        ii = pd.Series(ps).to_json(orient='values')

        ingorr = session['ingorr']
        inogg = session['inogg']
        inggg = session['inggg']
        inh2ss = session['inh2ss']
        inco22 = session['inco22']
        inn22 = session['inn22']
        inppmm = session['inppmm']
        pss = ii
        session['pss'] = pss
        tpp = i
        session['tpp'] = tpp
        cor1 = session['cor1']
        cor2 = session['cor2']
        cor3 = session['cor3']
        cor4 = session['cor4']

        if session['type'] == 'Guest':
            pass
        elif session['type'] == 'Admin':
            # pass value to session and later be combined into dataframe to be send to csv for registered user
            session['d1'] = stemp
            session['d2'] = etemp
            session['d3'] = stp1
            session['d4'] = spress
            session['d5'] = epress
            session['d6'] = stp2

        #PVT chart calculation
        mgpb = session['mpb1']
        mspb = session['mpb2']
        mvbpb = session['mpb3']
        mpfpb = session['mpb4']
        mampb = session['mpb5']
        cgpb = session['cpb1']
        cspb = session['cpb2']
        cvbpb = session['cpb3']
        cpfpb = session['cpb4']
        campb = session['cpb5']

        mgrs = session['mrs1']
        msrs = session['mrs2']
        mvbrs = session['mrs3']
        mpfrs = session['mrs4']
        mamrs = session['mrs5']
        cgrs = session['crs1']
        csrs = session['crs2']
        cvbrs = session['crs3']
        cpfrs = session['crs4']
        camrs = session['crs5']

        mgbo = session['mbo1']
        msbo = session['mbo2']
        mvbbo = session['mbo3']
        mpfbo = session['mbo4']
        mambo = session['mbo5']
        cgbo = session['cbo1']
        csbo = session['cbo2']
        cvbbo = session['cbo3']
        cpfbo = session['cbo4']
        cambo = session['cbo5']

        mbguo = session['muo1']
        mbluo = session['muo2']
        cbguo = session['cuo1']
        cbluo = session['cuo2']

        ingor = session['ingorr']
        inog = session['inogg']
        ingg = session['inggg']
        inh2s = session['inh2ss']
        inco2 = session['inco22']
        inn2 = session['inn22']
        inppm = session['inppmm']
        pss = session['pss']
        ps = pandas.io.json.read_json(pss)
        cor1 = session['cor1']
        cor2 = session['cor2']
        cor3 = session['cor3']
        cor4 = session['cor4']

        ntemp = form3.newT.data
        prm = form3.param.data
        plt.rcParams.update({'font.size': 13})
        fig, ax = plt.subplots()

        inws = inppm / 1000000 * 100

        if cor1 == "VB":
            if inog <= 30:
                finalpb = ((27.64 * ingor / ingg) * 10 ** ((-11.172 * inog) / (ntemp + 460))) ** (1 / 1.0937)
            else:
                finalpb = ((56.06 * ingor / ingg) * 10 ** ((-10.393 * inog) / (ntemp + 460))) ** (1 / 1.187)
            finalpb = mvbpb * finalpb + cvbpb
        elif cor1 == "AM":
            finalpb = 0.00538088 * ingor ** 0.715082 * ingg ** -1.87784 * (141.5 / (inog + 131.5)) ** 3.1437 * \
                      (ntemp + 460) ** 1.32657
            finalpb = mampb * finalpb + campb
        elif cor1 == "G":
            x = (ingor / ingg) ** 0.816 * ((ntemp ** 0.172) / (inog ** 0.989))
            logpb = 1.7669 + 1.7447 * math.log10(x) - (0.30218 * (math.log10(x) ** 2))
            finalpb = 10 ** logpb
            finalpb = mgpb * finalpb + cgpb
        elif cor1 == "PF":
            x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * ntemp ** 1.3911)
            finalpb = ((112.727 * ingor ** 0.577421) / (ingg ** 0.8439 * 10 ** x)) - 1391.051
            finalpb = mpfpb * finalpb + cpfpb
        elif cor1 == "S":
            finalpb = 18.2 * ((ingor / ingg) ** 0.83 * 10 ** (0.00091 * ntemp - 0.0125 * inog) - 1.4)
            finalpb = mspb * finalpb + cspb
        finalpb = round(finalpb + ps - ps, 2)

        yfinalpb = np.array(finalpb).ravel()
        pf = pd.Index(ps)

        data = np.zeros_like(pf)
        data = data.astype(float)

        yfinalrs = np.array(data).ravel()
        yfinalrs = pd.Series(yfinalrs)

        for ix in range(len(pf)):
            if pf[ix] <= 14.7:
                yfinalrs[ix] = 0
            else:
                if pf[ix] < yfinalpb[ix]:
                    if cor2 == "VB":
                        if inog <= 30:
                            yfinalrs[ix] = 0.0362 * ingg * pf[ix] ** 1.0937 * (math.exp(25.724 * inog / (ntemp + 460)))
                        else:
                            yfinalrs[ix] = 0.0178 * ingg * pf[ix] ** 1.187 * (math.exp(23.931 * inog / (ntemp + 460)))
                        yfinalrs[ix] = mvbrs * yfinalrs[ix] + cvbrs
                    elif cor2 == "AM":
                        yfinalrs[ix] = ((185.8432 * ingg ** 1.87784) * ((141.5 / (inog + 131.5)) ** -3.1437) * (
                            (ntemp + 460)
                            ** -1.32657) * pf[ix]) ** 1.398441
                        yfinalrs[ix] = mamrs * yfinalrs[ix] + camrs
                    elif cor2 == "G":
                        x = 2.8869 - (14.1811 - 3.3093 * np.log10(pf[ix])) ** 0.5
                        logrs = 10 ** x
                        yfinalrs[ix] = ingg * (((inog ** 0.989) / (ntemp ** 0.172)) * logrs) ** 1.2255
                        yfinalrs[ix] = mgrs * yfinalrs[ix] + cgrs
                    elif cor2 == "PF":
                        x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * ntemp ** 1.3911)
                        yfinalrs[ix] = ((((pf[ix] / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** x) ** 1.73184)
                        yfinalrs[ix] = mpfrs * yfinalrs[ix] + cpfrs
                    elif cor2 == "S":
                        x = 0.0125 * inog - 0.00091 * ntemp
                        yfinalrs[ix] = ingg * (((pf[ix] / 18.2) + 1.4) * 10 ** x) ** 1.2048
                        yfinalrs[ix] = msrs * yfinalrs[ix] + csrs
                else:
                    yfinalrs[ix] = ingor
        # yfinalrs = pd.Series.round(yfinalrs, 3)

        yfinalco = np.array(data).ravel()
        yfinalco = pd.Series(yfinalco)

        for ix in range(len(pf)):
            if pf[ix] > yfinalpb[ix]:
                # VB
                yfinalco[ix] = ((-1433) + (5 * yfinalrs[ix]) + (17.2 * ntemp) - (1180 * ingg) + (12.61 * inog)) / (
                    (10 ** 5) * pf[ix])
            elif pf[ix] < yfinalpb[ix]:
                # Mcain
                yfinalco[ix] = np.exp(-7.573 - (1.45 * np.log(pf[ix])) - (0.383 * np.log(yfinalpb[ix]))
                                      + (1.402 * math.log((ntemp + 460)) + (0.256 * math.log(inog)) + (
                    0.449 * np.log(ingor))))
        # yfinalco = pd.Series.round(yfinalco, 9)

        yfinalbw = np.array(data).ravel()
        yfinalbw = pd.Series(yfinalbw)

        for ix in range(len(pf)):
            # water fvf
            A1 = 0.9911 + (6.35 * 10 ** -5) * ntemp + (8.5 * 10 ** -7 * ntemp ** 2)
            A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * ntemp + (
                4.57 * 10 ** -12 * ntemp ** 2)
            A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * ntemp + (
                -1.43 * 10 ** -15 * ntemp ** 2)
            yfinalbw[ix] = A1 + A2 * pf[ix] + A3 * pf[ix] ** 2
        # yfinalbw = pd.Series.round(yfinalbw, 3)

        yfinalbo = np.array(data).ravel()
        yfinalbo = pd.Series(yfinalbo)

        for ix in range(len(pf)):
            if cor3 == "VB":
                if pf[ix] <= 14.7 and ntemp == 60:
                    yfinalbo[ix] = 1
                elif pf[ix] <= yfinalpb[ix]:
                    if inog <= 30:
                        yfinalbo[ix] = 1 + 0.0004677 * yfinalrs[ix] + (ntemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                                      (
                                                                                                          -1.811 * 10 ** -8) *
                                                                                                      yfinalrs[ix])
                    else:
                        yfinalbo[ix] = 1 + 0.000467 * yfinalrs[ix] + (ntemp - 60) * (inog / ingg) * (
                            0.000011 + (1.337 * 10 ** -9)
                            * yfinalrs[ix])
                    yfinalbo[ix] = mvbbo * yfinalbo[ix] + cvbbo
                elif pf[ix] > yfinalpb[ix]:
                    if inog <= 30:
                        yfinalbo[ix] = 1 + 0.0004677 * yfinalrs[ix] + (ntemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                                      (
                                                                                                          -1.811 * 10 ** -8) *
                                                                                                      yfinalrs[ix])
                    else:
                        yfinalbo[ix] = 1 + 0.000467 * yfinalrs[ix] + (ntemp - 60) * (inog / ingg) * (
                            0.000011 + (1.337 * 10 ** -9)
                            * yfinalrs[ix])
                    yfinalbo[ix] = yfinalbo[ix] * (1 - float(yfinalco[ix]) * (pf[ix] - yfinalpb[ix]))
                    yfinalbo[ix] = mvbbo * yfinalbo[ix] + cvbbo
            elif cor3 == "AM":
                if pf[ix] <= 14.7 and ntemp == 60:
                    yfinalbo[ix] = 1
                elif pf[ix] <= yfinalpb[ix]:
                    bob = yfinalrs[ix] ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                    yfinalbo[ix] = 0.497069 + (0.862963 * 10 ** -3 * (ntemp + 460)) + (0.182594 * 10 ** -2 * bob) + \
                                   (0.318099 * 10 ** -5 * bob ** 2)
                    yfinalbo[ix] = mambo * yfinalbo[ix] + cambo
                elif pf[ix] > yfinalpb[ix]:
                    bob = yfinalrs[ix] ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                    yfinalbo[ix] = 0.497069 + (0.862963 * 10 ** -3 * (ntemp + 460)) + (0.182594 * 10 ** -2 * bob) + \
                                   (0.318099 * 10 ** -5 * bob ** 2)
                    yfinalbo[ix] = yfinalbo[ix] * (1 - float(yfinalco[ix]) * (pf[ix] - yfinalpb[ix]))
                    yfinalbo[ix] = mambo * yfinalbo[ix] + cambo
            elif cor3 == "G":
                if pf[ix] <= 14.7 and ntemp == 60:
                    yfinalbo[ix] = 1
                elif pf[ix] <= yfinalpb[ix]:
                    bob = (yfinalrs[ix] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * ntemp)
                    A = -6.58511 + 2.91329 * np.log10(bob) - 0.27683 * (np.log10(bob) ** 2)
                    yfinalbo[ix] = 1 + 10 ** A
                    yfinalbo[ix] = mgbo * yfinalbo[ix] + cgbo
                elif pf[ix] > yfinalpb[ix]:
                    bob = (yfinalrs[ix] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * ntemp)
                    A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                    yfinalbo[ix] = 1 + 10 ** A
                    yfinalbo[ix] = yfinalbo[ix] * (1 - float(yfinalco[ix]) * (pf[ix] - yfinalpb[ix]))
                    yfinalbo[ix] = mgbo * yfinalbo[ix] + cgbo
            elif cor3 == "PF":
                if pf[ix] <= 14.7 and ntemp == 60:
                    yfinalbo[ix] = 1
                elif pf[ix] <= yfinalpb[ix]:
                    yfinalbo[ix] = 1.0113 + 7.2046 * (10 ** -5) * (yfinalrs[ix] ** 0.3738 * (
                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (ntemp) ** 0.5371) ** 3.0936
                    yfinalbo[ix] = mpfbo * yfinalbo[ix] + cpfbo
                elif pf[ix] > yfinalpb[ix]:
                    yfinalbo[ix] = 1.0113 + 7.2046 * (10 ** -5) * (yfinalrs[ix] ** 0.3738 * (
                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (ntemp) ** 0.5371) ** 3.0936
                    yfinalbo[ix] = yfinalbo[ix] * (1 - float(yfinalco[ix]) * (pf[ix] - yfinalpb[ix]))
                    yfinalbo[ix] = mpfbo * yfinalbo[ix] + cpfbo
            elif cor3 == "S":
                if pf[ix] <= 14.7 and ntemp == 60:
                    yfinalbo[ix] = 1
                elif pf[ix] <= yfinalpb[ix]:
                    yfinalbo[ix] = 0.9759 + 0.00012 * (yfinalrs[ix] * (
                        ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * ntemp) ** 1.2
                    yfinalbo[ix] = msbo * yfinalbo[ix] + csbo
                elif pf[ix] > yfinalpb[ix]:
                    yfinalbo[ix] = 0.9759 + 0.00012 * (yfinalrs[ix] * (ingg / (141.5 / (inog + 131.5)))
                                                       ** 0.5 + 1.25 * ntemp) ** 1.2
                    yfinalbo[ix] = yfinalbo[ix] * (1 - float(yfinalco[ix]) * (pf[ix] - yfinalpb[ix]))
                    yfinalbo[ix] = msbo * yfinalbo[ix] + csbo

        yfinaluo = np.array(data).ravel()
        yfinaluo = pd.Series(yfinaluo)

        for ix in range(len(pf)):
            if cor4 == "B":
                aa = 10 ** (0.43 + (8.33 / inog))
                deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (ntemp + 200)) ** aa

                if pf[ix] < yfinalpb[ix]:
                    aaa = 10.715 * (yfinalrs[ix] + 100) ** -0.515
                    bbb = 5.44 * (yfinalrs[ix] + 150) ** -0.338
                    yfinaluo[ix] = aaa * deadoil ** bbb
                elif pf[ix] > yfinalpb[ix]:
                    aaa = 10.715 * (yfinalrs[ix] + 100) ** -0.515
                    bbb = 5.44 * (yfinalrs[ix] + 150) ** -0.338
                    yfinaluo[ix] = aaa * deadoil ** bbb
                    ass = (-3.9 * (10 ** -5) * pf[ix]) - 5
                    m = 2.6 * pf[ix] ** 1.187 * 10 ** ass
                    yfinaluo[ix] = yfinaluo[ix] * (pf[ix] / yfinalpb[ix]) ** m
                yfinaluo[ix] = mbluo * yfinaluo[ix] + cbluo
            elif cor4 == "BR":
                zz = 3.0324 - 0.02023 * inog
                yy = 10 ** zz
                xx = yy * (ntemp) ** -1.163
                deadoil = (3.141 * (10 ** 10)) * (ntemp ** -3.444) * (math.log10(inog)) ** (
                    10.313 * (math.log10(ntemp)) - 36.447)

                if pf[ix] < yfinalpb[ix]:
                    aaa = 10.715 * (yfinalrs[ix] + 100) ** -0.515
                    bbb = 5.44 * (yfinalrs[ix] + 150) ** -0.338
                    yfinaluo[ix] = aaa * deadoil ** bbb
                elif pf[ix] > yfinalpb[ix]:
                    aaa = 10.715 * (yfinalrs[ix] + 100) ** -0.515
                    bbb = 5.44 * (yfinalrs[ix] + 150) ** -0.338
                    yfinaluo[ix] = aaa * deadoil ** bbb
                    ass = (-3.9 * (10 ** -5) * pf[ix]) - 5
                    m = 2.6 * pf[ix] ** 1.187 * 10 ** ass
                    yfinaluo[ix] = yfinaluo[ix] * (pf[ix] / yfinalpb[ix]) ** m
                yfinaluo[ix] = mbguo * yfinaluo[ix] + cbguo
        finalpo = np.array(data).ravel()
        finalpo = pd.Series(finalpo)

        for ix in range(len(pf)):
            finalpo[ix] = ((62.4 * (141.5 / (inog + 131.5))) + (0.0136 * yfinalrs[ix] * ingg)) / yfinalbo[ix]

        finalz = np.array(data).ravel()
        finalz = pd.Series(finalz)

        xg = 1 - inn2 - inco2 - inh2s
        gamghc = (ingg - 0.967 * inn2 - 1.52 * inco2 - 1.18 * inh2s) / xg
        tpchc = 168 + 325 * gamghc - 12.5 * gamghc ** 2
        ppchc = 677 + gamghc * (15 - 37.5 * gamghc)
        tpcm = xg * tpchc + 227 * inn2 + 548 * inco2 * 672 * inh2s
        ppcm = xg * ppchc + 493 * inn2 + 1071 * inco2 + 1036 * inh2s
        epslon = 120 * (xg ** 0.9 - xg ** 1.6) + 15 * (inco2 ** 0.5 - inh2s ** 4)
        tpc = tpcm - epslon
        ppc = ppcm * (tpc / (tpcm + inh2s * (1 - inh2s) * epslon))
        tpr = (ntemp + 460) / tpc

        for ix in range(len(pf)):
            ppr = pf[ix] / ppc
            AA = 1.39 * (tpr - 0.92) ** 0.5 - 0.36 * tpr - 0.101
            BB = (0.62 - 0.23 * tpr) * ppr + (0.066 / (tpr - 0.86) - 0.037) * ppr ** 2 + 0.32 / 10 ** (
                9 * (tpr - 1)) * ppr ** 6
            CC = 0.132 - 0.32 * np.log10(tpr)
            DD = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
            finalz[ix] = AA + ((1 - AA) / np.exp(BB)) + (CC * ppr ** DD)

        gfvf = np.array(data).ravel()
        gfvf = pd.Series(gfvf)
        gd = np.array(data).ravel()
        gd = pd.Series(gd)
        gv = np.array(data).ravel()
        gv = pd.Series(gv)

        for ix in range(len(pf)):
            ppr = pf[ix] / ppc

            E = 35.37 * pf[ix] / (finalz[ix] * (ntemp + 460))
            gfvf[ix] = 1 / E

            gd[ix] = (28.97 * pf[ix] * ingg) / (finalz[ix] * 10.7316 * (ntemp + 460))

            ugas1 = 0.001 * (8.1888 - 6.15 * math.log10(ingg) + (0.01709 - 0.002062 * ingg) * ntemp)
            gv[ix] = math.exp(-2.4621182 + ppr * (2.97054714 + ppr * (-0.286264054 + ppr * 0.00805420522)) + tpr * (
                2.80860949 + ppr * (-3.49803305 + ppr * (0.36037302 + ppr * -0.0104432413)) + tpr * (
                    -0.793385684 + ppr * (1.39643306 + ppr * (-0.149144925 + ppr * 0.00441015512)) + tpr *
                    (
                        0.0839387178 + ppr * (
                            -0.186408848 + ppr * (0.0203367881 + ppr * -0.000609579263)))))) / tpr * ugas1

        finaluw = np.array(data).ravel()
        finaluw = pd.Series(finaluw)
        finalpw = np.array(data).ravel()
        finalpw = pd.Series(finalpw)
        finalcw = np.array(data).ravel()
        finalcw = pd.Series(finalcw)
        xfiow = np.array(data).ravel()
        xfiow = pd.Series(xfiow)
        fiog = np.array(data).ravel()
        fiog = pd.Series(fiog)
        fiwg = np.array(data).ravel()
        fiwg = pd.Series(fiwg)

        for ix in range(len(pf)):
            finaluw[ix] = math.exp(1.003 - (1.479 * 10 ** -2 * ntemp) + (1.982 * 10 ** -5 * ntemp ** 2))

            pwsc = 62.368 + (0.438603 * inws) + (1.60074 * 10 ** -3 * inws)
            finalpw[ix] = pwsc / yfinalbw[ix]

            C1 = 3.8546 - 0.000134 * pf[ix]
            C2 = -0.01052 + 4.77 * 10 ** -7 * pf[ix]
            C3 = (3.9267 * 10 ** -5) - (8.8 * 10 ** -10 * pf[ix])
            finalcw[ix] = (C1 + C2 * ntemp + C3 * ntemp ** 2) * 10 ** -6

            xfiow[ix] = 30

            ido = (1.17013 - (1.694 * 10 ** -3 * ntemp)) * (38.085 - 0.259 * inog)
            fiog[ix] = ido * (0.056379 + (0.94362 * np.exp(-3.8491 * 10 ** -3 * yfinalrs[ix])))

            Wdens = finalpw[ix] * 0.0160185
            Gdens = gd[ix] * 0.0160185
            fiwg[ix] = ((1.53988 * (Wdens - Gdens) + 2.08339) / (((ntemp + 460) / 302.881) ** (0.821976 - 1.83785 *
                                                                                               10 ** -3 * (
                                                                                                   ntemp + 460) + 1.34016 * 10 ** -6 * (
                                                                                                   ntemp + 460) ** 2))) ** 3.6667

        if prm == "pb":
            labels = ["Bubble Point Pressure"]
            pt = ax.plot(ps, finalpb, '-o')
            ax.set_ylabel('Bubble Point')
            ax.set_title('Pressure vs Bubble Point')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            lgd = [pt]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "rs":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Gas Oil Ratio", ll]
            pt = ax.plot(ps, yfinalrs.round(9), '-o')
            pt2 = ax.plot(yfinalpb, yfinalrs)
            ax.set_ylabel('Gas Oil Ratio')
            ax.set_title('Pressure vs Gas Oil Ratio')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "bo":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Oil FVF", ll]
            pt = ax.plot(ps, yfinalbo.round(9), '-o')
            pt2 = ax.plot(yfinalpb, yfinalbo)
            ax.set_ylabel('Oil FVF')
            ax.set_title('Pressure vs Oil FVF')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "co":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Oil Compressibility", ll]
            pt = ax.plot(ps, yfinalco.round(9), '-o')
            pt2 = ax.plot(yfinalpb, yfinalco)
            ax.set_ylabel('Oil Compressibility')
            ax.set_title('Pressure vs Oil Compressibility')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "uo":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Oil Viscosity", ll]
            pt = ax.plot(ps, yfinaluo.round(9), '-o')
            pt2 = ax.plot(yfinalpb, yfinaluo)
            ax.set_ylabel('Oil Viscosity')
            ax.set_title('Pressure vs Oil Viscosity')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "po":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Oil Density", ll]
            pt = ax.plot(ps, finalpo.round(9), '-o')
            pt2 = ax.plot(yfinalpb, finalpo)
            ax.set_ylabel('Oil Density')
            ax.set_title('Pressure vs Oil Density')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "zf":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Z Factor", ll]
            pt = ax.plot(ps, finalz.round(9), '-o')
            pt2 = ax.plot(yfinalpb, finalz)
            ax.set_ylabel('Z Factor')
            ax.set_title('Pressure vs Z Factor')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "bg":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Gas FVF", ll]
            pt = ax.plot(ps, gfvf.round(9), '-o')
            pt2 = ax.plot(yfinalpb, gfvf)
            ax.set_ylabel('Gas FVF')
            ax.set_title('Pressure vs Gas FVF')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "pg":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Gas Density", ll]
            pt = ax.plot(ps, gd.round(9), '-o')
            pt2 = ax.plot(yfinalpb, gd)
            ax.set_ylabel('Gas Density')
            ax.set_title('Pressure vs Gas Density')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "ug":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Gas Viscosity", ll]
            pt = ax.plot(ps, gv.round(9), '-o')
            pt2 = ax.plot(yfinalpb, gv)
            ax.set_ylabel('Gas Viscosity')
            ax.set_title('Pressure vs Gas Viscosity')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "bw":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Water FVF", ll]
            pt = ax.plot(ps, yfinalbw.round(9), '-o')
            pt2 = ax.plot(yfinalpb, yfinalbw)
            ax.set_ylabel('Water FVF')
            ax.set_title('Pressure vs Water FVF')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "uw":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Water Viscosity", ll]
            pt = ax.plot(ps, finaluw.round(9), '-o')
            pt2 = ax.plot(yfinalpb, finaluw)
            ax.set_ylabel('Water Viscosity')
            ax.set_title('Pressure vs Water Viscosity')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "pw":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Water Density", ll]
            pt = ax.plot(ps, finalpw.round(9), '-o')
            pt2 = ax.plot(yfinalpb, finalpw)
            ax.set_ylabel('Water Density')
            ax.set_title('Pressure vs Water Density')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "cw":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs Water Compressibility", ll]
            pt = ax.plot(ps, finalcw.round(9), '-o')
            pt2 = ax.plot(yfinalpb, finalcw)
            ax.set_ylabel('Water Compressibility')
            ax.set_title('Pressure vs Water Compressibility')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "iow":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs IFT oil-water", ll]
            pt = ax.plot(ps, xfiow, '-o')
            pt2 = ax.plot(yfinalpb, xfiow)
            ax.set_ylabel('IFT oil-water')
            ax.set_title('Pressure vs IFT oil-water')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "iog":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs IFT oil-gas", ll]
            pt = ax.plot(ps, fiog.round(9), '-o')
            pt2 = ax.plot(yfinalpb, fiog)
            ax.set_ylabel('IFT oil-gas')
            ax.set_title('Pressure vs IFT oil-gas')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        elif prm == "iwg":
            ll = "Bubble Point Pressure = " + str(yfinalpb[0])
            labels = ["Pressure vs IFT water-gas", ll]
            pt = ax.plot(ps, fiwg.round(9), '-o')
            pt2 = ax.plot(yfinalpb, fiwg)
            ax.set_ylabel('IFT water-gas')
            ax.set_title('Pressure vs IFT water-gas')
            plugins.connect(fig, plugins.PointLabelTooltip(pt[0]))
            # plugins.connect(fig, plugins.LineLabelTooltip(pt2[0]))
            lgd = [pt, pt2]
            plugins.connect(fig, plugins.InteractiveLegendPlugin(lgd, labels))
            plugins.connect(fig, plugins.MousePosition(fontsize=14, fmt='.3f'))
            html = mpld3.fig_to_html(fig)

        session['chtchoice'] = prm
        if session['type'] == 'Guest':
            session['senpjt'] = form.pjt.data.pjt
        form3.newT.raw_data = [str(ntemp)]
        session['gtnc'] = 'yes'

    f = ""
    rs = ""
    bo = ""
    uo = ""
    rtemp = form4.restemp.data
    wrpress = form4.wrefpress.data

    if form4.sub2.data:
        ingor = session['ingorr']
        inog = session['inogg']
        ingg = session['inggg']
        inh2s = session['inh2ss']
        inco2 = session['inco22']
        inn2 = session['inn22']
        inppm = session['inppmm']
        cor1 = session['cor1']
        cor2 = session['cor2']
        cor3 = session['cor3']
        cor4 = session['cor4']
        pss = session['pss']
        ps = pandas.io.json.read_json(pss)

        mgrs = session['mrs1']
        msrs = session['mrs2']
        mvbrs = session['mrs3']
        mpfrs = session['mrs4']
        mamrs = session['mrs5']
        cgrs = session['crs1']
        csrs = session['crs2']
        cvbrs = session['crs3']
        cpfrs = session['crs4']
        camrs = session['crs5']

        mgbo = session['mbo1']
        msbo = session['mbo2']
        mvbbo = session['mbo3']
        mpfbo = session['mbo4']
        mambo = session['mbo5']
        cgbo = session['cbo1']
        csbo = session['cbo2']
        cvbbo = session['cbo3']
        cpfbo = session['cbo4']
        cambo = session['cbo5']

        mbguo = session['muo1']
        mbluo = session['muo2']
        cbguo = session['cuo1']
        cbluo = session['cuo2']

        pf = pd.Index(ps)
        inws = inppm / 1000000 * 100
        # water fvf
        A1 = 0.9911 + (6.35 * 10 ** -5) * rtemp + (8.5 * 10 ** -7 * rtemp ** 2)
        A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * rtemp + (
            4.57 * 10 ** -12 * rtemp ** 2)
        A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * rtemp + (
            -1.43 * 10 ** -15 * rtemp ** 2)
        bw = A1 + A2 * wrpress + A3 * wrpress ** 2

        C1 = 3.8546 - 0.000134 * wrpress
        C2 = -0.01052 + 4.77 * 10 ** -7 * wrpress
        C3 = (3.9267 * 10 ** -5) - (8.8 * 10 ** -10 * wrpress)
        cw = (C1 + C2 * rtemp + C3 * rtemp ** 2) * 10 ** -6

        uw = math.exp(1.003 - (1.479 * 10 ** -2 * rtemp) + (1.982 * 10 ** -5 * rtemp ** 2))

        # path = os.path.join('C:/Users/', os.getlogin(), 'Desktop/pvt.txt')
        # f = open(str(path), "w+")
        with open('/home/sapphirenitro/mysite/pvtcsv/pvt.txt', "w+") as f:
            f.write("PVTW")
            f.write("\r\n--PVT Properties of water")
            f.write("\r\n--\tPref\tBw\tCw\tWvisc\tCwvisc")
            f.write("\r\n\t" + str(wrpress) + "\t" + str("{:.4f}".format(bw)) + "\t" + str(
                "{:.4E}".format(cw)) + "\t" + str("{:.4f}".format(uw)) + "\t" + str(0))
            f.write("\r\n/\r\n")
            f.write("\r\nPVTO")
            f.write("\r\n--PVT Properties of oil")
            f.write("\r\n--\tRs\tP\tBo\tViscosity")
            xx = np.zeros_like(pf)
            xx = xx.astype(float)
            xxx = np.array(xx).ravel()
            d = 0
            j = 0
            i = 0
            z = 0
            while i < len(pf):
                z += 1

                while j < len(pf):
                    xxx[j] = pf[j]
                    if xxx[i] <= 14.7:
                        rs = 0
                    else:
                        if cor2 == "VB":
                            if inog <= 30:
                                rs = (mvbrs * (0.0362 * ingg * xxx[i] ** 1.0937 * (
                                math.exp(25.724 * inog / (rtemp + 460)))) + cvbrs) / 1000
                            else:
                                rs = (mvbrs * (0.0178 * ingg * xxx[i] ** 1.187 * (
                                math.exp(23.931 * inog / (rtemp + 460)))) + cvbrs) / 1000
                        elif cor2 == "AM":
                            rs = (mamrs * (
                            ((185.8432 * ingg ** 1.87784) * ((141.5 / (inog + 131.5)) ** -3.1437) * ((rtemp + 460)
                                                                                                     ** -1.32657) * xxx[
                                 i]) ** 1.398441) + camrs) / 1000
                        elif cor2 == "G":
                            x = 2.8869 - (14.1811 - 3.3093 * math.log10(xxx[i])) ** 0.5
                            logrs = 10 ** x
                            rs = (
                                 mgrs * (ingg * (((inog ** 0.989) / (rtemp ** 0.172)) * logrs) ** 1.2255) + cgrs) / 1000
                        elif cor2 == "PF":
                            x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * rtemp ** 1.3911)
                            rs = (mpfrs * (
                            (((xxx[i] / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** x) ** 1.73184) + cpfrs) / 1000
                        elif cor2 == "S":
                            x = 0.0125 * inog - 0.00091 * rtemp
                            rs = (msrs * (ingg * (((xxx[i] / 18.2) + 1.4) * 10 ** x) ** 1.2048) + csrs) / 1000

                    if rs > 0:
                        if xxx[j] > xxx[i]:
                            # VB
                            co = 1.705 * 10 ** -7 * rs ** 0.69357 * ingg ** 0.1885 * inog ** 0.3272 * rtemp ** 0.6729 * \
                                 xxx[j] ** -0.5906
                        elif xxx[j] < xxx[i]:
                            # Mcain
                            co = math.exp(-7.573 - (1.45 * math.log(xxx[j])) - (0.383 * math.log(xxx[i])) +
                                          (1.402 * math.log((rtemp + 460)) + (0.256 * math.log(inog)) + (
                                              0.449 * math.log(ingor))))
                    else:
                        co = 0

                    if cor3 == "VB":
                        if xxx[j] <= xxx[i]:
                            if inog <= 30:
                                bo = 1 + 0.0004677 * rs + (rtemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                          (-1.811 * 10 ** -8) * rs)
                            else:
                                bo = 1 + 0.000467 * rs + (rtemp - 60) * (inog / ingg) * (
                                    0.000011 + (1.337 * 10 ** -9)
                                    * rs)
                        elif xxx[j] > xxx[i]:
                            if inog <= 30:
                                finalbox = 1 + 0.0004677 * rs + (rtemp - 60) * (inog / ingg) * (0.00001751 +
                                                                                                (
                                                                                                -1.811 * 10 ** -8) * rs)
                            else:
                                finalbox = 1 + 0.000467 * rs + (rtemp - 60) * (inog / ingg) * (
                                    0.000011 + (1.337 * 10 ** -9) * rs)
                            bo = finalbox * (1 - float(co) * (xxx[j] - xxx[i]))
                        bo = mvbbo * bo + cvbbo
                    elif cor3 == "AM":
                        if xxx[j] <= xxx[i]:
                            F = rs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                            bo = 0.497069 + (0.862963 * 10 ** -3 * (rtemp + 460)) + (0.182594 * 10 ** -2 * F) + \
                                 (0.318099 * 10 ** -5 * F ** 2)
                        elif xxx[j] > xxx[i]:
                            F = rs ** 0.74239 * ingg ** 0.32394 * (141.5 / (inog + 131.5)) ** -1.20204
                            finalbox = 0.497069 + (0.862963 * 10 ** -3 * (rtemp + 460)) + (0.182594 * 10 ** -2 * F) + \
                                       (0.318099 * 10 ** -5 * F ** 2)
                            bo = finalbox * (1 - float(co) * (xxx[j] - xxx[i]))
                        bo = mambo * bo + cambo
                    elif cor3 == "G":
                        if xxx[j] <= xxx[i]:
                            bob = (rs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * rtemp)
                            A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                            bo = 1 + 10 ** A
                        elif xxx[j] > xxx[i]:
                            bob = (rs * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * rtemp)
                            A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                            finalbox = 1 + 10 ** A
                            bo = finalbox * (1 - float(co) * (xxx[j] - xxx[i]))
                        bo = mgbo * bo + cgbo
                    elif cor3 == "PF":
                        if xxx[j] <= xxx[i]:
                            bo = 1.0113 + 7.2046 * (10 ** -5) * (rs ** 0.3738 * (
                                ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                                                     rtemp) ** 0.5371) ** 3.0936
                        elif xxx[j] > xxx[i]:
                            finalbox = 1.0113 + 7.2046 * (10 ** -5) * (rs ** 0.3738 * (
                                ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                                                           rtemp) ** 0.5371) ** 3.0936
                            bo = finalbox * (1 - float(co) * (xxx[j] - xxx[i]))
                        bo = mpfbo * bo + cpfbo
                    elif cor3 == "S":
                        if xxx[j] <= xxx[i]:
                            bo = 0.9759 + 0.00012 * (rs * (
                                ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * rtemp) ** 1.2
                        elif xxx[j] > xxx[i]:
                            finalbox = 0.9759 + 0.00012 * (rs * (ingg / (141.5 / (inog + 131.5)))
                                                           ** 0.5 + 1.25 * rtemp) ** 1.2
                            bo = finalbox * (1 - float(co) * (xxx[j] - xxx[i]))
                        bo = msbo * bo + csbo

                    if cor4 == "B":
                        aa = 10 ** (0.43 + (8.33 / inog))
                        deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (rtemp + 200)) ** aa
                        if xxx[j] < xxx[i]:
                            aaa = 10.715 * (rs + 100) ** -0.515
                            bbb = 5.44 * (rs + 150) ** -0.338
                            uos = aaa * deadoil ** bbb
                            uo = uos
                        else:
                            aaa = 10.715 * (rs + 100) ** -0.515
                            bbb = 5.44 * (rs + 150) ** -0.338
                            uos = aaa * deadoil ** bbb
                            ass = (-3.9 * (10 ** -5) * xxx[j]) - 5
                            m = 2.6 * xxx[j] ** 1.187 * 10 ** ass
                            uo = uos * (xxx[j] / xxx[i]) ** m
                        uo = mbluo * uo + cbluo
                    elif cor4 == "BR":
                        zz = 3.0324 - 0.02023 * inog
                        yy = 10 ** zz
                        xx = yy * (rtemp) ** -1.163
                        deadoil = (3.141 * (10 ** 10)) * (rtemp ** -3.444) * (math.log10(inog)) ** (
                        10.313 * (math.log10(rtemp)) - 36.447)

                        if xxx[j] < xxx[i]:
                            aaa = 10.715 * (rs + 100) ** -0.515
                            bbb = 5.44 * (rs + 150) ** -0.338
                            uos = aaa * deadoil ** bbb
                            uo = uos
                        else:
                            aaa = 10.715 * (rs + 100) ** -0.515
                            bbb = 5.44 * (rs + 150) ** -0.338
                            uos = aaa * deadoil ** bbb
                            ass = (-3.9 * (10 ** -5) * xxx[j]) - 5
                            m = 2.6 * xxx[j] ** 1.187 * 10 ** ass
                            uo = uos * (xxx[j] / xxx[i]) ** m
                        uo = mbguo * uo + cbguo

                    if i < len(pf) and j == d:
                        f.write("\r\n\t" + str("{:.6f}".format(rs)) + "\t" + str("{:.4f}".format(xxx[j])) + "\t" + str(
                            "{:.6f}".format(bo)) + "\t" + str("{:.6f}".format(uo)))
                    else:
                        f.write(
                            "\r\n\t\t" + str("{:.4f}".format(xxx[j])) + "\t" + str("{:.6f}".format(bo)) + "\t" + str(
                                "{:.6f}".format(uo)))
                    j += 1
                f.write("\t/")
                d += 1
                j = 0
                j += z
                i += 1
            f.write("\r\n/")
            f.write("\r\n\r\nPVDG")
            f.write("\r\n--PVT Properties of dry gas")
            f.write("\r\n--\tP\tBg\tgas visc")

            for pp in range(len(pf)):
                xg = 1 - inn2 - inco2 - inh2s
                gamghc = (ingg - 0.967 * inn2 - 1.52 * inco2 - 1.18 * inh2s) / xg
                tpchc = 168 + 325 * gamghc - 12.5 * gamghc ** 2
                ppchc = 677 + gamghc * (15 - 37.5 * gamghc)
                tpcm = xg * tpchc + 227 * inn2 + 548 * inco2 * 672 * inh2s
                ppcm = xg * ppchc + 493 * inn2 + 1071 * inco2 + 1036 * inh2s
                epslon = 120 * (xg ** 0.9 - xg ** 1.6) + 15 * (inco2 ** 0.5 - inh2s ** 4)
                tpc = tpcm - epslon
                ppc = ppcm * (tpc / (tpcm + inh2s * (1 - inh2s) * epslon))
                tpr = (rtemp + 460) / tpc
                ppr = xxx[pp] / ppc
                AA = 1.39 * (tpr - 0.92) ** 0.5 - 0.36 * tpr - 0.101
                BB = (0.62 - 0.23 * tpr) * ppr + (0.066 / (tpr - 0.86) - 0.037) * ppr ** 2 + 0.32 / 10 ** (
                    9 * (tpr - 1)) * ppr ** 6
                CC = 0.132 - 0.32 * math.log10(tpr)
                DD = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
                fz = AA + ((1 - AA) / cmath.exp(BB)) + (CC * ppr ** DD)

                E = 35.37 * xxx[pp] / (fz * (rtemp + 460))
                bg = (1 / E) * 178.107

                ugas1 = 0.001 * (8.1888 - 6.15 * math.log10(ingg) + (0.01709 - 0.002062 * ingg) * rtemp)
                gv = cmath.exp(-2.4621182 + ppr * (2.97054714 + ppr * (-0.286264054 + ppr * 0.00805420522)) + tpr * (
                    2.80860949 + ppr * (-3.49803305 + ppr * (0.36037302 + ppr * -0.0104432413)) + tpr * (
                        -0.793385684 + ppr * (1.39643306 + ppr * (-0.149144925 + ppr * 0.00441015512)) + tpr *
                        (0.0839387178 + ppr * (
                        -0.186408848 + ppr * (0.0203367881 + ppr * -0.000609579263)))))) / tpr * ugas1

                f.write("\r\n\t" + str("{:.2f}".format(xxx[pp])) + "\t" + str("{:.6f}".format(bg.real)) + "\t" + str(
                    "{:.6f}".format(gv.real)))

            f.write("\r\n/")
            f.write("\r\n\r\nDENSITY")
            f.write("\r\n--Density at surface condition on lb/ft3")
            f.write("\r\n--\tOil\tWater\tGas")

            # water fvf
            A1 = 0.9911 + (6.35 * 10 ** -5) * 60 + (8.5 * 10 ** -7 * 60 ** 2)
            A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * 60 + (
                4.57 * 10 ** -12 * 60 ** 2)
            A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * 60 + (
                -1.43 * 10 ** -15 * 60 ** 2)
            bws = A1 + A2 * 14.7 + A3 * 14.7 ** 2

            d1 = (62.4 * (141.5 / (inog + 131.5))) + (0.0136 * 0 * ingg)
            pwsc = 62.368 + (0.438603 * inws) + (1.60074 * 10 ** -3 * inws)
            d2 = pwsc / bws
            d3 = (28.97 * 14.7 * ingg) / (1 * 10.7316 * (60 + 460))

            f.write(
                "\r\n\t" + str("{:.6f}".format(d1)) + "\t" + str("{:.6f}".format(d2)) + "\t" + str("{:.6f}".format(d3)))
            f.write("\r\n/\r\n")
            # f.close()
        # flash('File Successfully Generated!')
        return flask.send_file('pvt.txt', mimetype='text/plain', attachment_filename='pvt.txt', as_attachment=True)

    if form.sv.data:
        #save code for 1p1m calculation
        if session['type'] == 'Admin':
            # file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data)
            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
            # will update by read again csv and change the dataframe value for the selected case if it exists
            try:
                updf = pd.read_csv(file_name)
                updf.loc[int(form.cse2.data) - 1, 'gor'] = ingor
                updf.loc[int(form.cse2.data) - 1, 'og'] = inog
                updf.loc[int(form.cse2.data) - 1, 'gg'] = ingg
                updf.loc[int(form.cse2.data) - 1, 'temp'] = intemp
                updf.loc[int(form.cse2.data) - 1, 'press'] = inpress
                updf.loc[int(form.cse2.data) - 1, 'h2s'] = inh2s
                updf.loc[int(form.cse2.data) - 1, 'co2'] = inco2
                updf.loc[int(form.cse2.data) - 1, 'n2'] = inn2
                updf.loc[int(form.cse2.data) - 1, 'ppm'] = inppm
                updf.loc[int(form.cse2.data) - 1, 'calcor1'] = session['cor1']
                updf.loc[int(form.cse2.data) - 1, 'calcor2'] = session['cor2']
                updf.loc[int(form.cse2.data) - 1, 'calcor3'] = session['cor3']
                updf.loc[int(form.cse2.data) - 1, 'calcor4'] = session['cor4']
                updf.to_csv(file_name, index=False)

            # this code is for file not exists yet
            except FileNotFoundError:
                pass

        elif session['type'] == 'Guest':
            # check if project/case is new or already exists
            if db.session.query(Calc.id).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).scalar() != None:
                try:
                    db.session.flush()
                    updb = Calc.query.filter_by(pjt=form.pjt.data.pjt, cse=form.cse.data.cse).first()
                    updb.gor = session['ingorr']
                    updb.og = session['inogg']
                    updb.gg = session['inggg']
                    updb.temp = session['uptemp']
                    updb.press = session['uppress']
                    updb.h2s = session['inh2ss']
                    updb.co2 = session['inco22']
                    updb.n2 = session['inn22']
                    updb.ppm = session['inppmm']
                    updb.cor1 = session['cor1']
                    updb.cor2 = session['cor2']
                    updb.cor3 = session['cor3']
                    updb.cor4 = session['cor4']
                    updb.pb = session['xpb']
                    updb.rs = session['xrs']
                    updb.bo = session['xbo']
                    updb.co = session['xco']
                    updb.uo = session['xuo']
                    updb.po = session['xpo']
                    updb.z = session['xz']
                    updb.bg = session['xbg']
                    updb.pg = session['xpg']
                    updb.ug = session['xug']
                    updb.rmk = form.rmk.data
                    updb.bw = session['xbw']
                    updb.uw = session['xuw']
                    updb.pw = session['xpw']
                    updb.cw = session['xcw']
                    updb.iow = session['xiow']
                    updb.iog = session['xiog']
                    updb.iwg = session['xiwg']
                    db.session.commit()

                except exc.IntegrityError:
                    flash('Data is already saved')
            else:
                try:
                    db.session.flush()
                    calc = Calc(gor=ingor, og=inog, gg=ingg, temp=intemp, press=inpress, h2s=inh2s, co2=inco2,
                                proc_id=session['pid'],
                                n2=inn2, ppm=inppm, cor1=session['cor1'], cor2=session['cor2'], cor3=session['cor3'], cor4=session['cor4'], pb=session['xpb'],
                                rs=session['xrs'], bo=session['xbo'], co=session['xco'], uo=session['xuo'],
                                po=session['xpo'],
                                z=session['xz'], bg=session['xbg'], pg=session['xpg'], ug=session['xug'],
                                pjt=form.pjt.data.pjt, cse=form.cse.data.cse, rmk=form.rmk.data,
                                bw=session['xbw'], uw=session['xuw'], pw=session['xpw'], cw=session['xcw'],
                                iow=session['xiow'], iog=session['xiog'], iwg=session['xiwg'])
                    db.session.add(calc)
                    db.session.commit()

                except exc.IntegrityError:
                    flash('Data is already saved')
        # after saved change input in form field according to input entered before this
        form.igor.raw_data = [str(session['ingorr'])]
        form.iog.raw_data = [str(session['inogg'])]
        form.igg.raw_data = [str(session['inggg'])]
        form.itemp.raw_data = [str(session['uptemp'])]
        form.ipress.raw_data = [str(session['uppress'])]
        form.ih2s.raw_data = [str(session['inh2ss'])]
        form.ico2.raw_data = [str(session['inco22'])]
        form.in2.raw_data = [str(session['inn22'])]
        form.ippm.raw_data = [str(session['inppmm'])]

        #save code for match data
        if session['type'] == 'Admin':
            # file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data)
            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
            # will update by read again csv and change the dataframe value for the selected case if it exists
            try:
                updf = pd.read_csv(file_name)

                updf.loc[int(form.cse2.data) - 1, 'mtemp'] = session['mtemp']
                updf.loc[int(form.cse2.data) - 1, 'mbppress'] = session['mbppress']
                updf.loc[int(form.cse2.data) - 1, 'mpress'] = session['mpress']
                updf.loc[int(form.cse2.data) - 1, 'mrs'] = session['mrrs']
                updf.loc[int(form.cse2.data) - 1, 'mbo'] = session['mbbo']
                updf.loc[int(form.cse2.data) - 1, 'muo'] = session['muo']

                updf.loc[int(form.cse2.data) - 1, 'p1gpb'] = session['mpb1']
                updf.loc[int(form.cse2.data) - 1, 'p1spb'] = session['mpb2']
                updf.loc[int(form.cse2.data) - 1, 'p1vbpb'] = session['mpb3']
                updf.loc[int(form.cse2.data) - 1, 'p1pfpb'] = session['mpb4']
                updf.loc[int(form.cse2.data) - 1, 'p1ampb'] = session['mpb5']
                updf.loc[int(form.cse2.data) - 1, 'p2gpb'] = session['cpb1']
                updf.loc[int(form.cse2.data) - 1, 'p2spb'] = session['cpb2']
                updf.loc[int(form.cse2.data) - 1, 'p2vbpb'] = session['cpb3']
                updf.loc[int(form.cse2.data) - 1, 'p2pfpb'] = session['cpb4']
                updf.loc[int(form.cse2.data) - 1, 'p2ampb'] = session['cpb5']

                updf.loc[int(form.cse2.data) - 1, 'p1grs'] = session['mrs1']
                updf.loc[int(form.cse2.data) - 1, 'p1srs'] = session['mrs2']
                updf.loc[int(form.cse2.data) - 1, 'p1vbrs'] = session['mrs3']
                updf.loc[int(form.cse2.data) - 1, 'p1pfrs'] = session['mrs4']
                updf.loc[int(form.cse2.data) - 1, 'p1amrs'] = session['mrs5']
                updf.loc[int(form.cse2.data) - 1, 'p2grs'] = session['crs1']
                updf.loc[int(form.cse2.data) - 1, 'p2srs'] = session['crs2']
                updf.loc[int(form.cse2.data) - 1, 'p2vbrs'] = session['crs3']
                updf.loc[int(form.cse2.data) - 1, 'p2pfrs'] = session['crs4']
                updf.loc[int(form.cse2.data) - 1, 'p2amrs'] = session['crs5']

                updf.loc[int(form.cse2.data) - 1, 'p1gbo'] = session['mbo1']
                updf.loc[int(form.cse2.data) - 1, 'p1sbo'] = session['mbo2']
                updf.loc[int(form.cse2.data) - 1, 'p1vbbo'] = session['mbo3']
                updf.loc[int(form.cse2.data) - 1, 'p1pfbo'] = session['mbo4']
                updf.loc[int(form.cse2.data) - 1, 'p1ambo'] = session['mbo5']
                updf.loc[int(form.cse2.data) - 1, 'p2gbo'] = session['cbo1']
                updf.loc[int(form.cse2.data) - 1, 'p2sbo'] = session['cbo2']
                updf.loc[int(form.cse2.data) - 1, 'p2vbbo'] = session['cbo3']
                updf.loc[int(form.cse2.data) - 1, 'p2pfbo'] = session['cbo4']
                updf.loc[int(form.cse2.data) - 1, 'p2ambo'] = session['cbo5']

                updf.loc[int(form.cse2.data) - 1, 'p1bguo'] = session['muo1']
                updf.loc[int(form.cse2.data) - 1, 'p1bluo'] = session['muo2']
                updf.loc[int(form.cse2.data) - 1, 'p2bguo'] = session['cuo1']
                updf.loc[int(form.cse2.data) - 1, 'p2bluo'] = session['cuo2']

                updf.to_csv(file_name, index=False)

            except FileNotFoundError:
                pass

            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
            # will load input fields for the selected case if it exists
            try:
                lodf = pd.read_csv(file_name)
                if pd.isnull(lodf.loc[int(form.cse2.data) - 1, 'mtemp']):
                    pass
                else:
                    form5.mtemp.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mtemp'])]
                    form5.mbppress.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mbppress'])]
                    form5.mpress.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mpress'])]
                    form5.mrrs.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mrs'])]
                    form5.mbbo.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'mbo'])]
                    form5.muo.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'muo'])]
            except FileNotFoundError:
                pass

        elif session['type'] == 'Guest':
            try:
                # check if project/case is new or already exists
                if db.session.query(Matching.id).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).scalar() != None:
                    Matching.query.filter_by(pjt=form.pjt.data.pjt, cse=form.cse.data.cse).update(
                        dict(temp=session['mtemp'], pb=session['mbppress'], press=session['mpress'],
                             rs=session['mrrs'], bo=session['mbbo'], uo=session['muo'], pbG1=session['mpb1'], pbG2=session['cpb1'], pbS1=session['mpb2'],
                             pbS2=session['cpb2'],
                             pbVB1=session['mpb3'], pbVB2=session['cpb3'], pbP1=session['mpb4'], pbP2=session['cpb4'],
                             pbAM1=session['mpb5'], pbAM2=session['cpb5'],
                             rsG1=session['mrs1'], rsG2=session['crs1'], rsS1=session['mrs2'], rsS2=session['crs2'],
                             rsVB1=session['mrs3'], rsVB2=session['crs3'], rsP1=session['mrs4'], rsP2=session['crs4'],
                             rsAM1=session['mrs5'], rsAM2=session['crs5'],
                             boG1=session['mbo1'], boG2=session['cbo1'], boS1=session['mbo2'], boS2=session['cbo2'],
                             boVB1=session['mbo3'], boVB2=session['cbo3'], boP1=session['mbo4'], boP2=session['cbo4'],
                             boAM1=session['mbo5'], boAM2=session['cbo5'], uoBG1=session['muo1'], uoBG2=session['cuo1'],
                             uoBL1=session['muo2'], uoBL2=session['cuo2']))
                    db.session.commit()
                else:
                    db.session.flush()
                    db.session.add(
                        Matching(temp=session['mtemp'], pb=session['mbppress'], press=session['mpress'],
                                 rs=session['mrrs'], bo=session['mbbo'], uo=session['muo'], pbG1=session['mpb1'],
                                 pbG2=session['cpb1'], pbS1=session['mpb2'], pbS2=session['cpb2'],
                                 pbVB1=session['mpb3'], pbVB2=session['cpb3'], pbP1=session['mpb4'],
                                 pbP2=session['cpb4'],
                                 pbAM1=session['mpb5'], pbAM2=session['cpb5'],
                                 rsG1=session['mrs1'], rsG2=session['crs1'], rsS1=session['mrs2'], rsS2=session['crs2'],
                                 rsVB1=session['mrs3'], rsVB2=session['crs3'], rsP1=session['mrs4'],
                                 rsP2=session['crs4'],
                                 rsAM1=session['mrs5'], rsAM2=session['crs5'],
                                 boG1=session['mbo1'], boG2=session['cbo1'], boS1=session['mbo2'], boS2=session['cbo2'],
                                 boVB1=session['mbo3'], boVB2=session['cbo3'], boP1=session['mbo4'],
                                 boP2=session['cbo4'],
                                 boAM1=session['mbo5'], boAM2=session['cbo5'], uoBG1=session['muo1'],
                                 uoBG2=session['cuo1'],
                                 uoBL1=session['muo2'], uoBL2=session['cuo2'], pjt=form.pjt.data.pjt,
                                 cse=form.cse.data.cse, proc_id=session['pid']))
                    db.session.commit()

                # after saved change input in form field according to input entered before this
                form5.mtemp.raw_data = [str(mtemp)]
                form5.mbppress.raw_data = [str(mbppress)]
                form5.mpress.raw_data = [str(mpress)]
                form5.mrrs.raw_data = [str(mrrs)]
                form5.mbbo.raw_data = [str(mbbo)]
                form5.muo.raw_data = [str(muo)]

            except exc.IntegrityError:
                flash('Data is already saved')

        #save code for many m many p input
        if session['type'] == 'Admin':
            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
            # will update by read again csv and change the dataframe value for the selected case if it exists
            try:
                updf = pd.read_csv(file_name)
                updf.loc[int(form.cse2.data) - 1, 'stemp'] = session['d1']
                updf.loc[int(form.cse2.data) - 1, 'etemp'] = session['d2']
                updf.loc[int(form.cse2.data) - 1, 'step1'] = session['d3']
                updf.loc[int(form.cse2.data) - 1, 'spress'] = session['d4']
                updf.loc[int(form.cse2.data) - 1, 'epress'] = session['d5']
                updf.loc[int(form.cse2.data) - 1, 'step2'] = session['d6']
                updf.to_csv(file_name, index=False)

            except FileNotFoundError:
                pass

        elif session['type'] == 'Guest':
            # check if project/case is new or already exists
            if db.session.query(TblIn.id).filter_by(pjt=str(form.pjt.data.pjt),cse=str(form.cse.data.cse)).scalar() != None:
                TblIn.query.filter_by(pjt=form.pjt.data.pjt, cse=form.cse.data.cse).update(
                    dict(rmk=form.rmk.data, cor1=session['cor1'], cor2=session['cor2'], cor3=session['cor3'], cor4=session['cor4'], stemp=stemp, etemp=etemp,
                         stp1=stp1,
                         spress=spress, epress=epress, stp2=stp2))
                db.session.commit()
            else:
                db.session.flush()
                db.session.add(
                    TblIn(pjt=form.pjt.data.pjt, cse=form.cse.data.cse, proc_id=session['pid'], rmk=form.rmk.data,
                          cor1=session['cor1'], cor2=session['cor2'], cor3=session['cor3'], cor4=session['cor4'], stemp=stemp, etemp=etemp, stp1=stp1,
                          spress=spress, epress=epress, stp2=stp2))
                db.session.commit()

        #save code for many m many p output
        if session['type'] == 'Guest':
            if session['gtnc'] == 'no':
                pass
            elif session['gtnc'] == 'yes':
                ingor = session['ingorr']
                inog = session['inogg']
                ingg = session['inggg']
                inh2s = session['inh2ss']
                inco2 = session['inco22']
                inn2 = session['inn22']
                inppm = session['inppmm']
                pss = session['pss']
                ps = pandas.io.json.read_json(pss)
                tpp = session['tpp']
                tp = pandas.io.json.read_json(tpp)
                cor1 = session['cor1']
                cor2 = session['cor2']
                cor3 = session['cor3']
                cor4 = session['cor4']

                mgpb = session['mpb1']
                mspb = session['mpb2']
                mvbpb = session['mpb3']
                mpfpb = session['mpb4']
                mampb = session['mpb5']
                cgpb = session['cpb1']
                cspb = session['cpb2']
                cvbpb = session['cpb3']
                cpfpb = session['cpb4']
                campb = session['cpb5']

                mgrs = session['mrs1']
                msrs = session['mrs2']
                mvbrs = session['mrs3']
                mpfrs = session['mrs4']
                mamrs = session['mrs5']
                cgrs = session['crs1']
                csrs = session['crs2']
                cvbrs = session['crs3']
                cpfrs = session['crs4']
                camrs = session['crs5']

                mgbo = session['mbo1']
                msbo = session['mbo2']
                mvbbo = session['mbo3']
                mpfbo = session['mbo4']
                mambo = session['mbo5']
                cgbo = session['cbo1']
                csbo = session['cbo2']
                cvbbo = session['cbo3']
                cpfbo = session['cbo4']
                cambo = session['cbo5']

                mbguo = session['muo1']
                mbluo = session['muo2']
                cbguo = session['cuo1']
                cbluo = session['cuo2']

                pf = pd.Index(ps)
                tf = pd.Index(tp)

                data = np.zeros_like(pf)
                data = data.astype(float)

                inws = inppm / 1000000 * 100

                px = np.array(data).ravel()
                px = pd.Series(px)
                tx = np.array(data).ravel()
                tx = pd.Series(tx)

                yyfinalpb = np.array(data).ravel()
                yyfinalpb = pd.Series(yyfinalpb)
                yyfinalrs = np.array(data).ravel()
                yyfinalrs = pd.Series(yyfinalrs)
                yyfinalco = np.array(data).ravel()
                yyfinalco = pd.Series(yyfinalco)
                yyfinalbw = np.array(data).ravel()
                yyfinalbw = pd.Series(yyfinalbw)
                yyfinalbo = np.array(data).ravel()
                yyfinalbo = pd.Series(yyfinalbo)
                yyfinaluo = np.array(data).ravel()
                yyfinaluo = pd.Series(yyfinaluo)
                finalpo = np.array(data).ravel()
                finalpo = pd.Series(finalpo)
                finalz = np.array(data).ravel()
                finalz = pd.Series(finalz)
                gfvf = np.array(data).ravel()
                gfvf = pd.Series(gfvf)
                gd = np.array(data).ravel()
                gd = pd.Series(gd)
                gv = np.array(data).ravel()
                gv = pd.Series(gv)
                finaluw = np.array(data).ravel()
                finaluw = pd.Series(finaluw)
                finalpw = np.array(data).ravel()
                finalpw = pd.Series(finalpw)
                finalcw = np.array(data).ravel()
                finalcw = pd.Series(finalcw)
                xfiow = np.array(data).ravel()
                xfiow = pd.Series(xfiow)
                fiog = np.array(data).ravel()
                fiog = pd.Series(fiog)
                fiwg = np.array(data).ravel()
                fiwg = pd.Series(fiwg)

                try:
                    for j in range(len(tp)):
                        for i in range(len(ps)):
                            if cor1 == "VB":
                                if inog <= 30:
                                    yyfinalpb[i] = ((27.64 * ingor / ingg) * 10 ** (
                                    (-11.172 * inog) / (tf[j] + 460))) ** (
                                                       1 / 1.0937)
                                else:
                                    yyfinalpb[i] = ((56.06 * ingor / ingg) * 10 ** (
                                    (-10.393 * inog) / (tf[j] + 460))) ** (
                                                       1 / 1.187)
                                yyfinalpb[i] = mvbpb * yyfinalpb[i] + cvbpb
                            elif cor1 == "AM":
                                yyfinalpb[i] = 0.00538088 * ingor ** 0.715082 * ingg ** -1.87784 * (141.5 / (
                                    inog + 131.5)) ** 3.1437 * \
                                               (tf[j] + 460) ** 1.32657
                                yyfinalpb[i] = mampb * yyfinalpb[i] + campb
                            elif cor1 == "G":
                                x = (ingor / ingg) ** 0.816 * ((tf[j] ** 0.172) / (inog ** 0.989))
                                logpb = 1.7669 + 1.7447 * math.log10(x) - (0.30218 * (math.log10(x) ** 2))
                                yyfinalpb[i] = 10 ** logpb
                                yyfinalpb[i] = mgpb * yyfinalpb[i] + cgpb
                            elif cor1 == "PF":
                                x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * tf[j] ** 1.3911)
                                yyfinalpb[i] = ((112.727 * ingor ** 0.577421) / (ingg ** 0.8439 * 10 ** x)) - 1391.051
                                yyfinalpb[i] = mpfpb * yyfinalpb[i] + cpfpb
                            elif cor1 == "S":
                                yyfinalpb[i] = 18.2 * (
                                    (ingor / ingg) ** 0.83 * 10 ** (0.00091 * tf[j] - 0.0125 * inog) - 1.4)
                                yyfinalpb[i] = mspb * yyfinalpb[i] + cspb

                            if pf[i] <= 14.7:
                                yyfinalrs[i] = 0
                            else:
                                if pf[i] < yyfinalpb[i]:
                                    if cor2 == "VB":
                                        if inog <= 30:
                                            yyfinalrs[i] = 0.0362 * ingg * pf[i] ** 1.0937 * (
                                                math.exp(25.724 * inog / (tf[j] + 460)))
                                        else:
                                            yyfinalrs[i] = 0.0178 * ingg * pf[i] ** 1.187 * (
                                                math.exp(23.931 * inog / (tf[j] + 460)))
                                        yyfinalrs[i] = mvbrs * yyfinalrs[i] + cvbrs
                                    elif cor2 == "AM":
                                        yyfinalrs[i] = ((185.8432 * ingg ** 1.87784) * (
                                            (141.5 / (inog + 131.5)) ** -3.1437) * (
                                                            (tf[j] + 460)
                                                            ** -1.32657) * pf[i]) ** 1.398441
                                        yyfinalrs[i] = mamrs * yyfinalrs[i] + camrs
                                    elif cor2 == "G":
                                        x = 2.8869 - (14.1811 - 3.3093 * np.log10(pf[i])) ** 0.5
                                        logrs = 10 ** x
                                        yyfinalrs[i] = ingg * (((inog ** 0.989) / (tf[j] ** 0.172)) * logrs) ** 1.2255
                                        yyfinalrs[i] = mgrs * yyfinalrs[i] + cgrs
                                    elif cor2 == "PF":
                                        x = 7.916 * (10 ** -4) * inog ** 1.541 - (4.561 * (10 ** -5) * tf[j] ** 1.3911)
                                        yyfinalrs[i] = (
                                        (((pf[i] / 112.727) + 12.34) * ingg ** 0.8439 * 10 ** x) ** 1.73184)
                                        yyfinalrs[i] = mpfrs * yyfinalrs[i] + cpfrs
                                    elif cor2 == "S":
                                        x = 0.0125 * inog - 0.00091 * tf[j]
                                        yyfinalrs[i] = ingg * (((pf[i] / 18.2) + 1.4) * 10 ** x) ** 1.2048
                                        yyfinalrs[i] = msrs * yyfinalrs[i] + csrs
                                else:
                                    yyfinalrs[i] = ingor

                            if pf[i] > yyfinalpb[i]:
                                # VB
                                yyfinalco[i] = ((-1433) + (5 * yyfinalrs[i]) + (17.2 * tf[j]) - (1180 * ingg) + (
                                    12.61 * inog)) / (
                                                   (10 ** 5) * pf[i])
                            elif pf[i] < yyfinalpb[i]:
                                # Mcain
                                yyfinalco[i] = np.exp(-7.573 - (1.45 * np.log(pf[i])) - (0.383 * np.log(yyfinalpb[i]))
                                                      + (1.402 * math.log((tf[j] + 460)) + (0.256 * math.log(inog)) + (
                                    0.449 * np.log(ingor))))

                            # water fvf
                            A1 = 0.9911 + (6.35 * 10 ** -5) * tf[j] + (8.5 * 10 ** -7 * tf[j] ** 2)
                            A2 = (-1.093 * 10 ** -6) + (-3.497 * 10 ** -9) * tf[j] + (
                                4.57 * 10 ** -12 * tf[j] ** 2)
                            A3 = (5 * 10 ** -11) + (6.429 * 10 ** -13) * tf[j] + (
                                -1.43 * 10 ** -15 * tf[j] ** 2)
                            yyfinalbw[i] = A1 + A2 * pf[i] + A3 * pf[i] ** 2

                            if cor3 == "VB":
                                if pf[i] <= 14.7 and tf[j] == 60:
                                    yyfinalbo[i] = 1
                                elif pf[i] <= yyfinalpb[i]:
                                    if inog <= 30:
                                        yyfinalbo[i] = 1 + 0.0004677 * yyfinalrs[i] + (tf[j] - 60) * (inog / ingg) * (
                                            0.00001751 +
                                            (-1.811 * 10 ** -8) * yyfinalrs[i])
                                    else:
                                        yyfinalbo[i] = 1 + 0.000467 * yyfinalrs[i] + (tf[j] - 60) * (inog / ingg) * (
                                            0.000011 + (1.337 * 10 ** -9)
                                            * yyfinalrs[i])
                                    yyfinalbo[i] = mvbbo * yyfinalbo[i] + cvbbo
                                elif pf[i] > yyfinalpb[i]:
                                    if inog <= 30:
                                        yyfinalbo[i] = 1 + 0.0004677 * yyfinalrs[i] + (tf[j] - 60) * (inog / ingg) * (
                                            0.00001751 +
                                            (-1.811 * 10 ** -8) * yyfinalrs[i])
                                    else:
                                        yyfinalbo[i] = 1 + 0.000467 * yyfinalrs[i] + (tf[j] - 60) * (inog / ingg) * (
                                            0.000011 + (1.337 * 10 ** -9)
                                            * yyfinalrs[i])
                                    yyfinalbo[i] = yyfinalbo[i] * (1 - float(yyfinalco[i]) * (pf[i] - yyfinalpb[i]))
                                    yyfinalbo[i] = mvbbo * yyfinalbo[i] + cvbbo
                            elif cor3 == "AM":
                                if pf[i] <= 14.7 and tf[j] == 60:
                                    yyfinalbo[i] = 1
                                elif pf[i] <= yyfinalpb[i]:
                                    bob = yyfinalrs[i] ** 0.74239 * ingg ** 0.32394 * (141.5 / (
                                    inog + 131.5)) ** -1.20204
                                    yyfinalbo[i] = 0.497069 + (0.862963 * 10 ** -3 * (tf[j] + 460)) + (
                                        0.182594 * 10 ** -2 * bob) + \
                                                   (0.318099 * 10 ** -5 * bob ** 2)
                                    yyfinalbo[i] = mambo * yyfinalbo[i] + cambo
                                elif pf[i] > yyfinalpb[i]:
                                    bob = yyfinalrs[i] ** 0.74239 * ingg ** 0.32394 * (141.5 / (
                                    inog + 131.5)) ** -1.20204
                                    yyfinalbo[i] = 0.497069 + (0.862963 * 10 ** -3 * (tf[j] + 460)) + (
                                        0.182594 * 10 ** -2 * bob) + \
                                                   (0.318099 * 10 ** -5 * bob ** 2)
                                    yyfinalbo[i] = yyfinalbo[i] * (1 - float(yyfinalco[i]) * (pf[i] - yyfinalpb[i]))
                                    yyfinalbo[i] = mambo * yyfinalbo[i] + cambo
                            elif cor3 == "G":
                                if pf[i] <= 14.7 and tf[j] == 60:
                                    yyfinalbo[i] = 1
                                elif pf[i] <= yyfinalpb[i]:
                                    bob = (yyfinalrs[i] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * tf[j])
                                    A = -6.58511 + 2.91329 * np.log10(bob) - 0.27683 * (np.log10(bob) ** 2)
                                    yyfinalbo[i] = 1 + 10 ** A
                                    yyfinalbo[i] = mgbo * yyfinalbo[i] + cgbo
                                elif pf[i] > yyfinalpb[i]:
                                    bob = (yyfinalrs[i] * (ingg / (141.5 / (inog + 131.5))) ** 0.526) + (0.968 * tf[j])
                                    A = -6.58511 + 2.91329 * math.log10(bob) - 0.27683 * (math.log10(bob) ** 2)
                                    yyfinalbo[i] = 1 + 10 ** A
                                    yyfinalbo[i] = yyfinalbo[i] * (1 - float(yyfinalco[i]) * (pf[i] - yyfinalpb[i]))
                                    yyfinalbo[i] = mgbo * yyfinalbo[i] + cgbo
                            elif cor3 == "PF":
                                if pf[i] <= 14.7 and tf[j] == 60:
                                    yyfinalbo[i] = 1
                                elif pf[i] <= yyfinalpb[i]:
                                    yyfinalbo[i] = 1.0113 + 7.2046 * (10 ** -5) * (yyfinalrs[i] ** 0.3738 * (
                                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                                                                       tf[j]) ** 0.5371) ** 3.0936
                                    yyfinalbo[i] = mpfbo * yyfinalbo[i] + cpfbo
                                elif pf[i] > yyfinalpb[i]:
                                    yyfinalbo[i] = 1.0113 + 7.2046 * (10 ** -5) * (yyfinalrs[i] ** 0.3738 * (
                                        ingg ** 0.2914 / (141.5 / (inog + 131.5)) ** 0.6265) + 0.24626 * (
                                                                                       tf[j]) ** 0.5371) ** 3.0936
                                    yyfinalbo[i] = yyfinalbo[i] * (1 - float(yyfinalco[i]) * (pf[i] - yyfinalpb[i]))
                                    yyfinalbo[i] = mpfbo * yyfinalbo[i] + cpfbo
                            elif cor3 == "S":
                                if pf[i] <= 14.7 and tf[j] == 60:
                                    yyfinalbo[i] = 1
                                elif pf[i] <= yyfinalpb[i]:
                                    yyfinalbo[i] = 0.9759 + 0.00012 * (yyfinalrs[i] * (
                                        ingg / (141.5 / (inog + 131.5))) ** 0.5 + 1.25 * tf[j]) ** 1.2
                                    yyfinalbo[i] = msbo * yyfinalbo[i] + csbo
                                elif pf[i] > yyfinalpb[i]:
                                    yyfinalbo[i] = 0.9759 + 0.00012 * (yyfinalrs[i] * (ingg / (141.5 / (inog + 131.5)))
                                                                       ** 0.5 + 1.25 * tf[j]) ** 1.2
                                    yyfinalbo[i] = yyfinalbo[i] * (1 - float(yyfinalco[i]) * (pf[i] - yyfinalpb[i]))
                                    yyfinalbo[i] = msbo * yyfinalbo[i] + csbo

                            if cor4 == "B":
                                aa = 10 ** (0.43 + (8.33 / inog))
                                deadoil = (0.32 + (1.8 * 10 ** 7) / (inog ** 4.53)) * (360 / (tf[j] + 200)) ** aa

                                if pf[i] < yyfinalpb[i]:
                                    aaa = 10.715 * (yyfinalrs[i] + 100) ** -0.515
                                    bbb = 5.44 * (yyfinalrs[i] + 150) ** -0.338
                                    yyfinaluo[i] = aaa * deadoil ** bbb
                                elif pf[i] > yyfinalpb[i]:
                                    aaa = 10.715 * (yyfinalrs[i] + 100) ** -0.515
                                    bbb = 5.44 * (yyfinalrs[i] + 150) ** -0.338
                                    yyfinaluo[i] = aaa * deadoil ** bbb
                                    ass = (-3.9 * (10 ** -5) * pf[i]) - 5
                                    m = 2.6 * pf[i] ** 1.187 * 10 ** ass
                                    yyfinaluo[i] = yyfinaluo[i] * (pf[i] / yyfinalpb[i]) ** m
                                yyfinaluo[i] = mbluo * yyfinaluo[i] + cbluo
                            elif cor4 == "BR":
                                zz = 3.0324 - 0.02023 * inog
                                yy = 10 ** zz
                                xx = yy * (tf[j]) ** -1.163
                                deadoil = (3.141 * (10 ** 10)) * (tf[j] ** -3.444) * (math.log10(inog)) ** (
                                    10.313 * (math.log10(tf[j])) - 36.447)

                                if pf[i] < yyfinalpb[i]:
                                    aaa = 10.715 * (yyfinalrs[i] + 100) ** -0.515
                                    bbb = 5.44 * (yyfinalrs[i] + 150) ** -0.338
                                    yyfinaluo[i] = aaa * deadoil ** bbb
                                elif pf[i] > yyfinalpb[i]:
                                    aaa = 10.715 * (yyfinalrs[i] + 100) ** -0.515
                                    bbb = 5.44 * (yyfinalrs[i] + 150) ** -0.338
                                    yyfinaluo[i] = aaa * deadoil ** bbb
                                    ass = (-3.9 * (10 ** -5) * pf[i]) - 5
                                    m = 2.6 * pf[i] ** 1.187 * 10 ** ass
                                    yyfinaluo[i] = yyfinaluo[i] * (pf[i] / yyfinalpb[i]) ** m
                                yyfinaluo[i] = mbguo * yyfinaluo[i] + cbguo

                            finalpo[i] = ((62.4 * (141.5 / (inog + 131.5))) + (0.0136 * yyfinalrs[i] * ingg)) / \
                                         yyfinalbo[i]

                            xg = 1 - inn2 - inco2 - inh2s
                            gamghc = (ingg - 0.967 * inn2 - 1.52 * inco2 - 1.18 * inh2s) / xg
                            tpchc = 168 + 325 * gamghc - 12.5 * gamghc ** 2
                            ppchc = 677 + gamghc * (15 - 37.5 * gamghc)
                            tpcm = xg * tpchc + 227 * inn2 + 548 * inco2 * 672 * inh2s
                            ppcm = xg * ppchc + 493 * inn2 + 1071 * inco2 + 1036 * inh2s
                            epslon = 120 * (xg ** 0.9 - xg ** 1.6) + 15 * (inco2 ** 0.5 - inh2s ** 4)
                            tpc = tpcm - epslon
                            ppc = ppcm * (tpc / (tpcm + inh2s * (1 - inh2s) * epslon))
                            tpr = (tf[j] + 460) / tpc

                            ppr = pf[i] / ppc
                            AA = 1.39 * (tpr - 0.92) ** 0.5 - 0.36 * tpr - 0.101
                            BB = (0.62 - 0.23 * tpr) * ppr + (0.066 / (tpr - 0.86) - 0.037) * ppr ** 2 + 0.32 / 10 ** (
                                9 * (tpr - 1)) * ppr ** 6
                            CC = 0.132 - 0.32 * np.log10(tpr)
                            DD = 10 ** (0.3106 - 0.49 * tpr + 0.1824 * tpr ** 2)
                            finalz[i] = AA + ((1 - AA) / np.exp(BB)) + (CC * ppr ** DD)

                            ppr = pf[i] / ppc

                            E = 35.37 * pf[i] / (finalz[i] * (tf[j] + 460))
                            gfvf[i] = 1 / E

                            gd[i] = (28.97 * pf[i] * ingg) / (finalz[i] * 10.7316 * (tf[j] + 460))

                            ugas1 = 0.001 * (8.1888 - 6.15 * math.log10(ingg) + (0.01709 - 0.002062 * ingg) * tf[j])
                            gv[i] = math.exp(
                                -2.4621182 + ppr * (2.97054714 + ppr * (-0.286264054 + ppr * 0.00805420522)) + tpr * (
                                    2.80860949 + ppr * (
                                    -3.49803305 + ppr * (0.36037302 + ppr * -0.0104432413)) + tpr * (
                                        -0.793385684 + ppr * (
                                            1.39643306 + ppr * (-0.149144925 + ppr * 0.00441015512)) + tpr *
                                        (0.0839387178 + ppr * (
                                            -0.186408848 + ppr * (
                                            0.0203367881 + ppr * -0.000609579263)))))) / tpr * ugas1

                            finaluw[i] = math.exp(1.003 - (1.479 * 10 ** -2 * tf[j]) + (1.982 * 10 ** -5 * tf[j] ** 2))

                            pwsc = 62.368 + (0.438603 * inws) + (1.60074 * 10 ** -3 * inws)
                            finalpw[i] = pwsc / yyfinalbw[i]

                            C1 = 3.8546 - 0.000134 * pf[i]
                            C2 = -0.01052 + 4.77 * 10 ** -7 * pf[i]
                            C3 = (3.9267 * 10 ** -5) - (8.8 * 10 ** -10 * pf[i])
                            finalcw[i] = (C1 + C2 * tf[j] + C3 * tf[j] ** 2) * 10 ** -6

                            xfiow[i] = 30

                            ido = (1.17013 - (1.694 * 10 ** -3 * tf[j])) * (38.085 - 0.259 * inog)
                            fiog[i] = ido * (0.056379 + (0.94362 * np.exp(-3.8491 * 10 ** -3 * yyfinalrs[i])))

                            Wdens = finalpw[i] * 0.0160185
                            Gdens = gd[i] * 0.0160185
                            fiwg[i] = ((1.53988 * (Wdens - Gdens) + 2.08339) / (
                                ((tf[j] + 460) / 302.881) ** (0.821976 - 1.83785 *
                                                              10 ** -3 * (tf[j] + 460) + 1.34016 * 10 ** -6 * (
                                                                  tf[j] + 460) ** 2))) ** 3.6667

                            tx[j] = tf[j]
                            px[i] = pf[i]

                            if session['tabtype'] == 'normal':
                                db.session.flush()
                                db.session.add(
                                    BasicTblOut(pb=yyfinalpb[i].tolist(), rs=yyfinalrs[i].tolist(),
                                                bo=yyfinalbo[i].tolist(),
                                                co=yyfinalco[i].tolist(), uo=yyfinaluo[i].tolist(),
                                                po=finalpo[i].tolist(),
                                                z=finalz[i].tolist(), bg=gfvf[i].tolist(), pg=gd[i].tolist(),
                                                proc_id=session['pid'],
                                                ug=gv[i].tolist(), bw=yyfinalbw[i].tolist(), uw=finaluw[i].tolist(),
                                                pw=finalpw[i].tolist(),
                                                cw=finalcw[i].tolist(), iow=xfiow[i].tolist(), iog=fiog[i].tolist(),
                                                iwg=fiwg[i].tolist(), temp=tx[j].tolist(), press=px[i].tolist(),
                                                pjt=form.pjt.data.pjt, cse=form.cse.data.cse))
                                db.session.commit()

                            elif session['tabtype'] == 'matched':
                                db.session.flush()
                                db.session.add(
                                    LabTblOut(pb=yyfinalpb[i].tolist(), rs=yyfinalrs[i].tolist(),
                                              bo=yyfinalbo[i].tolist(),
                                              co=yyfinalco[i].tolist(), uo=yyfinaluo[i].tolist(),
                                              po=finalpo[i].tolist(),
                                              z=finalz[i].tolist(), bg=gfvf[i].tolist(), pg=gd[i].tolist(),
                                              ug=gv[i].tolist(), bw=yyfinalbw[i].tolist(), uw=finaluw[i].tolist(),
                                              pw=finalpw[i].tolist(),
                                              cw=finalcw[i].tolist(), iow=xfiow[i].tolist(), iog=fiog[i].tolist(),
                                              proc_id=session['pid'],
                                              iwg=fiwg[i].tolist(), temp=tx[j].tolist(), press=px[i].tolist(),
                                              pjt=form.pjt.data.pjt, cse=form.cse.data.cse))
                                db.session.commit()

                except exc.IntegrityError:
                    flash('Data is already saved')

        #save code for pvt chart
        if session['type'] == 'Admin':
            file_name = '/home/sapphirenitro/mysite/pvtcsv/' + str(form.pjt2.data.pjt) + '.csv'
            # will update by read again csv and change the dataframe value for the selected case if it exists
            try:
                updf = pd.read_csv(file_name)
                updf.loc[int(form.cse2.data) - 1, 'chartprm'] = session['chtchoice']
                updf.loc[int(form.cse2.data) - 1, 'charttemp'] = form3.newT.data
                updf.to_csv(file_name, index=False)
            except FileNotFoundError:
                pass

            # will load input fields for the selected case if it exists
            try:
                lodf = pd.read_csv(file_name)
                if pd.isnull(lodf.loc[int(form.cse2.data) - 1, 'charttemp']):
                    pass
                else:
                    form3.newT.raw_data = [str(lodf.loc[int(form.cse2.data) - 1, 'charttemp'])]
            except FileNotFoundError:
                pass

        elif session['type'] == 'Guest':
            if session['gtnc'] == 'no':
                pass
            elif session['gtnc'] == 'yes':
                for i in range(len(ps)):
                    try:
                        db.session.flush()
                        db.session.add(Chart(pb=yyfinalpb[i].tolist(), rs=yyfinalrs[i].tolist(), bo=yyfinalbo[i].tolist(),
                                             co=yyfinalco[i].tolist(), uo=yyfinaluo[i].tolist(), po=finalpo[i].tolist(),
                                             zf=finalz[i].tolist(), bg=gfvf[i].tolist(), pg=gd[i].tolist(),
                                             ug=gv[i].tolist(), bw=yyfinalbw[i].tolist(), uw=finaluw[i].tolist(),
                                             pw=finalpw[i].tolist(),
                                             cw=finalcw[i].tolist(), iow=xfiow[i].tolist(), iog=fiog[i].tolist(),
                                             proc_id=session['pid'],
                                             iwg=fiwg[i].tolist(), temp=form3.newT.data, press=px[i].tolist(), pjt=form.pjt.data.pjt,
                                             cse=form.cse.data.cse))
                        db.session.commit()
                    except exc.IntegrityError:
                        flash('Data is already saved')

        flash('Save completed!')
        session['saved'] = 'YES'

    return render_template('newapp.html',form=form,form2=form2,form3=form3,form4=form4,form5=form5,exf2=exf2,
                            xfinalpb=xfinalpb,xfinalrs=xfinalrs,xfinalbo=xfinalbo,xfinalco=xfinalco,xfinalbw=xfinalbw,
                            xfinaluo=xfinaluo,xfinalpo=xfinalpo,xfinalz=xfinalz,xfinaluw=xfinaluw,xfinalpw=xfinalpw,
                            xfinalcw=xfinalcw,xgfvf=xgfvf,xgd=xgd,xgv=xgv,fiow=fiow,xfiog=xfiog,xfiwg=xfiwg,ingorr=ingorr,
                            inogg=inogg,inggg=inggg,inh2ss=inh2ss,inco22=inco22,inn22=inn22,inppmm=inppmm,
                            cor1=cor1,cor2=cor2,cor3=cor3,cor4=cor4,
                            stemp=stemp,etemp=etemp,incr1=incr1,stp1=stp1,spress=spress,epress=epress,
                            incr2=incr2,tp=tp,i=i,ps=ps,ii=ii,stp2=stp2,html=html)

if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()


