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


def main(Finnames = ['ZnLiWO4_CrCl_2017-12-01_000_wf_0.root']):
    r.gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
    filelist = []
    for Finname in Finnames:
        if Finname == '-b':
            print 'Batch mode.'
            continue
        if len(Finname) < 6:
            continue
        if Finname[-5:] == '.root':
            filelist.append(Finname)
    n = len(filelist)
    if n > 1:
        print '{} files will be processed.'.format(n)
    elif n == 1:
        print 'One file will be processed.'
    elif n == 0:
        print 'There are not files.'
    else:
        print 'Something stranges just happend.'
    for Finname in filelist:
        submain(Finname)


def submain(Finname = 'ZnLiWO4_CrCl_2017-12-01_000_wf_0.root'):
    ########################################
    titles = {}
    # fin = open('info_2017-12-20.txt')
    if '2018-01-10' in Finname:
        fin = open('../2018-01-10/info_2018-01-10.txt')
    else:
        fin = open('info_2017-12-27.txt')
    for line in fin:
        if len(line) > 0:
            if line[0] == '#':
                print line
                continue
        line = line.replace('Zn,', 'Zn')
        line = line.replace('Pb,', 'Pb')
        line = line.replace('"', '')
        # print line
        lin = line.rstrip('\n').split(',')
        # print lin
        # lin[1] = lin[1][:-3] + '.root'
        lin[1] = lin[1] + '.root'
        titles[lin[1]] = '#splitline{' + lin[2] + ', #tau_{exp} = %s min,' % lin[3]
        titles[lin[1]] += '}{thr = %s LSB' % lin[4]
        if lin[5] != '-':
            titles[lin[1]] += ', {}'.format(lin[5])
        titles[lin[1]] += ', U_{PMT} = %s V' % lin[6]
        if lin[8] == 'yes':
            titles[lin[1]] += ', RC'
        titles[lin[1]] += '}'
    fin.close()
    '''
    for key in titles:
        print key, '\t\t', titles[key]
    '''
    ########################################
    Fin = r.TFile(Finname)
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.SetLogz()
    # t.Draw("tau:a>>h(100,0,300,100,4000)", "tau>0 && tau<4000 && amp<0 && amp>-50", "goff")
    t.Draw("tau:a>>h(50,0,300,50,4000)", "tau>0 && tau<4000 && amp<0 && amp>-50", "goff")
    h = r.gDirectory.Get('h')
    h.Draw('colz')
    # h.SetTitle(titles[Finname])
    h.SetTitle(titles[Finname.replace('_show', '').split('/')[-1]])
    h.GetYaxis().CenterTitle()
    h.GetYaxis().SetTitle('Long #tau, ns')
    h.GetYaxis().SetTitleOffset(1.5)
    h.GetXaxis().SetTitle('Amplitude, ADC channel')
    c1.Update()
    raw_input('Press ENTER to continue, please.')
    if 'save' in sys.argv:
        c1.SaveAs(Finname[:-5]+'.png')
    Fin.Close()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
