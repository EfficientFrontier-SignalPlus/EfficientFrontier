# Efficient Frontier排名规则说明

## 策略排名规则概述

在策略创建后，平台将依据策略的近期表现和特定规则，通过标准化流程计算每日得分、确定排名，并分配相应奖励。
我们的目标是奖励能够持续稳定获得正收益且回撤较小的策略，同时对疑似交易违规或参与不足的策略施加惩罚。

### ⏳ 观察期
- 14天观察期：新策略在创建后必须经过14天观察期才有资格参与排名并获取奖励。在此观察期间不计算得分。

### 📈 评分流程
- 每日评分：观察期结束后，每个交易日结束时平台将为策略计算得分。交易日从UTC+8时间下午16:00开始，到次日下午16:00结束。
- 评分公式：最终得分通过策略的加权日收益率与过去14天的最大回撤比值计算得出。

### 每日评分步骤
1. 每日收益计算

    每个交易日结束时，平台会计算策略当日的收益（以USDT计）。通过比较日初和日终账户余额来确定收益，同时扣除当天的出入金影响。

        $_Return  = Balance_DayEnd - Balance_DayStart - Net_Inflows

2. 每日收益率计算

    每日收益率通过将每日收益除以当日平均余额得到，并扣除当日出入金影响，以更准确地反映策略的日收益率。

        %_Return = $_Return / Avg(Balance_DayStart, Balance_DayStart+Net_Inflows)

3. 历史表现加权

    策略表现根据时间加权，近期表现占比更高，但历史表现仍有一定权重。表现更佳的近期策略将获得更高得分。

        Day_Weight =  EXP ^ ( - (Measurement_Day - Daily_Returns) / (Measurement_Day) )
        Exponentially Weighed Daily Returns = Sum(Day_Weight * %_Return) / Sum (Day_Weights)

4. 14天最大回撤 

    系统会滚动计算策略在过去14天内的最大回撤，即从高点到低点的资金损失。较小的回撤将提升最终得分，奖励那些风险控制能力强、能避免大幅亏损的策略。

         Strategy Daily Score = Exponentially Weighted Daily Returns / ABS [Min (-1%, 14D Max Drawdown ) ]

5. 过度杠杆惩罚

    对过度使用杠杆的策略将进行得分调整。

    如果保证金使用率（由相关交易所定义）超过50%，则最终得分扣减20%；若超过80%，则扣减50%。

    ![](pics/ExcessiveRiskTakingAdjustment.png)

6. 资产规模调整

    策略在相同表现（如回报率、回撤）下，管理的资产规模越大，得分越高。

    这是因为更大规模的资产管理难度更高，因此我们引入一个膨胀系数以奖励高AUM策略。

         Final Score = Strategy Daily Score*(1+ln(sqrt(max(1, AUM/100k))))

    ![](pics/AUMWalletSizeAdjustmentFactor1.png)
    ![](pics/AUMWalletSizeAdjustmentFactor2.png)

### 违规评分项（即零分条件）
如果策略违反以下任一规则，则该日得分将为零，且任何正收益将不计入得分，而负收益仍会影响得分。

这意味着违规策略在当天的最高得分为0，且负回撤将完整计入。

1. 最低余额要求

    在交易日开始和结束时，账户余额必须保持在至少10,000 USDT以上。交易日定义为UTC时间早上8:00到次日早上8:00。

    理由：确保策略有足够的资本投入，以避免小额账户因仓位过小而导致不合理的收益率。

