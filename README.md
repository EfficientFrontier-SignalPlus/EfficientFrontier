<div align="center">
  
# **EfficientFrontier-SignalPlus**
  
</div>

## Introduction
> Efficient Frontier: a set of optimal portfolios that offer the highest expected return for a defined level of risk, or the lowest risk for a given level of expected return.

Efficient Frontier is a project initiated by SignalPlus and Bittensor, designed to identify the optimal risk-weighted trading strategies through the integration of decentralized machine learning networks and live trading data. This project will allow SignalPlus platform users to participate in Bittensor's mining program, while earning the chance for TAO airdrop rewards based on trading performance rankings.

### What is Bittensor?
Bittensor is a decentralized protocol specifically designed for machine learning (ML) and artificial intelligence (AI). It offers a unique marketplace for both users and providers of ML algorithms, utilizing a decentralized network to facilitate the exchange of these resources. More than just a marketplace for ML models, Bittensor provides a platform for training these models in a censorship-resistant environment, challenging the resource-intensive monopolies of tech giants.

At the core of Bittensor is its distinctive architecture, which combines specialized subnets for AI tasks, a blockchain for decentralized operations, and an API for seamless integration. This structure is considered crucial in positioning Bittensor as the leading network for AI services, catering to both individuals and corporations, with its native token, TAO, serving as the medium for transactions. As the network evolves, its goal is to accelerate the growth of AI by making sophisticated ML models accessible to a broader audience.

### Powering a Trading Nexus with SignalPlus
Built by an exceptional team of former banking and technology veterans, the SignalPlus terminal is the industry's leading derivative trading and options risk management platform that is well recognized by crypto's largest players and exchanges.  With a professional suite of automated and industrial-grade tools available to all, we now have a ready-made platform and built-in measurement tools to power the Bittensor network.

Never has such a level-playing field been offered to the every day user, allowing each trader to focus on refining their craft rather than being inhibited by inadequate tools.  As a result, traders are empowered to develop better trading frameworks rather than risk tools, ensuring better trading results and quality data to train the machine learning processes.

## Design Ethos
### Defining 'Risk-Adjusted Returns'
The quest for quality alpha and risk-adjusted returns has been a never-ending pursuit in the world of financial investments.  Risks are defined differently for different folks, and target returns will vary across people with different time horizons, financial circumstances, and available choices.

However, capital preservation, efficient capital use, and high multiple returns are baseline concepts that should resonate with every investor, and sensible guidelines can be developed to separate a good money manager from another.

Ultimately, every investor is looking for some combination of trading's own 'impossible-trinity':
> [!NOTE]
> 1. Return --> High returns
> 2. Risk control --> Minimal drawdowns
> 3. Time --> Getting your money back earlier

In response, we have developed a ranking system that evaluates the 3 parameters in a normalized way that can accommodate different trading styles.

### Paper Returns vs Actual Performance
Traders are performance driven practitioners seeking quantifiable results, and are particularly in-tune with an increasingly data-driven world.  While academic literature provides value in its own way, there can be no substitute for actual performance, with the SignalPlus platform perfectly suited to provide the type of quality-filtered data that is needed to derive our crowd-driven, crypto-trading Efficient Frontier.

### Other Design Considerations
There are further considerations that we have incorporated in designing our ranking model:
- Trading Environment & Behavioural Limits: we are cognizant that our decentralized trading environment is fundamentally different than, say, a professional multi-strat hedge-fund, where their PMs are bound by the rules of employment with clear limits of what they are allowed or not allowed to trade.
- Unconstrained User Entry & Exits: in the open-access world of crypto and networked mining, users are free to deploy their own trading frameworks with unrestrained entry and exit points, unlike 'fixed' measurement periods and fiscal periods for professional managers.
- Single Strategies vs Diversified Portfolios:  our strategies are evaluated on a standalone rather than on a portfolio wide basis.  Benefits of portfolio hedging and diversification must be done on an individual basis rather than across 'PMs'.
- Time Horizon & Risk Preference: The measurement timeframes that our users would prefer are likely to be significantly shorter than a typical long-only manager,and with a more ambitious risk-return preference that is more representative of crypto.
- Model Elegance & Simplicity: We will work within the limits of the dataset we are working with within a decentralized trading environment, and have designed a model that is grounded in simple practicality, where its construction and results can be easily appreciated by even the casual observer.

