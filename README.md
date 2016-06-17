# Team
Team Blog

## LICENSE
MIT

### 设计与功能

```

# 博客

## API

### 功能作为API接口，实现某功能，就必须调用某接口，评论功能另说

### 接口文档

#### https://api.saintic.com

#### API资源

##### /user

##### /blog

##### /token

### 设计

#### 访问API，公开资源，不需要验证；非开放资源，要username+token(需要先username+password申请token)验证一致性通过返回数据。

#### flask-RESTFul，JSON，包含请求url全地址、错误信息、code状态码、数据等

#### 每个请求都包含requestId，由str(uuid.uuid4())生成，绑定到g中，全文应用

#### before_request, after_request(前者生成上下文需求变量和请求开启日志，后者记录日志和自定义响应头)

## front

### js调用API展现

### Bootstrap

#### 首页、登录注册(URL)、博客详情页、个人中心页、标签分类展示页

#### 首页分页展示博客及右侧栏，个人中心资料博客等管理，评论功能

### 登陆注册/user?action=log/reg

#### 账号唯一, 作为登录凭证

#### 用户及权限

### 插件化-可插拔模块

### 具体实现功能

#### 自定义站点资料

#### 文章，推荐置顶等

#### RSS，订阅

#### 站内搜索

#### 微博、空间、微信等文章同步(自动分享，由配置文件开启)

#### Windows live writer接口

#### 百度提交文章、Google Search Console

### backend

#### Flask-Admin

#### 文章管理、资料管理，写文章Markdown或可视化

```

### 分支与作用
> [1. api, 提供需要的接口][1]

> [2. front, 前端与后台][2]

  [1]: https://github.com/saintic/Team/tree/api
  [2]: https://github.com/saintic/Team/tree/front