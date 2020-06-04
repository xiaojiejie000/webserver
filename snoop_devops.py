import re
import sys
import time
import requests
import threading
import subprocess

pools_ttl_60 = ['xmr.pool.minergate.com', 'xmr.poolto.be', 'github.com', 'zoom.us']

pools_ttl_300 = ['youtube.com',
                 'xmr.crypto-pool.fr',
                 'ca01.supportxmr.com',
                 'fr05.supportxmr.com',
                 'fr06.supportxmr.com',
                 'fr04.supportxmr.com',
                 'fr01.supportxmr.com',
                 'fr02.supportxmr.com',
                 'fr03.supportxmr.com',
                 'xmr-eu1.nanopool.org',
                 'xmr-eu2.nanopool.org',
                 'xmr-us-east1.nanopool.org',
                 'xmr-us-west1.nanopool.org',
                 'xmr-asia1.nanopool.org',
                 'xmr-jp1.nanopool.org',
                 'xmr-au1.nanopool.org',
                 'mro.pool.minergate.com',
                 'aeon.pool.minergate.com',
                 'gulf.moneroocean.stream',
                 'jp.moneroocean.stream',
                 'de.moneroocean.stream',
                 'us.moneroocean.stream',
                 'fr.moneroocean.stream',
                 'pool.minexmr.com',
                 'fr.minexmr.com',
                 'de.minexmr.com',
                 'ca.minexmr.com',
                 'sg.minexmr.com',
                 'mine.xmr.mypool.online',
                 'pool.xmr.pt',
                 'pool.miners.pro',
                 'xmr.miners.pro',
                 'ratchetmining.com',
                 'xmr-eu.dwarfpool.com',
                 'xmr-usa.dwarfpool.com',
                 'monerohash.com',
                 'support.ipbc.io',
                 'mining.bit.tube',
                 'asia.mining.bit.tube',
                 'us.mining.bit.tube',
                 'us-east.cryptonight-hub.miningpoolhub.com',
                 'europe.cryptonight-hub.miningpoolhub.com',
                 'asia.cryptonight-hub.miningpoolhub.com',
                 'commutator.bid',
                 'mmmoneropool.com',
                 'multipooler.com',
                 'pool.xmr.semipool.com',
                 'hongkong.hub.semipool.com',
                 'paris.hub.semipool.com',
                 'losangeles.hub.semipool.com']

pools_ttl_600 = ['www.bs444.co', 'cryptmonero.com', 'sh0.xmr.skypool.org', 'reimu.website', 'wikipedia.org']

pools_ttl_1800 = ['monero.crypto-pool.fr',
                  'pool.supportxmr.com',
                  'de02.supportxmr.com',
                  'de01.supportxmr.com',
                  'phx01.supportxmr.com',
                  'de03.supportxmr.com',
                  'phx02.supportxmr.com',
                  'sg1.supportxmr.com',
                  'nyc04.supportxmr.com',
                  'nyc01.supportxmr.com',
                  'nyc05.supportxmr.com',
                  'nyc02.supportxmr.com',
                  'nyc03.supportxmr.com',
                  'fin01.supportxmr.com',
                  'sg2.supportxmr.com',
                  'sg3.supportxmr.com',
                  'mine.xmrpool.net',
                  'vegas-1.xmrpool.net',
                  'frankfurt-1.xmrpool.net',
                  'vegas-backup.xmrpool.net',
                  'xmr-eu.suprnova.cc',
                  'xmr.suprnova.cc',
                  'xmr.bohemianpool.com',
                  'xmr-cz01.bohemianpool.com',
                  'xmr.miner.center']

class Crawl_thread(threading.Thread):
    def __init__(self, o_ttl, platform):
        threading.Thread.__init__(self)
        # base info
        self.o_ttl = o_ttl
        # target url
        self.platform = platform

    def run(self):
        self.snoop_ttl()

    def resolve_snoop_results(self, pool):
        r_ttl = ""
        dnsserver = ""
        cmd = "dig a +recurse +ttlid " + pool
        results = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
        keyword = pool + "."
        try:
            for i in range(1, len(results)):
                last_line = results[i-1].decode().strip()
                line = results[i].decode().strip()
                if keyword in line and ";; ANSWER SECTION:" in last_line:
                    result = re.sub('\s+', ' ', line)
                    r_ttl = result.split(" ")[1]
                if ";; SERVER:" in line:
                    dnsserver = line.split(" ")[2]
        except:
            pass

        return r_ttl, dnsserver

    def log_dns_info(self, r_ttl, dnsserver, pool):
        dnsreportURL = "http://54.191.75.188/dnsreport"
        dnsreportDict = {'platform': self.platform, 'pool': pool, 'ttl': r_ttl, 'dnsserver': dnsserver}

        r = requests.get(dnsreportURL, params = dnsreportDict)

    def snoop_ttl(self):
        # pools that ttls is 300
        if self.o_ttl == 300:
            for pool in pools_ttl_300:
                for i in range(10):
                    print ("[INFO] pool is ", pool)
                    r_ttl, dnsserver = self.resolve_snoop_results(pool)
                    # TODO: send to server
                    self.log_dns_info(r_ttl, dnsserver, pool)

            # sleep 2*300 = 600
            time.sleep(2*305)

        # pools that ttls is 600
        elif self.o_ttl == 600:
            for pool in pools_ttl_600:
                for i in range(10):
                    print ("[INFO] pool is ", pool)
                    r_ttl, dnsserver = self.resolve_snoop_results(pool)
                    # TODO: send to server
                    self.log_dns_info(r_ttl, dnsserver, pool)

            # sleep 2*600 = 1200
            time.sleep(2*605)

        # pools that ttls is 60
        elif self.o_ttl == 60:
            for pool in pools_ttl_60:
                for i in range(10):
                    print ("[INFO] pool is ", pool)
                    r_ttl, dnsserver = self.resolve_snoop_results(pool)
                    # TODO: send to server
                    self.log_dns_info(r_ttl, dnsserver, pool)

            time.sleep(2*65)

        # pools that ttls is 60
        elif self.o_ttl == 1800:
            for pool in pools_ttl_1800:
                for i in range(10):
                    print ("[INFO] pool is ", pool)
                    r_ttl, dnsserver = self.resolve_snoop_results(pool)
                    # TODO: send to server
                    self.log_dns_info(r_ttl, dnsserver, pool)

            time.sleep(2*1805)

def snoop_devops_ttl():
    ttl_timelist = [60, 300, 600, 1800]
    analyze_thread = {}

    for ttl in ttl_timelist:
        thread = Crawl_thread(ttl, sys.argv[1])
        thread.start()
        analyze_thread[ttl] = thread

    # maintaining 4 hours
    for i in range(480):
        print ("[INFO] Start to snoop...", i)
        time.sleep(30)
        for t in ttl_timelist:
            if analyze_thread[t].is_alive():
                continue
            else:
                thread = Crawl_thread(t, sys.argv[1])
                thread.start()
                analyze_thread[t] = thread

if __name__ == '__main__':
    snoop_devops_ttl()
