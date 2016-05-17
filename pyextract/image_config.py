__author__ = 'sibirrer'

import numpy as np

import lenstronomy.DataAnalysis.Sextractor_wrapper.pysex as pysex



def config_arguments(exp_time, CCD_gain):
    """

    :return: config arguments for sextractor
    """
    conf_args={}
    conf_args['GAIN'] = exp_time * CCD_gain
    return conf_args

def get_source_cat(image, conf_args):
    """
    returns the sextractor catalogue of a given image
    :param system:
    :param image_name:
    :return:
    """
    nx, ny = image.shape
    borders = int(nx/10)
    image_no_borders = image[borders:ny-borders,borders:nx-borders]

    params = ['NUMBER', 'FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_BEST', 'FLUXERR_BEST', 'MAG_BEST', 'MAGERR_BEST',
                'FLUX_RADIUS', 'CLASS_STAR', 'A_IMAGE', 'B_IMAGE', 'THETA_IMAGE', 'ELLIPTICITY', 'X_WORLD', 'Y_WORLD']
    HDUFile = pysex.run(image_no_borders, params=params, conf_file=None, conf_args=conf_args, keepcat=False, rerun=False, catdir=None)
    return HDUFile, image_no_borders


