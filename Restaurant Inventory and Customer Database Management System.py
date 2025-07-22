import pymysql
mycon=pymysql.connect(host='localhost',user='Ujjwal',passwd='Ujjuk#1235',database='Kitchen_on_Wheels')
#mycon=sqltor.connect('localhost','Ujjwal','Ujjuk#1235','Kitchen_on_Wheels')

def viewfoodtable():
    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM Food")
    for i in cursor.fetchall():
        print(i)
        
def vieworderstable():
    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM Orders")
    for i in cursor.fetchall():
        print(i)
    
def add_food_item(item_name,price_perpiece,quantity_left,waiting_time,stock,appliance_capacity,hr_min):
    cursor=mycon.cursor()
    cursor.execute("INSERT INTO Food VALUES ('{}',{},{},{},{},{},'{}')".format(item_name,price_perpiece,quantity_left,waiting_time,stock,appliance_capacity,hr_min))
    mycon.commit()

def amending_stock(name,number):
    cursor=mycon.cursor()
    cursor.execute("SELECT stock FROM Food WHERE item_name = '{}'".format(name))
    prev=cursor.fetchone()
    new=prev[0] + number
    cursor.execute("UPDATE Food SET stock = {} WHERE item_name = '{}'".format(new,name))
    mycon.commit()

def amending_price(name,newprice):
    cursor=mycon.cursor()
    cursor.execute("UPDATE Food SET price_perpiece = {} WHERE item_name = '{}'".format(newprice,name))
    mycon.commit()

def amending_waiting_time(name,newtime):
    cursor=mycon.cursor()
    cursor.execute("UPDATE Food SET waiting_time = {} WHERE item_name = '{}'".format(newtime,name))
    mycon.commit()

def amending_appliance_capacity(name,newcapacity):
    cursor=mycon.cursor()
    cursor.execute("UPDATE Food SET Appliance_Capacity = {} WHERE item_name = '{}'".format(newcapacity,name))
    mycon.commit()

