# AOSC_HardwareData_Survey
https://aosc.io/news/detail/2024-11-19-hwdata-survey.zh-cn.md \
用于(几乎是)全自动处理通过《hwdata 信息缺漏征集表》收集到的缺失硬件信息。

## 用法
1. 确保您有一个良好的`Internet`环境
2. 确保您的计算机上安装了`Microsoft Office`,  `WPS`, `LibreOffice`或其它可以编辑`.xlsx`电子表格文件的应用程序
3. 执行`pip install -r requirements.txt`
4. 从金山在线文档中导出并下载"hwdata_信息缺漏征集表"(`.xlsx`格式)
5. 将表格放置在项目目录内, 其名称必须为`hwdata_信息缺漏征集表.xlsx`
6. 执行`python main.py`并按提示完成操作, 其中有部分操作需要手动完成

## TODO
自动提交？
