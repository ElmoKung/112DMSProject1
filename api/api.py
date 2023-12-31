import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
#login_manager.login_view = 'api.login' # type: ignore
login_manager.login_view = 'api.P1_Operatorlogin' # type: ignore
login_manager.login_message = "請先登入"
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    #data = Member.get_role(userid)
    data = P1Operator.get_operatorrole(userid)
    try:
        user.role = data[0]
        user.name = data[1]
        user.umpid = data[2]
    except:
        pass
    return user

@api.route('/P1_Operatorlogin', methods=['POST', 'GET'])
def P1_Operatorlogin():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']
        data = P1Operator.get_operator(account)  # type: ignore

        try:
            DB_password = data[0][1]
            user_id = data[0][0]
            identity = data[0][3]
            uempid=data[0][0]
        except:
            flash('*沒有此帳號')
            return redirect(url_for('api.P1_Operatorlogin'))

        if(DB_password == password ):
            user = User()
            user.id = user_id
            user.umpid = uempid
            login_user(user)

            if( identity == 'OP'):
                return redirect(url_for('WorkOrder.wostore'))
            else:
                return redirect(url_for('manager.P1_Tool'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    
    return render_template('P1_Operatorlogin.html')

@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']
        data = Member.get_member(account)  # type: ignore

        try:
            DB_password = data[0][1]
            user_id = data[0][2]
            identity = data[0][3]

        except:
            flash('*沒有此帳號')
            return redirect(url_for('api.login'))

        if(DB_password == password ):
            user = User()
            user.id = user_id
            login_user(user)

            if( identity == 'user'):
                return redirect(url_for('bookstore.bookstore'))
            else:
                return redirect(url_for('manager.Product'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    
    return render_template('login.html')
#
@api.route('/P1_OperatorRegister', methods=['POST', 'GET'])
def P1_OperatorRegister():
    if request.method == 'POST':
        user_operator = request.form['uEmpId']
        exist_operator = P1Operator.get_all_operator()
        operator_list = []
        for i in exist_operator:
            operator_list.append(i[0])

        if(user_operator in operator_list):
            flash('Falied!')
            return redirect(url_for('api.P1_OperatorRegister'))
        else:
            input = { 
                'uEmpId':user_operator, 
                'Name': request.form['username'], 
                'AccessLevel': request.form['AccessLevel'], 
                'Shift': request.form['Shift'], 
                'HiredDate':request.form['HiredDate'] ,
                'password':request.form['password']
            }
            P1Operator.create_operator(input)
            return redirect(url_for('api.P1_OperatorRegister'))

    return render_template('P1_OperatorRegister.html')

@api.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_account = request.form['account']
        exist_account = Member.get_all_account()
        account_list = []
        for i in exist_account:
            account_list.append(i[0])

        if(user_account in account_list):
            flash('Falied!')
            return redirect(url_for('api.register'))
        else:
            input = { 
                'name': request.form['username'], 
                'account':user_account, 
                'password':request.form['password'], 
                'identity':request.form['identity'] 
            }
            Member.create_member(input)
            return redirect(url_for('api.login'))

    return render_template('register.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))