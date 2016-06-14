__author__ = 'sibirrer'


import pyextract.pysex as pysex



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
    params = ['NUMBER', 'FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_BEST', 'FLUXERR_BEST', 'MAG_BEST', 'MAGERR_BEST',
                'FLUX_RADIUS', 'CLASS_STAR', 'A_IMAGE', 'B_IMAGE', 'THETA_IMAGE', 'ELLIPTICITY', 'X_WORLD', 'Y_WORLD']
    HDUFile = pysex.run(image, params=params, conf_file=None, conf_args=conf_args, keepcat=False, rerun=False, catdir=None)
    return HDUFile, image