## The SignalPlus Value Proposition
More so than many other projects, Efficient Frontier is a comprehensive initiative that relies on the unique infrastructure and capabilities of SignalPlus to ensure the integrity and accuracy of trading data. Current on-chain data infrastructure is not yet at the point where it can be used seamlessly or efficiently to deduce optimal trading strategies on its own, and this is where SignalPlus comes in.
### 1. Authenticity of Trading Data
In any performance evaluation, the authenticity of the trading data is paramount. On-chain data alone is not able to recognize trading irregularities or factitious trades that were made to 'game' the system.

If miners were allowed to upload their own trading records, there is no reliable way to ensure those records weren’t fabricated. Miners could simply generate false data to inflate their performance, making the entire system vulnerable to manipulation.

At the same time, it would be unrealistic for miners to give validators direct access to their personal trading accounts, given obvious security and privacy concerns.  This is where SignalPlus can help to break the deadlock to act as a neutral but trusted conduit to verify trading records.

**SignalPlus will act as a trusted intermediary** through its integrated connectivity with all the major trading exchanges. The platform is technically capable of verifying all trading data to ensure that they are from real accounts with commercial executions, ensuring the sanctity of PNL records.

The platform will strive to ensure the fairness and integrity of the competition, allowing the Bittensor subnet to operate with trustworthy data and develop reliable results.

### 2. Professional Trading Infrastructure
SignalPlus is a professionally recognized and trusted partner with most of crypto's largest exchanges, offering a comprehensive suite of trading tools and risk management features available to every user. Traders can utilize the SignalPlus platform to execute complex and algorithmic trades in a systematic way, freeing up their focus to refine trading frameworks and higher cognitive functions that ultimately generate true alpha.

Some of SignalPlus's advanced trading functions include:
- **Stop Loss/Take Profit**
- **Iceberg Orders**
- **Balance Trade**
- **TWAP (Time-Weighted Average Price)**
- **DDH (Dynamic Delta Hedging)**

In a nutshell, the **SignalPlus platform dramatically lowers the barriers to entry**, and directly expands the group of participating subnet miners into the Bittensor network.  **SignalPlus is the critical link** that ensures the authenticity of trading data and provides traders with the tools they need to succeed.

Without such a platform, it would be impossible to securely validate trades or to provide the professional trading infrastructure to promote a high quality data environment. By removing unwanted technical complexities, SignalPlus allows traders to focus on what really matters — their strategy — while ensuring a robust environment with the requisite fairness and transparency that will best accentuate the power of the Bittensor network as we unlock a new chapter in network-learning models.

## Ranking Model Parameters
| FIELD  | DESCRIPTION  <p> [x] = Variable |RATIONALE|
| ------------- | ------------- | ------------- |
|  Ranking_Index |  = Exponentially Weighted Daily Returns / ABS [Min (-1%, Worst 7d Rolling Peak-to-Trough Drawdown) ]|Exponentially Weighted Daily Returns / Worst 7d Rolling drawdowns<p><p>Conceptually similar to a Calmar ratio, with some adjustments down to daily return weights in order to favour more recent performance.<p><p>A 7-day lead-in period is applied in order to begin tracking the drawdown measurement window from strategy inception. |
|  Exponentially Weighed Daily Returns |  Sum(Day_Weight * %_Return) / Sum (Day_Weights)  |Time weighted daily returns|
|  Day_Weight |  = EXP ^ ( - (Measurement_Day - Daily_Returns) / (Measurement_Day) )  |Exponential day weighting|
| Measurement_Day  |  Current Day - Inception_Day  |# of trading days elapsed since start|
|Inception_Date|1st day for user to enter contest|Starts tracking|
|Balance_DayStart|Wallet balance at start of day|Starting principal|
|Net_Inflows|Net change in inflows/outflows on the wallet|To account for any inflows during the day (outflows capped at 5% of starting balance)|
|$_Return|PNL made during the day (in USDT)|Actual PNL made|
|Balance_DayEnd|Balance_DayStart + Net_Inflows + $_Return|Total wallet balance at end of day|
|%_Return|$_Return / Avg(Balance_DayStart, Balance_DayStart+Net_Inflows)|Calculate daily % return adjusted (approx) by any daily Net_Inflows|
|Index_Value|Yesterday's Index Value * (1 + %_Return)|Day 1 Value = 100 <p><p> Keeps track of normalized portfolio value growth|
|Worst 7d Rolling Peak-to-Trough Drawdown|= MIN ( LOOKUP(MIN (Index_Value) / Max (Index_Value)), -1%)|Look for the worst peak-to-trough in capital drawdown over a 7d rolling period in % terms.<p><p>If user has 7d of consecutive gains, assign a floor value of -1% to avoid #DIV/0 error.|

