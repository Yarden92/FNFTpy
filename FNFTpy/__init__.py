# import ctypes
from .auxilary import get_lib_path
from .fnft_kdvv_wrapper import kdvv_wrapper
from .fnft_nsep_wrapper import nsep_wrapper
from .fnft_nsev_wrapper import nsev_wrapper
from .typesdef import *

# get python ctypes object of libFNFT
libpath = get_lib_path()  # edit in auxilary.py
fnft_clib = ctypes.CDLL(libpath)


def kdvv(u, tvec, m=100, xi1=-2, xi2=2, dis=15):
    """calculates the Nonlinear Fourier Transform for the Korteweg-de Vries equation with vanishing boundaries
    Parameters:
    ----------       
        u : numpy array holding the samples of the field to be analyzed        
        tvec : time vector
        m : number of values for the continuous spectrum to calculate,
            [optional, standard=100]
        xi1, xi2 : min and max frequency for the continuous spectrum, 
                   [optional, standard=-/+ 2]        
        dis : determines the discretization, [optional, standard=15]
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        contspec : continuous spectrum        
    """
    d = len(u)
    k = 0  # not yet implemented
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_kdvv_options(dis)
    return kdvv_wrapper(fnft_clib.fnft_kdvv, d, u, t1, t2, m, xi1, xi2,
                        k, options)


def nsep(q, t1, t2, kappa=1, loc=2, filt=2, bb=None,
         maxev=20, dis=1, nf=1):
    """
    calculates the Nonlinear Fourier Transform for the periodic Nonlinear Schroedinger Equation
    Parameters:
    ----------
        clib_nsep_func : handle of the c function imported via ctypes
	
        q : numpy array holding the samples of the field to be analyzed
        t1, t2  : time positions of the first and the (d+1) sample
        kappa : +/- 1 for focussing/defocussing nonlinearity 
               [optional, standard = +1]
        loc : localization of spectrum
             0=Subsample and Refine,
             1=Gridsearch,
             2=Mixed [optional, default=2]
        filt : filtering of spectrum
               0=None,
               1=Manual,
               2=Auto [optional, default=2]
        bb: bounding box used for manual filtering
            [optional, default=None (bb is set to [-200,200,-200,200])]
        maxev : maximum number of evaluations for root refinement
                [optional, default=20]
        nf : normalization Flag 0=off, 1=on [optional, default=1]
        dis : discretization
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO [optional, default=2] 
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        k : number of points in the main spectrum
        main : main spectrum
        m: number of points in the auxilary spectrum
	aux: auxilary spectrum
    """
    if bb is None:  # set standard value for bb
        bb = [-200, 200, -200, 200]
    d = len(q)
    options = get_nsep_options(loc, filt, bb, maxev, dis, nf)
    return nsep_wrapper(fnft_clib.fnft_nsep, d, q, t1, t2,
                        kappa, options)


def nsev(q, tvec, xi1=-2, xi2=2, m=100, k=100, kappa=1, bsf=2,
         bsl=2, niter=10, dst=0, cst=0, nf=1, dis=3):
    """Calculates the Nonlinear Fourier Transform for the Nonlinear Schroedinger equation with vanishing boundaries.
    Parameters:
    ----------
        q : numpy array holding the samples of the field to be analyzed
        tvec: time vector for q samples
        xi1, xi2 : min and max frequency for the continuous spectrum. [optional, standard = -2,2]
        m : number of values for the continuous spectrum to calculate [optional, standard = 100]
        k : maximum number of bound states to calculate [optional, standard = 100]
        kappa : +/- 1 for focussing/defocussing nonlinearity [optional, standard = +1]
        bsf : bound state filtering
              0=none, 
              1=basic, 
              2=full; [optional, default=2]
        bsl : bound state localization
              0=Fast Eigenvalue, 
              1=Newton, 
              2=Subsample and Refine; [optional, default=0]
        niter : number of iterations for Newton bsl [optional, default=10]
        dst : type of discrete spectrum
             0=norming constants, 
             1=residues, 
             2=both; [optional, defaul=2]
        cst : type of continuous spectrum
             0=reflection coefficient,
             1=a and b,
             2=both; [optional, default=0]
        nf : normalization Flag
             0=off
             1=on; [optional, default=1]
        dis : discretization
              0=2split2modal,
              1=2split2a,
              2=2split4a,
              3=2split4b,
              4=BO; [optional, default=3]
    Returns:
    ----------
    rdict : dictionary holding the fields (depending on options)
        return_value : return value from libFNFT
        bound_states_num : number of bound states found
        bound_states : array of bound states found 
        d_norm : discrete spectrum - norming constants
        d_res : discrete spectrum - residues
        c_ref : continuous spectrum - reflection coefficient
        c_a : continuous spectrum - scattering coefficient a
        c_b : continuous spectrum - scattering coefficient b
    """
    d = len(q)
    t1 = np.min(tvec)
    t2 = np.max(tvec)
    options = get_nsev_options(bsf, bsl, niter, dst, cst, nf, dis)
    return nsev_wrapper(fnft_clib.fnft_nsev, d, q, t1, t2, xi1, xi2,
                        m, k, kappa, options)
