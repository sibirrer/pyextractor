__author__ = 'sibirrer'


import pyextract.pysex as pysex



def config_arguments(exp_time, CCD_gain):
    """

    :return: config arguments for sextractor
    """
    conf_args={}
    conf_args['GAIN'] = exp_time * CCD_gain
    return conf_args


def get_source_cat(imageref='', params=[], conf_file=None, conf_args={}, keepcat=True, rerun=True, catdir=None):
    """
    returns the sextractor catalogue of a given image
    :param system:
    :param image_name:
    :return:
    """

    if len(params) < 1:
        params = ['NUMBER', 'FLAGS', 'X_IMAGE', 'Y_IMAGE', 'FLUX_BEST', 'FLUXERR_BEST', 'MAG_BEST', 'MAGERR_BEST',
                'FLUX_RADIUS', 'CLASS_STAR', 'A_IMAGE', 'B_IMAGE', 'THETA_IMAGE', 'ELLIPTICITY', 'X_WORLD', 'Y_WORLD']
    HDUFile = pysex.run(imageref=imageref, params=params, conf_file=conf_file, conf_args=conf_args, keepcat=keepcat, rerun=rerun, catdir=catdir)
    return HDUFile


