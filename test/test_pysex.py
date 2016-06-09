
# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

"""
Tests for `pyextract` module.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest
import os
import astropy.io.fits as pyfits
from pyextract import pysex


class TestPyextract(object):

    def setup(self):
        #prepare unit test. Load data etc
        test_dir = os.path.join(os.path.dirname(__file__ ))
        filename = os.path.join(test_dir,'test_data','test1.fits')
        image = pyfits.open(filename)
        self.image_data = image[0].data
        print("setting up " + __name__)
        pass

    def test_run(self):
        params = ['NUMBER', 'FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_BEST', 'FLUXERR_BEST', 'MAG_BEST', 'MAGERR_BEST',
                  'FLUX_RADIUS', 'CLASS_STAR', 'A_IMAGE', 'B_IMAGE', 'THETA_IMAGE', 'ELLIPTICITY']

        HDUFile = pysex.run(image=self.image_data, params=params, conf_file=None, conf_args={}, keepcat=False,
                        rerun=False, catdir=None)
        list = HDUFile[1].data[0][0]
        mean = 0
        for line in list:
            line = line.strip()
            line = line.split()
            if line[0] == 'SEXBKGND' or line[0] == 'SEXBKGND=':
                mean = float(line[1])
        assert mean == 1.419248461723

    def teardown(self):
        #tidy up
        print("tearing down " + __name__)
        pass

if __name__ == '__main__':
    pytest.main()