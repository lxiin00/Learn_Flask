# web安全规范
目前无论是简单的博客，还是大型的其他类型网站，Web安全都应该放在第一位置上，这里简单记录下几种常见的Web攻击和其他常见的漏洞
## 1、注入攻击
注入攻击包括系统命令注入（OS Command）、SQL（结构化查询语言）注入、NoSQL注入、ORM（对象关系映射）注入等，这里简单介绍SQL注入。
### SQL注入
SQL是一种功能齐全的数据库语言，也是关系型数据库的通用操作语言。可以使用它来进行对数据库中的数据进行修改、查询和删除等操作；ORM是用来操作数据库的工具，使用它可以在不手动编写SQL语句的情况下操作数据库。

1、攻击原理

在编写SQL语句时，如果直接将用户传入的数据作为参数使用字符串拼接的方式插入到SQL查询中，那么可以通过注入其他语句来执行攻击操作，就可以获取到敏感数据、修改/删除数据等操作。

2、攻击示例（以Falsk框架为例）

假设有一个学生信息的查询程序，其中的某个视图函数接收用户输入的密码，返回根据密码查询对于的数据。数据库由一个db对象表示，SQL语句通过execute()方法执行：

```python
@app.route('/students')
def bobby_table():
    password = request.args.get('password')
    cur = db.execute("SELECT students WHERE password='%s';" % password )
    results = cur.fetchall()
    return results
```
我们通过查询字符串获取用户输入的查询参数，并且不经过处理就使用字符串格式化的方法拼接到SQL语句中。在这种情况下，如果攻击者通过输入的password参数为"'' or 1=1 --;"，那么视图函数中被执行的语句变成为：
```sql
SELECT * FROM students WHERE password='' or 1=1 --;'

```
这个时候会把studets表中的所有记录全部查询并返回，这也就意味着被攻击者获取到了数据，当然，攻击者可以通过把password的参数值写成"SELECT * FROM students WHERE password=''； drop table users; --"，就会把表格中的全部记录删除掉。

3、防范方法

1)、使用ORM可以一定程度上避免SQL注入问题。

2)、验证输入类型，比如某个视图函数接收整型的id来查询，那么在URL规则中限制URL变量为整型。

3)、参数化查询，在构造SQL语句时避免使用拼接字符串或字符串格式化的方式来构建SQL语句。

4)、转移特殊字符，比如引号、分号和横线等。

