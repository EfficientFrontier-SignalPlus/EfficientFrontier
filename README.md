<div align="center">
  
# **EfficientFrontier-SignalPlus**
  
</div>

**Quick Overview of [Strategy Ranking Rules](docs/Introduction/RankingRulesEN.md)**


## Introduction
   > Efficient Frontier: a set of optimal portfolios that offer the highest expected return for a defined level of risk, or the lowest risk for a given level of expected return.

   Efficient Frontier is a project initiated by SignalPlus and Bittensor, designed to identify the optimal risk-weighted trading strategies through the integration of decentralized machine learning networks and live trading data. This project will leverage Bittensor's innovative blockchain-powered AI learning protocol to advance our journey in discovering optimal crypto trading strategies. Furthermore, through the use of SignalPlus' market-leading platform, every day users will now be equipped with a professional trading toolkit that is available right on their desktop, enabling true democratised access and empowering the open-access initiative.

### What is Bittensor?
   Bittensor is a decentralized protocol specifically designed for machine learning (ML) and artificial intelligence (AI). It offers a unique marketplace for both users and providers of ML algorithms, utilizing a decentralized network to facilitate the exchange of these resources. More than just a marketplace for ML models, Bittensor provides a platform for training these models in a censorship-resistant environment, challenging the resource-intensive monopolies of tech giants.

   At the core of Bittensor is its distinctive architecture, which combines specialized subnets for AI tasks, a blockchain for decentralized operations, and an API for seamless integration. This structure is considered crucial in positioning Bittensor as the leading network for AI services, catering to both individuals and corporations, with its native token, TAO, serving as the medium for transactions. As the network evolves, its goal is to accelerate the growth of AI by making sophisticated ML models accessible to a broader audience.

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



## Ranking Rules Overview
   After creating a strategy, there will be a standardized process for calculating daily scores, determining rankings, and distributing rewards based on recent performance and adherence to specific conditions.

   The project goal is to reward strategies that can produce consistently positive returns with minimal drawdowns, while applying penalties on certain conditions that may indicate trading violations or insufficient participation. 

### ⏳ Observation Period
   - 14-Day Lead-in: New strategies must undergo a 14-day observation period before they are eligible to be ranked for rewards. No scores will be calculated during this observation period.

### 📈 Scoring Process
   - Daily Scoring: At the end of the observation period, the strategy’s score will be calculated at the end of each trading day. A day is defined from 8:00 AM UTC to the next 8:00 AM UTC.
   - Scoring Formula: The final score is derived as a ratio of the strategy's exponentially daily weighted returns against a rolling maximum peak-to-trough drawdown over the past 14 days.

### 💯 Daily Score Calculations

   - Daily Score Formula: 

   $$\text{Strategy Score = } \frac {\text{Weighted Daily \% Returns}}{\text{Maximum Decayed Drawdown}} \cdot 10$$
   

1. Daily Return Calculation

    At the end of each trading day, the platform will calculate the daily strategy PNL (in USDT). The return is derived by comparing the account balance at the start and end of the day, and adjusting for any deposits or withdrawals that might have occurred during the session.

       $_Return  = Balance_DayEnd - Balance_DayStart - Net_Inflows

2. Daily % Return Calculation

    The Daily % Return is calculated by dividing the Daily Return by the average balance for the day, adjusting for any deposits or withdrawals. This represents the daily percentage return of the strategy.

      $$\text{Return\\%=}\frac {\text{Return\\$}}{\text{Avg}(\text{Balance Day End},\text{Balance Day Start+Net Inflows})}$$

   The daily return will be limited to twice the maximum return on the inception date, and to the maximum return on all other days. The maximum return is calculated as follows:

$$\text{Max Return}\=\min\left(\frac{1\\%\cdot(\text{Balance Day Start}-10000)}{40000}+8\\%,12\\%\right)+|14\text{Days Drawdown}|$$
   
