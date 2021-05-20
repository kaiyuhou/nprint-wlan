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
    
    os.system(f'{nprint} -w -P {pcap} -W {NPT_DIR}{npt_fliename}')
    return f'{NPT_DIR}{npt_fliename}'


def load_npt(npt_file, n_vendors=10):
    nprint_wlan = pd.read_csv(npt_file, index_col=0)
    print('nPrint_wlan: Number of Packets: {0}, Features per packet: {1}'.format(nprint_wlan.shape[0], nprint_wlan.shape[1]))

    nprint_wlan_with_src_mac = nprint_wlan.loc[nprint_wlan.index != 'None']
    # nprint_wlan_with_src_mac = nprint_wlan_with_src_mac.loc[nprint_wlan_with_src_mac.index != '00:00:00:00:00:00']
    print('nprint_wlan_with_src_mac: Number of Packets: {0}, Features per packet: {1}'.format(nprint_wlan_with_src_mac.shape[0], nprint_wlan_with_src_mac.shape[1]))

    num_sample_packets = nprint_wlan_with_src_mac.shape[0]

    unique_macs = set([row.name for _, row in nprint_wlan_with_src_mac.iterrows()])
    # vendor_counter = Counter([get_vendor(row.name) for _, row in nprint_wlan_with_src_mac.iterrows()])
    print(f'Unique MACs: {len(unique_macs)}')
    
    vendor_counter = Counter([get_vendor(mac) for mac in unique_macs])
    
    top_vendors = get_top_vendors(nprint_wlan, n_vendors)
    print(f'Top {n_vendors} vendors: {top_vendors}')
    print(f'{vendor_counter.most_common(n_vendors)}')

    samples, labels, samples_without_vendor = label_packets(nprint_wlan_with_src_mac, top_vendors)
    print(f'Samples: {len(samples)}, Features: {len(samples[0])}')
    print(f'Samples without Vendor label: {len(samples_without_vendor)}')

    return samples, labels, vendor_counter, top_vendors


def build_classifier(samples, labels, sample_name='train'):
    X_train, X_test, y_train, y_test = train_test_split(samples, labels)
    clf = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=2, random_state=0)
    clf.fit(X_train, y_train) 
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)

    # Draw
    mpl_use('agg')
    create_dir_if_not_exist(IMG_DIR)

    plot_confusion_matrix(clf, X_test, y_test, xticks_rotation='vertical')
    plt.tight_layout()
    plt.savefig(f'{IMG_DIR}train-{sample_name}.png', transparent=False, facecolor='white')
    print(f'save file: {IMG_DIR}train-{sample_name}.png')

    plot_confusion_matrix(clf, X_test, y_test, xticks_rotation='vertical', normalize='pred', include_values=False)
    plt.tight_layout()
    plt.savefig(f'{IMG_DIR}train-{sample_name}-normalize.png', transparent=False, facecolor='white')
    print(f'save file: {IMG_DIR}train-{sample_name}-normalize.png')

    return clf


def apply_classifier(clf, test_samples, test_labels, vendor_counter, top_vendors, sample_name='test'):

    y_test_pred = clf.predict(test_samples)
    report = classification_report(test_labels, y_test_pred)
    print(report)

    # Draw
    mpl_use('agg')
    create_dir_if_not_exist(IMG_DIR)

    test_labels = [vendor for vendor, _ in vendor_counter.most_common() if vendor in top_vendors]
    test_labels.append('Others')

    plot_confusion_matrix(clf, test_samples, y_test_pred, labels=test_labels, xticks_rotation='vertical')
    plt.tight_layout()
    plt.savefig(f'{IMG_DIR}test-{sample_name}.png', transparent=False, facecolor='white')
    print(f'save file: {IMG_DIR}test-{sample_name}.png')

    plot_confusion_matrix(clf, test_samples, y_test_pred, labels=test_labels, xticks_rotation='vertical', normalize='pred', include_values=False)
    plt.tight_layout()
    plt.savefig(f'{IMG_DIR}test-{sample_name}-normalize.png', transparent=False, facecolor='white')
    print(f'save file: {IMG_DIR}test-{sample_name}-normalize.png')


def train(train_file, nprint, n_vendors=10):
    print('**Train**')
    npt_file = execute_nprint(train_file, nprint)
    samples, labels, _, top_vendors = load_npt(npt_file, n_vendors)

    print('Training...')
    return build_classifier(samples, labels, sample_name=os.path.split(npt_file)[1]), top_vendors


def test(clf, top_vendors, test_file, nprint, n_vendors=10):
    print('**Test**')
    npt_file = execute_nprint(test_file, nprint)
    samples, labels, vendor_counter, _ = load_npt(npt_file, n_vendors)

    apply_classifier(clf, samples, labels, vendor_counter, top_vendors, sample_name=os.path.split(npt_file)[1])


def uzip_cp(file_path):
    path, name = os.path.split(file_path)
    os.system(f'cp {file_path} .')
    os.system(f'gzip -dk {name}')
    return name[:-3]


if __name__ == '__main__':
    _, train_file, test_file, nprint, n_vendors = sys.argv
    n_vendors = int(n_vendors)

    if train_file.endswith('.gz'):
        train_file = uzip_cp(train_file)

    if test_file.endswith('.gz'):
        test_file = uzip_cp(test_file)

    clf, top_vendors = train(train_file, nprint, n_vendors=n_vendors)
    test(clf, top_vendors, test_file, nprint, n_vendors=n_vendors)