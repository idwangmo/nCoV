# nCoV

## 参考

春节闲的照着方糖的[nCoV-push](https://github.com/easychen/nCoV-push)防止的一个项目，没啥核心逻辑，就是无聊

## 使用

修改`settings.py`中`SERVER_CHAIN_KEY`的值，然后在`Redis`中进行如下操作:

```
set 2019ncov 0
set ncov 0
```

然后在命令行中执行`bash ncov.sh`就行，可以考虑将其加入到`crontab`中