def order_item(name,quantity,d,hr_min):
    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM Food WHERE item_name = '{}'".format(name))
    a=cursor.fetchone() #row of that item i.e. item_name,price_perpiece,quantity_left,waiting_time,stock,appliance_capacity,appliance_occupied_till
    
    if a[2]>=quantity:
        price=quantity*a[1]
        items_left=a[2]-quantity
        d[name]=[quantity,price,0]
        cursor=mycon.cursor()
        cursor.execute("UPDATE Food SET quantity_left={} WHERE item_name = '{}'".format(items_left,name))
        mycon.commit()
        
    else:
        if a[2]+a[4]>=quantity:
            price=quantity*a[1]
            if (quantity-a[2])%a[5]==0:
                waittime=((quantity-a[2])//a[5])*a[3]
            else:
                waittime=(((quantity-a[2])//a[5]) +1)*a[3]
            #for checking whether appliance is occupied or not
            if a[6]<=hr_min:
                d[name]=[quantity,price,waittime]
            else:
                extrawait=(int(a[6].split(':')[0])-int(hr_min.split(':')[0]))*60 +(int(a[6].split(':')[1])-int(hr_min.split(':')[1]))
                waittime+=extrawait
                d[name]=[quantity,price,waittime]
            #for changing the time till which appliance will be occupied
            x=hr_min.split(':')
            x[0]=int(x[0])
            x[1]=int(x[1])
            x[0]+=(waittime)//60
            if x[1]+(waittime)%60>=60:
                x[0]+=1
                x[1]=x[1]+(waittime)%60-60
            else:
                x[1]+=(waittime)%60
            if x[0]<10:
                x[0]='0'+str(x[0])
            else:
                x[0]=str(x[0])
            if x[1]<10:
                x[1]='0'+str(x[1])
            else:
                x[1]=str(x[1])
            if int(x[0])>23:
                x[0]=int(x[0])-24
                if x[0]<10:
                    x[0]='0'+str(x[0])
                else:
                    x[0]=str(x[0])
            finaltime=(x[0])+':'+(x[1])
            stock_left=a[2]+a[4] - quantity
            cursor=mycon.cursor()
            qtyleft=0
            
            cursor.execute("UPDATE Food SET quantity_left={}, stock={}, Appliance_occupied_till='{}' WHERE item_name = '{}'".format(qtyleft,stock_left,finaltime,name))
            mycon.commit()
            
        else:
            print("Sorry for the inconvenience, we are out of stock")
            print("You can get",a[2],"of them right now and",a[4],"more in lots of ",a[5], " in time intervals of ",a[3],' minutes')
            qty=int(input("Enter the number of items you want to order now: "))
            order_item(name,qty,d,hr_min)
                
print("Welcome to Kitchen on Wheels!")
print("What would you like to do, type the number ")
print('''1-view food table
2-view orders table
3-place an order
4-add a new food item
5-make amendments in current stock
6-make amendments in prices
7-make amendments in preparation time
8-make amendments in appliance capacity''')

n=int(input())

#new day,so all appliances unoccupied
from time import ctime
today=ctime()
L=today.split(' ') #['Sun', 'Jan', '15', '16:32:36', '2023']
month_date=L[1]+','+L[2]
Li=L[3].split(':')
hr_min=Li[0]+':'+Li[1]

cursor=mycon.cursor()
cursor.execute("SELECT * FROM Orders")
a=cursor.fetchall() # a tuple of tuples
if a[-1][-1]!=month_date and hr_min>='06:00':
    cursor=mycon.cursor()
    cursor.execute("UPDATE Food SET Appliance_occupied_till='{}'".format(hr_min))
    mycon.commit()
    
if n==1:
    viewfoodtable()

elif n==2:
    vieworderstable()
    
elif n==3:
    name=input('please tell your name: ')
    d={} #order- itemname:[qty,price,waitingtime] 
    while True:
        itemname=input('enter name of the food item: ')
        quantity=int(input('enter its quantity: '))
        order_item(itemname,quantity,d,hr_min)
        a=input('do you want to order anything else? (Y/N): ')
        if a=='N':
            print('Complete Order in the form of itemname:[qty,price,waitingtime]')
            print(d)
            break
        else:
            continue
    totalprice=0
    time=[]
    for i in d:
         totalprice+=d[i][1]
         time+=[d[i][2]]

    if time==[]:
        finaltime=hr_min
    else:    
        totalpreptime=max(time)
        x=hr_min.split(':')
        x[0]=int(x[0])
        x[1]=int(x[1])
        x[0]+=(totalpreptime)//60
        if x[1]+(totalpreptime)%60>=60:
            x[0]+=1
            x[1]=x[1]+(totalpreptime)%60-60
        else:
            x[1]+=(totalpreptime)%60
        if x[0]<10:
            x[0]='0'+str(x[0])
        else:
            x[0]=str(x[0])
        if x[1]<10:
            x[1]='0'+str(x[1])
        else:
            x[1]=str(x[1])
        if int(x[0])>23:
            x[0]=int(x[0])-24
            if x[0]<10:
                x[0]='0'+str(x[0])
            else:
                x[0]=str(x[0])
        finaltime=(x[0])+':'+(x[1])

    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM Orders")
    prev_ordernum=cursor.fetchall()[-1][0]
    cursor=mycon.cursor()
    cursor.execute("INSERT INTO Orders VALUES ({},'{}',{},'{}','{}','{}')".format(prev_ordernum+1,name,totalprice,hr_min,finaltime,month_date))
    mycon.commit()
    
elif n==4:
    item_name=input('enter name of the food item')
    price_perpiece=int(input('enter its price'))
    quantity_left=int(input('enter its quantity prepared'))
    waiting_time=int(input('enter its preparation time'))
    stock=int(input('enter its stock'))
    appliance_capacity=int(input('enter the capacity of appliance used to make this'))
    add_food_item(item_name,price_perpiece,quantity_left,waiting_time,stock,appliance_capacity,hr_min)
    
elif n==5:
    name=input('enter name of the food item')
    stk=int(input('enter its new stock which arrived'))
    amending_stock(name,stk)
    
elif n==6:
    name=input('enter name of the food item')
    price=int(input('enter its new price'))
    amending_price(name,price)
    
elif n==7:
    name=input('enter name of the food item')
    preptime=int(input('enter its preparation time'))
    amending_waiting_time(name,preptime)
    
elif n==8:
    name=input('enter name of the food item')
    newcapacity=int(input('enter its new capacity'))
    amending_appliance_capacity(name,newcapacity)
    
mycon.close()