$$\text{Daily \\% Return}=\begin{cases}\min(\text{Return\\%}, 2\cdot\text{Max Return}), & \text{at inception date}\\\min(\text{Return\\%}, \text{Max Return}), & \text{other dates}\\ \end{cases}$$

  
3. Weighted Historical Performance

    The performance of the strategy is exponentially weighted, giving more importance to recent results but still recognizing one's historical performance. Strategies that have performed better in the near term will receive higher scores.

    $$\text{Weighted Daily Returns = } \frac{\text{CrossProduct(DayWeights * Daily \\% Returns)}}{\text{Sum(DayWeights)}}$$

    $$\text{DayWeight} = \exp(-\lambda \cdot \text{Return Decay} \cdot \text {(Measurement Date - Inception Date}))$$

    $$\text{Return Decay =} \exp(\frac{\ln(20\\%)}{\text{14 Days}})$$

4. Trading Frequency (λ)

    In order to accommodate different trading styles, we will give users the option to define their trading styles to be 'Frequent', 'Base', or 'Infrequent'.  The trading style selection will affect the decay weights of daily returns, with faster decay giving more weights to recent returns (high frequency), and slower decay favouring historical performance.

    where λ = decay parameter
      - λ = 2, faster decay
      - λ  = 1, base decay
      - λ = 0.5, slower decay
   
   (Note: This feature is currently disabled while we fine-tune our parameters to the appropriate decay factors)
    
   ![](docs/Introduction/pics/ExponentialDecayWithDifferentλValues.png)

    To discourage inappropriate mis-use of the formula weights, there will be a 30-day cooldown period before a frequency change can be made again.

