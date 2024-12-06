
# Running Subnet on Mainnet

### Note: We $\color{green}{\textsf{encourage}}$ you to independently deploy a fully operational miner on your own server at no cost, as long as you ensure that your miner program remains continuously online.
### If you prefer not to manage a miner on Bittensor yourself, or are unsure how to do so, you have the option to use the SignalPlus-provided cloud hosting service. While this cloud hosting is currently free of charge, please be aware that it may become a paid service in the future.

---

## This tutorial explains how to become a validator on the mainnet.

**DANGER**
- Do not expose your private keys.
- Only use your mainnet wallet.
- Do not reuse the password of your mainnet wallet.

## 1. Prerequisites

Please follow the tutorial in the links to install bittensor environment. 

https://docs.bittensor.com/getting-started/installation

https://docs.bittensor.com/getting-started/install-btcli

https://docs.bittensor.com/getting-started/install-wallet-sdk

https://docs.bittensor.com/getting-started/wallets


## 2. Create wallets 
**If you already have a wallet, please skip this step.**

This step creates local coldkey and hotkey pairs for your validator.

The validator will be registered to the subnet. This ensures that the validator can run the respective validator scripts.


Create a coldkey and hotkey for your validator wallet:

```bash
btcli wallet new_coldkey --wallet.name validator
```

and

```bash
btcli wallet new_hotkey --wallet.name validator --wallet.hotkey default
```

## 3. Register keys

This step registers your subnet validator keys to the subnet, giving it a slots on the subnet.

register your validator key to the subnet:

```bash
btcli subnet register --netuid 53 --subtensor.network finney --wallet.name validator --wallet.hotkey default
```

## 4. Check that your keys have been registered

This step returns information about your registered keys.

Check that your validator key has been registered:

```bash
btcli wallet overview --wallet.name validator --subtensor.network finney
```

The above command will display the below:

```bash
Subnet: 53

  COLDKEY          HOTKEY           UID      ACTIVE   STAKE…         RANK        TRUST    CONSENSUS    INCENTIVE    DIVIDENDS   EMISSION(…       VTRUST   VPE…   UPDAT…   AXON                 HOTKEY_SS58
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  validator       default          0          True   1000.…      0.00000      0.00000      0.00000      0.00000      0.53239          935      1.00000    *        111   1.1.1.1:8123   5F9KGGQuZa
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  3                3                3                 τ1000…      0.00000      0.00000      0.00000      0.00000      0.53239         ρ935      1.00000    
```


## 5. Run subnet miner

It is recommended to use Python 3.11, as it helps avoid various issues and saves time.

```bash
pip install -r requirements.txt
```

You can obtain the **strategy_secret** from https://t.signalplus.com/mining

Please keep your strategy_secret **secure** and avoid any leaks.
```bash
python run_miner.py --netuid 53 --subtensor.chain_endpoint finney --wallet.name miner --wallet.hotkey default --axon.port 9100 --logging.debug --env prod --neuron.strategy_secret strategy_secret
```

You will see the below terminal output:

```bash
>> 2024-10-22 11:45:02.206 |       INFO       | bittensor:loggingmachine.py:442 | Running validator Axon([::], 9100, 5F9KGGQuZms7Ph4QfwZp9pMWYaEcpJZc9kbom2ZYk, stopped, ['Synapse']) on network: finney with netuid: 53

```

## 6. Run subnet validator

It is recommended to use Python 3.11, as it helps avoid various issues and saves time.

```bash
pip install -r requirements.txt
```

```bash
python run_validator.py --netuid 53 --subtensor.chain_endpoint finney --wallet.name validator --wallet.hotkey default --axon.port 9100 --logging.debug --env prod
```

You will see the below terminal output:

```bash
| INFO     | _sdk.template.base.neuron:__init__:113 - Running neuron on subnet: 232 with uid 2 using network: wss://test.finney.opentensor.ai:443/
```


## 7. Get emissions flowing
Register a validator on the root subnet and boost to set weights for your subnet. This is a necessary step to ensure that the subnet is able to receive emissions.

Register to the root network using the `btcli`:

```bash
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint finney
```

Boost your subnet on the root subnet

```bash
btcli root boost --netuid 53 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint finney
```

## 8. Stopping your nodes

To stop your nodes, press CTRL + C in the terminal where the nodes are running.
