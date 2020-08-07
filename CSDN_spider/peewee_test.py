from peewee import *

db = MySQLDatabase("spider", host="222.223.239.147", port=3307, user="root", password="Xinboway@803")


class Person(Model):  #默认生成主键id,如果有一个列名是id，那么一定要设置好主键
    name = CharField(max_length=20,null=True)
    birthday = DateField()


    class Meta:
        database = db
        table_name = "users"

if __name__ == "__main__":
    # db.create_tables([Person])
    from datetime import date
    #生成数据
    # uncle_bob = Person(name='Bob',birthday=date(1960,1,15))
    # uncle_bob.save()
    # uncle_bob = Person(name='Bobby',birthday=date(1980,7,15))
    # uncle_bob.save()
    # uncle_bob = Person(name='syb',birthday=date(2000,1,15))
    # uncle_bob.save()
    #查询数据
    # bobby = Person.select().where(Person.name == 'bobby').get()
    # print(bobby.birthday)
    query = Person.select().where(Person.name=='Bob')
    for person in query:
        #删除查询到的数据
        person.delete_instance()
        #查询多条
        # print(person.name,person.birthday)
    #修改数据
        # person.birthday = date(1960,1,17)
        # person.save()# 既可以完成新建，也可以完成修改
    # grandma = Person.get(Person.name=='Granda L.')