2. 最低交易量要求

    为满足每日得分条件，每个策略在任意滚动的7天内总交易量需达到至少5,000 USDT。不同产品的交易量计算标准如下：

    期权：
      - 计分交易量 = 期权权利金
   
    期货和现货：
      - 计分交易量 = 订单数量 × 订单价格 × 币种比率
      - 币种比率：根据加密货币类型和初始保证金率有所不同，详细比率可参考[OKX保证金率](https://www.okx.com/trade-market/position/swap)页面。
      
    理由：确保策略有一定活跃度，以表明策略仍在有效参与市场。

3. 净提现限制

    策略在每个交易日内不得发生资金净流出（即资金流出 > 流入），否则将无法计算收益。

    若策略在当日有净流出，则该日得分即使为正也将记为零。
    
    理由：退出策略的用户不应再享有奖励资格。

4. 白名单交易要求

    仅涉及以下白名单资产及其衍生品（现货、期货、期权）的交易才有资格计分：
    - BTC, ETH, SOL
    - USDT, USDC
    - ADA, AVAX, BCH, BNB, DAI, DOGE, DOT, LEO, LINK, SHIB, SUI, TAO, TON, TRX, XRP.
   
    若当日交易涉及白名单以外的资产或衍生品，则当天计分为零。

5. 平台交易执行要求

    所有符合条件的策略开仓和平仓交易必须在SignalPlus平台上执行；但因交易所自动处理的清算或交割交易则不受此限。
    
    理由：确保所有交易数据的真实性，要求交易行为必须为真实的市场行为。

6. 防止洗单与非正常市场交易
   
   任何被标记为非正常市场价格或洗单的交易都将导致当天得分为零，且无论其正收益如何。

   a. 规则1
   
    当单笔交易同时满足以下两个条件时，将被判定为违反非市场价格保护规则：
    - BTC/ETH 期权: 
      1. 期权的MTM value超过基础资产价值的 30bp，且
      2. 期权的MTM value超过期权市场价中间值的30%
         
    - All Other Options: 
      1. 期权的MTM value超过基础资产价值的 50bp，且
      2. 期权的MTM value超过期权市场价中间值的50%
    
    计算公式会根据期权的保证金类型略有不同，在以下情况下会触发违规：
    - 对于U本位期权
      
      $$ABS(filledPrice - markPrice) > underlyingPercent$$ AND
      
      $$ABS(filledPrice - markPrice) > markPrice * Percent$$
      
    - 对于币本位期权
      
      $$ABS(filledPrice - markPrice) > underlyingPrice * underlyingPercent$$ AND
      
      $$ABS(filledPrice - markPrice) > markPrice * Percent$$

   b. 规则2 【规则新增于 2024年11月26日】
   
    对于成交价格> 50bp且成交时标记价格> 50bp的期权交易，适用以下规则：
    如果当天所有执行交易的 MTM 总价值超过 100 USDT，则执行价格与标记价格的平均偏差不得超过总名义价值的 10%。
    
    出现以下情况将触发违规行为:
    - 对于U本位期权
      
      $$SUM(ABS(filledPrice - markPrice) * qty) > 100\:USDT$$ AND
      
      $$SUM(ABS(filledPrice - markPrice) * Qty) / sum(markPrice * Qty) > 10%$$
      
    - 对于币本位期权
      
      $$SUM(ABS(filledPrice - markPrice) * qty * index) > 100\:USDT$$ AND
      
      $$SUM(ABS(filledPrice - markPrice) * Qty)\:/\:SUM(markPrice * Qty) > 10%$$
      
   c. 规则3 【规则新增于 2024年11月28日】
   
    对于成交时标记价格 < 3bp的期权交易，适用以下规则：
   
    如果当前所有执行交易的总Spread PnL超过当日初始资产的0.2%，则视作违规。
    
    计算逻辑：
    1. **Spread 计算**
       - 对于买方订单:  $$Spread = markPrice - filledPrice$$
       - 对于卖方订单:  $$Spread = filledPrice - markPrice$$
   
    2. **将 Spread 转为 USDT 计算**
       - 对于 U本位期权:  $$Spread = spread \times qty$$
       - 对于 币本位期权:  $$Spread = spread \times indexPrice \times qty$$
    
    3. **违规阈值**
       - 计算当日总的 Spread PnL。盈利部分与亏损部分会相互抵消，计算出最终总的 Spread。
       - 如果 $$totalSpread / equityStart > 0.002$$，将视作当日违规。


    理由：检测和防止任何潜在的虚假交易或恶意刷单赚取收益的行为。
   

### 🏅 排名与奖励分配

- 每日排名：策略根据其当日得分进行排名，得分越高排名越靠前。
- 奖励分配：
  - 请注意，每日奖励将在次日交易日结束后发放。
  - 奖励根据策略当日得分与前50名策略的得分对比来分配。
  - 奖励公式如下：
  
          Strategy Reward = (Strategy's Daily Score / Total Daily Score of the Top-50 Strategies) * Total Daily Reward Pool of the Day