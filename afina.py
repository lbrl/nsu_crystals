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
    for Finname in Finnames:
        if Finname == '-b':
            continue
        if len(Finname) < 6:
            continue
        if Finname[-5:] == '.root':
            submain(Finname)


def submain(Finname = 'ZnLiWO4_CrCl_2017-12-01_000_wf_0.root'):
    Fin = r.TFile(Finname)
    t = Fin.Get('t')
    names = ['amp_vs_integ', 'amp', 'integ']
    # t has tail, mi, ma and integ. The length of any initial histogram is 48.
    t.Draw('1:1>>h(100,0,1,100,0,1)', '', 'goff')
    t.Draw('tail-mi:48*tail-integ>>h1()', '48*tail-integ > -500', 'goff')
    t.Draw('tail-mi>>h2(300)', '48*tail-integ > -500', 'goff')
    t.Draw('48*tail-integ>>h3(300)', '48*tail-integ > -500', 'goff')
    h1 = r.gDirectory.Get('h1')
    h2 = r.gDirectory.Get('h2')
    h3 = r.gDirectory.Get('h3')
    hh = [h1, h2, h3]
    for h in hh:
        h.SetTitle(Finname[:-10].replace('_', ' '))
        h.SetLineWidth(2)
    h1.GetXaxis().SetTitle('Integrated  amplitude,  ADC  #times  4 ns')
    h1.GetYaxis().SetTitle('Amplitude,  ADC')
    h2.GetXaxis().SetTitle('Amplitude,  ADC')
    h2.GetYaxis().SetTitle('Entries')
    h3.GetXaxis().SetTitle('Integrated  amplitude,  ADC  #times  4 ns')
    h3.GetYaxis().SetTitle('Entries')
    c1 = r.TCanvas('c1', 'c1', 3*600, 600)
    c1.Divide(3, 1)
    for i in xrange(3):
        c1.cd(i+1)
        if i > 0:
            r.gPad.SetLogy()
            hh[i].Draw()
        else:
            r.gPad.SetLogz()
            hh[i].Draw('colz')
    c1.Update()
    c1.SaveAs('img/{}.png'.format(Finname[:-5]))
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
    raw_input('Press ENTER to continue, please.')
    Fin.Close()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
