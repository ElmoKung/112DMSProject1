from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.P1_Tool'))

#-------------Tool----------------

@manager.route('/P1_Tool', methods=['GET', 'POST'])
@login_required
def P1_Tool():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = P1EquipementUseTool.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = P1Tool.get_Tool(pid)
            P1Tool.delete_Tool(pid)
    
    elif 'edit' in request.values:
        tid = request.values.get('edit')
        return redirect(url_for('manager.Tooledit', tid=tid))
    
    Tool_data = Tool()
    return render_template('P1_Tool.html', P1_Tool_data = Tool_data, user=current_user.name)

def Tool():
    Tool_row = P1Tool.get_all_Tool()
    Tool_data = []
    for i in Tool_row:
        Tool = {
            '配件編號': i[0],
            '配件名稱': i[1],
            '配件類別': i[2]
        }
        Tool_data.append(Tool)
    return Tool_data

@manager.route('/Tooladd', methods=['GET', 'POST'])
def Tooladd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = P1Tool.get_Tool(pid)

        name = request.values.get('Toolname')
        tId = request.values.get('ToolId')
        ToolType = request.values.get('ToolType')
        UpdateTime = request.values.get('UpdateTime')
        
        duprecord=P1Tool.preadd_Tool(name)
        
        if(duprecord!=None):
            flash('duplicated product name')
            return redirect(url_for('manager.P1_Tool'))
        
        P1Tool.add_Tool(
            {'tId' : tId,
             'ToolName' : name,
             'Type' : ToolType,
             'uEmpId' : current_user.umpid,
             'UpdateTime':UpdateTime
            }
        )

        return redirect(url_for('manager.P1_Tool'))

    return render_template('P1_Tool.html')

@manager.route('/Tooledit', methods=['GET', 'POST'])
@login_required
def Tooledit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        P1Tool.update_Tool(
            {
            'ToolName' : request.values.get('ToolName'),
            'Type' : request.values.get('Type'),
            'uEmpid' : current_user.umpid, 
            'updatetime' : request.values.get('updatetime'),
            'tid' : request.values.get('tid')
            }
        )
        
        return redirect(url_for('manager.P1_Tool'))

    else:
        Tool = show_Tool_info()
        return render_template('Tooledit.html', data=Tool)

def show_Tool_info():
    tid = request.args['tid']
    data = P1Tool.get_Tool(tid)
    tname = data[1]
    type = data[2]
    updatetime = data[4]

    tool = {
        '配件編號': tid,
        '配件名稱': tname,
        '配件類型': type,
        '更新時間': updatetime
    }
    return tool

#-------------Equipment----------------
@manager.route('/P1_Equipment', methods=['GET', 'POST'])
@login_required
def P1_Equipment():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = P1EquipementUseTool.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = P1Equipment.get_Equipment(pid)
            P1Equipment.delete_Equipment(pid)
    
    elif 'edit' in request.values:
        eid = request.values.get('edit')
        return redirect(url_for('manager.Equipmentedit', eid=eid))

    Equipment_data = Equipment()
    return render_template('P1_Equipment.html', P1_Equipment_data = Equipment_data, user=current_user.name)

def Equipment():
    Equipment_row = P1Equipment.get_all_Equipment()
    Equipment_data = []
    for i in Equipment_row:
        #get Equipment Binding which Operation
        aOperation=P1Operation.get_Operation(i[3])
        Equipment = {
            '設備編號': i[0],
            '設備名稱': i[1],
            '設備類別': i[2],
            '綁定工作站編號': i[3],
            '綁定工作站': aOperation[0]
        }
        Equipment_data.append(Equipment)
    return Equipment_data

