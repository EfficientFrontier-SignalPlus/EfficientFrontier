
# Running Subnet on Testnet

This tutorial explains how to become a validator on the testnet.

**DANGER**
- Do not expose your private keys.
- Only use your testnet wallet.
- Do not reuse the password of your mainnet wallet.
- Make sure your incentive mechanism is resistant to abuse. 

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

## 3. (Optional) Get faucet tokens
   
Faucet is disabled on the testnet. Hence, if you don't have sufficient faucet tokens, ask the [Bittensor Discord community](https://discord.com/channels/799672011265015819/830068283314929684) for faucet tokens.


## 4. Register keys

This step registers your subnet validator keys to the subnet, giving it a slots on the subnet.

register your validator key to the subnet:

```bash
btcli subnet register --netuid 232 --subtensor.network test --wallet.name validator --wallet.hotkey default
```

## 5. Check that your keys have been registered

This step returns information about your registered keys.

Check that your validator key has been registered:

```bash
btcli wallet overview --wallet.name validator --subtensor.network test
```

The above command will display the below:

```bash
Subnet: 232

  COLDKEY          HOTKEY           UID      ACTIVE   STAKE…         RANK        TRUST    CONSENSUS    INCENTIVE    DIVIDENDS   EMISSION(…       VTRUST   VPE…   UPDAT…   AXON                 HOTKEY_SS58
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  validator       default          0          True   1000.…      0.00000      0.00000      0.00000      0.00000      0.53239          935      1.00000    *        111   1.1.1.1:8123   5F9KGGQuZa
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  3                3                3                 τ1000…      0.00000      0.00000      0.00000      0.00000      0.53239         ρ935      1.00000    
```


## 6. Run subnet validator

It is recommended to use Python 3.11, as it helps avoid various issues and saves time.

Run the subnet validator:

```bash
pip install -r requirements.txt
```

```bash
python run_validator.py --netuid 232 --subtensor.chain_endpoint test --wallet.name validator --wallet.hotkey default --axon.port 9100 --logging.debug --env test
```

You will see the below terminal output:

```bash
>> 2024-10-22 11:45:02.206 |       INFO       | bittensor:loggingmachine.py:442 | Running validator Axon([::], 9100, 5F9KGGQuZms7Ph4QfwZp9pMWYaEcpJZc9kbom2ZYk, stopped, ['Synapse']) on network: test with netuid: 232

```


## 7. Get emissions flowing
Register a validator on the root subnet and boost to set weights for your subnet. This is a necessary step to ensure that the subnet is able to receive emmissions.

Register to the root network using the `btcli`:

```bash
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint test
```

Boost your subnet on the root subnet

```bash
btcli root boost --netuid 232 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint test
```

## 8. Stopping your nodes

To stop your nodes, press CTRL + C in the terminal where the nodes are running.
