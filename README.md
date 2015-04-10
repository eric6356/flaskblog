# flaskblog
一个用flask写的博客

## 部署
设置管理员邮箱环境变量

```
export BLOG_ADMIN=foo@bar.com
```
  
初始化

```
git clone https://github.com/eric6356/flaskblog.git
cd flaskblog
pip install -r requirement.txt
python manage.py deploy
python runserver
```   

然后即可用管理员邮箱及密码```admin```登陆
