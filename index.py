from bottle import route, run, template, redirect, request, get, static_file, Bottle
from paste import httpserver as web
import os.path, functools
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = [
   os.path.join(BASE_DIR, 'views'),
]
STATIC_DIR = os.path.join(BASE_DIR, 'static')
import sqlite3

app = Bottle()

# データベースに接続
dbname = "sqlite.db"
conn = sqlite3.connect(dbname)

c = conn.cursor()

# person
try:
    # テーブルの作成
    # c.execute("DROP TABLE IF EXISTS table_person")
    c.execute(
        "CREATE TABLE IF NOT EXISTS table_person (id INTEGER PRIMARY KEY, person_name TEXT)")
    # c.execute("INSERT INTO table_person VALUES (1, '担当者名')")
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

# category1
try:
    # テーブルの作成
    # c.execute("DROP TABLE IF EXISTS table_category1")
    c.execute(
        "CREATE TABLE IF NOT EXISTS table_category1 (id INTEGER PRIMARY KEY, category1_name TEXT)")
    # プログラムから試しに１つだけtable_category1を追加しておく
    # c.execute("INSERT INTO table_category1 VALUES (1, '親カテゴリ')")
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

try:
    # テーブルの作成
    # c.execute("DROP TABLE IF EXISTS table_category2")
    c.execute(
        "CREATE TABLE IF NOT EXISTS table_category2 (id INTEGER PRIMARY KEY, category1_name TEXT, category2_name TEXT)")
    # c.execute("INSERT INTO table_category2 VALUES (1, '親カテゴリ名', 'カテゴリ名')")
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

try:
    # テーブルの作成
    # c.execute("DROP TABLE IF EXISTS table_assign")
    c.execute(
        "CREATE TABLE IF NOT EXISTS table_assign (id INTEGER PRIMARY KEY, category2_id INTEGER, counter_persons TEXT, responsible_person TEXT)")
    # c.execute("INSERT INTO table_assign VALUES (1, 1, '担当者１,担当者2', '責任者')")
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

conn.commit()
conn.close()


# Static file
@app.route('/static/css/<filename:path>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/css')

@app.route('/static/font/<filename:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/font')

@app.route('/static/imgs/<filename:re:.*\.(jpg|png|gif|ico|svg)>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/img')

@app.route('/static/js/<filename:re:.*\.js>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/js')


# / にアクセスしたら、index関数が呼ばれる
@app.route("/")
# @app.route("/search/") #キーワード未指定の場合
def index():
    table_person = get_table_person()
    table_category1 = get_table_category1()
    table_category2 = get_table_category2()
    table_assign = get_table_assign()
    return template("index.html",
        table_person=table_person,
        table_category1=table_category1,
        table_category2=table_category2,
        table_assign=table_assign,
        template_lookup=TEMPLATE_PATH)

@app.route("/search", method="POST")
def callback():
    txt = request.forms.getunicode("searchText")
    if len(txt) > 0:
        table_assign = search_table_assign(txt)
        return template("search.html",
            table_assign=table_assign,
            searchTxt=txt,
            template_lookup=TEMPLATE_PATH)
    else :
        return redirect("/")

""" -------------------------
 person
------------------------- """
# methodにPOSTを指定して、add関数を実装する
@app.route("/person_add", method="POST")
def add():
    person_name = request.forms.getunicode("person_name")
    save_table_person(person_name)
    return redirect("/#tab5")

# @app.routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
@app.route("/person_delete/<id:int>")
def delete(id):
    delete_table_person(id)
    return redirect("/#tab5")


def get_table_person():
    conn = sqlite3.connect(dbname, isolation_level="DEFERRED")
    c = conn.cursor()
    select = "select id, person_name from table_person"
    c.execute(select)
    table_person = []
    for row in c.fetchall():
        table_person.append({
            "id": row[0],
            "person_name": row[1]
        })
    conn.close()
    return table_person

