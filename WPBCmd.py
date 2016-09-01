#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    @version: 1.0
    @author : Carrot
    @time   : 16/9/1 15:45
"""


Unknown = 0                             # 未知
Heartbeat = 3101                        # 心跳包

Connect_Socket = 8888                   # 连接包SOCKET
Connect = 9999                          # 连接包

Customer = 10000                        # 个人信息
Balance = 10001                         # 账户资金
StatementList = 10002                   # 资金流水
StatementDetail = 10003                 # 单笔流水明细
TransactionList = 10004                 # 交易历史
TransactionDetail = 10005               # 单笔交易明细
OrderList = 10006                       # 订单列表
OrderDetail = 10007                     # 单笔订单明细
Coupon = 10008                          # 券
QueryQuote = 10009                      # 查询行情
KLine = 10010                           # 查询K线数据
VerificationCode = 10011                # 验证码
ProductList = 10012                     # 品种配置信息

CouponCount = 10014                     # 券数量
QueryInOutList = 10015                  # 查询出入金资金流水
QueryOpenCloseOrderList = 10016         # 查询建平仓资金流水

QueryCardBind = 10021                   # 查询绑定银行卡信息
IsCardBinded = 10022                    # 是否绑定银行卡(暂不用)

BuywithoutCoupon = 11000                # 建仓(无券)
BuyWithCoupon = 11001                   # 建仓(券)
UpdateLimits = 11002                    # 设置止盈止损
CloseOrder = 11003                      # 手动平仓
Deposit = 11004                         # 充值
Withdraw = 11005                        # 提现

UpdateCardBind = 11007                  # 修改绑定银行卡信息(暂不用)
DepositWithCardBound = 11008            # 绑定银行卡充值
withdrawWithCardBound = 11009           # 绑定银行卡提现

BuywithoutCouponJointBuy = 11011        # 建仓(合买)
UpdateLimitsJointBuy = 11012            # 设置止盈止损（合买）
CloseOrderJointBuy = 11013              # 手动平仓(合买)

CreateOrderFlashLight = 11014           # 闪赚建仓
CloseOrderFlashLight = 11015            # 闪赚平仓

WithdrawableBalance = 15001             # 可出金余额

RegisterNotification = 20001            # 注册通知
LoginNotification = 20002               # 登录通知
DepositNotification = 20003             # 充值通知

DisableIntro = 21000                    # 取消操作指引

AutoCloseOrder = 30001                  # 自动平仓通知
AgQuote = 30002                         # 白银行情通知
CloseOrderInfo = 30003                  # 平仓信息同步
OilQuote = 30004                        # 石油行情通知

QueryAgQuote = 31001                    # 查询白银行情
QueryOilQuote = 31002                   # 查询石油行情
FlashingLight = 31003                   # 闪电图数据接口命令号

MarketStateNotification = 40001         # 交易状态通知
CouponChangeNotification = 40002        # 券更新通知
Blacklist = 40003                       # 黑名单更新通知

LongShortRatioNotification = 40005      # 用户多空比推送通知

QueryMarketState = 41001                # 查询交易状态
QueryMarketStatistics = 41002           # 查询交易人数次数
QueryFriendCircleRank = 41003           # 分享者朋友圈排名
QueryContractInfo = 41004               # 合约信息
QueryLongShortRatio = 41005             # 用户多空比请求
QueryWithdrawInfo = 41006               # 用户体现银行卡信息

CommonRequestInfo = 41012               # 通用请求
QueryUserProfit = 41013                 # 查询用户盈亏模拟数据
RegisterUrl = 41014                     # 获取注册页面URL
LoginUrl = 41015                        # 获取登录页面URL

DepositUrl = 41017                      # 获取充值页面URL

OrderInfo = 51009                       # 持仓信息 包括建仓时间 建仓类型
