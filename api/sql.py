from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class P1Operator():
    def get_operator(OPName):
        sql = "SELECT UEMPID,Password,NAME,ACCESSLEVEL,Shift,HiredDate FROM Operator WHERE UEMPID = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : OPName}))
    def get_all_operator():
        sql = "SELECT UEMPID FROM Operator"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    def create_operator(input):
        sql = 'INSERT INTO Operator VALUES (:uEmpId, :name, :AccessLevel, :Shift, :HiredDate,:password)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def get_operatorrole(UEMPID):
        sql = 'SELECT ACCESSLEVEL, NAME,UEMPID FROM Operator WHERE UEMPID = :UEMPID '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'UEMPID':UEMPID}))
    
class P1Tool():
    def get_all_Tool():
        sql = 'SELECT * FROM Tool'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Tool(pid):
        sql ='SELECT * FROM Tool WHERE TID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))
    def preadd_Tool(pname):
        sql = 'SELECT TOOLNAME FROM Tool WHERE TOOLNAME = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':pname}))
    def delete_Tool(pid):
        sql = 'DELETE FROM Tool WHERE TID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()
    def add_Tool(input):
        sql = 'INSERT INTO Tool VALUES (:tId, :ToolName, :Type, :uEmpId, :UpdateTime)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Tool(input):
        sql = 'UPDATE Tool SET ToolName=:ToolName, Type=:Type, updatetime=:updatetime, uEmpid=:uEmpid WHERE TID=:tid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()    
    
class P1Equipment():
    def count():
        sql = 'SELECT COUNT(*) FROM Equipment'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    def get_all_Equipment():#eId,EquipmentName,Type,OId
        sql = 'SELECT * FROM Equipment'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_all_Equipment_Relatedinfo():#eId,EquipmentName,Type,OId,OID_1,
        sql = 'select rops.sequence seq, eq.* ,opers.OPerationName,opers.description OperDesc,opers.PPid,rt.rid,rt.routename,rt.routedesc from operation opers right join equipment eq on  opers.oid=eq.oid , routeopers rops left join route rt on rops.rid=rt.rid where rops.oid=opers.oid order by rt.rid asc, rops.sequence asc'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Equipment(eid):#eId,EquipmentName,Type,OId
        sql ='SELECT * FROM Equipment WHERE eID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': eid}))
    def get_Equipment_Relatedinfo(eid):#eId,EquipmentName,Type,OId
        sql ='select eq.* ,opers.OPerationName,opers.description OperDesc,opers.PPid,rt.rid,rt.routename,rt.routedesc from operation opers right join equipment eq on  opers.oid=eq.oid , routeopers rops left join route rt on rops.rid=rt.rid where rops.oid=opers.oid and eID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': eid}))
    def preadd_Equipment(ename):
        sql = 'SELECT EquipmentName FROM Equipment WHERE EquipmentName = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':ename}))
    def delete_Equipment(eid):
        sql = 'DELETE FROM Equipment WHERE EID = :id '
        DB.execute_input(DB.prepare(sql), {'id': eid})
        DB.commit()
    def add_Equipment(input):
        sql = 'INSERT INTO Equipment VALUES (:eId, :EquipmentName, :Type,:OId)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Equipment(input):
        sql = 'UPDATE Equipment SET EquipmentName=:EquipmentName, Type=:Type, OId=:OId WHERE EID=:eId'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()  
    def Operdelete_check(oId):
        sql = 'SELECT * FROM Equipment WHERE oId=:oId'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'oId':oId}))      
        
class P1Production():
    def count():
        sql = 'SELECT COUNT(*) FROM Production'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_all_Production(): #pId,ProductName,Vendor,Device
        sql = 'SELECT * FROM Production'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Production(pid):
        sql ='SELECT * FROM Production WHERE pId = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))
    def preadd_Production(pname):
        sql = 'SELECT ProductName FROM Production WHERE ProductName = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':pname}))
    def delete_Production(pid):
        sql = 'DELETE FROM Production WHERE pId = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()
    def add_Production(input):
        sql = 'INSERT INTO Production VALUES (:pId, :ProductionName, :Vendor, :Device)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Production(input):
        sql = 'UPDATE Production SET ProductName=:ProductionName, Vendor=:Vendor, Device=:Device WHERE pId=:pId'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()  
           
