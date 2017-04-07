# **Line-bot Webhook 创建与部署**


## **前言**

　　最近在研究LINE bot，通过搭建环境，编写webhook，终于实现bot与line 用户的对话。此过程并不是一帆风顺，期间遇到很多问题，咨询了很多朋友，在此表示感谢，特别感谢line-bot-sdk-python 的维护者。
line-bot 实现reply功能的关键在于`Webhook` 的编写。本文使用了[flask](http://docs.jinkan.org/docs/flask/)框架来编写Webhook. 在此，就需要解决两个问题：

- **1. Webhook 是什么？**
- **2. Webhook 怎么用？**

### **1. Webhook 是什么？**

> 官网解释：  Receive notifications in real-time when a user sends a message or friends your account. 
> When an event, such as when a user adds your account or sends a message, is triggered, an HTTPS POST request is sent to the webhook URL that is configured on the Channel Console. 

咋一看，似懂非懂。可参考github或者coding中钩子的思想。
意思是 当有好友添加你或者发消息给你时，会触发一个事件，然后 就会发送一个HTTPS POST请求到你的 `webhook url`.(不懂没事，后面还会提到，本文的重点。)


### **2. Webhook 有什么作用？**

最简洁的方式，莫过于图。

![Webhook url](http://img.blog.csdn.net/20170407211231027?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

LINE bot的运作流程是这样的：
1. 使用者传送消息到LINE bot账号；
2. LINE bot收到消息会将消息post给Webhook URL；
3. Webhook URL就是我们所说的web service，负责实际处理的消息。

从问题1和问题2，我们可知，我们需要填写一个`webhook url`, 且必须是HTTPS协议。而这个 `webhook rul` 对应的就是我们编写webhook生成的。

这里，我是将项目部署在 [Heroku](https://www.heroku.com/python)，免费，且支持HTTPS. 不足的是，因为是国外的一个云服务器，反应略慢。
另外，你们也可尝试   `ngrok`.

## **效果图**

先看效果，再看值不值得学。
本文的目的在于`webhook url`, 所以这里我做了一个很简单的line-bot，支持简单的自动应答功能。
可以体验下，添加我的bot为好友，QR code 如下：
![QR code](http://img.blog.csdn.net/20170407212531173?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

然后，你就可以和我的bot进行对话了。
![bot](http://img.blog.csdn.net/20170407212641497?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


## **搭建步骤**

本部分是在[twtrubiks](https://github.com/twtrubiks/line-bot-tutorial)的基础上做些修改和补充，内容是繁体书写，不影响阅读。再次表示感谢作者的付出。

---
### 环境
本人实践环境及所需工具。

* Windows server 2008 r2
* Heroku
* line-bot-sdk-python
* flask
* git
* python 3.6.1


### 步骤如下：

1. 请先到 [https://business.line.me/zh-hant/](https://business.line.me/zh-hant/) 这里登入自己原本的 line 账号，然后选择Messaging API

![alt tag](http://i.imgur.com/KIzExmQ.jpg)

接下来你会看到 <b>開始使用Messaging API</b> 以及 <b>開始使用Developer Trial</b>

在这里我们选择 <b>開始使用Messaging API</b>

![alt tag](http://i.imgur.com/graLPrj.jpg)

這兩個差別在哪裡呢? 可以到同一個頁面的下方觀看，基本上就只是方案不同而已

![alt tag](http://i.imgur.com/bERbTGz.jpg)

接著就是一些設定，點選 選擇公司/經營者

![alt tag](http://i.imgur.com/d1pVdx9.jpg)

點選 新增公司/經營者

![alt tag](http://i.imgur.com/of23y7W.jpg)

填寫一些資料

![alt tag](http://i.imgur.com/7L9nulI.jpg)

line bot 的 大頭貼 以及 名稱 設定

![alt tag](http://i.imgur.com/7483ljT.jpg)

![alt tag](http://i.imgur.com/a4Mf3Rl.jpg)

設定完後，請選擇 申請

![alt tag](http://i.imgur.com/Q6q8zGA.jpg)

以上設定應該不會有什麼問題

請選擇 開始使用 API

![alt tag](http://i.imgur.com/DOEjH0F.jpg)

請選擇 確認

![alt tag](http://i.imgur.com/pKWBvsj.jpg)

這些請注意，  選擇 <b>允許</b> ，然後記得 <b>儲存</b>

![alt tag](http://i.imgur.com/Ofm9SeJ.jpg)

點選 <b>Line Developers</b>

![alt tag](http://i.imgur.com/cW9713h.jpg)

你會進入下面這個畫面，在這個畫面中，有兩個東西很重要，分別是

* Channel Secret

* Channel Access Token

<b>Channel Secret</b>

![alt tag](http://i.imgur.com/jpIEMh4.jpg)

<b>Channel Access Token</b>

如果你看到的是空的，請點選 <b>ISSUE</b> 就會顯示了

![alt tag](http://i.imgur.com/PcCEL4P.jpg)

請將你的 <b>Channel Secret</b> 以及 <b>Channel Access Token </b>

貼到下方的程式碼

```
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
``` 

更多内容可參考 [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)

接下來因為 Line Bot 需要 SSL憑證 ( https )，所以我直接使用 [Heroku](https://dashboard.heroku.com/) 

如果不知道什麼是 [Heroku](https://dashboard.heroku.com/)  以及它的使用方法

請參考我之前寫的 [Deploying-Flask-To-Heroku](https://github.com/twtrubiks/Deploying-Flask-To-Heroku)

佈署

![alt tag](http://i.imgur.com/kseRgxr.jpg)

如上圖，我的網址是 [https://python-ine-bot.herokuapp.com/](https://python-ine-bot.herokuapp.com/)

接著我們要加入 Webhook URL ，請點選 EDIT ，並且加入你自己的網址，網址格式

```
https://{你的網址}/callback
``` 

舉例，我的網址就是

```
https://python-ine-bot.herokuapp.com/callback
``` 

![alt tag](http://i.imgur.com/5ckn24T.jpg)

![alt tag](http://i.imgur.com/TIjIM9W.jpg)


我的源码已上传至github,请查看[line-bot-flaskr](https://github.com/Deen12520/line-bot-flaskr)。

部署成功后，会在Heroku 中看到以下内容：
![Heroku deploy](http://img.blog.csdn.net/20170407220433460?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


## **注意事项**

### 1.填入 `webhook url` 后不需要进行verify.

我使用 [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)當我按下 VERIFY，出现了如图所示所示错误，不影响bot的使用。原因是点击verify时，会返回一个虚拟的reply_token,所以failed。

![alt tag](http://i.imgur.com/wb0Qw5W.jpg)

<font color=#0099ff>**本人的`webhook url` :**</font>
![这里写图片描述](http://img.blog.csdn.net/20170407215139719?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
关于这个问题的详细解释，请查看我提交的[issue](#jump).

### 2.部署过程中，请创建一个独立的Python运行环境,并保证是在虚拟环境下进行的。
虚拟环境有个标志(env)，如下图：
![env](http://img.blog.csdn.net/20170407221429828?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGluZ2RpbmdfMTIzNDU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

### 3. 多用 `Heroku logs --tail` 查看日志，从日志中你就可以找到大多数错误的原因。



## **总结**

本文的重点是在构造`webhook url`.
主要步骤如下：
1. 申请一个messaging api 的账号；
2. 书写callback函数，并部署到Heroku;
(代码可直接download我的github源码，执行过程请参照 [Deploying-Flask-To-Heroku](https://github.com/twtrubiks/Deploying-Flask-To-Heroku) )
3. 进行bot与好友对话，进行测试。

部署花了我很长时间，需要对git很熟悉，一步一步的来。


我的源码已上传至github,请查看[line-bot-flaskr](https://github.com/Deen12520/line-bot-flaskr)。

## **链接**

### **Github issue**
1. <span id="jump">[webhook url cannot be verified.](https://github.com/line/line-bot-sdk-python/issues/37) </span>

### **参考网址**

1. 两个教学视频：
* [Youtube Demo Tutorial V1 ](https://youtu.be/EToFs-ysXKw)   

* [Youtube Demo V2](https://youtu.be/1IxtWgWxtlE)   

2. [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
3. [Line Echo Bot on Django](http://lee-w-blog.logdown.com/posts/1134898-line-echo-bot-on-django)
(这篇文章很好，内部写了两种webhook的处理方式。)
4. [line messaging-api](https://devdocs.line.me/en/#messaging-api) 


## License
MIT license






