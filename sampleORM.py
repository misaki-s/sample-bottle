from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# SQLite 使用時
# SQLite - File（通常のファイル保存）
#engine = create_engine('sqlite:///sample_db.sqlite3')  # スラッシュは3本

# SQLログを表示したい場合には echo=True を指定
engine = create_engine('sqlite:///sample_db.sqlite3', echo=True)

# SQLite - Memory（インメモリー）
# engine = create_engine('sqlite:///:memory:')

# モデルの作成
# 説明のためファイル内に定義しますが、実際は別ファイル化して import します。

# まずベースモデルを生成します
Base = declarative_base()


# 次にベースモデルを継承してモデルクラスを定義します
class Student(Base):
    """
    生徒モデル
    必ず Base を継承
    """
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    score = Column(Integer)  # 点数

    def __repr__(self):
        return "<Student(id='%s', name='%s', score='%s')>" % (self.id, self.name, self.score)


# テーブルの作成
# テーブルがない場合 CREATE TABLE 文が実行される
Base.metadata.create_all(engine)  # 作成した engine を引数にすること

# SQLAlchemy はセッションを介してクエリを実行する
Session = sessionmaker(bind=engine)
session = Session()

# セッション・クローズ
# DB処理が不要になったタイミングやスクリプトの最後で実行
# session.close()

# 1レコードの追加
session.add(Student(id=1, name='Suzuki', score=70))

# コミット（データ追加を実行）
session.commit()

# 複数レコードの追加
session.add_all([
    Student(id=5, name='Yamada', score=73),
    Student(id=7, name='Watanabe', score=88),
    Student(id=10, name='Tanaka', score=65),
])

# コミット（データ追加を実行）
session.commit()


# 全件取得
result = session.query(Student).all()  # .all() は省略可
for student in result:
    print(student.name, student.score)
    """
    Suzuki 70
    Yamada 73
    Watanabe 88
    Tanaka 65
    """

for student in session.query(Student):  # .all() を省略
    print(student.name, student.score)
    """
    Suzuki 70
    Yamada 73
    Watanabe 88
    Tanaka 65
    """

# 1レコード取得
student = session.query(Student).filter_by(name='Yamada').one()

# 条件に一致するレコードがない場合は NoResultFound エラーになるので注意
print('\nSELECT No Result')
try:
    # sqlalchemy.orm.exc.NoResultFound: No row was found for one()
    student = session.query(Student).filter_by(name='Sato').one()
    print(student)
except NoResultFound as ex:
    print(ex)


# 1レコード取得
student = session.query(Student).filter_by(name='Yamada').one()

# 条件に一致するレコードがない場合は NoResultFound エラーになるので注意
print('\nSELECT No Result')
try:
    # sqlalchemy.orm.exc.NoResultFound: No row was found for one()
    student = session.query(Student).filter_by(name='Sato').one()
    print(student)
except NoResultFound as ex:
    print(ex)


# 1レコード取得
student = session.query(Student).filter_by(name='Yamada').one()

# 条件に一致するレコードがない場合は NoResultFound エラーになるので注意
print('\nSELECT No Result')
try:
    # sqlalchemy.orm.exc.NoResultFound: No row was found for one()
    student = session.query(Student).filter_by(name='Sato').one()
    print(student)
except NoResultFound as ex:
    print(ex)

# ORDER BY ... ASC
for student in session.query(Student).order_by(Student.score.asc()):  # .asc() は省略可
    print(student.name, student.score)
    """
    Tanaka 65
    Suzuki 70
    Yamada 73
    Watanabe 88
    """

# ORDER BY ... DESC
for student in session.query(Student).order_by(Student.score.desc()):  # 降順にするには .desc()
    print(student.name, student.score)
    """
    Watanabe 88
    Yamada 73
    Suzuki 70
    Tanaka 65
    """

# ページネーションで必須の LIMIT と OFFSET はスライス表記で指定
print('\nLIMIT and OFFSET')
for student in session.query(Student).order_by(Student.score.desc())[1:3]:
    print(student.name, student.score)
    """
    Yamada 73
    Suzuki 70
    """

# SQLAlchemy ではフィルターにより抽出条件を指定できます。（WHERE句に相当）
for student in session.query(Student).filter(Student.name == 'Yamada'):
    print(student.name, student.score)
    """
    Yamada 73
    """

# 一致しないものを抽出
# filter !=
for student in session.query(Student).filter(Student.name != 'Yamada'):
    print(student.name, student.score)
    """
    Suzuki 70
    Watanabe 88
    Tanaka 65
    """

# 部分一致 LIKE
# WHERE LIKE '%...%'
for student in session.query(Student).filter(Student.name.like('%na%')):
    print(student.name, student.score)
    """
    Watanabe 88
    Tanaka 65
    """

# 複数条件指定（AND）- コンマ区切りによるAND検索
# AND (send multiple expressions to .filter())
for student in session.query(Student).filter(Student.score > 70, Student.score < 80):
    print(student.name)
    """
    Yamada
    """

# 複数条件指定（AND）- メソッドチェーンによるAND検索
# AND - chain multiple filter()/filter_by() calls
for student in session.query(Student).filter(Student.score > 70).filter(Student.score < 80):
    print(student.name)
    """
    Yamada
    """

# 複数条件指定（OR）
for student in session.query(Student).filter((Student.score < 70) | (Student.score > 80)):
    print(student.name)
    """
    Watanabe
    Tanaka
    """

# OR検索は or_ モジュールをインポートする方法もあり
# from sqlalchemy import or_ # for student in session.query(Student).filter(or_(Student.score < 70, Student.score > 80)): # http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.or_

# count()メソッドでレコード数を取得できます
count = session.query(Student).count()
print(count)  # 4

count = session.query(Student).filter(Student.name.like('%na%')).count()
print(count)  # 2


student = session.query(Student).filter_by(name='Tanaka').one()
student.score = 75
session.add(student)
 
# コミット（変更を実行）
session.commit()
 
# 変更されたかを確認
student = session.query(Student).filter_by(name='Tanaka').one()
print(student)  # <Student(id='10', name='Tanaka', score='75')>


# Delete one record
student = session.query(Student).get(10)
session.delete(student)

# コミット（削除を実行）
session.commit()

# 削除を確認
for student in session.query(Student):
    print(student.name)
    """
    Suzuki
    Yamada
    Watanabe
    """

# Delete one record
student = session.query(Student).get(10)
session.delete(student)

# コミット（削除を実行）
session.commit()

# 削除を確認
for student in session.query(Student):
    print(student.name)
    """
    Suzuki
    Yamada
    Watanabe
    """