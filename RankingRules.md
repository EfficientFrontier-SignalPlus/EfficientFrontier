# V1.0   【Oct 17, 2024】

## Strategy Ranking Rules Overview
After creating a strategy, there is a standardized process for calculating daily scores, determining rankings, and distributing rewards based on recent performance and adherence to specific conditions. The goal is to reward strategies that can produce consistently positive returns with minimal drawdowns, while applying penalties on certain conditions that may indicate trading violations or insufficient activity. 

⏳ Observation Period
- 7-Day Wait: New strategies must undergo a 7-day observation period before they start earning points. No scores are calculated during this time.

📈  Scoring Process
- Daily Scoring: Once the observation period ends, the strategy’s score will be calculated at the end of each trading day. A day is defined from 8:00 AM UTC to the next 8:00 AM UTC.
- Scoring Formula: The final score is derived from a combination of the strategy's exponentially weighted returns and its rolling maximum drawdown over the past 7 days.

## Steps to Calculate Daily Scores
### 1. Daily Return Calculation
At the end of each trading day, the platform will calculate how much profit or loss (in USDT) the strategy has generated. This is derived by comparing the account balance at the start and end of the day, and adjusting for any deposits or withdrawals that might have occurred during the session.

$_Return  = Balance_DayEnd - Balance_DayStart - Net_Inflows

### 2. Daily % Return Calculation
The Daily % Return calculated by dividing the Daily Return by the average balance for the day, adjusting for any deposits or withdrawals. This represents the daily percentage return of the strategy.

%_Return = $_Return / Avg(Balance_DayStart, Balance_DayStart+Net_Inflows)

### 3. Weighted Historical Performance
The performance of the strategy is exponentially weighted, giving more importance to recent results but still recognizing one's historical performance. Strategies that have performed better in the near term will receive higher scores.

Day_Weight =  EXP ^ ( - (Measurement_Day - Daily_Returns) / (Measurement_Day) )
Exponentially Weighed Daily Returns = Sum(Day_Weight * %_Return) / Sum (Day_Weights)

### 4. 7-Day Maximum Drawdown
The system tracks the largest capital drawdown incurred by the strategy on a rolling 7-day basis. A smaller drawdown will have a considerable impact on the final ranking score, rewarding strategies with strong risk discipline that can avoid taking large losses.

Strategy Daily Score = Exponentially Weighted Daily Returns / ABS [Min (-1%, 7D Max Drawdown ) ]

## Scoring Violations (ie. Zero Score Conditions)
If a strategy violates any of the following rules, it will receive a zero score for any positive return performance for that day, while retaining the full impact of a negative performance day.
Said in another way, miners who are subject to trading violations will lose any positive benefits of a positive day, but suffer the full impact from a negative session on the ranking score calculations.

### 1. Minimum Balance Requirement
The wallet must have a minimum balance of at least 10,000 USDT at both the start and end of the trading day.  A trading day is defined with a start time of 8:00 AM UTC.

### 2. Minimum Trading Volume Requirement
To qualify for the daily scoring, each miner must meet a minimum adjusted trading volume of 1,000 USDT on each trading day.  The adjusted volume is defined as follows across the different instruments:
  Options:
  - Adjusted Volume = Option Premium
  Futures and Spot:
  - Adjusted Volume = Order Quantity × Order Price × Coin Ratio
  - Coin Ratio: Varies by cryptocurrency and is based on the initial margin rates. For specific Coin Ratios, please refer to the [OKX Margin Rates](https://www.okx.com/trade-market/position/swap) page.

### 3. Net Withdrawal Restriction
Strategies cannot have net withdrawal of capital (ie. Outflows > Inflows) on each trading day in order to qualify for return calculations. Any net withdrawals of capital from a strategy will result in a zero-score calculation against any positive performance on the day.

### 4. Platform Execution
All eligible trades must be executed on the SignalPlus platform on all opening and closing trades; however, liquidation or settlement trades are exempted as they are automatically handled by exchanges.

### 5. No Wash or Off-Market Trading
Any trades flagged as off-market or wash trades will result in a zero score for the strategy on that day, regardless of any positive performance.
- For Buy Orders: A trade will be flagged if the execution price is more than 30% lower than the mark price and exceeds the mark price by more than 3 ticks.
- For Sell Orders: A trade will be flagged if the execution price is more than 30% higher than the mark price and falls below the mark price by more than 3 ticks.

These rules are designed to detect and prevent any potential wash trading or price manipulation, ensuring that buy and sell orders are executed within a fair range of the market price.


## 🏅 Rankings and Rewards Distribution
### Daily Rankings:
- Strategies are ranked based on their daily scores from the scoring formula, with higher scores leading to better rankings.
### Reward Distribution: 
  - The rewards for each day will be distributed after the conclusion of the next trading day.
  - Rewards are distributed based on the strategy’s score relative to the total peer group.
  - The formula for calculating rewards is:
Strategy Reward = (Strategy's Daily Score / Total Daily Score of All Strategies) * Total Daily Reward Pool of the Day
