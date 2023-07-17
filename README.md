# flomo2memos
将flomo导出至memos

## 使用方式

1. 克隆本仓库到本地，并安装```requirements.txt/environment.yaml```中依赖

   ```bash
   git clone https://github.com/1eif/flomo2memos.git
   ```

2. 在[flomo](https://v.flomoapp.com/mine?source=account)中点击**导出所有数据（as HTML）**

3. ```bash
   cd flomo2memos
   ```

   将压缩包中```index.html```和```file```文件夹（如有）解压到项目根目录中

4. ```python main.py index.html <your_memos_url> <open_id>```
   - <your_memos_url> 替换为你的memos域名，例如```https://usememos.com/```
   - <open_id> 替换为你自己的Open ID，例如```h874916b-a9j9-77ug-kj8y-123hfve295ifm```

5. 等待完成

## 已知问题

通过API上传的图片，不能显示缩略图，怀疑是数据库写入没有type字段信息

## TODO

为了方便使用，如有前端同学有空闲时间可以弄个简单的页面


## 感谢

[Alwayfeels/flomoParse: 一个能将flomo导出数据转换为JSON数据的小工具](https://github.com/Alwayfeels/flomoParse)