## How to Use Efficient Frontier

### Miners Installation
- The miner will call the official public API to retrieve account-related metadata such as balance, equity, PnL, and drawdown, which are generated from the user's trading activities on the platform [t.signalplus.com](https://t.signalplus.com).
- This data is then passed to the validator for evaluating the strategy's performance.
- During transmission, asymmetric encryption is used to ensure the data remains untampered with, guaranteeing fairness and integrity.
- You can find detailed instructions on how to become a miner via the following link: <p> [how-to-join-the-greatest-tournament-of-crypto](./HowToJoin.md)


### Validation Installation
- The validator locally synchronizes the latest blockchain and retrieves all metadata uploaded by the corresponding miners.
- Initially, it verifies the authenticity of the data using asymmetric encryption.
- Once validated, the validator applies a Ranking Model to calculate the miner's weight and updates the results on the blockchain. This will determine the amount of airdrops the miner can receive in the next cycle.
- During this process, risk control checks are conducted, and if any fraudulent activity is detected, penalties may be imposed, including disqualification from the competition.


## FAQ
### What are the expected operations for a miner?
- You need to operate with a certain capital base, be actively trading, with a goal of maximizing your return against the lowest possible drawdowns via the [t.signalplus.com](https://t.signalplus.com) platform.
- Your scores will be judged based on a 'drawdown-adjusted' return (as defined above), with airdrop rewards based on your daily rankings.

### Do I need a GPU to run a miner or validator?
- No, you don't.

### Are there any additional rules we need to comply with for ranking considerations?
- Yes, please see an outline below for the current requirements. Additional modifications might be added overtime based on user feedback and project iterations.
- Users must comply with all of the following rules in order for their scores to be counted for daily airdrop rankings.
- Any parameter violation will lead to a zero score, and the daily return number will not be used in any of the model formula calculations.
- However, negative daily returns will always be counted in the user's score rankings, regardless of any condition, thus downside protection and risk management are key for long-term success.
  
|RULE DEFINITION|VARIABLE|RATIONALE|
|--|--|--|
|Minimum Maintenance Wallet Size|[USDT 10,000]|Rankings are based on normalized % balances to equalize different sizes, and a minimum threshold is applied in order to filter out excessively large % gains from marginal wallets.|
|24 Hour Period|[4pm HKT] cycles|For daily ranking measurements.|
|Minimum Daily Trading Volumes|Daily traded premium (or initial margin) must be >5% of the starting equity balance on the day.|Simulate Value-at-Risk requirement<p><p>Force users to trade at least some portion of their starting balance daily<p><p>Prevents users with a lucky big win early on to sit on their balance and not trade, but still ranking very high for the daily airdrops|
|Minimum Trading Volume Breaches|Users must have maintained the minimum trading quota for at least [8] out of the last 10 calendar days|Give users a small break if needed<p><p>Users with a big historical gains will see their daily ranking index get pulled down by the formula<p><p>Users who don't meet the threshold will have to restart trading until they meet the [8] out of 10 days record before their records can be recognized again|
|Withdrawal Limits|Net cashflow into the account must be positive (>0) each day in order for the day's return to quality for ranking calculations.  Ie. There cannot be net cash withdrawals.|Prevent users from getting a lucky big win early then cashing out, while leaving a small balance to keep airdrop farming.<p><p>Users are allowed to withdraw anytime, as long as they acknowledge that their results will not be counted.|
|Execution Through SignalPlus Platform|All order executions must be executed through SignalPlus's designated platform in order to be considered for airdrop rankings.|To ensure trading data authenticity and validation of the day's trading results.|
|Negative Daily Returns|Negative daily returns will always be included in ranking calculations.|To prevent users from trying to 'take out' their negative return days by purposely violating one of the prior parameters to inflate their negative drawdown measures.<p><p>Emphasize the importance of loss protection and risk management discipline.|

### Can you provide a numerical example?
- Please see the attached file.
  
  [Ranking Model Example](./RankingModelExample.xlsx)

## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2024 Opentensor Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