5. Maximum Decayed Drawdown

    The system measures the largest peak-to-trough capital drawdown incurred by the strategy on a life-to-date basis, but adjusted by a separate Drawdown Decay factor. A smaller drawdown will have a considerable impact on the final ranking score, rewarding strategies with strong risk discipline that can avoid taking large losses over time.

    $$\text{Min(Today's \\% Drawdown, (}\frac{\text{Trough Index Value}}{\text{Peak Index Value}}-1) \cdot \text{Drawdown Decay, -1\\%)}$$

    $$\text{Drawdown Decay =} \exp(\frac{\ln(80\\%)}{\text{14 Days}})$$

6. Excessive Risk Taking Adjustment

   Strategies that are excessively risk-levered with high margin usage will be subject to a score adjustment. Specifically, strategies that employ margin usage (as defined by the relevant CEX) in excess of 50% will see a 20% discount on their final score, and excesses of >80% will suffer a 50% discount.
   
   <div style="center;">
      <img src="docs/Introduction/pics/ExcessiveRiskTakingAdjustment.png" alt="Excessive Risk Taking">
   </div>

7. AUM / Wallet Size Adjustment Factor

    For strategies achieving the same performance (i.e., return rate、drawdown), a higher AUM / wallet size will result in a higher score. This reflects the exponentially higher difficulty of managing larger portfolios, rewarding high-AUM strategies with an added scaling factor.
    
   
   $$\text {AUM Adjustment Factor = Strategy Score} \cdot \text {(1+} \ln( \sqrt{ \max{(1, \frac{\text{AUM}}{100,000}})}$$

   <div style="display: flex; flex-direction: row; align-items: center;">
     <img src="docs/Introduction/pics/AUMWalletSizeAdjustmentFactor1.png" alt="1" style="max-width: 50%; margin-right: 10px;">
     <img src="docs/Introduction/pics/AUMWalletSizeAdjustmentFactor2.png" alt="2" style="max-width: 50%;">
   </div>
   
8. Scoring Cap vs AUM (Wallet Size)

    Each mining strategy will have a daily scoring cap to prevent small wallet balances from having an outsized ranking impact from limited trade samples vs the entire subnet population.

    $$\text {Scoring Cap = } \frac {\text{7 day Average Equity Balance}}{10,000}$$

    eg. a 25k equity balance will have a scoring cap of 2.5

### ❌ Scoring Violations (i.e. Zero Score Conditions)

  If a strategy violates any of the following rules, it will be penalized with a zero score against that day's positive return, while retaining the full impact of a negative drawdown.

  Said in another way, miners who are subject to trading violations will have a maximum daily score of 0 with a downside score equal to its negative daily performance.

1. Minimum Balance Requirement
   
    The wallet must have a minimum balance of at least 10,000 USDT at both the start and end of the trading day.  A trading day is defined with a start time of 8:00 AM UTC.

    Rationale: to require enough 'skin in the game' to encourage authentic trading while minimizing outsized % gains from marginal wallets.

2. Minimum Trading Volume Requirement
   
   - To qualify for the daily scoring, each miner must meet a minimum adjusted trading volume of 5,000 USDT on each rolling 7-day trading period.  The adjusted volume is defined as follows across the different instruments:

       The purpose of this provision is to encourage trading; actions that solely focus on inflating volume without legitimate transactions may be subject to penalties.

       Options:
       - Adjusted Volume = Option Premium
   
       Futures and Spot:
       - Adjusted Volume = Order Quantity × Order Price × Coin Ratio
       - Coin Ratio: Varies by cryptocurrency and is based on the initial margin rates. For specific Coin Ratios, please refer to the [OKX Margin Rates](https://www.okx.com/trade-market/position/swap) page.
  
       Rationale: to require some minimal level of participation from traders to suggest that the trading strategy is still relevant.

   - (Starting from 2024-12-30 08:00:01 UTC) Increase the requirement for Daily Trading Volume. The daily trade volume must be ten times the average USD value of TAO claimed by the strategy over the past 7 days. If this volume is not reached, that day is considered ineligible. (Trade volume will no longer include any option trades with a markPrice > 0.2 index)
   - Regular and active trading is required during the initial 14d observation period as a preparatory measure.  Accounts will be invalidated during that period if they fail to meet the minimum trading requirements, or if suspicious activities were noted during that time.
   
3. Net Withdrawal Restriction
   
    Strategies cannot have net withdrawal of capital (ie. Outflows > Inflows) on each trading day in order to qualify for return calculations. Any net withdrawals of capital from a strategy will result in a zero-score calculation against any positive performance on the day.

    Rationale: users who 'cash out' of the strategies should no longer be eligible for rewards.

4. Whitelisted Assets Requirement

    Only transactions involving the following whitelisted assets and their derivatives (spot, futures, options) are eligible for scoring: 
     - BTC, ETH, SOL
     - USDT, USDC
     - ADA, AVAX, BCH, BNB, DAI, DOGE, DOT, LEO, LINK, SHIB, SUI, TAO, TON, TRX, XRP.
     - Stablecoin pairs will no longer be included in the trade volume statistics (e.g., USTC/USDT).

     Trades involving any non-whitelisted assets or derivatives will result in a zero score for the day.

5. Platform Execution
   
    All eligible trades must be executed on the SignalPlus platform on all opening and closing trades; however, liquidation or settlement trades are exempted as they are automatically handled by exchanges.
  
    Rationale: to ensure the sanctity of the trading data as all trades must be authentic and commercially driven

6. Off-Market and Wash-Trading Prevention
   
    Any trades flagged as off-market or wash trades will result in a zero score for the strategy on that day, regardless of any positive performance.

    **We strongly condemn all malicious score-boosting activities.** The system automatically detects violations using the following three rules.
   
    Any suspicious activities identified through automated checks or manual reviews will result in penalties. A manual zero-score penalty may be applied.

   Rule 1 - Price Deviation Checks: For option instruments specifically, a significant deviation between the transaction price and the mark price will result in a penalty.

   Rule 2 - Unusual Trading Patterns: Engaging in irregular trading behaviors, such as using duplicate or identical portfolios to claim multiple airdrops for the same strategy, artificially inflating trading volume, or conducting circular trades between accounts, etc.,  will result in disqualification from receiving airdrop rewards. These activities will also trigger automated alerts for further investigation.

   Rule 3 - Profit Threshold Violations: Any potential wash trading or malicious wash trading aimed at generating profits will be detected and prohibited, including activities such as disproportionately exploiting price spreads, etc.
  
   Rule 4: Please refrain from using inappropriate or offensive words as strategy names or trader handles, as such actions will result in penalties.

   Rule 5: We do not encourage trading options with a mark price below 4 basis points, as it may be deemed a wash trade.


7. Note: Situations that may result in account suspension:

   - When equity becomes 0
   - When the API fails
   - Cheating    
   
### 🏅 Rankings and Rewards Distribution
- Daily Rankings: Strategies are ranked based on their daily scores from the scoring formula, with higher scores leading to better sequential rankings.
- Reward Distribution: 
  - Please Note: The rewards for each day will be distributed **after the conclusion of the next trading day.**
  - Rewards are distributed based on the strategy’s score relative to the **Top-50 performing strategies** on the day.
  - The formula for calculating rewards is:
    
       $$\text{Strategy Reward = } \frac {\text{Strategy's Daily Score (Capped)}}{\text{Total Daily Score of Top-50 Strategies}} \cdot \text{Total Daily Reward Pool}$$ 

### Model Parameters

| FIELD  | DESCRIPTION  <p> [x] = Variable |RATIONALE|
| ------------- | ------------- | ------------- |
|  Ranking_Index <p> (Strategy Score)|  $$\max{(\frac {\text{Weighted Daily \\% Returns}}{\text{Maximum Decayed Drawdown}} \cdot 10, \text{ Scoring Cap)}}$$|**Weighted Daily Returns / Maximum Drawdown Applied Against a Decay Factor (with a Scoring Cap)**<p>Conceptually similar to a Calmar ratio, with some adjustments down to daily return weights in order to favour more recent performance.|
|  Weighed Daily Returns |  $$\frac{\text{CrossProduct(DayWeights * Daily \\% Returns)}}{\text{Sum(DayWeights)}}$$  |Time weighted daily returns|
|DayWeight|$$\exp(-\lambda \cdot \text{Return Decay} \cdot \text {(Measurement Date - Inception Date}))$$|Day-weighting against a 14d / 20% half-life|
|Trading Frequency (λ)|$$\text{\\{2,1,0\\}}$$<p>(Note: TBD, not yet implemented in current version)|Adjusts pace of return decay to trader frequency.<p>Faster decay = more weight on more recent performance|
|Return Decay|$$\exp(\frac{\ln(20\\%)}{\text{14 Days}})$$|14-day half-life exponential decay to 20% on historical returns|
|Daily % Returns|$$\frac {\text{Daily \\$ Return}}{\text{Avg(Balance\\_DayStart, Balance\\_DayStart + Net\\_Inflows)}}$$|Calculate daily % return adjusted (approx) by any daily Net_Inflows|
|Maximum Decayed Drawdown|$$\text{Min(Today's \\% Drawdown, (}\frac{\text{Trough Index Value}}{\text{Peak Index Value}}-1) \cdot \text{Drawdown Decay, -1\\%)}$$|Iteratively search for the worst peak-to-trough in % decayed drawdown on a life-to-date basis, with a floor value of -1%|
|Drawdown Decay|$$\exp(\frac{\ln(80\\%)}{\text{14 Days}})$$|14-day half-life exponential decay to 80% on LTD peak-to-trough % drawdowns|
|Index Value|$$\text{Yesterday's Index Value} \cdot \text{(1 + Daily \\% Return)}$$|Day 1 Value = 100<p>Keeps track of normalized portfolio value growth|
|Scoring Cap|$$\frac {\text{7 day Average Equity Balance}}{10,000}$$|Strategy Score is capped by the 7d average balance of the equity (wallet) balance to prevent small wallet and trade samples to have an outsized ranking impact vs the entire subnet population. |
|AUM Adjustment Factor|$$\text{Strategy Score} \cdot \text {(1+} \ln( \sqrt{ \max{(1, \frac{\text{AUM}}{100,000}})}$$|Scaling factor to adjustment for rising difficulties of managing a larger AUM portfolio.|
|Measurement_Day|Current day|Current day|
|Inception_Date|1st day for users to enter contest|Starts tracking|
|Balance_DayStart|Wallet balance at start of day|Starting principal|
|Net_Inflows|Net change in inflows on the wallet|To account for any inflows during the day|
|Daily $ Return|PNL made during the day (in USDT)|Actual PNL made|
|Balance_DayEnd| $$Sum(Balance\\_DayStart, Net\\_Inflows, Daily \\$ Return)$$ | Total wallet balance at end of day|
|LTD|$$\le90\text{ days}$$|Life to date records of the strategy.  Currently capped at 90 days.|

## SignalPlus's Role

Built by an exceptional team of former banking and technology veterans, the SignalPlus terminal is the industry's leading derivative trading and options risk management platform that is well recognized by crypto's largest players and exchanges.  With a professional suite of automated and industrial-grade tools available to all, we now have a ready-made platform and built-in measurement tools to power the Bittensor network.

Never has such a level-playing field been offered to the every day user, allowing each trader to focus on refining their craft rather than being inhibited by inadequate tools.  As a result, traders are empowered to develop better trading frameworks rather than risk tools, ensuring better trading results and quality data to train the machine learning processes.

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

## Product Roadmap

### December 2024 Roadmap

While SN53 is barely 1 month old, we are proud to report that there are over 60 miners with total positive trading profits surpassing US$2M since inception.  We are grateful for the tremendous support of our community and are hard at work to deliver a series of important milestone upgrades in the weeks ahead.

![](docs/Introduction/pics/roadmap1.png)

1. Continuous Refinement and Optimization of the Scoring System

    We are continuously refining the scoring system to strike the right balance between ranking fairness and commercially meaningful results to highlight the best strategies.  With approximately 3 weeks of factual data, we are able to fine-tune our scoring rules to achieve even more representative rankings of our best miners.


2. Support for Running Miners Locally

    As one of the most requested features from our community, miners will be able to run their operations locally without relying on SignalPlus’s cloud server by next week.
In the interim, miners' emissions can be viewed directly via the direct link within their personalized page to confirm their direct emissions via taostats.

![](docs/Introduction/pics/roadmap2.png)

![](docs/Introduction/pics/roadmap3.png)

3. Providing Validators with Open API Access

    By mid-December, we will be able to offer validators with an open API and subscription service to get access to real-time trading data. This will allow validators to verify strategies' effectiveness with various monetization possibilities, including early forms of 'copy trading'.
(Dev Note: We prioritized the development of local mining support ahead of the API feature based on community feedback.  Please bear with us!)


4. Enabling Validators to Perform All Calculations Independently

    Currently, just 1-5% of calculations are still conducted 'centrally' as our scoring system is still being updated. We didn't want the hassle of troubling every individual validator to update their code manually on every minor model tweak, and this is strictly meant to be a temporary measure as we converge on our finalized model based on community feedback.
We expect to fully decentralize this process (100% of calculations delegated) once the scoring model has stabilized, with an ETA of ~2-3 weeks into mid/late December.

    Outside of this, we are brainstorming a number of interesting and innovative mechanisms to evolve our subnet to be even more aligned with Bittensor's network prediction initiatives.  Thank you for your continued support and we are extremely excited about our journey ahead!

## User Guide

### Miners Installation
- The miner will call the official public API to retrieve account-related metadata such as balance, equity, PnL, and drawdown, which are generated from the user's trading activities on the platform [t.signalplus.com](https://t.signalplus.com).
- This data is then passed to the validator for evaluating the strategy's performance.
- During transmission, asymmetric encryption is used to ensure the data remains untampered with, guaranteeing fairness and integrity.
- You can find detailed instructions on how to become a miner via the following link: <p> [how-to-join-the-greatest-tournament-of-crypto](docs/Introduction/HowToJoin.md)
- [running_miner_on_mainnet](docs/running_on_mainnet.md)

### Validator Installation
- The validator locally synchronizes the latest blockchain and retrieves all metadata uploaded by the corresponding miners.
- Initially, it verifies the authenticity of the data using asymmetric encryption.
- Once validated, the validator applies a Ranking Model to calculate the miner's weight and updates the results on the blockchain. This will determine the amount of rewards the miner can receive in the next cycle.
- During this process, risk control checks are conducted, and if any fraudulent activity is detected, penalties may be imposed, including disqualification from the competition.
- [running_validator_on_testnet](docs/running_on_testnet.md)
- [running_validator_on_mainnet](docs/running_on_mainnet.md)

### Real Time Transaction API
SignalPlus will provide a special API which will allow validators to obtain real-time transaction data for each miner.  This will allow the necessary validators to:
1. Verify the validity of all transactions in real time;
2. Monitor the miners' trading activities
3. Design certain products and services based on observed trading signals

Please note, this API will only be made available to validators and not all users to encourage more active network participation.


### Registration Fee for Miners

Each miner wishing to participate in the Efficient Frontier subnet is required to pay a registration fee of **1 TAO** to Bittensor. This amount may be adjusted in the future based on the subnet's weight. Recognizing that our target miners are primarily quantitative trading teams and individuals engaged in complex derivatives trading—who may not be familiar with Bittensor or DeFi and might not have their own crypto wallets—we aim to simplify the onboarding process.

To lower the entry barrier, **SignalPlus** will directly charge miners in **USDT** and exchange it for TAO on their behalf, handling the cross-chain payment to Bittensor. Considering the current value of TAO is approximately **\$450 USD**, plus additional cross-chain and network gas fees, we plan to initially charge a registration fee of **\$500 USD**. This fee will be periodically adjusted to reflect any significant changes in TAO's market price.

If there is any surplus from the registration fee after paying the required 1 TAO to Bittensor, we will allocate the excess USDT as follows:

1. **Price Fluctuation Buffer**: To hedge against potential losses if TAO's price increases sharply before we can adjust the USDT registration fee.
2. **Community Rewards**: Periodically distribute the surplus directly to participating miners as rewards.

By handling the TAO acquisition and payment process, we aim to make it as easy as possible for miners to join the subnet, allowing them to focus on what they do best—trading.


## FAQ

### What are the expected operations for a miner?
- You need to operate with a certain capital base, be actively trading, with a goal of maximizing your return against the lowest possible drawdowns via the [t.signalplus.com](https://t.signalplus.com) platform.
- Your scores will be judged based on a 'drawdown-adjusted' return (as defined above), with rewards based on your daily rankings.

### Do I need a GPU to run a miner or validator?
- No, you don't.
  
### Does SignalPlus require KYC?
- KYC is not required for our new SignalPlus users as our platform does not touch customer assets at any point of the workflow; however, the platform requires a CEX account API to work as most derivative trading liquidity is still aggregated on CEX.
  
### What CEXs does SignalPlus support?
- Binace, Bybit, Deribit, OKX, and Paradigm (for OTC trading).
### Why did we make the decision to support CEX venues over pure DEX protocols?
- Capital markets are exceptionally efficient creatures and trading evaluation and prediction are only as good as the scope and quality of the incoming data.
- Current CEX venues still have many orders of magnitudes above DEX venues, and will likely continue to stay this way in the foreseeable future given the 1) liquidity breadth & depth, 2) execution slippage, 3) product complexity and availability, 4) number of participants, and 5) readily availability of advanced spread and 'portfolio-based' trading strategies and 6) trading data authenticity that are simply much superior in the CEX venues.
- As such, in order to ensure that we have the best available data quality, authenticity (minimize wash trades), and trading signals, we needed to make this full anonymity compromise where users will need to have a CEX account in order to participate.
![](docs/Introduction/pics/DexCexSpotVolumeRatio.jpeg)

### Will users have access to any trading signals from the results output?
- Yes, SignalPlus will be able to provide users with an API for receiving trading signals post production release.
### How will we ensure the sanctity and authenticity of input data?
- SignalPlus is a leading institutional platform that's recognized by the industry's largest exchanges as the go-to 3rd party benchmark platform for crypto derivatives trading, especially for crypto options.
- All data that will be used for ranking purposes come from real, factual trades that take place on CEX with actual monetary exchanges.  Outside of our own platform validation, these are trades that have been recognized and recorded on exchanges' own platforms.
- All transactions are recorded in chronological order in real-time, with PNL results calculated at the end of the mark as per any professional trading outfit.
- Finally, we have built-in further 'sanity checks' to ensure that even the exchange trades are 'commercially-authentic' versus the current market levels and current traded prices.

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
