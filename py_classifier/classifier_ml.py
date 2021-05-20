import sys
import os
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import use as mpl_use

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import plot_confusion_matrix

# Project files
from mac_vendor import *


NPT_DIR = 'npt/'
IMG_DIR = 'img/'

def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def execute_nprint(pcap, nprint):
    create_dir_if_not_exist(NPT_DIR)

    pcap_path, pcap_filename = os.path.split(pcap)
    npt_fliename = pcap_filename.replace('.pcap', '.npt')

    filter_cmd = f'tshark -r {pcap} -w {pcap_filename}_with_src_mac.pcap "wlan.ta"'
    print(filter_cmd)
    os.system(filter_cmd)

    pcap_filename = f'{pcap_filename}_with_src_mac.pcap'
    
    
    nprint_cmd = f'{nprint} -w -P {pcap_filename} -W {NPT_DIR}{npt_fliename}'
    print(nprint_cmd)
    os.system(nprint_cmd)



    nprint_wlan = pd.read_csv(f'{NPT_DIR}{npt_fliename}', index_col=0)

    top_10_vendors = get_top_vendors(nprint_wlan, 10)

    # create labels file
    labels_path = f'vendor-labels.txt'
    labels_map = {}

    for mac in nprint_wlan.index:
        if mac == 'None': labels_map[mac] = 'None'
        else:
            vendor = get_vendor(mac)
            if vendor in top_10_vendors: labels_map[mac] = vendor
            else: labels_map[mac] = 'Others'

    with open(labels_path, 'w') as f:
        f.write('item,label\n')
        for k, v in labels_map.items():
            f.write(f'{k},{v}\n')

    nml_cmd = f'nprintml --wlan --pcap-file {pcap_filename} --label-file {labels_path} --aggregator index'
    os.system(nml_cmd)



def train(train_file, nprint, n_vendors=10):
    print('**Train**')
    npt_file = execute_nprint(train_file, nprint)


def uzip_cp(file_path):
    path, name = os.path.split(file_path)
    os.system(f'cp {file_path} .')
    os.system(f'gzip -dk {name}')
    return name[:-3]


if __name__ == '__main__':
    _, train_file, nprint = sys.argv
    # n_vendors = int(n_vendors)

    if train_file.endswith('.gz'):
        train_file = uzip_cp(train_file)

    train(train_file, nprint)
