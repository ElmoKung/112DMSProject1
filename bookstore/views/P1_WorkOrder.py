import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import *

P1_WorkOrder = Blueprint('WorkOrder', __name__, template_folder='../templates')

@P1_WorkOrder.route('/', methods=['GET', 'POST'])
@login_required
def wostore():
    result = P1Production.count()
    count = math.ceil(result[0]/9)
    flag = 0
    
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        search = request.values.get('keyword')
        keyword = search
        
        cursor.prepare('SELECT * FROM Production WHERE pId LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        Prod_row = cursor.fetchall()
        Prod_data = []
        final_data = []
        
        for i in Prod_row:
            Prod = {
                '產品編號': i[0],
                '產品名稱': i[1],
                '需求廠商': i[2],
                '使用料號': i[3]
            }
            Prod_data.append(Prod)
            total = total + 1
        
        if(len(Prod_data) < end):
            end = len(Prod_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(Prod_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('P1_ProductionOrder.html', single=single, keyword=search, Prod_data=Prod_data, user=current_user.name, page=1, flag=flag, count=count)    

    
    elif 'pid' in request.args:
        pid = request.args['pid']
        data=P1Production.get_Production(pid)
        route=P1Route.get_all_Route()
        
        pname = data[1]
        vendor = data[2]
        device = data[3]
        image = 'sdg.jpg'


        
        product = {
            '產品編號': pid,
            '產品名稱': pname,
            '需求廠商': vendor,
            '使用料件': device,
            '產品圖片': image
        }

        return render_template('P1Production.html', data = product,RouteData=route, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        Prod_row = P1Production.get_all_Production()
        Prod_data = []
        final_data = []
        
        for i in Prod_row:
            Prod = {
                '產品編號': i[0],
                '產品名稱': i[1],
                '需求廠商': i[2],
                '使用料號': i[3]
                
            }
            Prod_data.append(Prod)
            
        if(len(Prod_data) < end):
            end = len(Prod_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(Prod_data[j])
        
        return render_template('P1Production.html', Prod_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM PRODUCT WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        Prod_row = cursor.fetchall()
        Prod_data = []
        total = 0
        
        for i in Prod_row:
            Prod = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2]
            }

            Prod_data.append(Prod)
            total = total + 1
            
        if(len(Prod_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('P1_ProductionOrder.html', keyword=search, single=single, Prod_data=Prod_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        Prod_row = P1Production.get_all_Production()
        Prod_data = []
        temp = 0
        for i in Prod_row:
            Prod = {
                '產品編號': i[0],
                '產品名稱': i[1],
                '需求廠商': i[2],
                '使用料件': i[3],
            }
            if len(Prod_data) < 9:
                Prod_data.append(Prod)
        
        return render_template('P1_ProductionOrder.html', Prod_data=Prod_data, user=current_user.name, page=1, flag=flag, count=count)


#--------------------------------------Equipment--------------------------------------#

@P1_WorkOrder.route('/EquipmentUse', methods=['GET', 'POST'])
@login_required
def EquipmentUse():
    result = P1Equipment.count()
    count = math.ceil(result[0]/9)
    flag = 0
    
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        search = request.values.get('keyword')
        keyword = search
        
        cursor.prepare('SELECT * FROM Equipment WHERE eId LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        Equip_row = cursor.fetchall()
        Equip_data = []
        final_data = []
        
        for i in Equip_row:
            Equip = {
                '設備編號': i[0],
                '設備名稱': i[1],
                '設備類型': i[2],
                '綁訂工作站編號': i[3]
            }
            Equip_data.append(Equip)
            total = total + 1
        
        if(len(Equip_data) < end):
            end = len(Equip_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(Equip_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('P1_EquipmentUse.html', single=single, keyword=search,Equip_data=Equip_data, user=current_user.name, page=1, flag=flag, count=count)    

    
    elif 'eid' in request.args:
        eid = request.args['eid']
        data=P1Equipment.get_Equipment(eid)
        tool=P1Tool.get_all_Tool()
        
        EquipmentName = data[1]
        Type = data[2]
        oId = data[3]
        image = 'sdg.jpg'


        
        Equip = {
            '設備編號': eid,
            '設備名稱': EquipmentName,
            '設備類型': Type,
            '綁訂工作站編號': oId,
            '產品圖片': image
        }

        return render_template('P1Equipment.html', data = Equip,ToolData=tool, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        Equip_row = P1Equipment.get_all_Equipment()
        Equip_data = []
        final_data = []
        
        for i in Equip_row:
            Equip = {
                '設備編號': i[0],
                '設備名稱': i[1],
                '設備類型': i[2],
                '綁訂工作站編號': i[3]
                
            }
            Equip_data.append(Equip)
            
        if(len(Equip_data) < end):
            end = len(Equip_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(Equip_data[j])
        
        return render_template('P1Equipment.html', Equip_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM Equipment WHERE EquipmentName LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        Equip_row = cursor.fetchall()
        Equip_data = []
        total = 0
        
        for i in Equip_row:
            Equip = {
                '設備編號': i[0],
                '設備名稱': i[1],
                '設備類型': i[2],
                '綁訂工作站編號': i[3]
            }

            Equip_data.append(Prod)
            total = total + 1
            
        if(len(Equip_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('P1_EquipmentUse.html', keyword=search, single=single, Equip_data=Equip_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        Equip_row = P1Equipment.get_all_Equipment()
        Equip_data = []
        temp = 0
        for i in Equip_row:
            Equip = {
                '設備編號': i[0],
                '設備名稱': i[1],
                '設備類型': i[2],
                '綁訂工作站編號': i[3]
            }
            if len(Equip_data) < 9:
                Equip_data.append(Equip)
        
        return render_template('P1_EquipmentUse.html', Equip_data=Equip_data, user=current_user.name, page=1, flag=flag, count=count)

@P1_WorkOrder.route('/wo', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def wo():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            #data = Cart.get_cart(current_user.id)
            
            #if( data == None): #假如購物車裡面沒有他的資料
            #    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #    Cart.add_cart(current_user.id, time) # 幫他加一台購物車
            #    data = Cart.get_cart(current_user.id) 
                
            #tno = data[2] # 取得交易編號
            
            data = ""
            while(data != None):
                number = str(random.randrange( 10000, 99999))
                en = random.choice(string.ascii_letters)
                tno111 = en + number
                data = P1ProductionOrder.get_Number(tno111)
             
            data2 = ""    
            while(data2 != None):
                number = str(random.randrange( 10000, 99999))
                en = random.choice(string.ascii_letters)
                wono1 = en + number
                data2 = P1ProductionOrder.get_Order(wono1)
                
            
            pId111 = request.values.get('pid') # 要生產的產品編號
            rId111 = request.values.get('Route') # 要生產的流程編號
            # 檢查購物車裡面有沒有商品
            #product = Record.check_product(pid, tno)
            # 取得商品價錢
            #price = Product.get_product(pid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            #if(product == None):
                #Record.add_product( {'id': tno, 'tno':pid, 'price':price, 'total':price} )
            P1ProductionOrder.add_order( {'woNumber': tno111, 'pId':pId111, 'rId':rId111,'WorkOrder':wono1} )
            #else:
                # 假如購物車裡面有的話，就多加一個進去
            #    amount = Record.get_amount(tno, pid)
            #    total = (amount+1)*int(price)
            #    Record.update_product({'amount':amount+1, 'tno':tno , 'pid':pid, 'total':total})

        elif "delete" in request.form :
            pid = request.values.get('delete')
            tno = Cart.get_cart(current_user.id)[2]
            
            Member.delete_product(tno, pid)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('bookstore.bookstore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('bookstore.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_order( {'mid': current_user.id, 'time':time, 'total':total, 'format':format, 'tno':tno} )

            return render_template('complete.html', user=current_user.name)

    product_data = show_WO_info()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('wo.html', data=product_data, user=current_user.name)

@P1_WorkOrder.route('/eq', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def eq():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :            
            eId = request.values.get('pid') # 要生產的設備編號
            tId = request.values.get('Tool') # 使用的配件編號
            st = request.values.get('workStartAt') 
            et = request.values.get('workEndAt') 

            P1UserProduceEquip.add_Use({'uEmpId':current_user.umpid,'eId':eId,'workStartAt':st,'workEndAt':et})
            P1EquipementUseTool.add_use({'eId':eId,'tId':tId,'DateTime':et,'UsedTime':et})

            return render_template('complete.html', user=current_user.name)

    equse_data = show_EQUSE_info()
    
    if equse_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('eq.html', data=equse_data, user=current_user.name)






# 會員購物車
@P1_WorkOrder.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            data = Cart.get_cart(current_user.id)
            
            if( data == None): #假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Cart.add_cart(current_user.id, time) # 幫他加一台購物車
                data = Cart.get_cart(current_user.id) 
                
            tno = data[2] # 取得交易編號
            pid = request.values.get('pid') # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            product = Record.check_product(pid, tno)
            # 取得商品價錢
            price = Product.get_product(pid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            if(product == None):
                Record.add_product( {'id': tno, 'tno':pid, 'price':price, 'total':price} )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                amount = Record.get_amount(tno, pid)
                total = (amount+1)*int(price)
                Record.update_product({'amount':amount+1, 'tno':tno , 'pid':pid, 'total':total})

        elif "delete" in request.form :
            pid = request.values.get('delete')
            tno = Cart.get_cart(current_user.id)[2]
            
            Member.delete_product(tno, pid)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('bookstore.bookstore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('bookstore.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_order( {'mid': current_user.id, 'time':time, 'total':total, 'format':format, 'tno':tno} )

            return render_template('complete.html', user=current_user.name)

    product_data = only_cart()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=product_data, user=current_user.name)

@P1_WorkOrder.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[1])
        product = {
            '商品編號': i[1],
            '商品名稱': pname,
            '商品價格': i[3],
            '數量': i[2]
        }
        product_data.append(product)
    
    total = Record.get_total(tno)[0]

    return render_template('order.html', data=product_data, total=total, user=current_user.name)

@P1_WorkOrder.route('/orderlist')
def orderlist():
    if "oid" in request.args :
        pass
    
    user_id = current_user.id

    data = Member.get_order(user_id)
    orderlist = []

    for i in data:
        temp = {
            '訂單編號': i[0],
            '訂單總價': i[3],
            '訂單時間': i[2]
        }
        orderlist.append(temp)
    
    orderdetail_row = Order_List.get_orderdetail()
    orderdetail = []

    for j in orderdetail_row:
        temp = {
            '訂單編號': j[0],
            '商品名稱': j[1],
            '商品單價': j[2],
            '訂購數量': j[3]
        }
        orderdetail.append(temp)


    return render_template('orderlist.html', data=orderlist, detail=orderdetail, user=current_user.name)

def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Record.get_record(data[2])

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Record.update_product({
                'amount':request.form[i[1]],
                'pid':i[1],
                'tno':tno,
                'total':int(request.form[i[1]])*int(i[3])
            })
            print('change')

    return 0


def only_cart():
    
    count = Cart.check(current_user.id)

    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    tno = data[2]
    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pid = i[1]
        pname = Product.get_name(i[1])
        price = i[3]
        amount = i[2]
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '數量': amount
        }
        product_data.append(product)
    
    return product_data

def show_WO_info():
    data_row = P1ProductionOrder.get_all_Order()
    wolist_data = []
    for i in data_row:
        pId = i[0]
        wono = i[2]
        worder = i[3]
        rId = i[1]
        

        wolist = {
            '產品編號': pId,
            '工單名稱': worder,
            '工單編號': wono,
            '流程編號': rId
        }
        
        wolist_data.append(wolist)  
    
    
    return wolist_data

def show_EQUSE_info():
    data_row = P1UserProduceEquip.get_all_Use()
    eqlist_data = []
    for i in data_row:
        uId = i[0]
        eId = i[1]
        wA = i[2]
        wE = i[3]
        

        equselist = {
            '員工編號': uId,
            '設備編號': eId,
            '開始時間': wA,
            '結束時間': wE
        }
        
        eqlist_data.append(equselist)  
    
    
    return eqlist_data