## Strategy Ranking Rules Overview
After creating a strategy, there will be a standardized process for calculating daily scores, determining rankings, and distributing rewards based on recent performance and adherence to specific conditions.

The project goal is to reward strategies that can produce consistently positive returns with minimal drawdowns, while applying penalties on certain conditions that may indicate trading violations or insufficient participation. 

### ⏳ Observation Period
- 14-Day Lead-in: New strategies must undergo a 14-day observation period before they are eligible to be ranked for rewards. No scores will be calculated during this observation period.

### 📈 Scoring Process
- Daily Scoring: At the end of the observation period, the strategy’s score will be calculated at the end of each trading day. A day is defined from 8:00 AM UTC to the next 8:00 AM UTC.
- Scoring Formula: The final score is derived as a ratio of the strategy's exponentially daily weighted returns against a rolling maximum peak-to-trough drawdown over the past 14 days.

### 💯 Daily Score Calculations
1. Daily Return Calculation

    At the end of each trading day, the platform will calculate the daily strategy PNL (in USDT). The return is derived by comparing the account balance at the start and end of the day, and adjusting for any deposits or withdrawals that might have occurred during the session.

       $_Return  = Balance_DayEnd - Balance_DayStart - Net_Inflows

2. Daily % Return Calculation

    The Daily % Return is calculated by dividing the Daily Return by the average balance for the day, adjusting for any deposits or withdrawals. This represents the daily percentage return of the strategy.

        %_Return = $_Return / Avg(Balance_DayStart, Balance_DayStart+Net_Inflows)

3. Weighted Historical Performance

    The performance of the strategy is exponentially weighted, giving more importance to recent results but still recognizing one's historical performance. Strategies that have performed better in the near term will receive higher scores.

        Day_Weight =  EXP ^ ( - (Measurement_Day - Daily_Returns) / (Measurement_Day) )
        Exponentially Weighed Daily Returns = Sum(Day_Weight * %_Return) / Sum (Day_Weights)

4. Trading Frequency Adjustment

    In order to accommodate different trading styles, we will give users the option to define their trading styles to be 'Frequent', 'Base', or 'Infrequent'.  The trading style selection will affect the decay weights of daily returns, with faster decay giving more weights to recent returns (high frequency), and slower decay favouring historical performance.

      $$
      \text{Weight}(d) = \exp\left(-\lambda \cdot \frac{N-d}{N}\right)$$

    where λ = decay parameter
      - λ = 2, faster decay
      - λ  = 1, base decay
      - λ = 0.5, slower decay
    ![](pics/ExponentialDecayWithDifferentλValues.png)

    To discourage inappropriate mis-use of the formula weights, there will be a 30-day cooldown period before a frequency change can be made again.

5. 14-Day Maximum Drawdown

    The system measures the largest peak-to-trough capital drawdown incurred by the strategy on a rolling 14-day basis. A smaller drawdown will have a considerable impact on the final ranking score, rewarding strategies with strong risk discipline that can avoid taking large losses over time.
   
        Strategy Daily Score = Exponentially Weighted Daily Returns / ABS [Min (-1%, 14D Max Drawdown ) ]

6. Excessive Risk Taking Adjustment

    Strategies that are excessively risk-levered with high margin usage will be subject to a score adjustment. Specifically, strategies that employ margin usage (as defined by the relevant CEX) in excess of 50% will see a 20% discount on their final score, and excesses of >80% will suffer a 50% discount.
   
    ![](pics/ExcessiveRiskTakingAdjustment.png)

7. AUM / Wallet Size Adjustment Factor

    For strategies achieving the same performance (i.e., return rate、drawdown), a higher AUM / wallet size will result in a higher score. This reflects the exponentially higher difficulty of managing larger portfolios, rewarding high-AUM strategies with an added scaling factor.
    
        Final Score = Strategy Daily Score*(1+ln(sqrt(max(1, AUM/100k))))
    ![](pics/AUMWalletSizeAdjustmentFactor1.png)
    ![](pics/AUMWalletSizeAdjustmentFactor2.png)


### ❌ Scoring Violations (i.e. Zero Score Conditions)

  If a strategy violates any of the following rules, it will be penalized with a zero score against that day's positive return, while retaining the full impact of a negative drawdown.

  Said in another way, miners who are subject to trading violations will have a maximum daily score of 0 with a downside score equal to its negative daily performance.

1. Minimum Balance Requirement
   
    The wallet must have a minimum balance of at least 10,000 USDT at both the start and end of the trading day.  A trading day is defined with a start time of 8:00 AM UTC.

    Rationale: to require enough 'skin in the game' to encourage authentic trading while minimizing outsized % gains from marginal wallets.