@manager.route('/Equipmentadd', methods=['GET', 'POST'])
def Equipmentadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            eid = en + number
            data = P1Equipment.get_Equipment(eid)
            
        name = request.values.get('Equipmentname')
        category = request.values.get('EquipmentType')
        OperationId = request.values.get('OperationId')
        
        duprecord=P1Equipment.preadd_Equipment(name)
        
        Operation_check=P1Operation.get_Operation(OperationId)
        if(Operation_check==None):
            flash('No such OperationId')
            return redirect(url_for('manager.P1_Equipment'))
        
        if(duprecord!=None):
            flash('duplicated Equipment name')
            return redirect(url_for('manager.P1_Equipment'))
        
        P1Equipment.add_Equipment(
            {'eId' : eid,
             'EquipmentName' : name,
             'Type' : category,
             'OId' : OperationId,
            }
        )

        return redirect(url_for('manager.P1_Equipment'))

    return render_template('P1_Equipment.html')

@manager.route('/Equipmentedit', methods=['GET', 'POST'])
@login_required
def Equipmentedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        
        checkOperation=P1Operation.get_Operation(request.values.get('OId'))
        if(checkOperation==None):
            flash('No such OperationId')
            return redirect(url_for('manager.P1_Equipment'))
        
        P1Equipment.update_Equipment(
            {
            'EquipmentName' : request.values.get('EquipmentName'),
            'Type' : request.values.get('Type'),
            'OId' : request.values.get('OId'), 
            'eId' : request.values.get('eId')
            }
        )
        
        return redirect(url_for('manager.P1_Equipment'))

    else:
        Equipment = show_Equipment_info()
        return render_template('Equipmentedit.html', data=Equipment)

def show_Equipment_info():
    eid = request.args['eid']
    data = P1Equipment.get_Equipment(eid)
    ename = data[1]
    type = data[2]
    oid = data[3]

    equipment = {
        '設備編號': eid,
        '設備名稱': ename,
        '設備類型': type,
        '綁定工作站編號': oid
    }
    return equipment

#-------------Production----------------

