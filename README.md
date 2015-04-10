# flaskblog
一个用flask写的博客

## 部署
1. 设置管理员邮箱环境变量


    export BLOG_ADMIN=foo@bar.com
  
2. 初始化


    git clone https://github.com/eric6356/flaskblog.git
    cd flaskblog
    pip install -r requirement.txt
    python manage.py deploy
    