2. Minimum Trading Volume Requirement
   
    To qualify for the daily scoring, each miner must meet a minimum adjusted trading volume of 5,000 USDT on each rolling 7-day trading period.  The adjusted volume is defined as follows across the different instruments:

    Options:
    - Adjusted Volume = Option Premium
   
    Futures and Spot:
    - Adjusted Volume = Order Quantity × Order Price × Coin Ratio
    - Coin Ratio: Varies by cryptocurrency and is based on the initial margin rates. For specific Coin Ratios, please refer to the [OKX Margin Rates](https://www.okx.com/trade-market/position/swap) page.
  
    Rationale: to require some minimal level of participation from traders to suggest that the trading strategy is still relevant.

3. Net Withdrawal Restriction
   
    Strategies cannot have net withdrawal of capital (ie. Outflows > Inflows) on each trading day in order to qualify for return calculations. Any net withdrawals of capital from a strategy will result in a zero-score calculation against any positive performance on the day.

    Rationale: users who 'cash out' of the strategies should no longer be eligible for rewards.

4. Whitelisted Assets Requirement

    Only transactions involving the following whitelisted assets and their derivatives (spot, futures, options) are eligible for scoring: 
     - BTC, ETH, SOL
     - USDT, USDC
     - ADA, AVAX, BCH, BNB, DAI, DOGE, DOT, LEO, LINK, SHIB, SUI, TAO, TON, TRX, XRP.
     
     Trades involving any non-whitelisted assets or derivatives will result in a zero score for the day.
   

5. Platform Execution
   
    All eligible trades must be executed on the SignalPlus platform on all opening and closing trades; however, liquidation or settlement trades are exempted as they are automatically handled by exchanges.
  
    Rationale: to ensure the sanctity of the trading data as all trades must be authentic and commercially driven

6. Off-Market and Wash-Trading Prevention
   
    Any trades flagged as off-market or wash trades will result in a zero score for the strategy on that day, regardless of any positive performance.

    1. Rule 1
       
        For Option instruments specifically, a simultaneous violation of both conditions will result in a penalty:
        - BTC/ETH Options: 
          1. MTM value of the option is >30bp of the underlying token's value AND
          2. MTM value of the option is >30% of the mid-market mark of the premium price
             
        - All Other Options: 
          1. MTM value of the option is >50bp of the underlying token's value AND
          2. MTM value of the option is >50% of the mid-market mark of the premium price
          
        Calculation formulas will vary slightly depending on the underlying margin, but violations will be triggered when:
        - For USDT-Margin instruments
          $$ABS(filledPrice - markPrice) > underlyingPercent$$ AND
          $$ABS(filledPrice - markPrice) > markPrice * Percent$$
          
        - For Coin-Margin Instruments
          $$ABS(filledPrice - markPrice) > underlyingPrice * underlyingPercent$$
          AND$$ABS(filledPrice - markPrice) > markPrice * Percent$$

   2. Rule 2  【Added on November 26, 2024】
       
        For option trades where markPrice > 50bp and filledPrice > 50bp, the following rule applies:
        If the total MTM value of all executed trades exceeds 100 USDT on the day, the average deviation of the executed vs marked price must not exceed 10% of the total notional value.
        
        Violations will be triggered when:
        - For USDT-Margin instruments
          $$SUM(ABS(filledPrice - markPrice) * qty) > 100\:USDT$$ AND
          
          $$SUM(ABS(filledPrice - markPrice) * Qty) / sum(markPrice * Qty) > 10%$$
          
        - For Coin-Margin Instruments
          $$SUM(ABS(filledPrice - markPrice) * qty * index) > 100\:USDT$$
          
          AND$$SUM(ABS(filledPrice - markPrice) * Qty)\:/\:SUM(markPrice * Qty) > 10%$$

   3. Rule 3  【Added on November 28, 2024】
       
        For option trades where markPrice < 3bp, the following rule applies:
       
        If the total spread PnL of all executed trades exceeds 0.2% of the day's initial equity, it will be considered a violation.
        
        Calculation formulas：
        1. Spread Calculation
              - For a Buy order:  $$Spread = markPrice - filledPrice$$ 
              - For a Sell order:  $$Spread = filledPrice - markPrice$$
   
        2. Spread Value in USDT
              - For USDT-Margin instruments:  $$Spread = spread × qty$$ 
              - For Coin-Margin instruments:  $$Spread = spread × indexPrice × qty$$
            
        3. Violation Threshold
              - Calculate the sum of all spread values for the day. The profit spread and loss spread will offset each other, and the final total spread is obtained.
              If $$totalSpread / equityStart > 0.002$$,  the trade violates the rule.
    
    Rationale: to detect and prevent any potential wash trading or malicious wash trading aimed at generating profits.

### 🏅 Rankings and Rewards Distribution
- Daily Rankings: Strategies are ranked based on their daily scores from the scoring formula, with higher scores leading to better sequential rankings.
- Reward Distribution: 
  - Please Note: The rewards for each day will be distributed after the conclusion of the next trading day.
  - Rewards are distributed based on the strategy’s score relative to the Top-50 performing strategies on the day.
  - The formula for calculating rewards is:
    
        Strategy Reward = (Strategy's Daily Score / Total Daily Score of the Top-50 Strategies) * Total Daily Reward Pool of the Day