def save_table_person(person_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    insert = "insert into table_person(person_name) values(?)"
    c.execute(insert, (person_name,)) # table_personのあとにカンマをつけないとなぜかエラーになる
    conn.commit()
    conn.close()

def delete_table_person(id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    delete = "delete from table_person where id=?"
    c.execute(delete, (id,))
    conn.commit()
    conn.close()

""" -------------------------
 category1
------------------------- """
# methodにPOSTを指定して、add関数を実装する
@app.route("/category1_add", method="POST")
def add():
    category1_name = request.forms.getunicode("category1_name")
    save_table_category1(category1_name)
    return redirect("/#tab4")

# @app.routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
@app.route("/category1_delete/<id:int>")
def delete(id):
    delete_table_category1(id)
    return redirect("/#tab4")

def get_table_category1():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = "select id, category1_name from table_category1"
    c.execute(select)
    table_category1 = []
    for row in c.fetchall():
        table_category1.append({
            "id": row[0],
            "category1_name": row[1]
        })
    conn.close()
    return table_category1

def save_table_category1(category1_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    insert = "insert into table_category1(category1_name) values(?)"
    c.execute(insert, (category1_name,)) # table_category1のあとにカンマをつけないとなぜかエラーになる
    conn.commit()
    conn.close()

def delete_table_category1(id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    delete = "delete from table_category1 where id=?"
    c.execute(delete, (id,))
    conn.commit()
    conn.close()


""" -------------------------
 category2
------------------------- """
# methodにPOSTを指定して、add関数を実装する
@app.route("/category2_add", method="POST")
def add():
    category1_name = request.forms.getunicode("category1_name")
    category2_name = request.forms.getunicode("category2_name")
    save_table_category2(category1_name, category2_name)
    return redirect("/#tab3")

# @app.routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
@app.route("/category2_delete/<id:int>")
def delete(id):
    delete_table_category2(id)
    return redirect("/#tab3")

def get_table_category2():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = "select id, category1_name, category2_name from table_category2"
    c.execute(select)
    table_category2 = []
    for row in c.fetchall():
        table_category2.append({
            "id": row[0],
            "category1_name": row[1],
            "category2_name": row[2]
        })
    conn.close()
    return table_category2

def save_table_category2(category1_name, category2_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    insert = "insert into table_category2(category1_name, category2_name) values(?, ?)"
    c.execute(insert, (category1_name, category2_name,))
    conn.commit()
    conn.close()

def delete_table_category2(id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    delete = "delete from table_category2 where id=?"
    c.execute(delete, (id,))
    conn.commit()
    conn.close()

""" -------------------------
 assign
------------------------- """
# methodにPOSTを指定して、add関数を実装する
@app.route("/assigns_add", method="POST")
def add():
    category2_id = request.forms.getunicode("category2_id")
    counter_persons = request.forms.decode().getall("counter_persons") # getAll() charcode `latin1`
    lst_counter_persons = []
    for counter_person in counter_persons:
        lst_counter_persons.append(counter_person)

    counter_person_csv = ','.join(lst_counter_persons)
    responsible_person = request.forms.getunicode("responsible_person")
    save_table_assign(category2_id, counter_person_csv, responsible_person)
    return redirect("/#tab2")

# @app.routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
@app.route("/assigns_delete/<id:int>")
def delete(id):
    delete_table_assign(id)
    return redirect("/#tab2")

def get_table_assign():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = '''
select
table_assign.id,
table_assign.category2_id,
table_category2.category1_name,
table_category2.category2_name,
table_assign.counter_persons,
table_assign.responsible_person
 from table_assign inner join table_category2
on table_assign.category2_id = table_category2.id
order by table_category2.category1_name asc
'''
    c.execute(select)
    table_assign = []
    for row in c.fetchall():
        table_assign.append({
            "id": row[0],
            "category2_id": row[1],
            "category1_name": row[2],
            "category2_name": row[3],
            "counter_persons": row[4],
            "responsible_person": row[5]
        })
    conn.close()
    return table_assign

def save_table_assign(category2_id, counter_person_csv, responsible_person):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    insert = "insert into table_assign(category2_id, counter_persons, responsible_person) values(?, ?, ?)"
    c.execute(insert, (category2_id, counter_person_csv, responsible_person,))
    conn.commit()
    conn.close()

def update_table_assign(assign_id, category2_id, counter_person_csv, responsible_person):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    insert = "update table_assign set category2_id = ?, counter_persons = ?, responsible_person = ? where id = ?"
    c.execute(insert, (category2_id, counter_person_csv, responsible_person, assign_id))
    conn.commit()
    conn.close()

def delete_table_assign(id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    delete = "delete from table_assign where id=?"
    c.execute(delete, (id,))
    conn.commit()
    conn.close()

""" -------------------------
 search
------------------------- """
def search_table_assign(txt):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = '''
select
table_assign.id,
table_assign.category2_id,
table_category2.category1_name,
table_category2.category2_name,
table_assign.counter_persons,
table_assign.responsible_person
 from table_assign inner join table_category2
on table_assign.category2_id = table_category2.id
where
table_category2.category1_name like '%'''+txt+'''%' or
table_category2.category2_name like '%'''+txt+'''%' or
table_assign.counter_persons like '%'''+txt+'''%' or
table_assign.responsible_person like '%'''+txt+'''%'
'''
    c.execute(select)
    table_assign = []
    for row in c.fetchall():
        table_assign.append({
            "id": row[0],
            "category2_id": row[1],
            "category1_name": row[2],
            "category2_name": row[3],
            "counter_persons": row[4],
            "responsible_person": row[5]
        })
    conn.close()
    return table_assign

""" -------------------------
 edit
------------------------- """
# @app.routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
@app.route("/assigns_edit/<id:int>")
def edit(id):
    table_person = get_table_person()
    table_category1 = get_table_category1()
    table_category2 = get_table_category2()
    table_assign = get_table_assign()
    table_assign_edit = get_table_assign_byid(id)
    # 担当者
    # for assigns in table_assign:
    #     lst_counter_persons = assigns["counter_persons"].split(",")
    # 担当者選択情報
    for assigns in table_assign_edit:
        if assigns["counter_persons"] == None:
            lst_counter_persons_edit = ""
        else:
            lst_counter_persons_edit = assigns["counter_persons"].split(",")
    for assigns in table_assign_edit:
        if assigns["responsible_person"] == None:
            lst_responsible_person_edit = ""
        else:
            lst_responsible_person_edit = assigns["responsible_person"].split(",")
    return template("edit.html",
        table_person=table_person,
        table_category1=table_category1,
        table_category2=table_category2,
        table_assign=table_assign,
        table_assign_edit=table_assign_edit,
        # lst_counter_persons=lst_counter_persons,
        lst_counter_persons_edit=lst_counter_persons_edit,
        lst_responsible_person_edit=lst_responsible_person_edit,
        template_lookup=TEMPLATE_PATH)

def get_table_assign_byid(id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = '''
select
table_assign.id,
table_assign.category2_id,
table_category2.category1_name,
table_category2.category2_name,
table_assign.counter_persons,
table_assign.responsible_person
 from table_assign inner join table_category2
on table_assign.category2_id = table_category2.id
 where table_assign.id = ?
'''
    c.execute(select, (id,))
    # c.execute(select)
    table_assign = []
    for row in c.fetchall():
        table_assign.append({
            "id": row[0],
            "category2_id": row[1],
            "category1_name": row[2],
            "category2_name": row[3],
            "counter_persons": row[4],
            "responsible_person": row[5]
        })
    conn.close()
    return table_assign

# methodにPOSTを指定して、add関数を実装する
@app.route("/assigns_update", method="POST")
def add():
    assign_id = request.forms.getunicode("assign_id")
    category2_id = request.forms.getunicode("category2_id")
    counter_persons = request.forms.decode().getall("counter_persons") # getAll() charcode `latin1`
    lst_counter_persons = []
    for counter_person in counter_persons:
        lst_counter_persons.append(counter_person)

    counter_person_csv = ','.join(lst_counter_persons)
    responsible_person = request.forms.getunicode("responsible_person")
    print(responsible_person)
    update_table_assign(assign_id, category2_id, counter_person_csv, responsible_person)
    return redirect("/#tab2")

# テスト用のサーバをlocalhost:8888で起動する
# run(host="192.168.45.82", port=8888, debug=None, reloader=False, interval=180, quiet=True)
web.serve(app, host='0.0.0.0', port=8888, daemon_threads=False, threadpool_workers=25, use_threadpool=True)