@manager.route('/P1_Production', methods=['GET', 'POST'])
@login_required
def P1_Production():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = P1ProductionOrder.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = P1Production.get_Production(pid)
            P1Production.delete_Production(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.Productionedit', pid=pid))
    
    Production_data = Production()
    return render_template('P1_Production.html', P1_Production_data = Production_data, user=current_user.name)

def Production():
    Production_row = P1Production.get_all_Production()
    Production_data = []
    for i in Production_row:
        Production = {
            '產品編號': i[0],
            '產品名稱': i[1],
            '需求廠商': i[2],
            '料號': i[3]
        }
        Production_data.append(Production)
    return Production_data

@manager.route('/Productionadd', methods=['GET', 'POST'])
def Productionadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = P1Recipe.get_Recipe(pid)
            
        name = request.values.get('Productionname')
        Vendor = request.values.get('Vendor')
        Device = request.values.get('Device') 
        
        duprecord=P1Production.preadd_Production(name)
        
        if(duprecord!=None):
            flash('duplicated production name')
            return redirect(url_for('manager.P1_Production'))
        
        P1Production.add_Production(
            {'pId' : pid,
             'ProductionName' : name,
             'Vendor' : Vendor,
             'Device' : Device,
            }
        )

        return redirect(url_for('manager.P1_Production'))

    return render_template('P1_Production.html')

@manager.route('/Productionedit', methods=['GET', 'POST'])
@login_required
def Productionedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        P1Production.update_Production(
            {
            'ProductionName' : request.values.get('ProductionName'),
            'Vendor' : request.values.get('Vendor'),
            'Device' : request.values.get('Device'), 
            'pId' : request.values.get('pId')
            }
        )
        
        return redirect(url_for('manager.P1_Production'))

    else:
        Production = show_Production_info()
        return render_template('Productionedit.html', data=Production)

def show_Production_info():
    pid = request.args['pid']
    data = P1Production.get_Production(pid)
    pname = data[1]
    vendor = data[2]
    device = data[3]

    production = {
        '產品編號': pid,
        '產品名稱': pname,
        '需求廠商': vendor,
        '料號': device
    }
    return production

#-------------Route----------------
@manager.route('/P1_Route', methods=['GET', 'POST'])
@login_required
def P1_Route():
    if request.method == 'GET':
        if(current_user.role == 'user'): # type: ignore
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        rid = request.values.get('delete')
        data = P1RouteOpers.delete_check(rid) # type: ignore
        
        if(data != None):
            flash('failed')
        else:
            data = P1Route.get_Route(rid) # type: ignore
            P1Route.delete_Route(rid) # type: ignore
    
    elif 'edit' in request.values:
        rId = request.values.get('edit')
        return redirect(url_for('manager.Routeedit', rId=rId))
    
    Route_data = Route()
    return render_template('P1_Route.html', P1_Route_data = Route_data, user=current_user.name)# type: ignore

def Route():
    Route_row = P1Route.get_all_Route() # type: ignore
    Route_data = []
    for i in Route_row:
        Route = {
            '流程編號': i[0],
            '流程名稱': i[1],
            '流程說明': i[2]
        }
        Route_data.append(Route)
    return Route_data

@manager.route('/Routeadd', methods=['GET', 'POST'])
def Routeadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            rId = en + number
            data = P1Recipe.get_Recipe(rId)
            
        name = request.values.get('Routename')
        description = request.values.get('RouteDesc')
        
        duprecord=P1Route.preadd_Route(name)
        
        if(duprecord!=None):
            flash('duplicated route name')
            return redirect(url_for('manager.P1_Route'))
        
        P1Route.add_Route(
            {'rId' : rId,
             'RouteName' : name,
             'RouteDesc' : description
            }
        )

        return redirect(url_for('manager.P1_Route'))

    return render_template('P1_Route.html')

@manager.route('/Routeedit', methods=['GET', 'POST'])
@login_required
def Routeedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        P1Route.update_Route(
            {
            'RouteName' : request.values.get('RouteName'),
            'RouteDesc' : request.values.get('RouteDesc'),
            'rId' : request.values.get('rId')
            }
        )
        
        return redirect(url_for('manager.P1_Route'))

    else:
        Route = show_Route_info()
        return render_template('Routeedit.html', data=Route)

def show_Route_info():
    rId = request.args['rId']
    data = P1Route.get_Route(rId)
    rname = data[1]
    rdesc = data[2]

    route = {
        '流程編號': rId,
        '流程名稱': rname,
        '流程說明': rdesc
    }
    return route

#-------------Recipe----------------
@manager.route('/P1_Recipe', methods=['GET', 'POST'])
@login_required
def P1_Recipe():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        ppid = request.values.get('delete')
        data = P1Operation.Recipedelete_check(ppid)
        
        if(data != None):
            flash('failed')
        else:
            data = P1Recipe.get_Recipe(ppid)
            P1Recipe.delete_Recipe(ppid)
    
    elif 'edit' in request.values:
        ppid = request.values.get('edit')
        return redirect(url_for('manager.Recipeedit', ppid=ppid))
    
    Recipe_data = Recipe()
    return render_template('P1_Recipe.html', P1_Recipe_data = Recipe_data, user=current_user.name)

def Recipe():
    Recipe_row = P1Recipe.get_all_Recipe()
    Recipe_data = []
    for i in Recipe_row:
        Recipe = {
            '配方編號': i[0],
            '配方名稱': i[2],
            '配方說明': i[1]
        }
        Recipe_data.append(Recipe)
    return Recipe_data

@manager.route('/Recipeadd', methods=['GET', 'POST'])  
def Recipeadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            ppid = en + number
            data = P1Recipe.get_Recipe(ppid)
        
        name = request.values.get('Recipename')
        description = request.values.get('RecipeDesc')
        
        duprecord=P1Recipe.preadd_Recipe(name)
        
        if(duprecord!=None):
            flash('duplicated recipe name')
            return redirect(url_for('manager.P1_Recipe'))
        
        P1Recipe.add_Recipe(
            {'PPId' : ppid,
             'Recipe' : name,
             'Description' : description,
            }
        )

        return redirect(url_for('manager.P1_Recipe'))

    return render_template('P1_Recipe.html')

@manager.route('/Recipeedit', methods=['GET', 'POST'])
@login_required
def Recipeedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        P1Recipe.update_Recipe(
            {
            'Recipe' : request.values.get('Recipe'),
            'Description' : request.values.get('Description'),
            'PPId' : request.values.get('PPId')
            }
        )
        
        return redirect(url_for('manager.P1_Recipe'))

    else:
        Recipe = show_Recipe_info()
        return render_template('Recipeedit.html', data=Recipe)

def show_Recipe_info():
    ppid = request.args['ppid']
    data = P1Recipe.get_Recipe(ppid)
    pname = data[2]
    pdesc = data[1]

    recipe = {
        '配方編號': ppid,
        '配方名稱': pname,
        '配方說明': pdesc
    }
    return recipe

#-------------Operation----------------
@manager.route('/P1_Operation', methods=['GET', 'POST'])   
@login_required
def P1_Operation():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        oid = request.values.get('delete')
        data = P1RouteOpers.Operdelete_check(oid)
        if(data == None):
            data = P1Equipment.Operdelete_check(oid)
        
        if(data != None):
            flash('failed')
        else:
            P1Operation.delete_Operation(oid)
    
    elif 'edit' in request.values:
        oid = request.values.get('edit')
        return redirect(url_for('manager.Operationedit', oid=oid))
    
    Operation_data = Operation()
    return render_template('P1_Operation.html', P1_Operation_data = Operation_data, user=current_user.name)

def Operation():
    Operation_row = P1Operation.get_all_Operation()
    Operation_data = []
    for i in Operation_row:
        Operation = {
            '工作站編號': i[0],
            '工作站名稱': i[1],
            '工作站說明': i[2],
            '配方ID': i[3],
            '維護人員': i[4],
            '維護時間': i[5],
        }
        Operation_data.append(Operation)
    return Operation_data

@manager.route('/Operationadd', methods=['GET', 'POST'])
def Operationadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            OId = en + number
            data = P1Operation.get_Operation(OId)
        
        OperationName = request.values.get('Operationname')
        Description = request.values.get('OperationDesc')
        PPId = request.values.get('PPId')
        uEmpId = current_user.umpid
        UpdateTime = request.values.get('UpdateTime')
        
        duprecord=P1Operation.preadd_Operation(OperationName)
        
        if(duprecord!=None):
            flash('duplicated operation name')
            return redirect(url_for('manager.P1_Operation'))
        
        PPIDCheck=P1Recipe.get_Recipe(PPId)
        if(PPIDCheck==None):
            flash('No such PPId')
            return redirect(url_for('manager.P1_Operation'))
        
        P1Operation.add_Operation(
            {'OId' : OId,
             'OperationName' : OperationName,
             'Description' : Description,
             'PPId' : PPId,
             'uEmpId' : uEmpId,
             'UpdateTime':UpdateTime
            }
        )

        return redirect(url_for('manager.P1_Operation'))

    return render_template('P1_Operation.html')

@manager.route('/Operationedit', methods=['GET', 'POST'])
@login_required
def Operationedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if request.method == 'POST':
        
        PPIDCheck=P1Recipe.get_Recipe(request.values.get('PPId'))
        if(PPIDCheck==None):
            flash('No such PPId')
            return redirect(url_for('manager.P1_Operation'))
        
        P1Operation.update_Operation(
            {'OperationName' : request.values.get('OperationName'),
            'Description' : request.values.get('Description'),
            'PPId' : request.values.get('PPId'),
            'uEmpId' : current_user.umpid,
            'UpdateTime' : request.values.get('UpdateTime'),
            'OId' : request.values.get('OId')
            }
        )
        
        return redirect(url_for('manager.P1_Operation'))

    else:
        Operation = show_Operation_info()
        return render_template('Operationedit.html', data=Operation)

def show_Operation_info():
    oid = request.args['oid']
    data = P1Operation.get_Operation(oid)
    oname = data[1]
    odesc = data[2]
    ppid = data[3]
    uempid = data[4]
    updatetime = data[5]

    operation = {
        '工作站編號': oid,
        '工作站名稱': oname,
        '工作站說明': odesc,
        '配方ID': ppid,
        '維護人員': uempid,
        '維護時間': updatetime
    }
    return operation


#-----------------RouteOpers----------------
@manager.route('/P1_RouteOpers', methods=['GET', 'POST'])
@login_required
def P1_RouteOpers():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
    if 'delete' in request.values:
        roid = request.values.get('delete')
        data = P1RouteOpers.Operdelete_check(roid)
        if(data == None):
            data = P1Equipment.Operdelete_check(roid)
        
        if(data != None):
            flash('failed')
        else:
            P1RouteOpers.delete_RouteOpers(roid)
    
    elif 'edit' in request.values:
        roid = request.values.get('edit')
        return redirect(url_for('manager.RouteOpersedit', roid=roid))
          
        
        
        
        
    RouteOpers_data = RouteOpers()
    return render_template('P1_RouteOpers.html', P1_RouteOpers_data = RouteOpers_data, user=current_user.name)

def RouteOpers():
    RouteOpers_row = P1RouteOpers.get_all_RouteOpers()
    RouteOpers_data = []
    for i in RouteOpers_row:
        RouteOpers = {
            '工作站流程編號': i[3],
            '工作站編號': i[1],
            '流程編號': i[0],
            '工作站流程順序': i[2]
        }
        RouteOpers_data.append(RouteOpers)
    return RouteOpers_data

@manager.route('/RouteOpersadd', methods=['GET', 'POST'])
def RouteOpersadd():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            ROId = en + number
            data = P1RouteOpers.get_RouteOpers(ROId)
        
        oId = request.values.get('OId')
        rId = request.values.get('rId')
        Sequence = request.values.get('Sequence')
        
        duprecord=P1RouteOpers.preadd_RouteOpers(ROId)
        
        if(duprecord!=None):
            flash('duplicated RouteOpers')
            return redirect(url_for('manager.P1_RouteOpers'))
        elif(P1RouteOpers.preadd2_RouteOpers({'oId':oId,'rId':rId})!=None):
            flash('duplicated RouteOpers No')
            return redirect(url_for('manager.P1_RouteOpers'))
        
        
        P1RouteOpers.add_RouteOpers(
            {'ROId' : ROId,
             'oId' : oId,
             'rId' : rId,
             'Sequence' : Sequence
            }
        )

        return redirect(url_for('manager.P1_RouteOpers'))

    return render_template('P1_RouteOpers.html')

@manager.route('/RouteOpersedit', methods=['GET', 'POST']) 
@login_required
def RouteOpersedit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
    if request.method == 'POST':
        P1RouteOpers.update_RouteOpers(
            {'oId' : request.values.get('oId'),
             'rId' : request.values.get('rId'),
             'Sequence' : request.values.get('Sequence'),
             'roId' : request.values.get('roId')
            }
        )
        
        return redirect(url_for('manager.P1_RouteOpers'))

    else:
        RouteOpers = show_RouteOpers_info()
        return render_template('RouteOpersedit.html', data=RouteOpers)

def show_RouteOpers_info():
    roid = request.args['roid']
    data = P1RouteOpers.get_RouteOpers(roid)
    oid = data[1]
    rid = data[0]
    sequence = data[2]

    routeopers = {
        '工作站流程編號': roid,
        '工作站編號': oid,
        '流程編號': rid,
        '工作站流程順序': sequence
    }
    return routeopers



























@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    
    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)


def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '商品編號': i[0],
            '商品名稱': i[1],
            '商品售價': i[2],
            '商品類別': i[3]
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = Product.get_product(pid)

        name = request.values.get('name')
        price = request.values.get('price')
        category = request.values.get('category')
        description = request.values.get('description')

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        
        duprecord=Product.preadd_name(name)
        
        if(duprecord!=None):
            flash('duplicated product name')
            return redirect(url_for('manager.productManager'))
        
        Product.add_product(
            {'pid' : pid,
             'name' : name,
             'price' : price,
             'category' : category,
             'description':description
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_product(
            {
            'name' : request.values.get('name'),
            'price' : request.values.get('price'),
            'category' : request.values.get('category'), 
            'description' : request.values.get('description'),
            'pid' : request.values.get('pid')
            }
        )
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_Tool_info()
        return render_template('edit.html', data=product)

def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[2]
    category = data[3]
    description = data[4]

    product = {
        '商品編號': pid,
        '商品名稱': pname,
        '單價': price,
        '類別': category,
        '商品敘述': description
    }
    return product



@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)