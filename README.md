# Blog_Django
django 3.2， python 3.9  

## 已实现功能
- 博客用户界面
- 登录，注册
- 文章首页显示
- 文章详情显示
- admin管理界面，编辑文章，集成富文本编辑器
- 登录界面优化：增加vanta.js动画，修改登录界面->flatui样式

## 待实现功能
- 忘记密码
- 注册界面样式优化 flatui
- 将admin界面的文章编辑功能，由新增的用户中心界面的文章编辑按钮，跳转到自实现的新的文章编辑界面，不在使用admin的默认编辑功能

### 
- 22.9.25, 增加用户中心文章编辑按钮，文章保存未作，富文本编辑器上传图片出现问题需要调试
- 22.9.26, kindeditor存在问题，目前采用wangeditor已成功实现富文本编辑器上传图片
- 22.9.28, kindedtor 图片问题已解决
- 22.10.15, 增加富文本编辑器下方 文章标签类，类别类，显示和选择【checkbox】
- 22.10.17，完成富文本编辑器数据存储到数据库