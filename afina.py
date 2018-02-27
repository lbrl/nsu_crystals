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
    if os.path.isfile(Finname[:-4] + 'dat'):
        finname = Finname[:-4] + 'dat'
        fin = open(finname)
        nbin = 0
        for line in fin:
            if line[0] == '0' and nbin > 1:
                break
            nbin += 1
        fin.close()
        print 'Automatically set the number of bins to {}.'.format(nbin)
    else:
        nbin = 100
    titles = {}
    # fin = open('info_2017-12-20.txt')
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
        lin[1] = lin[1][:-3] + 'root'
        titles[lin[1]] = '#splitline{' + lin[2] + ', #tau_{exp} = %s min,' % lin[3]
        titles[lin[1]] += '}{thr = %s LSB' % lin[4]
        titles[lin[1]] += ', {}'.format(lin[5])
        titles[lin[1]] += ', U_{PMT} = %s V' % lin[6]
        if lin[8] == 'yes':
            titles[lin[1]] += ', RC'
        titles[lin[1]] += '}'
    fin.close()
    #
    Fin = r.TFile(Finname)
    t = Fin.Get('t')
    names = ['amp_vs_integ', 'amp', 'integ']
    # t has tail, mi, ma and integ. The length of any initial histogram is 48.
    t.Draw('1:1>>h(300,0,1,300,0,1)', '', 'goff')
    rngs = [[0, 200, -20e3, 5e3], [0, 2000, 0, 200], [-20e3, 5e3, 0, 2000],
            [0, 200], [0, 2e3], [-20e3, 5e3]]
    hdefs = []
    nb, nbx, nby = 200, 200, 200
    for i in xrange(6):
        rng = rngs[i]
        if len(rng) == 2:
            hdefs.append( '({}, {}, {})'.format(nb, rng[0], rng[1]) )
        else:
            hdefs.append( '({}, {}, {}, {}, {}, {})'.format(nbx, rng[0],
                rng[1], nby, rng[2], rng[3]) )
    t.Draw('integ-%d*(head+tail)/2 : (tail+head)/2 - mi >> h1%s' % (nbin, hdefs[0]), '', 'off')
    t.Draw('(tail+head)/2 - mi : (t1-t0)*4 >> h2%s' % hdefs[1], '', 'off')
    t.Draw('(t1-t0)*4 : integ-%d*(head+tail)/2 >> h3%s' % (nbin, hdefs[2]), '', 'off')
    t.Draw('(tail+head)/2 - mi >> h4%s' % hdefs[3], '', 'off')
    t.Draw('(t1-t0)*4 >> h5%s' % hdefs[4], '', 'off')
    t.Draw('integ-%d*(head+tail)/2 >> h6%s' % (nbin, hdefs[5]), '', 'off')
    h1 = r.gDirectory.Get('h1')
    h2 = r.gDirectory.Get('h2')
    h3 = r.gDirectory.Get('h3')
    h4 = r.gDirectory.Get('h4')
    h5 = r.gDirectory.Get('h5')
    h6 = r.gDirectory.Get('h6')
    hh = [h1, h2, h3, h4, h5, h6]
    for h in hh:
        if Finname in titles:
            h.SetTitle( titles[Finname] )
        else:
            h.SetTitle(Finname[:-10].replace('_', ' '))
        h.SetLineWidth(2)
    h1.GetXaxis().SetTitle('Amplitude, ADC')
    h1.GetYaxis().SetTitle('"Integrated amplitude", ADC #times 4 ns')
    h2.GetXaxis().SetTitle(r'100% to 20% amplitude fall time, ns')
    h2.GetYaxis().SetTitle('Amplitude, ADC')
    h3.GetYaxis().SetTitle(r'100% to 20% amplitude fall time, ns')
    h3.GetXaxis().SetTitle('"Integrated amplitude", ADC #times 4 ns')
    h4.GetXaxis().SetTitle('Amplitude, ADC')
    h4.GetYaxis().SetTitle('Entries')
    h5.GetXaxis().SetTitle(r'100% to 20% amplitude fall time, ns')
    h5.GetYaxis().SetTitle('Entries')
    h6.GetXaxis().SetTitle('"Integrated amplitude", ADC #times 4 ns')
    h6.GetYaxis().SetTitle('Entries')
    c1 = r.TCanvas('c1', 'c1', 3*600, 2*600)
    c1.Divide(3, 2)
    for i in xrange(len(hh)):
        c1.cd(i+1)
        hh[i].SetNdivisions(506)
        hh[i].GetYaxis().SetTitleOffset(1.5)
        if i in [3, 4, 5]:
            r.gPad.SetLogy()
            hh[i].Draw()
        elif i in [0, 1, 2]:
            r.gPad.SetLogz()
            hh[i].Draw('colz')
            # hh[i].Draw()
    c1.Update()
    c1.SaveAs('{}.png'.format(Finname[:-5]))
    '''
    c = [r.TCanvas('c{}'.format(x), 'c{}'.format(x), 600, 600) for x in xrange(3)]
    c[0].SetLogz()
    c[1].SetLogy()
    c[2].SetLogy()
    for ic, cc in enumerate(c):
        cc.cd()
        hh[ic].Draw('colz')
        cc.Update()
        cc.SaveAs('img/{}_{}.png'.format(Finname[:-5], names[ic]))
    '''
    if not '-b' in sys.argv:
        raw_input('Press ENTER to continue, please.')
    Fin.Close()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
