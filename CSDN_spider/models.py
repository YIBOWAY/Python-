from peewee import *

db = MySQLDatabase("spider", host="222.223.239.147", port=3307, user="root", password="Xinboway@803")


class BaseModel(Model):
    class Meta:
        database = db


# 设计数据表的时候几个点：
# char类型要设置最大长度
# 对于无法确定最大长度的字段，可以设置为Text
# 设计表的时候，采集到的数据要尽量先做格式化处理
# default和null
class Topic(BaseModel):
    title = CharField()
    content = TextField(default="")
    id = IntegerField(primary_key=True)
    author = CharField()
    create_time = DateTimeField()
    answer_nums = IntegerField(default=0)
    click_nums = IntegerField(default=0)
    praised_nums = IntegerField(default=0)
    jtl = FloatField(default=0.0)  # 结贴率
    score = IntegerField(default=0)  # 赏分
    status = CharField()  # 状态
    last_answer_time = DateTimeField()


class Answer(BaseModel):
    topic_id = IntegerField()
    author = CharField()
    content = TextField(default="")
    create_time = DateTimeField()
    parised_nums = IntegerField(default=0)  # 点赞数


class Author(BaseModel):
    name = CharField()
    id = CharField(primary_key=True)
    original_nums = IntegerField(default=0)  # 原创数
    rate = CharField(default=-1)  # 排名
    desc = TextField(null=True)
    follower_nums = IntegerField(default=0)  # 粉丝数
    following_nums = IntegerField(default=0)  # 关注数


if __name__ == "__main__":
    db.create_tables([Author])
