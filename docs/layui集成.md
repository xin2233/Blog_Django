## 集成layui
可以学习以下模板  
layuicms2.0  
layuicms  
layuiAdmin  
这些模板都是多标签页。  
目前遇到的问题：在集成时js的网页更新不方便，无法一键集成  
方法1；使用模板进行分割拆开，不适用layui里的js方式进行页面管理。

方法2：启用iframe 功能：  
已找到方法：再setting 中设置 X_FRAME_OPTIONS = 'SAMEORIGIN' ，即可启动iframe 功能。