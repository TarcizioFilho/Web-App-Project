from flask import Flask, render_template, request, redirect, url_for # funções utilizadas para trabalhar em conjunto com o HTML, servem para renderizar, redirecionar e requisitar. 
from flask_sqlalchemy import SQLAlchemy # Utilizado para criar a ligação entre o SQLite é o Flask
from sqlalchemy import func # func será utilizado para fazer algumas filtros na database
from flask_login import LoginManager ,UserMixin, login_user, logout_user, login_required, current_user #Login manager faz o gerenciamento do login; UserMixin fornece implementações padrão para os métodos que o flask-login espera que os objetos do usuário tenham; login_user fornece o gerenciamento de sessão do user para o flask; logout_user desconecta o user; login_required limita o acesso às páginas apenas para o user logado; current_user é utilizado aceder ao user logado em todos os templates.
from matplotlib import pyplot as plt #Biblioteca utilizada para plotar os gráficos 
from matplotlib.figure import Figure
import pandas as pd # O pandas será utilizado para criar dataframes que serão utilizados em conjunto com o matplot para gerar os gráficos
import datetime as dt # biblioteca utilizada para trabalhar as informações temporais
from datetime import datetime

#Conexão e inicialização das bases de dados
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_users_pass.db"
app.config["SQLALCHEMY_BINDS"] = {
    'database': "sqlite:///database.db"
}
app.config['SECRET_KEY'] = 'secret' # Chave utilizada para previnir adulteração de cookies
db.init_app(app)


#inicialização do login manager, os códigos abaixo estão disponíveis na documentação do flask
login_manager = LoginManager()
login_manager.login_view = 'login' #Caso o usuário tente aceder alguma página que não tenha autorização(@login_required) será reencaminhado para a página do login
login_manager.init_app(app)

#O método abaixo server para carregar o usuário criado
@login_manager.user_loader
def get_user(user_id):
    
    return Create_model_common_users_pwd.query.filter_by(id=user_id).first()

# As classes abaixo se referem aos modelos de  tabelas criadas no banco de dados SQLite
class Create_model_common_users_pwd(db.Model, UserMixin):
    __tablename__ = 'common users'
    id = db.Column(db.Integer,autoincrement=True ,primary_key=True)
    user_name = db.Column(db.String(100))
    user_email = db.Column(db.String(50), unique=True)
    user_pass = db.Column(db.String(20))
    supplier_email = db.Column(db.String(50),unique=True)
    supplier_pass = db.Column(db.String(20))
    user_type = db.Column(db.String(10))
    
    #Este método é utilizado para verificar a senha informada pelo usuário com a senha registada na base de dados
    def verify_password(self, password):
        
        if self.user_pass == password or self.supplier_pass == password:
            return 'login acepted'
            
        else:
            return 'login not acepted'      
         
class Create_model_suppliers_users_pwd(db.Model, UserMixin):
    __tablename__ = 'suppliers_users'
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    supplier_NIF = db.Column(db.Numeric(9), nullable=False ,unique=True)
    supplier_address = db.Column(db.String(100), nullable=False)
    supplier_address_code = db.Column(db.Integer(), nullable=False)
    supplier_country = db.Column(db.String(30), nullable=False)
    supplier_phone = db.Column(db.Integer(), nullable=False)
    
