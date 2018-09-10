# Hostmasternode Sentinel

### Follow the installation steps below or the official Hostmasternode sentinel guide: 


Sentinel is an all-powerful toolset for hostmasternode.

Sentinel is an autonomous agent for persisting, processing and automating hostmasternode V12.1 governance objects and tasks, and for expanded functions in upcoming releases.

Sentinel is implemented as a Python application that binds to a local version 12.1 hostmasternoded instance on each hostmasternode V12.1 Masternode.

This guide covers installing Sentinel onto an existing 12.1 Masternode in Ubuntu 14.04 / 16.04.

Alternatively to the guide on the hostmasternode website, you can also follow the simple step-by-step guide below. Before you proceed it is advisable to restart your masternode with -reindex to make sure you start off the steps fresh and fully synced - it will save you time later on in the guide as well.


    cd .hostmasternodecore   // Adjust according to your root hostmasternode directory path

    ./hostmasternode-cli stop

    rm mncache.dat

    rm mnpayments.dat

    ./hostmasternoded -daemon -reindex



## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv
    $ sudo apt-get install virtualenv -y

Make sure the local hostmasternode daemon running is at least version 12.1 (120100)

    $ hostmasternode-cli getinfo | grep version

### 2. Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/hmn-dev/sentinel.git && cd sentinel
    $ virtualenv ./venv
    $ ./venv/bin/pip install -r requirements.txt


### 3. Configure & Test Your Configuration

Open sentinel.conf - Run the following command in linux:

    $ nano sentinel.conf

Uncomment the #hostmasternode_conf line, at the top of the file, then adjust the path to your Masternode’s hostmasternode.conf. Save the file then close it.

    hostmasternode_conf=/path/to/hostmasternode.conf

Now run:

    $ venv/bin/python bin/sentinel.py

You should see: “hostmasternoded not synced with network! Awaiting full sync before running Sentinel.”
This is exactly what we want to see at this stage.

If the wallet has been resynched alreaedy, you will see no output which is what you want to see and it means you can skip the next sync step.


## 4. Check That Your hostmasternode Wallet is Synced 

Go back into your root hostmasternode directory, then check the status of your sync:

    cd .. 
    ./hostmasternode-cli mnsync status


This is what you’re waiting to see:

AssetId 999, all trues, one false, and a FINISHED. Keep issuing ./hostmasternode-cli mnsync status until it looks like this:


    {
    “AssetID”: 999,
    “AssetName”: “MASTERNODE_SYNC_FINISHED”,
    “Attempt”: 0,
    “IsBlockchainSynced”: true,
    “IsMasternodeListSynced”: true,
    “IsWinnersListSynced”: true,
    “IsSynced”: true,
    “IsFailed”: false
    }
    
At this point, your remote masternode is synchronized and chatting with the network but is not accepted as a masternode because it hasn’t been introduced to the network by your collateral.


## 5. Start Your Masternode

 Go back to your local wallet, open the debug console, and run these commands to start your masternode (LABEL is the name you used for your MN in the masternode.conf):

    walletpassphrase <YOURPASSPHRASE> 120 (only if you have a wallet password)
    masternode start-alias <LABEL>


## 6. Test Your Sentinel

You’re needed back in Sentinel directory:

    cd sentinel

Run:

    venv/bin/python bin/sentinel.py

It should return no output if everything is working correctly. This is how you know it’s working, and your masternode and sentinel setup is properly configured.

## 7. Create Your Sentinel Crontab Entry

Run:

    crontab -e

Add the following line below to the end of the file:

    * * * * * cd /home/YOURUSERNAME/.hostmasternodecore/sentinel && ./venv/bin/python bin/sentinel.py 2>&1 >> sentinel-cron.log
    

Make sure you:

1) Change USERNAME to your username.
2) Hit enter to create another line at the end after this line, or the file will not work.

Save and exit.

## 8. All Done On Sentinel. Finally Check Your Masternode

Go back into your hostmasternode root directory:

    cd ..

Run:

    ./hostmasternode-cli masternode debug

You should see the message “Masternode successfully started.”. If you have followed all the steps outlined in the guide accurately and achieved this result - this is it, you've made it. Congratulations!

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

