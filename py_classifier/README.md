# Auto python script for nprint-wlan classifier

## configure conda vitrual environment

```shell
# create conda venv nprint-wlan and install requrie packages
source config_conda_venv.sh 
```
## classifier with Random Forest

```shell
python3 classifier.py TRAIN_FILE_PATH.pcap TEST_FILE_PATH.pcap NPRINT_PATH
# example
python3 classifier.py ../example/wlan_2020_11_05_03.pcap ../example/wlan_2020_11_05_02.pcap ../nprint
```