class P1Route():
    def get_all_Route():
        sql = 'SELECT * FROM Route' #rId,RouteName,RouteDesc
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Route(rid):
        sql ='SELECT * FROM Route WHERE rId = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': rid}))
    def preadd_Route(RouteName):
        sql = 'SELECT RouteName FROM Route WHERE RouteName = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':RouteName}))
    def delete_Route(rId):
        sql = 'DELETE FROM Route WHERE rId = :id '
        DB.execute_input(DB.prepare(sql), {'id': rId})
        DB.commit()
    def add_Route(input):
        sql = 'INSERT INTO Route VALUES (:rId, :RouteName, :RouteDesc)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Route(input):
        sql = 'UPDATE Route SET RouteName=:RouteName, RouteDesc=:RouteDesc WHERE rId=:rId'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()     
        
class P1Recipe():
    def get_all_Recipe():
        sql = 'SELECT * FROM Recipe' # PPId,Description,Recipe
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Recipe(PPid):
        sql ='SELECT * FROM Recipe WHERE PPID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': PPid}))
    def preadd_Recipe(Recipename):
        sql = 'SELECT Recipe FROM Recipe WHERE Recipe = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':Recipename}))
    def delete_Recipe(pid):
        sql = 'DELETE FROM Recipe WHERE PPId = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()
    def add_Recipe(input):
        sql = 'INSERT INTO Recipe VALUES (:PPId, :Description, :Recipe)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Recipe(input):
        sql = 'UPDATE Recipe SET Recipe=:Recipe, Description=:Description WHERE PPId=:PPId'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()   
                  
class P1Operation():
    def get_all_Operation():
        sql = 'SELECT * FROM Operation' #OId,OperationName,Description,PPID,uEmpId,UpdateTime
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_Operation(oid):
        sql ='SELECT * FROM Operation WHERE OID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': oid}))
    def preadd_Operation(oname):
        sql = 'SELECT OperationName FROM Operation WHERE OperationName = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':oname}))
    def delete_Operation(oid):
        sql = 'DELETE FROM Operation WHERE OID = :id '
        DB.execute_input(DB.prepare(sql), {'id': oid})
        DB.commit()
    def add_Operation(input):
        sql = 'INSERT INTO Operation VALUES (:OId, :OperationName, :Description, :PPId, :uEmpId,:UpdateTime)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_Operation(input):
        sql = 'UPDATE Operation SET OperationName=:OperationName, Description=:Description, PPId=:PPId, uEmpId=:uEmpId,UpdateTime=:UpdateTime WHERE OId=:OId'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()     
    def Recipedelete_check(PPId):
        sql = 'SELECT * FROM Operation WHERE PPId=:PPId'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'PPId':PPId}))     
    
              
class P1EquipementUseTool():
    def delete_check(pid):
        sql = 'SELECT * FROM EQUIPMENTUSETOOL WHERE TID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))
    def add_use(input):
        sql = 'INSERT INTO EQUIPMENTUSETOOL VALUES ( :eId,:tId,:DateTime,:UsedTime)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