class Create_model_database(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'product'
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    product_name = db.Column(db.String(100))
    product_imported = db.Column(db.String())
    product_category = db.Column(db.String(20))
    product_entry_data = db.Column(db.String(15))
       
class Create_model_register_invoices(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'registerInvoices'
    id = db.Column(db.Integer,primary_key=True)
    supplier_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    invoice_supplier_name = db.Column(db.String(50))
    invoice_number = db.Column(db.String(50))
    invoice_date = db.Column(db.Integer())
    invoice_date_register = db.Column(db.Integer())
    invoice_product = db.Column(db.String(50))
    invoice_quantity = db.Column(db.Integer())
    invoice_value_s_IVA = db.Column(db.Integer())   
    invoice_TAX_IVA = db.Column(db.Integer()) 
    invoice_value_c_IVA = db.Column(db.Integer())
    product_warehouse = db.Column(db.String(20))
    minimum_stock = db.Column(db.Integer())

class Create_model_register_product_price(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'registerProductprice'
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(50))    
    price_s_iva = db.Column(db.Integer())
    iva_tax = db.Column(db.Integer())
    register_date = db.Column(db.Integer())
    price_c_iva = db.Column(db.Integer())
    
class Create_model_register_sales(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'sales'
    id = db.Column(db.Integer,primary_key=True)
    costumer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(50))
    product_quantity = db.Column(db.Integer())
    price_s_iva = db.Column(db.Integer())
    total_amount_s_iva = db.Column(db.Integer())
    price_c_iva = db.Column(db.Integer())
    total_amount = db.Column(db.Integer()) 
    sales_date = db.Column(db.Integer())
    product_sold = db.Column(db.Boolean)
    
class Create_model_inventory_manager(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'inventory manager'
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    entry_date = db.Column(db.Integer())
    entry_product_name = db.Column(db.String(50))
    entry_product_quantity = db.Column(db.Integer, default=0)
    sales_date = db.Column(db.Integer())
    sales_product_name = db.Column(db.String(50))
    sales_product_quantity = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer())

# Fim das classes utilizadas no SQLIte

#o app_context é um comando standard do flask, pode ser encontrado na documentação do flask, é utilizado para criar no bancos e dados às tabelas e modelos definidos.
with app.app_context():
    db.create_all()
    db.session.commit()

#App Route mapea as URL´s para uma função específica. A rota abaixo é referente a página principal da aplicação
@app.route('/')
def home():
    #a funçõa render _template é utilizada para renderizar o conteúdo do HTML index.html
    return render_template('index.html')

#Rota utilizada para o login dos usuários, nesta rota temos o método login que contempla toda a lógica de validação de acesso, bem como encaminha os usuários através de função 'redirect(url_for(...))' para as devidas páginas HTML 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
            
        user = Create_model_common_users_pwd.query.filter_by(user_email=email).first()
        user_password = Create_model_common_users_pwd.query.filter_by(user_pass=password).first()
        user_type = Create_model_common_users_pwd.query.filter_by(user_type='master')
        
        user_list = [] # Esta lista recebe através da iteração abaixo o emails dos usuários indicados como master no bando de dados.
        for row in user_type:
            user_list.append(row.user_email)
            #print(row.user_email in email)
        
                
        try: #A função verify_password pode ser encontrada na linha 45, esta serve para validar a senha no bando de dados. 
            if user and user_password.verify_password(password) and  email in user_list:
                login_user(user, remember=True)# Se o email, senha e email do admin estiverem corretos, O login_user irá receber
                #o email informado e criará uma sessão. O remenber=True irá criar um cookie no computador do usuário, e seguida o
                # Flask-login restaurará automaticamente o ID desse usuário desse cookie se ele não estiver na sessão. Isto serve 
                # como segurança, caso o usuário tente inserir outro ID que nõa seja o seu, o cookie será rejeitado pelo Flask-login.
                return redirect(url_for('internal_work'))    
        except AttributeError:
            if user or user_password.verify_password(password):
                return redirect(url_for('login'))
    
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
                
        user = Create_model_common_users_pwd.query.filter_by(user_email=email).first()
        user_password = Create_model_common_users_pwd.query.filter_by(user_pass=password).first()
                
        try:
            if user and user_password.verify_password(password): 
                login_user(user, remember=True)
                return redirect(url_for('home'))
                    
        except AttributeError:
                if user or user_password.verify_password(password):
                    return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
                
        user = Create_model_common_users_pwd.query.filter_by(supplier_email=email).first()
        user_password = Create_model_common_users_pwd.query.filter_by(supplier_pass=password).first()
                
        try:
            if user and user_password.verify_password(password): 
                login_user(user, remember=True)
                return redirect(url_for('my_account_supplier'))
        except AttributeError:
                if user or user_password.verify_password(password):
                    return redirect(url_for('login'))


    return render_template('login.html')
# fim da rota 'Login'

#Se refere a página a página principal do cliente.
@app.route('/myAccount')
@login_required
def my_account():
    
    return render_template('myAccount.html')

# Páginas(HTML´s) dos produtos 
@app.route('/product-1')
@login_required
def product_1():
    
    return render_template('product_1.html')

@app.route('/product-2')
@login_required
def product_2():
    
    return render_template('product_2.html')

@app.route('/product-3')
@login_required
def product_3():
    
    return render_template('product_3.html')
# Fim das páginas dos produtos

#esta rota retorna/mostra os produtos escolhidos pelo cliente atráves da página carrinho.html.
@app.route('/carrinho', methods=['GET', 'POST'])
@login_required
def carrinho():
    
    get_produt_by_id = Create_model_register_sales.query.filter(Create_model_register_sales.costumer_id==current_user.id).all()
    
    return render_template('carrinho.html', get_produt_by_id=get_produt_by_id)


# A rota abaixo regista no banco de dados os produtos escolhidos pelo cliente, quando este carrega no botão adicionar ao carrinho. 
@app.route('/add_carrinho', methods=['GET', 'POST'])
@login_required
def add_carrinho():
    
    #Quando o cliente clica no botão adicionar ao carrinho(ver o link em button nos HTML´s product_1, 2 e 3.),
    #o disparado o evento add_carrinho, que por sua vez contém o método add_carrinho() o qual recebe o input de produto 
    # e quantidade selecionados atráves do request. Nota: O tipo de request é POST, este é utilizado quando as informações 
    # partem do HTML para o Flask, por exemplo, inputs do usuário, requisição de pesquisa do usuário ao banco de dados.
    if request.method == 'POST':
        
        product = request.form['product']
        product_id = db.session.query(Create_model_database.id).filter_by(product_name=product)
        quantity = request.form['quantity']
      
        dt = datetime.now()
        current_date = dt.strftime("%Y-%m-%d")
        
        #Query utilizada para buscar no bancos de dados o nome, preço com iva e preço sem iva do produto adicionado pelo
        #cliente, será utilizada no loop abaixo em conjunto com as listas para que possamos calcular o valor total com iva e sem iva do produto. 
        get_product = db.session.query(Create_model_register_product_price.product_name, Create_model_register_product_price.price_c_iva, Create_model_register_product_price.price_s_iva).filter_by(product_name=product)

        product_name_list = []
        price_list_c_iva = []
        price_list_s_iva = []
        for row in get_product:
            product_name_list.append(row[0])
            price_list_c_iva.append(row[1])
            price_list_s_iva.append(row[2])
        
        product_name = product_name_list[0]
        price = price_list_c_iva[0]
        price_s_iva = price_list_s_iva[0]
        
        if quantity != 0:
            total_amount = (float(price) * int(quantity))
            total_amount_s_iva = round(float(price_s_iva) * int(quantity))
        #Foi utilizada o try para executar a condição abaixo, o objetivo do try é tratar o ValueError, uma vez que se
        #algum campo não for preenchido corretamente, o usuário deverá continuar na 'home'. Como estamos a fazer algumas
        #operações matemáticas o Try podeá ajudar caso algum valor inesparado seja inserido.     
        try:
            if product_name and quantity and price and total_amount and current_date and product_id:
                    
                sales_entry = Create_model_register_sales(costumer_id=current_user.id,product_name=product_name, product_quantity=quantity, price_s_iva=price_s_iva,total_amount_s_iva=total_amount_s_iva ,price_c_iva=price, total_amount=total_amount, sales_date=current_date, product_id=product_id)    
                
                inventory_manager_sales = Create_model_inventory_manager(product_id=product_id, sales_date=current_date,sales_product_name=product_name, sales_product_quantity=quantity)
                
                db.session.add(sales_entry)
                db.session.add(inventory_manager_sales)
                db.session.commit()
                
                return redirect(url_for('carrinho'))
            
        except ValueError:
            if product_name and quantity and price and total_amount and current_date and product_id:
                return redirect(url_for('home'))

    
    return render_template('index.html')


# Esta rota recebe o ID do produto quando o cliente clica no botão comprar, o ID do produto é pesquisado através de query definida na função 'sales_confirm_id', em seguida, as informações referentes ao produto são armazenadas em 'line_by_id_sales'
@app.route('/sales-confirm-id/<id>')
@login_required
def sales_confirm_id(id):
    
    line_by_id_sales = Create_model_register_sales.query.get(id)

    return render_template('carrinho.html', line_by_id_sales=line_by_id_sales)

#A rota abaixo serve para indicar registar no banco de dados a venda do produto. Após o cliente clicar n obotão comprar, um modal de confirmação aparecerá, este modal se refere a rota abaixo, quando o objeto 'line_by_id_sales'(rota acima) passar a conter um id, automaticamente a rota abaixo é ativada(no HTML Carrinho, ver a linha 77), esta recebe o id do produto em questão, vai ao banco de dados através da query definida no método sales_confirm, e na coluna 'product_sold' no banco de dados, o valor que inicialmente está como Null é alterado para 1. 
@app.route('/sales-confirm/<id>', methods=['POST', 'GET'])
@login_required
def sales_confirm(id):
    
    line_purchase_content = Create_model_register_sales.query.filter_by(id=int(id)).first()
    
    line_purchase_content.product_sold = not(line_purchase_content.product_sold)
        
    db.session.commit()
    return redirect(url_for('carrinho'))


#Esta rota remove do banco de dados do produto que foi adicionado ao carrinho
@app.route('/remove-line-product/<id>')
@login_required
def remove_line_product(id):
    
    invoice_content = Create_model_register_sales.query.filter_by(id=int(id)).delete() 
    db.session.commit()
    return redirect(url_for('carrinho'))



#Esta rota se erefere ao cadastro dos clientes e usuários internos(por exemplo, master)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        passsword = request.form['password']
        
        if name and email and passsword:
            
            user = Create_model_common_users_pwd(user_name=name, user_email=email, user_pass=passsword)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('register.html')

#Está rota se refere ao cadastro dos fornecedores
@app.route('/register_supplier', methods=['GET', 'POST'])
def register_supplier():
    if request.method == 'POST':
        name = request.form['name']
        nif = request.form['nif']
        address = request.form['address']
        address_code = request.form['address_code']
        country = request.form['country']
        phone = request.form['phone']
        email = request.form['email']
        passsword = request.form['password']
        
        if name and nif and address and address_code and country and email and passsword and phone:
            
            user = Create_model_suppliers_users_pwd(supplier_name=name, supplier_NIF=nif, supplier_address=address, supplier_address_code=address_code, supplier_country=country, supplier_phone=phone)
            email_pass = Create_model_common_users_pwd(supplier_email=email, supplier_pass=passsword)
            
            db.session.add(user)
            db.session.add(email_pass)
            db.session.commit()
            return redirect(url_for('login'))
        
    return render_template('registerSupplier.html')

#Esta rota se refere a página principal do fornecedor. Nota: No HTML myAccount foi utilizado o iframe para criar mostar a página salesReportsupplier.html dentro desta página.
@app.route('/myAccountsupplier')
@login_required
def my_account_supplier():
    
    return render_template('myAccountsupplier.html')

#trata~se da rota responsável por gerar obter as informações do fornecedor que está logado e inserir estas no gráfico, aqui utilizanmos o Pandas para criar o Dataframe e o matplotlib que receberá o Datraframe e plotará as informações no gráfico
@app.route('/sales_report_supplier', methods=['POST', 'GET'])
@login_required
def sales_report_supplier():
    
    #consulta a databse para obter os valores c/Iva e datas de registo das faturas por id do user
    content = db.session.query(Create_model_register_invoices.invoice_date_register, Create_model_register_invoices.invoice_value_c_IVA ).filter_by(supplier_id=current_user.id)
   
    
    date_list = []
    date_dict = {}
    value_list = []
    value_dict = {}
    # As informações da query acima serão guardadas em listas
    for row in content:
            date_list.append(row[0])
            value_list.append(row[1])

    
    #Foi criado um dicinário com as informações das listas acima
    dict_dates_values = {
        'date': date_list,
        'values': value_list,
    }
    
    df = pd.DataFrame(dict_dates_values) # DataFRame Pandas, recebe o dicionário criado anteriomente.
    
    
     # O try é utilizado para tratar do IndexError, caso o usuário tente aceder ao relatório e ainda não estiver nada registar no banco de dados, teremos um problema no gráfico, IndexError: index 0 is out of bounds for  axis 0 with size 0, uma vez que no gráfico o array não pode ser 0.
    try:
        #configuração do gráfico. Nota: Este gráfico mostra todos os registos do usuário que está logado.
        df['date'] = pd.to_datetime(df['date'])
        s = df.groupby(pd.Grouper(freq='M', key='date'))['values'].sum()
        plt.rcParams["figure.figsize"] = [6.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots(1,1)
        ax = s.plot(kind='bar')
        ax.set(title='Produtos Vendidos',
            xlabel="",
            )
        ax.bar_label(ax.containers[0], label_type='edge', fontsize=7, fmt='%.2f')
        plt.setp(ax.set_xticklabels(s.index.strftime('%m-%Y')), rotation=45, fontsize=8)
        ax.set_yticklabels('')
        fig.savefig('static/sales_plot.png')
    #fim da configuração do gráfico
    except IndexError as e:
        print(f'{e}')
    
    #Relativamente ao POST abaixo, este se refere a opção de visualizar as faturas já registadas pela empresa, adicionalmente, será gerado um novo gráfico apenas para o período selecionado.
    if request.method == 'POST':   
        
        start_date = request.form['trip-start']
        end_date = request.form['trip-end']
 
        #filtro que retorna as datas de registo das faturas de acordo com o período selecionado pelo usuário.
        filter_date = Create_model_register_invoices.query.filter(Create_model_register_invoices.invoice_value_c_IVA ,Create_model_register_invoices.invoice_date_register.between(start_date, end_date)).filter_by(supplier_id=current_user.id)
        
        date_list = []
        date_dict = {}
        value_list = []
        value_dict = {}
        
        # As informações da query acima serão guardadas em listas
        for row in filter_date:
            date_list.append(row.invoice_date_register)
            value_list.append(row.invoice_value_c_IVA)
        
        #Foi criado um dicinário com as informações das listas acima
        dict_dates_values = {
            'date': date_list,
            'values': value_list,
        }
        
        df = pd.DataFrame(dict_dates_values) # DataFRame Pandas

        # O try é utilizado para tratar do IndexError, caso o usuário tente aceder ao relatório e ainda não estiver nada registar no banco de dados, teremos um problema no gráfico, IndexError: index 0 is out of bounds for  axis 0 with size 0, uma vez que no gráfico o array não pode ser 0. 
        try: 
            #configuração do gráfico. 
            df['date'] = pd.to_datetime(df['date'])
            s = df.groupby(pd.Grouper(freq='M', key='date'))['values'].sum()
            plt.rcParams["figure.figsize"] = [6.00, 3.50]
            plt.rcParams["figure.autolayout"] = True
            fig, ax = plt.subplots(1,1)
            ax = s.plot(kind='bar')
            ax.set(title='Produtos Vendidos',
                xlabel="",
                )
            ax.bar_label(ax.containers[0], label_type='edge', fontsize=7, fmt='%.2f')
            plt.setp(ax.set_xticklabels(s.index.strftime('%m-%Y')), rotation=45, fontsize=8)
            ax.set_yticklabels('')
            fig.savefig('static/sales_plot.png')
            #fim da configuração do gráfico
        except IndexError as e:
            print(f'{e}')
        
        return render_template('salesReportsupplier.html', filter_date=filter_date, url='/static/sales_plot.png')

    return render_template('salesReportsupplier.html', url='/static/sales_plot.png')

# Esta rota é refernte ao gráfico de compras na área do cliente
@app.route('/sales_report_costumer', methods=['POST', 'GET'])
@login_required
def sales_report_costumer():
    
     #consulta a databse para obter todos os valores c/Iva e datas de registo das faturas por id do user
    content = db.session.query(Create_model_register_sales.sales_date, Create_model_register_sales.total_amount).filter_by(costumer_id=current_user.id)
    
   # As informações da query acima serão guardadas em listas
    date_list = []
    date_dict = {}
    value_list = []
    value_dict = {}
    for row in content:
        date_list.append(row[0])
        value_list.append(row[1])
    
    
    #Foi criado um dicinário com as informações das listas acima
    dict_dates_values = {
        'date': date_list,
        'values': value_list,
    }
    
    df = pd.DataFrame(dict_dates_values) # DataFRame Pandas
    # O try é utilizado para tratar do IndexError, caso o usuário tente aceder ao relatório e ainda não estiver nada registar no banco de dados, teremos um problema no gráfico, IndexError: index 0 is out of bounds for axis 0 with size 0, uma vez que no gráfico o array não pode ser 0.
    try:
        #configuração do gráfico. Este gráfico mostra todos os registos do usuário que está logado.
        df['date'] = pd.to_datetime(df['date'])
        s = df.groupby(pd.Grouper(freq='M', key='date'))['values'].sum()
        plt.rcParams["figure.figsize"] = [6.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots(1,1)
        ax = s.plot(kind='bar')
        ax.set(title='Histórico de Compras',
            xlabel="",
            )
        ax.bar_label(ax.containers[0], label_type='edge', fontsize=8, fmt='%.2f')
        plt.setp(ax.set_xticklabels(s.index.strftime('%m-%Y')), rotation=45, fontsize=8)
        ax.set_yticklabels('')
        fig.savefig('static/sales_costumer_plot.png')
         #fim da configuração do gráfico
    except IndexError as e:
        print(f'{e}')
       
    #Relativamente ao POST abaixo, este se refere a opção de visualizar às compras efetuadas pelo cliente por mês, adicionalmente, será gerado um novo gráfico apenas para o período selecionado.
    if request.method == 'POST':   
        
        start_date = request.form['trip-start']
        end_date = request.form['trip-end']
 
        #filtro que retorna as datas de registo das faturas de acordo com o período selecionado pelo usuário.
        filter_date = Create_model_register_sales.query.filter(Create_model_register_sales.price_c_iva, Create_model_register_sales.sales_date.between(start_date, end_date)).filter_by(costumer_id=current_user.id)
       
        date_list = []
        date_dict = {}
        value_list = []
        value_dict = {}
        # As informações da query acima serão guardadas em listas
        for row in filter_date:
            date_list.append(row.sales_date)
            value_list.append(row.total_amount)
        
        #Foi criado um dicinário com as informações das listas acima
        dict_dates_values = {
            'date': date_list,
            'values': value_list,
        }
        
        df = pd.DataFrame(dict_dates_values) # DataFRame Pandas
        
        try:
            #configuração do gráfico. Este gráfico mostra todos os registos do usuário que está logado.
            df['date'] = pd.to_datetime(df['date'])
            s = df.groupby(pd.Grouper(freq='M', key='date'))['values'].sum()
            plt.rcParams["figure.figsize"] = [6.00, 3.50]
            plt.rcParams["figure.autolayout"] = True
            fig, ax = plt.subplots(1,1)
            ax = s.plot(kind='bar')
            ax.set(title='Histórico de Compras',
                xlabel="",
                )
            ax.bar_label(ax.containers[0], label_type='edge', fontsize=8, fmt='%.2f')
            plt.setp(ax.set_xticklabels(s.index.strftime('%m-%Y')), rotation=45, fontsize=8)
            ax.set_yticklabels('')
            fig.savefig('static/sales_costumer_plot.png')
            #fim da configuração do gráfico
        except IndexError as e:
            print(f'{e}')
                
        
        return render_template('salesReportcostumer.html', filter_date=filter_date,  url='/static/sales_costumer_plot.png')
   
    return render_template('salesReportcostumer.html', url='/static/sales_costumer_plot.png')

# Esta rota é referente a página principal do usuário master. Nota: Nesta página internalWork.html, foi utilizado o iframe para mostrar as páginas RegisterProduct.html, registerInvoice, registerProductprice, updateProductprice, inventoryAdjustements, viewProducts e salesCompanyreport.html
@app.route('/internalWork')
@login_required
def internal_work():
     
    return render_template('internalWork.html')

#Esta rota contém o método que regista os produtos. 
@app.route('/registerProduct', methods=['GET', 'POST'])
@login_required
def register_product():
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        importedProduct = request.form['importedProduct']
        registerDate = request.form['registerDate']
        
        try:
            if name and category and importedProduct and registerDate:
                
                content = Create_model_database(product_name=name, product_imported=importedProduct, product_category=category, product_entry_data=registerDate)
                
                db.session.add(content)
                db.session.commit()
                return redirect(url_for('register_product'))
            
        except ValueError:
             if name and category and importedProduct and registerDate :
                 return redirect(url_for('register_product'))
            
    return render_template('registerProduct.html')

#Esta rota regista o preço do produto, após o produto ser criado, deve-se desiginar o preço dele, esta rota é responsável por isto.
@app.route('/register_product_price', methods=['GET', 'POST'])
@login_required
def register_product_price():
    
    #query que retorna o contéudo da tabela dos produtos registados, será utilizado para em conjunto com <select> html para que o usuário apenas escolha entre os pordutos já cadastrados.
    all_content = db.session.query(Create_model_database).group_by(Create_model_database.product_name)
    
    for row in all_content:
        print(row.product_name)
    
    #Ao caregar no botão registar, as infomrmações inseridas pelo usuário será guadardas nas variáveis abaixo através do request.form. após isto estas informações serão inseridas no bando de dados caso a condição do 'if' seja atendida.
    if request.method == 'POST':
        
        product_name = request.form['productName']
        product_id = db.session.query(Create_model_database.id).filter_by(product_name=product_name)
        price_s_iva = request.form['price']
        iva_tax = request.form['ivaTax']
        register_date = request.form['registerDate']
        
        # É utilizado o try para tratar possível erros de valor, uma vez que estamos receber strings e converte-las em int e float para trabalhar com operações matemáticas.
        try:
            if price_s_iva !='' or iva_tax != '':
                price_c_iva = round(float(price_s_iva) * ((int(iva_tax)/100)+1), 2)
            else:
                return render_template('registerProductprice.html')
        except ValueError:
            if price_s_iva !='' or iva_tax != '':
                return render_template('registerProductprice.html')
            
        
        try:
            if product_name and price_s_iva and iva_tax and register_date and price_c_iva and product_id:
                    
                content = Create_model_register_product_price(product_name=product_name, price_s_iva=price_s_iva, iva_tax=iva_tax, register_date=register_date, price_c_iva=price_c_iva, product_id=product_id)
                
                db.session.add(content)
                db.session.commit()
                
                return redirect(url_for('register_product_price', price_c_iva=price_c_iva))
            
        except ValueError:
             if product_name and price_s_iva and iva_tax and register_date and price_c_iva:
                return redirect(url_for('register_product_price'))
                
    
        return render_template('registerProductprice.html', price_c_iva=price_c_iva)
        
    
    return render_template('registerProductprice.html', all_content=all_content)


#Esta rota é responsável por mostrar ao usuário os produtos disponíveis para atualização dos preços.
@app.route('/update_product_price', methods=['GET', 'POST'])
@login_required
def update_product_price():
    
    #query que retorna o contéudo da tabela dos produtos registados, será utilizado para em conjunto com <select> html para que o usuário apenas escolha entre os pordutos já cadastrado.
    product_name = Create_model_register_product_price.query.all()
    
    if request.method == 'POST':
 
        #guardar na variável o produto escolhido pelo usuário
        product_name = request.form['productName']
        #Query para buscar o contúdo da produto selecionado pelo usuário
        all_content = Create_model_register_product_price.query.filter_by(product_name=product_name)
    
        #Esta query foi inserida aqui, para que após o 'POST' seja ativado, o usuário possa escolher outro produto, caso queira.
        product_name = db.session.query(Create_model_register_product_price)
        
        
        return render_template('updateProductprice.html', product_name=product_name,all_content=all_content)
        

    return render_template('updateProductprice.html', product_name=product_name)


#Quando o produto selecionado através da rota acima é mostrado no ecrã, devemos carregar no botão editar, ao carregar neste botão o evento update-price-id/<id>(abaixo) é disparado, ver updateProductprice.html linha 47. A rota abixo irá receber o id do produto o qual o botão editar foi acionado e irá buscar as respetivas informações na query contido no método update_price_by_id e guardá-las em li_by_id_update.
@app.route('/update-price-id/<id>')
@login_required
def update_price_by_id(id):
    
    line_by_id_update = Create_model_register_product_price.query.get(id)
    
    return render_template('updateProductprice.html', line_by_id_update=line_by_id_update)

#Esta rota irá receber as informações quardadas no objeto line_by_id_update que pertence a rota acima. Em sequida será disparado o evento update-price-line/<id>(abaixo) uma vez que a condição da linha 66 do html updateProductprice.html foi satisfeita.  Isto irá fazer com que o modal de edição seja aberto, neste momento o usuário deverá escolher o que deseja alterar. Ao carregar em confirmar será ativado o método POST da rota abaixo, isto fará com que as informações sejam registadas no banco de dados, de acordo com os critérios definidos. 
@app.route('/update-price-line/<id>', methods=['POST', 'GET'])
@login_required
def price_edit_line(id):
    
    line_invoice_content = Create_model_register_product_price.query.filter_by(id=int(id)).first()
    
    if request.method == 'POST':
        
        #se não for inserido nenhum novo valor, mantém-se o que já estava.
        if not request.form['new_price'] and not request.form['new_iva_tax'] and not request.form['register_date']:
            line_invoice_content.price_s_iva = line_invoice_content.price_s_iva
            line_invoice_content.iva_tax = line_invoice_content.iva_tax
            line_invoice_content.register_date = line_invoice_content.register_date
            
            db.session.commit()
            return redirect(url_for('update_product_price'))
        
        # regra para alterar os campos individualmente.  
        elif request.form['new_price'] and request.form['register_date'] and request.form['new_iva_tax']:
            line_invoice_content.price_s_iva = (float(request.form['new_price']))
            line_invoice_content.register_date = request.form['register_date']
            line_invoice_content.iva_tax = (int(request.form['new_iva_tax']))
            line_invoice_content.price_c_iva = float(request.form['new_price']) * ((int(request.form['new_iva_tax'])/100)+1)
            db.session.commit()    
            return redirect(url_for('update_product_price'))
             
        elif request.form['new_price'] and request.form['register_date'] and not request.form['new_iva_tax']:
            line_invoice_content.price_s_iva = request.form['new_price']
            line_invoice_content.register_date = request.form['register_date']
            line_invoice_content.price_c_iva = float(request.form['new_price']) * ((line_invoice_content.iva_tax/100)+1)
            db.session.commit()    
            return redirect(url_for('update_product_price'))
        
        elif request.form['new_iva_tax'] and request.form['register_date'] and not request.form['new_price']:
            line_invoice_content.iva_tax = request.form['new_iva_tax']
            line_invoice_content.register_date = request.form['register_date']
            line_invoice_content.price_c_iva = line_invoice_content.price_s_iva * ((int(request.form['new_iva_tax'])/100)+1)
            db.session.commit()    
            return redirect(url_for('update_product_price'))

    return render_template('updateProductprice.html')

#Esta rota é responsável por registar as faturas de fornecedores no módulo do usuário administrador. Este registo está dividido em duas partes, a saber: rota registerInvoice e rota addLineinvoice. a primeira é responsável por registar o nome do fornecedorm data de emissão da fatura e data de registo da fatura no banco de dados, também regista na banco de dados na tabela inventory manager a data de registo do produto. A segunda parte, rota addLineinvoice é responsável por registar o produto, id do produto, valor, quantidade, preço, armazém, e iva. Também regista em simultâneo na tabela inventory manager o nome do produto e quantidade e id do produto. O objetivo de dividir o registo da fatura foi para faciliar o trabalho do usuário, uma vez que uma fatura pode conter várias linhas e o idéal são registá-las todas uma única vez.
# Observção: Tentei outras formas para implementar esta rotina, entretanto está foi a melhor que consegui.
@app.route('/registerInvoice', methods=['GET', 'POST'])
@login_required
def register_invoice():

    
    #query retorna os registos dos fornecedores, é utilizado na linha 21 do ficheiro registerInvoice.html na função opition, para que seja possível selecionar apenas os fornecedores cadastrados.
    supplier_content = Create_model_suppliers_users_pwd.query.all()
    
    #query que retorna todo o conteudo dos produtos registados, é utilizado na linha 50 do ficheiro registerInvoice.html na função option, para que seja possível selecionar apenas os produtos cadastrados
    all_content = Create_model_database.query.all()
    
    #query que retorna o conteúdo dos produtos registados, é utilizado no loop for na linha 69 do ficheiro registerInvoice.html 
    line_invoice_content = Create_model_register_invoices.query.all()

    #query que retorna apenas os produtos registados na tabela, mas, apenas os que contém valor None na coluna invoice_number, isto serve para que após o registo de todas as linhas da fatura, o nome de fornecedor, a data da emissão da fatura e data de registo, sejam registados em todas as linhas dos produtos cadastrados. 
    selectNull = Create_model_register_invoices.query.filter(Create_model_register_invoices.invoice_number==None).all()
    
    #Esta query tem a mesma função da query acima, entretanto ela irá buscar a informação a tabela inventory manager, coluna entry_date.
    selectNull_entry_date = Create_model_inventory_manager.query.filter(Create_model_inventory_manager.entry_date==None).all()
    
    #Lista de armazéns
    warehouse_list = ['Lisboa', 'Porto', 'Coimbra']
    
    # O loop abaixo tem com objetivo calcular o valor total com iva e sem iva da fatura, e mostrá-los no ecrã para o usuário.
    value_list = []
    value_list_c_iva = []
    value_amount_s_iva = 0
    value_amount_c_iva = 0
    for content in selectNull:
        value_list.append((float(content.invoice_value_s_IVA)) * (int(content.invoice_quantity)))
        value_list_c_iva.append((content.invoice_value_s_IVA * content.invoice_quantity) * ((content.invoice_TAX_IVA/100)+1))
        value_amount_s_iva = round(sum(value_list),2)
        value_amount_c_iva = round(sum(value_list_c_iva),2)
    
    name_list = []
    for content_name in supplier_content:
        name_list.append(content_name.supplier_name)
    
    
    if request.method == 'POST':
        
        supplierName = request.form['supplierName']
        invoiceNumber = request.form['invoiceNumber']
        invoiceDate = request.form['invoiceDate']
        invoiceRegister = request.form['invoiceRegister']
        

        try:
            if supplierName and invoiceNumber and invoiceDate and invoiceRegister:
                
                #Consulta por nome do fornecedor para obter seu id 
                supplier_content = Create_model_suppliers_users_pwd.query.filter_by(supplier_name=supplierName)
                
                #itera o resultado da query supplier_content a fim de obter o id do fornecedor
                supplier_id = []
                for contents in supplier_content:
                    supplier_id.append(contents.id)
                
                #O loop baixo é utilizado para percorrer as informações da query selectNull, e registrar as informação inseridas pelo usuário nas colunas da tabela registerInvoices. 
                for content in selectNull:  
                    
                    content.supplier_id = supplier_id[0] #esta linha recebe o ID do fornecedor através da iteração em supplier_content
                    content.invoice_supplier_name = supplierName
                    content.invoice_number = invoiceNumber
                    content.invoice_date = invoiceDate
                    content.invoice_date_register = invoiceRegister
                
                #este loop segue a mesma lógica do anterior, mas, neste caso a informação será registada na tabela inventory manager
                for content in selectNull_entry_date:
                    
                    content.entry_date = invoiceRegister
                
               
                db.session.commit()
                return redirect(url_for('register_invoice'))
            
        except ValueError:
             if supplierName and invoiceNumber and invoiceDate and invoiceRegister:
                 return redirect(url_for('internal_work'))
             
    return render_template('registerInvoice.html',all_content=all_content, supplier_content=supplier_content, line_invoice_content=line_invoice_content, value_amount_s_iva=value_amount_s_iva, value_amount_c_iva=value_amount_c_iva, warehouse_list=warehouse_list)

#está rota é responsável por registar as informações relativas aos produtos de uma fatura de fornecedor, ao passo que os produtos são registadas as linhas são mostradas no ecrã, também é possível editá-las ou apagá-las. Está rota trabalha em conjunto com a rota acima \'registerIncoice'
@app.route('/addLineinvoice', methods=['GET', 'POST'])
@login_required
def add_line_invoice():
         
    if request.method == 'POST':
        
        productName = request.form['productName']
        #Esta query recebe o nome do produto selecionado pelo usuário e retorna o ID do produto correspondente
        product_id = db.session.query(Create_model_database.id).filter_by(product_name=productName)
        quantity = request.form['quantity']
        price = request.form['price']
        ivaTax = request.form['ivaTax']
        minimum_stock = request.form['minimumStock']
        warehouse = request.form['wareHouse']
        
        # A condição abaixo caso satisfeita, faz o calculo do valor do produto com iva e armazena na variável totalValue
        if price !='' and quantity !='' and ivaTax !='' and minimum_stock !='':
            totalValue = round(float(price) * int(quantity) * ((int(ivaTax)/100)+1), 2)
            #minimum_stock_percentage = int(quantity) * (int(minimum_stock)/100)
        
        # Esta query retorna todo o conteúdo da tabela registerInvoice, esta informação é utilizada na linha 69 do ficheiro registerInvoice.html para mostrar no ecrâ os produtos adicionados pelo usuário
        line_invoice_content = Create_model_register_invoices.query.all()
        
        try:
            if productName and quantity and price and ivaTax and product_id and warehouse:
                    
                stock_entry = Create_model_register_invoices(product_id=product_id,invoice_product=productName, invoice_quantity=quantity, invoice_value_s_IVA=price, invoice_TAX_IVA=ivaTax, invoice_value_c_IVA=totalValue, minimum_stock=minimum_stock, product_warehouse=warehouse)
                
                inventory_manager = Create_model_inventory_manager(product_id=product_id, entry_product_name=productName, entry_product_quantity=quantity, minimum_stock=minimum_stock)
                
                db.session.add(inventory_manager)
                db.session.add(stock_entry)
                db.session.commit()
                
                
                return redirect(url_for('register_invoice'))
            
        except ValueError:
             if productName and quantity and price and ivaTax and product_id:
                 return redirect(url_for('internal_work'))
            
             
        
        return render_template('registerInvoice.html', line_invoice_content=line_invoice_content)



#Esta rota é reponsável por pesquisar e mostrar ao usuário movimentos de entrada e saída de estoque de acordo com o período informado pelo usuário.
@app.route('/inventory-movements', methods=['POST', 'GET'])
@login_required
def inventory_movements():
    
    if request.method == 'POST':   
        
        start_date = request.form['trip-start']
        end_date = request.form['trip-end']
        movement_type = request.form['movement_type']
 
        #query que retorna o movimento de estoque de entrada de acordo com as datas definidas pelo usuário
        inventory_detail_entry = Create_model_register_invoices.query.filter(Create_model_register_invoices.invoice_date_register.between(start_date, end_date)).all()
        #query que retorna o movimento de estoque de saída de acordo com as datas definidas pelo usuário
        inventory_detail_sales = Create_model_register_sales.query.filter(Create_model_register_sales.sales_date.between(start_date, end_date)).all()
      
        
        return render_template('inventoryMovements.html', inventory_detail_entry=inventory_detail_entry, movement_type=movement_type, inventory_detail_sales=inventory_detail_sales)

    return render_template('inventoryMovements.html')

# Esta rota é responsável por gerar e mostrar o gráfico da quantidade de estoques atual, bem como pesquisar e mostrar os produtos comprados já registados.
@app.route('/viewProducts', methods=['POST', 'GET'])
@login_required
def view_products():
    
    #Esta query retorna todos os produtos que não foram registados na rotina de registos de faturas, estes produtos são deletados da tabela inventory manager. Esta Query garante que apenas aparecam na tabala os produtos que foram efetivamente registados na rotina de registo de faturas.
    products_not_registered = Create_model_inventory_manager.query.filter(Create_model_inventory_manager.entry_date==None, Create_model_inventory_manager.entry_product_name!=None).delete()
        
    db.session.commit()

    #query retorna os produtos de estoque, a infomação disponível é: Nome do produto, estoque mínimo agrupado por produto e valor atual do estoque, neste ultimo, utilizamos a quantidade dos produtos registadados de entrada e subtraimos das quantidades dos produtos vendidos, é utilizado um filtro por ID para relacionar os produtos de entrada e saída. 
    inventory_products = db.session.query(Create_model_inventory_manager.entry_product_name, func.sum(Create_model_inventory_manager.minimum_stock), func.sum(Create_model_inventory_manager.entry_product_quantity - Create_model_inventory_manager.sales_product_quantity)).filter(Create_model_inventory_manager.product_id).group_by(Create_model_inventory_manager.product_id)

      
    product_list = []
    product_quantity_list = []
        
    for row in inventory_products:
        product_list.append(row[0])
        product_quantity_list.append(row[2])

    dict_inventory_products = {
        'product': product_list,
        'quantity': product_quantity_list,
    }
        
    df = pd.DataFrame(dict_inventory_products) #DataFrame Pandas, inserimos o dicionário criado anteriormente pra que possa ser utilizado no gráfico da biblioteca matplotlib, abaixo. 
    
    # O try é utilizado para tratar do IndexError, caso o usuário tente aceder ao relatório e ainda não estiver nada registado no banco de dados, teremos um problema no gráfico, IndexError: index 0 is out of bounds for axis 0 with size 0, uma vez que no gráfico o array não pode ser 0.
    try:    
        #configuração do gráfico 
        s = df.groupby(pd.Grouper(key='product'))['quantity'].sum()
        plt.rcParams["figure.figsize"] = [6.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots(1,1)
        ax = s.plot(kind='bar')
        ax.set(title='Estoque\n(Produto/Quantidade)',
            xlabel="",
            )
        ax.bar_label(ax.containers[0], label_type='edge', fontsize=8,)
        plt.setp(ax.set_xticklabels(s.index), rotation=45, fontsize=8)
        ax.set_yticklabels('')
        fig.savefig('static/inventory_plot.png')
        #fim da configuração do gráfico
    except IndexError as e:
        print(f'{e}')
        
    if request.method == 'POST':
        
        start_date = request.form['trip-start']
        end_date = request.form['trip-end']
        
        inventory_manager_entries = Create_model_inventory_manager.query.filter(Create_model_inventory_manager.entry_date.between(start_date, end_date)).all()
        
        
        return render_template('viewProducts.html', url='/static/company_sales_plot.png', inventory_manager_entries=inventory_manager_entries)
    

    return render_template('viewProducts.html', inventory_products=inventory_products, url='/static/company_sales_plot.png')

#Esta rota é reposnsável por gerar e mostrar o gráfico de vendas vs custos na rotina Relatório de vendas, também é responsável por pesquisar e mostar na mesma rotina os documentos já registados, sejam eles de compra ou venda.
@app.route('/sales_report_company', methods=['POST', 'GET'])
@login_required
def sales_report_company():
    
    #consulta a databse para pegar os valores s/Iva e datas de registo das faturas por id do user
    sales_revenue = db.session.query(Create_model_register_sales.sales_date, Create_model_register_sales.total_amount_s_iva).all()
    
    #filtrar o valor médio de custo dos produtos por id
    get_average_cost = db.session.query(func.avg(Create_model_register_invoices.invoice_value_s_IVA).label('average'), Create_model_register_invoices.product_id).group_by(Create_model_register_invoices.product_id).subquery()
    
    #filtrar as quantidades vendidas por ID e multiplicar pelo get_average_cost, assim temos o custo médio da mercadoria vendida
    cost_of_sales = db.session.query(Create_model_register_sales.sales_date, func.sum(get_average_cost.c.average * Create_model_register_sales.product_quantity)).filter(Create_model_register_sales.product_id==get_average_cost.c.product_id).group_by(Create_model_register_sales.sales_date)
    
    date_list_cost_of_sales = []
    value_list_cost_of_sales = []
    #O loop abaixo é utilizado para guardar as datas e valores nas listas    
    for row in cost_of_sales:
        date_list_cost_of_sales.append(row[0])
        value_list_cost_of_sales.append(row[1])
    #print(len(date_list_cost_of_sales))
    #print(len(value_list_cost_of_sales))

    
    #Criar dicionário para que as informações de cost_of_sales sejam inseridas no gráfico matplot
    dict_dates_values_cost_of_sales = {
        'date_cost_of_sales': date_list_cost_of_sales,
        'values_cost_of_sales': value_list_cost_of_sales,
    }
   
    #Inserir as informações de cost_of_sales no dicionário abaixo.
    date_list = []
    value_list = []
    #O loop abaixo é utilizado para guardar as datas e valores nas listas
    for row in sales_revenue:
        date_list.append(row[0])
        value_list.append(row[1])
    #print(len(date_list))
    #print(len(value_list))
    
    #Criar dicionário para que as informações de cost_of_sales sejam inseridas no gráfico matplot
    dict_dates_values = {
        'date': date_list,
        'values': value_list,
    }
    
    #Criar data frames no pandas, serão utilizados para gerar o gráfico de vendas vs custo das mercadorias através do matplotlib
    df = pd.DataFrame(dict_dates_values)
    df1 = pd.DataFrame(dict_dates_values_cost_of_sales)

    #configuração do gráfico de vendas vs custo das vendas
    df['date'] = pd.to_datetime(df['date'])
    df1['date_cost_of_sales'] = pd.to_datetime(df1['date_cost_of_sales'])# converter a data para o formato date_time
    
    # O try é utilizado para tratar do IndexError, caso o usuário tente aceder ao relatório e ainda não estiver nada registar no banco de dados, teremos um problema no gráfico, IndexError: index 0 is out of bounds for axis 0 with size 0, uma vez que no gráfico o array não pode ser 0.
    try:
        s = df.groupby(pd.Grouper(freq='M', key='date'))['values'].sum()
        s1 = df1.groupby(pd.Grouper(freq='M', key='date_cost_of_sales'))['values_cost_of_sales'].sum()
        plt.rcParams["figure.figsize"] = [6.00, 4.5]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots(1,1)
        ax = s.plot(kind='bar')
        ax1 = ax.twiny()
        ax1 = s1.plot(kind='bar', color='tomato')
        
        ax.set(title='Vendas vs custo de vendas',
            xlabel="",
            )
        ax.bar_label(ax.containers[0], label_type='edge', fontsize=10, fmt='%.0f')
        plt.setp(ax.set_xticklabels(s.index.strftime('%m-%Y')), rotation=45, fontsize=8)
        ax.set_yticklabels(" ")
        ax.legend(['Vendas'], loc='upper center', bbox_to_anchor=(0.3, 1.1),
          fancybox=True, shadow=True, ncol=5 ,fontsize=8)
        
        ax1.set(title='',
            xlabel="",
            )
        
        ax1.bar_label(ax1.containers[0], label_type='center', fontsize=10, fmt='%.0f')
        plt.setp(ax1.set_xticklabels(s1.index.strftime('%m-%Y')), rotation=45, fontsize=8, color='white')
        ax1.legend(['Custo das Merc. Vendidas'], bbox_to_anchor=(0.8, 1.1),
          fancybox=True, shadow=True, ncol=5 ,fontsize=8)
        
        fig.savefig('static/company_sales_plot.png', bbox_inches = 'tight')
        #fim da configuração do gráfico
        
    except IndexError as e:
        print('{e}')    
    
    if request.method == 'POST':   
        
        #As variáveis start_date e end_date recebem as datas informadas pelo usuário, a variável invoice_type recebe a opção do botão de rádio escolhida pelo usuário. Estas informações serão utilizadas nas queries abaixo para obter as informações relativas aos critérios do usuário, estas informações serão mostradas no ecrã.
        start_date = request.form['trip-start']
        end_date = request.form['trip-end']
        invoice_type = request.form['invoiceType']
 
        #filtro que retorna as datas de registo das faturas de acordo com o período selecionado pelo usuário.
        purchases_content = Create_model_register_invoices.query.filter(Create_model_register_invoices.invoice_date_register.between(start_date, end_date)).all()
        
        #filtro que retorna as datas de registo das faturas de acordo com o período selecionado pelo usuário.
        sales_content = Create_model_register_sales.query.filter(Create_model_register_sales.sales_date.between(start_date, end_date)).all()
        
        
        return render_template('salesReportcompany.html', purchases_content=purchases_content,sales_content=sales_content, invoice_type=invoice_type)

    return render_template('salesReportcompany.html', url='/static/company_sales_plot.png')



#Esta rota captura o id do produto selecionado para ser excluído, após isto este id é consultado no banco de dados através de query no método get_line_by_id_remove, as informações serão guardadas em line_by_id_remove.
@app.route('/line-remove-id/<id>')
@login_required
def get_line_by_id_remove(id):
    
    line_by_id_remove = Create_model_register_invoices.query.get(id)
    
    return render_template('registerInvoice.html', line_by_id_remove=line_by_id_remove)

#Esta rota remove do banco de dados a linha da fatura que está a ser registada, esta rota utiliza como parametro o ID guardado em line_by_id_remove da rota acima. Quando o usuário carrega em confimar o método remove_line é ativado, então a query contida neste método, 'recebe' o ID que está registado em line_by_id_remove pesquisa exatamente o produto na tabela e o remove. 
@app.route('/removeLine/<id>')
@login_required
def remove_line(id):
    #procurar na base de dados o id correspondente ao id que vem da página web, e depois faz delete
    line_invoice_content = Create_model_register_invoices.query.filter_by(id=int(id)).delete()
    
    db.session.commit()
    return redirect(url_for('register_invoice'))


#query para buscar o ID da linha que será editada na rotina de gerenciamento de estoque
@app.route('/inventory-line-edit-id/<id>')
@login_required
def inventory_get_line_by_id_edit(id):
    line_by_id_edit = Create_model_inventory_manager.query.get(id)
    return render_template('viewProducts.html', line_by_id_edit=line_by_id_edit)

#Edita a quantidade do estoque mínimo por produto na rotina visualizar estoque, esta rota recebe a informaçao contida no objeto line_by_id_edit(rota acima), quando o  usuário carregar no botão de editar, será aberto um modal de edição para que o  usuário possa atualizar o valor, após carregar em confirmar o método POST será ativado e o input do usuário será registado no banco de dados, conforme as regras do método abaixo.  
@app.route('/inventory-update-line/<id>', methods=['POST', 'GET'])
@login_required
def inventory_edit_line(id):
    
    line_invoice_content = Create_model_inventory_manager.query.filter_by(id=int(id)).first()
    
    if request.method == 'POST':
        
        
        #se não for inserido nenhum novo valor, mantém-se o que já estava.
        if not request.form['new_minimum_stock']:
            line_invoice_content.minimum_stock = line_invoice_content.minimum_stock
            
            db.session.commit()
            return redirect(url_for('view_products'))
        
        # regra para alterar os campos individualmente.       
        
        elif request.form['new_minimum_stock']:
            line_invoice_content.minimum_stock = request.form['new_minimum_stock']
            
            db.session.commit()    
            return redirect(url_for('view_products'))

    return render_template('viewProducts.html.html')


#Esta função será utilizada para buscar o id do produto que será editado na rotina entrada de produtos 
@app.route('/line-edit-id/<id>')
@login_required
def get_line_by_id_edit(id):
    #query para buscar o ID da linha que será editada na rotina de entrada de estoque
    line_by_id_edit = Create_model_register_invoices.query.get(id)

    return render_template('registerInvoice.html', line_by_id_edit=line_by_id_edit)



#Esta função recebe o Id capturado da função 'line-edit-id'(acima) e executa o método edit_line de acordo com os critérios definidos 
@app.route('/updateLine/<id>', methods=['POST', 'GET'])
@login_required
def edit_line(id):
    
    line_invoice_content = Create_model_register_invoices.query.filter_by(id=int(id)).first()
    
    if request.method == 'POST':
        

        #se não for inserido nenhum novo valor, mantém-se o que já estava.
        if not request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_quantity = line_invoice_content.invoice_quantity
            line_invoice_content.invoice_value_s_IVA = line_invoice_content.invoice_value_s_IVA
            line_invoice_content.invoice_TAX_IVA = line_invoice_content.invoice_TAX_IVA
            line_invoice_content.minimum_stock = line_invoice_content.minimum_stock
            #db.session.commit()
            return redirect(url_for('register_invoice'))
        # regra para alterar os campos individualmente.
                    
        elif request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_quantity = request.form['new_invoice_quantity']
            line_invoice_content.invoice_value_c_IVA = (int(request.form['new_invoice_quantity']) * line_invoice_content.invoice_value_s_IVA) * ((line_invoice_content.invoice_TAX_IVA/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_invoice_quantity'] and request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_quantity = request.form['new_invoice_quantity']
            line_invoice_content.invoice_value_s_IVA = request.form['new_invoice_value_s_IVA']
            line_invoice_content.invoice_value_c_IVA = (int(request.form['new_invoice_quantity']) * float(request.form['new_invoice_value_s_IVA'])) * ((line_invoice_content.invoice_TAX_IVA/100)+1)
                
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_quantity = request.form['new_invoice_quantity']
            line_invoice_content.invoice_TAX_IVA = request.form['new_invoice_TAX_IVA']
            line_invoice_content.invoice_value_c_IVA = (int(request.form['new_invoice_quantity']) * line_invoice_content.invoice_value_s_IVA) * ((int(request.form['new_invoice_TAX_IVA'])/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_quantity'] and not request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_value_s_IVA = request.form['new_invoice_value_s_IVA']
            line_invoice_content.invoice_value_c_IVA = (line_invoice_content.invoice_quantity * float(request.form['new_invoice_value_s_IVA'])) * ((line_invoice_content.invoice_TAX_IVA/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_quantity'] and request.form['new_invoice_TAX_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_value_s_IVA = request.form['new_invoice_value_s_IVA']
            line_invoice_content.invoice_TAX_IVA = request.form['new_invoice_TAX_IVA']
            line_invoice_content.invoice_value_c_IVA = (line_invoice_content.invoice_quantity * float(request.form['new_invoice_value_s_IVA'])) * ((int(request.form['new_invoice_TAX_IVA'])/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_invoice_TAX_IVA'] and not request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and not request.form['new_minimum_stock']:
            line_invoice_content.invoice_TAX_IVA = request.form['new_invoice_TAX_IVA']
            line_invoice_content.invoice_value_c_IVA = (line_invoice_content.invoice_quantity * line_invoice_content.invoice_value_s_IVA) * ((int(request.form['new_invoice_TAX_IVA'])/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_minimum_stock'] and not request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_TAX_IVA']:
            line_invoice_content.minimum_stock = request.form['new_minimum_stock']
            db.session.commit()    
            return redirect(url_for('register_invoice'))
            
        elif request.form['new_minimum_stock'] and request.form['new_invoice_quantity'] and not request.form['new_invoice_value_s_IVA'] and not request.form['new_invoice_TAX_IVA']:
            line_invoice_content.minimum_stock = request.form['new_minimum_stock']
            line_invoice_content.invoice_quantity = request.form['new_invoice_quantity']
            line_invoice_content.invoice_value_c_IVA = (int(request.form['new_invoice_quantity']) * line_invoice_content.invoice_value_s_IVA) * ((line_invoice_content.invoice_TAX_IVA/100)+1)
            db.session.commit()    
            return redirect(url_for('register_invoice'))


    return render_template('registerInvoice.html', line_invoice_content=line_invoice_content)


 
# Esta rota se refere ao logout dos usuário, é standard do flask, poderá ser encontrado na documentação do flask       
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
                    
if __name__ == '__main__':
    app.run(debug=True)