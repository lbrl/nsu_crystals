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


def main(Finname):
    print sys.argv
    if '-b' in sys.argv:
        isBatch = True
    else:
        isBatch = False
    Fin = r.TFile(Finname)
    r.gStyle.SetOptStat(0)
    t = Fin.Get('t')
    i = 0
    # c1 = r.TCanvas('c1', 'c1', 400, 400)
    c1 = r.TCanvas('c1', 'c1', 1600, 800)
    line = r.TLine()
    lat = r.TLatex()
    lat.SetTextFont(12)
    lat.SetTextSize(.04)
    fexp = r.TF1('fexp', '[0]*exp(-(x-[1])/[2]) + [3]', 75*4, 400*4)
    fexp.SetParNames('A', r'x_{0}', '#tau', r'c_{0}')
    fexp.SetLineColor(r.kBlack)
    fexp.SetLineWidth(1)
    ##########################
    if isBatch:
        Fout = r.TFile('{}_show.root'.format(Finname[:-5]), 'recreate')
        tout = r.TTree('t', 't')
        a_t = array('f', [0])
        amp = array('f', [0])
        tau = array('f', [0])
        beg = array('f', [0])
        tout.Branch('a', a_t, 'a/F')
        tout.Branch('amp', amp, 'amp/F')
        tout.Branch('tau', tau, 'tau/F')
        tout.Branch('x0', beg, 'x0/F')
    ##########################
    for eve in t:
        if eve.nbin <= 0:
            continue
        # if (eve.head+eve.tail)/2.-eve.mi < 30:
        if isBatch:
            amp_thr = 10
        else:
            amp_thr = 30
        if eve.head-eve.mi < amp_thr:
            continue
        h = r.TH1I('h_{}'.format(i), '{} #{};time, ns; Voltage, ADC channel'.format(Finname, i),
                eve.nbin, 0, eve.nbin*4)
        for j, val in enumerate(eve.hi):
            h.SetBinContent(j+1, val)
        # h.Rebin(4)
        ##########################
        fexp.SetParameters(-10, 135, 400, 2117)
        fexp.FixParameter(3, eve.head)
        h.Fit(fexp, 'r', 'goff')
        ##########################
        if not isBatch:
            h.Draw()
            fexp.Draw('same')
            line.SetLineColor(r.kRed)
            line.SetLineWidth(1)
            # line.DrawLine(0, (eve.head+eve.tail)/2., eve.nbin, (eve.head+eve.tail)/2.)
            line.DrawLine(0, eve.head, eve.nbin*4, eve.head)
            line.SetLineColor(r.kMagenta)
            line.DrawLine(45*4, eve.mi, 75*4, eve.mi)
            line.DrawLine(55*4, eve.head, 55*4, eve.mi)
            ##########################
            lat.SetTextColor(r.kMagenta)
            lat.SetTextAngle(90)
            lat.DrawLatex(45*4, (eve.mi+eve.head)/2., '{:.1f}'.format(eve.head-eve.mi))
            ##########################
            lat.SetTextColor(r.kBlack)
            lat.SetTextAngle(0)
            lat.DrawLatex(100*4, eve.head - (eve.head-eve.mi)*.2, '#tau = {:.1f} ns'.format(fexp.GetParameter(2)))
        ##########################
        if isBatch:
            amp[0] = fexp.GetParameter(0)
            beg[0] = fexp.GetParameter(1)
            tau[0] = fexp.GetParameter(2)
            a_t[0] = eve.head-eve.mi
            tout.Fill()
        ##########################
        c1.Update()
        if not isBatch:
            inp = raw_input('Press ENTER to continue, please.')
            if inp in ['exit', 'q', 'quit']:
                break
        i += 1
    Fin.Close()
    tout.Write()
    Fout.Close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
