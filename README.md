<div align="center"> 
<h1 align="center">贴吧签到助手</h1>
<img src="https://img.shields.io/github/issues/LuoSue/TiebaSignIn-1?color=green">
<img src="https://img.shields.io/github/stars/LuoSue/TiebaSignIn-1?color=yellow">
<img src="https://img.shields.io/github/forks/LuoSue/TiebaSignIn-1?color=orange">
<img src="https://img.shields.io/github/license/LuoSue/TiebaSignIn-1?color=ff69b4">
<img src="https://img.shields.io/github/languages/code-size/LuoSue/TiebaSignIn-1?color=blueviolet">
</div>

# 简介

用的是手机端的接口，签到经验更多，用户只需要填写`BDUSS`即可，使用Github Actions自动签到。

# 功能

+ 贴吧自动签到

+ 支持推送签到结果至微信（PushPlus / Server酱，可选）

# 使用方法

## 1.fork本项目
### 必须检查的仓库设置

1. 确保 `Settings -> Actions -> General` 中 Actions 处于启用状态。`tieba.yml` 中的 `workflow-keepalive` job 已配置 `actions: write` 权限，无需授予仓库 `Read and write permissions`。

2. 确保仓库没有被 Archived（Settings -> General -> Danger Zone: Archive repository）。

## 2.获取BDUSS

在网页中登录上贴吧，然后按下`F12`打开调试模式，在`cookie`中找到`BDUSS`，并复制其`Value`值。

![](./assets/获取BDUSS.gif)

## 3.将BDUSS添加到仓库的Secrets中

Name | Value
-|-
BDUSS | xxxxxxxxxxx

将上一步骤获取到的`BDUSS`粘贴到`Secrets`中

![](./assets/添加BDUSS.gif)

## 4.配置微信推送（可选）

签到结束后会把结果推送到微信，支持`PushPlus`和`Server酱`，二选一即可，不需要推送可以跳过这一步。

### 方案一：Server酱

1. 打开 [Server酱](https://sct.ftqq.com/)，用微信扫码登录，复制页面上的`SendKey`（`SCT`开头的 34 位字符）。

2. 在仓库`Settings -> Secrets and variables -> Actions`中新建 Secret：`SCKEY`，值为上一步的`SendKey`。

### 方案二：PushPlus

1. 打开 [PushPlus](https://www.pushplus.plus/)，用微信扫码登录，复制页面上的`token`。

2. 在同一个位置新建 Secret：`PUSHPLUS_TOKEN`，值为上一步的`token`。

### 可用变量对照

Name | Value
-|-
PUSH_KEY | 可选，通用推送 key，优先级最高
SERVERCHAN_SENDKEY | Server酱官方文档推荐的变量名，值为 SendKey
PUSHPLUS_TOKEN | PushPlus 的 token
SCKEY | Server酱的 SendKey
PUSH_TOPIC | 可选，仅 PushPlus 群组推送使用，留空则推送给本人

程序按 key 前缀自动选择通道：`SCT`/`sctp`开头走 Server酱（`sctapi.ftqq.com`，`sctp`开头为 Server酱³），其它走 PushPlus。

## 5.开启actions

默认`actions`是处于禁止的状态，需要手动开启。

![](./assets/开启actions.gif)

## 6.第一次运行actions

+ 自己提交一次`push`。

将`run.txt`中的`flag`由`0`改为`1`

```patch
- flag: 0
+ flag: 1
```

![](./assets/运行结果.gif)

## 成功了

每天早上`6:30`将会自动进行签到。`tieba.yml` 中的 `workflow-keepalive` job 会自动保持该定时工作流处于启用状态。


Name | Value
-|-
SCKEY | xxxxxxxxxx

## 2026-5-30

+ 代码重构

+ 修改 API 以及签到策略

## 2020-11-01

+ 代码重构

+ 修改签到策略

大大提高一次运行，贴吧签到的成功率，基本很少的贴吧会签到失败。

+ 去除多用户的支持

+ 增加支持server酱推送，可以推送至微信

## 2020-10-19

~~增加支持多账户签到，每个账号的`BDUSS`使用`&&`分割，具体格式如下。~~
