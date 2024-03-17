## 作业一
```
改进characterglm_api_demo_streamlit.py的代码，为文生图功能加上风格选项，在页面上加上一个可指定图片风格的选项框。
```
```
streamlit run characterglm_api_demo_streamlit.py
```

## 作业二
```
实现 role-play 对话数据生成工具，要求包含下列功能：
基于一段文本（例如小说，百科）生成角色人设，可借助 ChatGLM 实现。
给定两个角色的人设，调用 CharacterGLM 交替生成他们的回复。
将生成的对话数据保存到文件中。
（可选）设计图形界面，通过点击图形界面上的按钮执行对话数据生成，并展示对话数据。
```
```
streamlit run role_play.py
```

## 运行环境
```
python==3.11

zhipuai==2.0.1
streamlit==1.32.2
python-dotenv==1.0.1
jwt==1.3.1
```

