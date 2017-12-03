#! /usr/bin/env python

import os
# from ROOT import *
import ROOT as r
# import numpy as np
# import re
import sys
# import glob
# import math as m
# import datetime as dt
from array import array
# import subprocess as sp
# import time
# import numpy as np



def main(finnames = ['ZnLiWO4_CrCl_2017-12-01_000_wf_0.dat']):
    for finname in finnames:
        if finname == '-b':
            continue
        if len(finname) < 5:
            continue
        if finname[-4:] == '.dat':
            submain(finname)


def submain(finname):
    fin = open(finname)
    Foutname = finname[:-3]+'root'
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
    tail = array('f', [0])
    t.Branch('ma', ma, 'ma/I')
    t.Branch('mi', mi, 'mi/I')
    t.Branch('integ', integ, 'integ/I')
    t.Branch('tail', tail, 'tail/F')
    for line in fin:
        lin = line.split()
        if lin[0] == '0':
            ma[0] = max(x)
            mi[0] = min(x)
            integ[0] = sum(x)
            tail[0] = sum(x[-10:])/10.
            # hmin.Fill(min(x))
            # hmax.Fill(max(x))
            x = [int(lin[1])]
            t.Fill()
        else:
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
