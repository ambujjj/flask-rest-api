from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import secret
import pymysql
import json
app = Flask(__name__)

# Configure db

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secret.mysql_user, secret.mysql_password, secret.mysql_host, secret.mysql_db)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
mysql = SQLAlchemy(app)

class Customers(mysql.Model):
    CustomerID = mysql.Column(mysql.String(50), primary_key=True)
    CompanyName = mysql.Column(mysql.String(150), nullable=False)
    ContactName = mysql.Column(mysql.String(150), nullable=False)
    ContactTitle = mysql.Column(mysql.String(150), nullable=False)
    Address = mysql.Column(mysql.String(250), nullable=False)
    City = mysql.Column(mysql.String(50), nullable=False)
    Region = mysql.Column(mysql.String(50), nullable=True)
    PostalCode = mysql.Column(mysql.String(50), nullable=False)
    Country = mysql.Column(mysql.String(50), nullable=False)
    Phone = mysql.Column(mysql.String(50), nullable=False)
    Fax = mysql.Column(mysql.String(50), nullable=True)
    def __repr__(self):
        return f"Customers('{self.CustomerID}, {self.CompanyName}, {self.ContactName}, {self.ContactTitle}, {self.Address}, {self.City}, {self.Region}, {self.PostalCode}, {self.Country}, {self.Phone}, {self.Fax}')"

class Products(mysql.Model):
    ProductID = mysql.Column(mysql.Integer, primary_key=True)
    ProductName = mysql.Column(mysql.String(150), nullable=False)
    SupplierID = mysql.Column(mysql.Integer, nullable=False)
    CategoryID = mysql.Column(mysql.Integer, nullable=False)
    QuantityPerUnit = mysql.Column(mysql.String(250), nullable=False)
    UnitPrice = mysql.Column(mysql.Float, nullable=False)
    UnitsInStock = mysql.Column(mysql.Integer, nullable=False)
    UnitsOnOrder = mysql.Column(mysql.Integer, nullable=False)
    
    ReorderLevel = mysql.Column(mysql.Integer, nullable=False)
    Discontinued = mysql.Column(mysql.Integer, nullable=False)
    def __repr__(self):
        return f"Products('{self.ProductID}, {self.ProductName}, {self.SupplierID}, {self.CategoryID}, {self.QuantityPerUnit}, {self.UnitPrice}, {self.UnitsInStock}, {self.UnitsOnOrder}, {self.ReorderLevel}, {self.Discontinued}')"

class Orders(mysql.Model):
    OrderID = mysql.Column(mysql.Integer, primary_key=True)
    CustomerID = mysql.Column(mysql.String(150), nullable=False)
    EmployeeID = mysql.Column(mysql.Integer, nullable=False)
    OrderDate = mysql.Column(mysql.String(150), nullable=False)
    RequiredDate = mysql.Column(mysql.String(250), nullable=False)
    ShippedDate = mysql.Column(mysql.String(50), nullable=False)
    ShipVia = mysql.Column(mysql.Integer, nullable=False)
    Freight = mysql.Column(mysql.Float, nullable=False)
    ShipName = mysql.Column(mysql.String(50), nullable=False)
    ShipAddress = mysql.Column(mysql.String(50), nullable=False)
    ShipCity = mysql.Column(mysql.String(50), nullable=False)
    ShipRegion = mysql.Column(mysql.String(50), nullable=False)
    ShipPostalCode = mysql.Column(mysql.String(50), nullable=False)
    ShipCountry = mysql.Column(mysql.String(50), nullable=False)
    def __repr__(self):
        return f"Orders('{self.OrderID},{self.CustomerID},{self.EmployeeID},{self.OrderDate},{self.RequiredDate},{self.ShippedDate},{self.ShipVia},{self.Freight},{self.ShipName},{self.ShipAddress},{self.ShipCity},{self.ShipRegion},{self.ShipPostalCode},{self.ShipCountry}')"

@app.route('/')
def index():
    
    return render_template('index.html')