class P1ProductionOrder():
    def get_all_Order(): #pId,rId,woNumber,WorkOrder
        sql = 'SELECT * FROM ProductionOrder'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def delete_check(pid):
        sql = 'SELECT * FROM ProductionOrder WHERE pId=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))
    def get_Number(woid):
        sql ='SELECT * FROM ProductionOrder WHERE woNumber = :woid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'woid': woid}))
    def get_Order(woid):
        sql ='SELECT * FROM ProductionOrder WHERE WOrkOrder = :woid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'woid': woid}))
    def add_order(input):
        sql = 'INSERT INTO ProductionOrder VALUES ( :pId, :rId,:woNumber, :WorkOrder,:quantity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class P1RouteOpers():
    def get_all_RouteOpers():
        sql = 'SELECT * FROM RouteOpers' #rId,oId,Sequence,roId
        return DB.fetchall(DB.execute( DB.connect(), sql))
    def get_RouteOpers(roid):
        sql = 'SELECT * FROM RouteOpers where roid=:roid' 
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'roid':roid}))
    def delete_check(rid):
        sql = 'SELECT * FROM RouteOpers WHERE rId=:rid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'rid':rid}))             
    def Operdelete_check(oId):
        sql = 'SELECT * FROM RouteOpers WHERE oId=:oId'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'oId':oId}))           
    def delete_RouteOpers(roid):
        sql = 'DELETE FROM RouteOpers WHERE roid=:roid '
        DB.execute_input(DB.prepare(sql), roid)
        DB.commit()
    def preadd_RouteOpers(preadd_RouteOpers):
        sql = 'SELECT ROID FROM RouteOpers WHERE ROID = :ROID'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'ROID':preadd_RouteOpers}))
    def preadd2_RouteOpers(Input):
        sql = 'SELECT ROID FROM RouteOpers WHERE rId = :rId and oId = :oId'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), Input))
    def add_RouteOpers(input):
        sql = 'INSERT INTO RouteOpers VALUES ( :rId, :oId,:Sequence, :ROId)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_RouteOpers(input):
        sql = 'UPDATE RouteOpers SET rId=:rId, oId=:oId, roId=:roId, Sequence=:Sequence'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()           
      
class P1UserProduceEquip():      
    def add_Use(input):
        sql = 'INSERT INTO UserProduceEquip VALUES ( :uEmpId, :eId,:workStartAt, :workEndAt,:quantity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def get_all_Use(): #pId,rId,woNumber,WorkOrder
        sql = 'SELECT * FROM UserProduceEquip'
        return DB.fetchall(DB.execute( DB.connect(), sql))  
    def get_produceqty(input):
        sql = 'select po.productname,pqty.equipmentname,po.quantity poqty,pqty.produceqty from route rt left join routeopers rtops on rt.rid=rtops.rid left join operation opers on rtops.oid=opers.oid left join (select eq.eid,eq.oid,eq.equipmentname,nvl(sum (upe.quantity),0) produceqty from equipment eq left join userproduceequip upe on eq.eid=upe.eid group by eq.eid,eq.equipmentname,eq.oid ) pqty on  opers.oid=pqty.oid left join (select po.pid, po.rid,prod.productname,nvl(sum(po.quantity),0) quantity from productionorder po left join  production prod on po.pid=prod.pid group by po.pid,po.rid,prod.productname) po on  rt.rid=po.rid where  po.rid=:rid and pqty.eid=:eid order by rt.rid,sequence'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), input))
class Member():
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (null, :name, :account, :password, :identity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        sql ='SELECT * FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_product():
        sql = 'SELECT * FROM PRODUCT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]
    
    def preadd_name(pname):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PNAME = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':pname}))

    def add_product(input):
        sql = 'INSERT INTO PRODUCT VALUES (:pId, :ProductionName, :Vendor,:Device)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql)) # type: ignore

class MFGAnalysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\')), count(*) FROM UserProduceEquip WHERE EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\'))=:mon GROUP BY EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\'))'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i})) # type: ignore

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\')), COUNT(*) FROM UserProduceEquip WHERE EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\'))=:mon GROUP BY EXTRACT(MONTH FROM to_date(WORKSTARTAT,\'yyyy/MM/dd\'))'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i})) # type: ignore
    
    def category_sale():
        sql = 'SELECT count(*), PRODUCTNAME FROM(SELECT * FROM Production,Productionorder WHERE Production.PID = Productionorder.PID) GROUP BY PRODUCTNAME'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT sum(quantity), Operator.UEMPID, Operator.NAME FROM UserProduceEquip, Operator WHERE UserProduceEquip.UEMPID = Operator.UEMPID AND Operator.ACCESSLEVEL = :identity GROUP BY Operator.UEMPID, Operator.NAME ORDER BY sum(quantity) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'OP'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), Operator.UEMPID, Operator.NAME FROM UserProduceEquip, Operator WHERE UserProduceEquip.UEMPID = Operator.UEMPID AND Operator.ACCESSLEVEL = :identity GROUP BY Operator.UEMPID, Operator.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'OP'}))

class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i})) # type: ignore

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i})) # type: ignore
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))