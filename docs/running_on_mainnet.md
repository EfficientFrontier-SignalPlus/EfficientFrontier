
# Running Subnet on Mainnet

### Please note, this is very important: currently, direct execution of the miner program is $\color{red}{\textsf{Not}}$ supported.
### Please $\color{red}{\textsf{Do Not}}$ spend TAO to register as a miner at this time. Refer to [HowToJoin](Introduction/HowToJoin.md) to become our miner.
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


## 5. Run subnet validator

It is recommended to use Python 3.11, as it helps avoid various issues and saves time.

Run the subnet validator:

```bash
pip install -r requirements.txt
```

```bash
python run_validator.py --netuid 53 --subtensor.chain_endpoint finney --wallet.name validator --wallet.hotkey default --axon.port 9100 --logging.debug --env prod
```

You will see the below terminal output:

```bash
>> 2024-10-22 11:45:02.206 |       INFO       | bittensor:loggingmachine.py:442 | Running validator Axon([::], 9100, 5F9KGGQuZms7Ph4QfwZp9pMWYaEcpJZc9kbom2ZYk, stopped, ['Synapse']) on network: finney with netuid: 53

```


## 6. Get emissions flowing
Register a validator on the root subnet and boost to set weights for your subnet. This is a necessary step to ensure that the subnet is able to receive emissions.

Register to the root network using the `btcli`:

```bash
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint finney
```

Boost your subnet on the root subnet

```bash
btcli root boost --netuid 53 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint finney
```

## 7. Stopping your nodes

To stop your nodes, press CTRL + C in the terminal where the nodes are running.