@app.route('/newcustomer', methods=['GET', 'POST'])
def newcustomer(): 
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax = userDetails["CustomerID"], userDetails["CompanyName"], userDetails["ContactTitle"], userDetails["Address"], userDetails["City"], userDetails["Region"], userDetails["Region"], userDetails["PostalCode"], userDetails["Country"], userDetails["Phone"], userDetails["Fax"]
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO customers(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax))
        # mysql.connection.commit()
        # cur.close()
        customer_new = Customers(CustomerID=CustomerID, CompanyName=CompanyName, ContactName=ContactName, Address=Address, City=City, Region=Region, PostalCode=PostalCode, Country=Country, Phone=Phone, Fax=Fax)
        mysql.session.add(customer_new)
        mysql.session.commit()
        return redirect('/customers')
    return render_template('newcustomer.html')

@app.route('/customers')
def customers():
    #cur = mysql.connection.cursor()
    resultValue = Customers.query.all()
    #resultValue = cur.execute("select * from customers")
    # if resultValue > 0:
    #     custDetails = cur.fetchall()
    #return render_template('customers.html',custDetails=resultValue)
    return str(resultValue)

@app.route('/neworder', methods=['GET', 'POST'])
def neworder(): 
    if request.method == 'POST':
        # Fetch form data
        orderDetails = request.form
        OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry = orderDetails["OrderID"], orderDetails["CustomerID"], orderDetails["EmployeeID"], orderDetails["OrderDate"], orderDetails["RequiredDate"], orderDetails["ShippedDate"], orderDetails["ShipVia"], orderDetails["Freight"], orderDetails["ShipName"], orderDetails["ShipAddress"], orderDetails["ShipCity"], orderDetails["ShipRegion"], orderDetails["ShipPostalCode"], orderDetails["ShipCountry"]
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO customers(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax))
        # mysql.connection.commit()
        # cur.close()
        order_new = Orders(OrderID=OrderID, CustomerID=CustomerID, EmployeeID=EmployeeID, OrderDate=OrderDate, RequiredDate=RequiredDate, ShippedDate=ShippedDate, ShipVia=ShipVia, Freight=Freight, ShipName=ShipName, ShipAddress=ShipAddress, ShipCity=ShipCity, ShipRegion=ShipRegion, ShipPostalCode=ShipPostalCode, ShipCountry=ShipCountry)
        mysql.session.add(order_new)
        mysql.session.commit()
        return redirect('/orders')
    return render_template('neworder.html')

@app.route('/orders')
def orders():
    #cur = mysql.connection.cursor()
    resultValue = Orders.query.all()
    #resultValue = cur.execute("select * from customers")
    # if resultValue > 0:
    #     custDetails = cur.fetchall()
    #return render_template('customers.html',custDetails=resultValue)
    return str(resultValue)
    
@app.route('/newproduct', methods=['GET', 'POST'])
def newproduct(): 
    if request.method == 'POST':
        # Fetch form data
        productDetails = request.form
        ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued = productDetails["ProductID"], productDetails["ProductName"], productDetails["SupplierID"], productDetails["CategoryID"], productDetails["QuantityPerUnit"], productDetails["UnitPrice"], productDetails["UnitsInStock"], productDetails["UnitsOnOrder"], productDetails["ReorderLevel"], productDetails["Discontinued"]
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO customers(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax))
        # mysql.connection.commit()
        # cur.close()
        product_new = Products(ProductID=ProductID, ProductName=ProductName, SupplierID=SupplierID, CategoryID=CategoryID, QuantityPerUnit=QuantityPerUnit, UnitPrice=UnitPrice, UnitsInStock=UnitsInStock, UnitsOnOrder=UnitsOnOrder, ReorderLevel=ReorderLevel, Discontinued=Discontinued)
        mysql.session.add(product_new)
        mysql.session.commit()
        return redirect('/products')
    return render_template('newproduct.html')

@app.route('/products')
def products():
    #cur = mysql.connection.cursor()
    resultValue = Products.query.all()
    #resultValue = cur.execute("select * from customers")
    # if resultValue > 0:
    #     custDetails = cur.fetchall()
    #return render_template('customers.html',custDetails=resultValue)
    return str(resultValue)


if __name__ == '__main__':
    app.run(debug=True)