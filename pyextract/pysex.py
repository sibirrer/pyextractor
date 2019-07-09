"""
Author: Nicolas Cantale - n.cantale@gmail.com

Small module wrapping sextractor. The idea is to have a single function taking an image and returning a sextractor cataloge.

Dependencies:
 - sextractor (mandatory)
 - astroasciidata (mandatory)
 - numpy (optional, needed for the array support)
 - pyfits (optional, needed for the array support)


Usage:

	import pysex
	cat = pysex.run(myimage, params=['X_IMAGE', 'Y_IMAGE', 'FLUX_APER'], conf_args={'PHOT_APERTURES':5})
	print cat['FLUX_APER']

"""
from __future__ import print_function
import os, shutil
import astropy.io.fits as pyfits

dir_name = os.path.dirname(__file__)
default_sex = os.path.join(dir_name,'default.sex')
default_conv = os.path.join(dir_name,'gauss_2.0_5x5.conv')
default_nnw = os.path.join(dir_name,'default.nnw')


def _check_files(conf_file, conf_args, verbose=True):
    # dir_name = os.path.dirname(__file__)
    if conf_file is None:
        shutil.copyfile(default_sex, '.pysex.sex')  # changed .
        conf_file = '.pysex.sex'  # changed .
    if not 'FILTER_NAME' in conf_args or not os.path.isfile(conf_args['FILTER_NAME']):
        if verbose:
            print('No filter file found, using default filter')
        shutil.copyfile(default_conv, '.pysex.conv')  # changed .
        conf_args['FILTER_NAME'] = '.pysex.conv'  # changed .
    if not 'STARNNW_NAME' in conf_args or not os.path.isfile(conf_args['STARNNW_NAME']):
        if verbose:
            print('No NNW file found, using default NNW config')
        shutil.copyfile(default_nnw, '.pysex.nnw')  # changed .
        conf_args['STARNNW_NAME'] = '.pysex.nnw'  # changed .
    return conf_file, conf_args


def _setup(conf_file, params):
    try:
        shutil.copy(conf_file, '.pysex.sex')  # changed .
    except:
        pass #already created in _check_files

    f=open('.pysex.param', 'w') # changed .
    print('\n'.join(params), file=f)
    #print>>f, '\n'.join(params)
    f.close()


def _setup_img(image, name):
    if not type(image) == type(''):
        pyfits.writeto(name, image)


def _get_cmd(img, img_ref, conf_args):
    ref = img_ref if img_ref is not None else ''
    # cmd = ' '.join(['sex', ref, img, '-c .pysex.sex '])  # changed .
    cmd = ' '.join(['sex', ref, '-c .pysex.sex '])  # changed .
    args = [''.join(['-', key, ' ', str(conf_args[key])]) for key in conf_args]
    cmd += ' '.join(args)
    return cmd


def _read_cat(path = '.pysex.cat'):  # changed .
    cat = pyfits.open(path)
    return cat


def _cleanup():
    """
    delets all files with .pysex.
    """
    files = [f for f in os.listdir('.') if '.pysex.' in f]
    for f in files:
        os.remove(f)


def run(image='', imageref='', params=[], conf_file=None, conf_args={}, keepcat=True, rerun=True, catdir=None):
    """
    Run sextractor on the given image with the given parameters.

    image: filename or numpy array
    imageref: optional, filename or numpy array of the the reference image
    params: list of catalog's parameters to be returned
    conf_file: optional, filename of the sextractor catalog to be used
    conf_args: optional, list of arguments to be passed to sextractor (overrides the parameters in the conf file)


    keepcat : should I keep the sex cats ?
    rerun : should I rerun sex even when a cat is already present ?
    catdir : where to put the cats (default : next to the images)


    Returns an asciidata catalog containing the sextractor output

    Usage exemple:
        import pysex
        cat = pysex.run(myimage, params=['X_IMAGE', 'Y_IMAGE', 'FLUX_APER'], conf_args={'PHOT_APERTURES':5})
        print cat['FLUX_APER']
    """

    # Preparing permanent catalog filepath :
    if type(image) == type(''):
        (imgdir, filename) = os.path.split(image)
        (common, ext) = os.path.splitext(filename)
        catfilename = common + ".pysexcat" # Does not get deleted by _cleanup(), even if in working dir !
        if keepcat:
            if catdir:
                if not os.path.isdir(catdir):
                    os.makedirs(catdir)
                    #raise RuntimeError("Directory \"%s\" for pysex cats does not exist. Make it !" % (catdir))
        if catdir:
            catpath = os.path.join(catdir, catfilename)
        else:
            catpath = os.path.join(imgdir, catfilename)

    # Checking if permanent catalog already exists :
    if rerun == False and type(image) == type(''):
        if os.path.exists(catpath):
            cat = _read_cat(catpath)
            return cat

    # Otherwise we run sex :
    conf_args['CATALOG_NAME'] = '.pysex.cat'  # changed .
    conf_args['PARAMETERS_NAME'] = '.pysex.param'  # changed .
    if 'VERBOSE_TYPE' in conf_args and conf_args['VERBOSE_TYPE']=='QUIET':
        verbose = False
    else: verbose = True
    _cleanup()
    if not type(image) == type(''):
        # import pyfits
        im_name = '.pysex.fits'
        pyfits.writeto(im_name, image.transpose())
    else: im_name = image
    if not type(imageref) == type(''):
        # import pyfits
        imref_name = '.pysex.ref.fits'
        pyfits.writeto(imref_name, imageref.transpose())
    else: imref_name = imageref
    conf_file, conf_args = _check_files(conf_file, conf_args, verbose)
    _setup(conf_file, params)
    cmd = _get_cmd(im_name, imref_name, conf_args)
    print("sextractor command:", cmd)
    res = os.system(cmd)
    if res:
        print("Error during sextractor execution!")
        _cleanup()
        return

    # Keeping the cat at a permanent location :
    if keepcat and type(image) == type(''):
        shutil.copy('.pysex.cat', catpath)

    # Returning the cat :
    cat = _read_cat()
    #_cleanup()
    return cat
