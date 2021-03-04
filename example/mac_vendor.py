vender_map = {} # key: mac, '00:00:01', value: ('short name', 'long name')
manuf_path = 'MAC_OUI/manuf.txt'

def load_vender_map():
    with open(manuf_path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith('#'): continue
            if '#' in line: line = line[:line.index('#')].strip()
            
            lsp = list(filter(None, line.split('\t')))
            assert 2 <= len(lsp) <= 3, f'{line}, {lsp}'

            if len(lsp) == 2: mac, sname, lname = lsp[0], lsp[1], lsp[1]
            else: mac, sname, lname = lsp

            if mac.endswith('/28'): # eample: 00:55:DA:00:00:00/28
                mac = mac[:10]
            
            vender_map[mac] = (sname, lname)


def get_vendor(mac: str):
    mac = mac.upper()
    if mac == 'None':
        return 'None'
    if mac[:8] in vender_map.keys():
        return vender_map[mac[:8]][0]
    if mac[:10] in vender_map.keys():
        return vender_map[map[:10]][0]
    return 'None'


def get_top_vendors(pd_sample, n: int=10):
    num_samples = pd_sample.shape[0]

    from collections import Counter
    c = Counter([get_vendor(row.name) for _, row in pd_sample.iterrows()])
    
    top_vendors = []
    for vendor, n_packets in c.most_common():
        if len(top_vendors) >= n: break
        if vendor == 'None': continue
        # if n_packets < num_samples / 100: break

        top_vendors.append(vendor)

    return top_vendors


load_vender_map()

