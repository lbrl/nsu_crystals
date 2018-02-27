#! /usr/bin/env python

import os
# from ROOT import *
import ROOT as r
# import numpy as np
# import re
import sys
# import glob
# import math as m
import datetime as dt
from array import array
# import subprocess as sp
# import time
# import numpy as np



def main(finnames = ['ZnLiWO4_CrCl_2017-12-01_000_wf_0.dat']):
    filelist = []
    for finname in finnames:
        if finname == '-b':
            print 'Batch mode.'
            continue
        if len(finname) < 5:
            continue
        if finname[-4:] == '.dat':
            filelist.append(finname)
    n = len(filelist)
    if n > 1:
        print '{} files will be processed.'.format(n)
    elif n == 1:
        print 'One file will be processed.'
    elif n == 0:
        print 'There are not files.'
    else:
        print 'Something stranges just happend.'
    for finname in filelist:
        submain(finname)


def submain(finname):
    fin = open(finname)
    Foutname = finname[:-3]+'root'
    print 'Input file :  ', finname
    print 'Output file : ', Foutname
    x = [0]
    # hmin = r.TH1I('hmin', '{} min'.format(finname), 2000, 1000, 3000)
    # hmax = r.TH1I('hmax', '{} max'.format(finname), 2000, 1000, 3000)
    # hmax.SetLineColor(r.kBlue)
    # hmin.SetLineColor(r.kRed)
    '''
    '''
    Fout = r.TFile(Foutname, 'recreate')
    t = r.TTree('t', finname)
    integ = array('i', [0])
    ma = array('i', [0])
    mi = array('i', [0])
    t0 = array('i', [0])
    t1 = array('i', [0])
    tail = array('f', [0])
    head = array('f', [0])
    nbin = array('i', [0])
    hi = array('i', [0]*5000)# 20 us
    t.Branch('ma', ma, 'ma/I')
    t.Branch('mi', mi, 'mi/I')
    t.Branch('t0', t0, 't0/I')
    t.Branch('t1', t1, 't1/I')
    t.Branch('integ', integ, 'integ/I')
    t.Branch('tail', tail, 'tail/F')
    t.Branch('head', head, 'head/F')
    t.Branch('nbin', nbin, 'nbin/I')
    t.Branch('hi', hi, 'hi[nbin]/I')
    timer = 0
    if '2017-12-01' in finname:
        nhead = 5
    else:
        nhead = 10
    for line in fin:
        lin = line.split()
        if lin[0] == '0':
            if timer % 5000 == 0:
                print '{:%Y-%m-%d %H:%M:%S} : '.format( dt.datetime.now() ) + '{} wafeforms have been processed.'.format(timer)
            timer += 1
            ma[0] = max(x)
            mi[0] = min(x)
            t0[0] = x.index(mi[0])
            t1[0] = t0[0]
            integ[0] = sum(x)
            head[0] = sum(x[:nhead])/float(nhead)
            tail[0] = sum(x[-10:])/10.
            level = mi[0] + .8 * (tail[0] - mi[0])
            lenx = len(x)
            while lenx > t1[0] and x[t1[0]] < level:
                t1[0] += 1
            # hmin.Fill(min(x))
            # hmax.Fill(max(x))
            x = [int(lin[1])]
            t.Fill()
            hi[0] = int(lin[1])
            nbin[0] = 1
        else:
            hi[nbin[0]] = int(lin[1])
            nbin[0] += 1
            x.append(int(lin[1]))

    Fout.Write()
    Fout.Close()
    '''
    c1 = r.TCanvas('c1', 'c1', 800, 800)
    c1.SetLogy()
    hmax.Draw()
    hmin.Draw('same')
    hmax.GetXaxis().SetRangeUser(2050, 2300)
    hmax.GetXaxis().SetTitle('Amplitude, ADC channel')
    hmax.GetYaxis().SetTitle('Entries')
    lat = r.TLatex()
    lat.SetTextColor(r.kRed)
    lat.DrawLatexNDC(.12, .85, 'Minimum amplitude')
    lat.SetTextColor(r.kBlue)
    lat.DrawLatexNDC(.12, .80, 'Maximum amplitude')
    raw_input()
    # c1.SaveAs('ZnLiWO4_CrCl_2017-12-01_000_wf_0_amplitude.png')
    c1.SaveAs(finname[:-3] + 'png')
    '''


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
