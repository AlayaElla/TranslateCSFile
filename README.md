# TranslateCSFile
使用python翻译unity的插件C#脚本的注释以及tooltip和header。

TopdownEngine的代码注释相当良心，基本上所有的方法全部加了注释。

不过全英文对我来说看着难免还是有些吃力。。

所以尝试使用python写了个翻译脚本，使用正则表达式来匹配注释内容。


**配置相关：**

keylist是注释关键字列表，注释的翻译方式为在英文注释下新加一行翻译好的中文注释。

insplist是unity面板中的提示列表，提示的方式为在英文后加“\n”和翻译好的中文

ignorekeylist为忽略的文本，如果注释中有此列表中的内容，则不翻译。

ignorefolderlist 为忽略的文件夹，此列表中文件夹的C#脚本不翻译。

做了两个翻译api的模块，可以在import中替换
- 百度（TranslateBaidu）：百度api需要申请appid和secret。
- 有道（TranslateYoudao）：可以直接用，但是有道每天免费翻译的上限实在太少了，几乎不可能把所有脚本翻译完。。

翻译代码中做了一些省额度的操作，

比如：tooltips的文本大概率和之前的注释是一样，所以只提取一次翻译文本。

代码还有很多可优化空间，只是做个记录用。

**效果如下：**

翻译header：

![image](https://user-images.githubusercontent.com/21375302/186697941-12abf791-6046-4a36-9eef-210629d8dfa0.png)

翻译tooltips：

![image](https://user-images.githubusercontent.com/21375302/186697959-71efb147-bce5-404a-86d2-35760a1601f9.png)

翻译注释：

![image](https://user-images.githubusercontent.com/21375302/186697981-c1926c4e-8c02-4f94-a8cd-138b6a25cc65.png)

