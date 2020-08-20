# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:47:05 2020

@author: Fatemeh
"""

import os
import itertools
import numpy as np
from parsers import csv_parser, fsl_parser, vbm_parser


def test_csv_parser():
    """test csv_parser"""
    args = {
            "input":{
                    "covariates":{
                            "sample0":{
                                    "feature0": "0.00632",
                                    "feature1": "18.0"
                                    },
                            "sample1":{
                                    "feature0": "0.02731",
                                    "feature1": "0.0"
                                    }
                                },
                    "data":[{
                            "type":"float",
                            "value":[["sample-id", "label"],
                                     ["sample0", "24.0"],
                                     ["sample1", "21.6"]]
                            }],
                    "lambda":0
                    }
             }
    covariates = [0.00632, 18.0, 0.02731, 0.0]
    data = [24.0, 21.6]
    x, y = csv_parser(args)
#    to compare dataframes in one assert they are converted to 1 D lists
    assert list(itertools.chain(x.values.flatten(), y.values.flatten())) == list(itertools.chain(covariates, data))
   
    
def test_fsl_parser():
    """test fsl_parser, working directory is given as baseDirectory to read freesurfer files specified in args"""
    wd_dir = os.getcwd()
    args = {
            'input': {
                    'covariates': {
                            'subject0_aseg_stats.txt': {
                                    'isControl': False,
                                    'age': '22.0'},
                            'subject1_aseg_stats.txt': {
                                    'isControl': True, 
                                    'age': '47.0'}
                                   },
                    'data': [{
                            'type': 'FreeSurfer', 
                            'value': ['5th-Ventricle']
                            }],
                    'lambda': 1
                    },
            'cache': {},
            'state': {'baseDirectory': wd_dir,
                      'outputDirectory': wd_dir,
                      'cacheDirectory': wd_dir,
                      'transferDirectory': wd_dir,
                      'clientId': 'local0',
                      'iteration': 1}
            }
    covariates = [0, 22.0, 1, 47.0]
#    values for 5th-Ventricle in the freesurfer files
    data = [6188.10, 10824.89]
    x, y = fsl_parser(args)
#    to compare dataframes in one assert they are converted to 1 D lists
    assert list(itertools.chain(x.values.flatten(), y.values.flatten())) == list(itertools.chain(covariates, data))
        
    
def test_vbm_parser():
    """test vbm_parser, working directory is given as baseDirectory to read nifti file specified in args. The mask
    should be in working directory. Only ten first voxel values of nifti file are compared to what vmb_parser returns. 
    The values are rounded"""
    wd_dir = os.getcwd()
    mask = os.path.join(wd_dir, 'aal_1.5.nii')
    args = {
            'input': {
                    'covariates': {
                            "M02101222_swc1t1avg.nii": {
                                    "isControl": False,
                                    "age": 28,
                                    "sex": "M"
                                    }
                            },
                    'data': [{
                            "type": ["boolean", "int", "string"],
                            "value": ["niftifile"]
                            }],
                    'lambda': 1
                    },
            'cache': {},
            'state': {'baseDirectory': wd_dir,
                      'outputDirectory': wd_dir,
                      'cacheDirectory': wd_dir,
                      'transferDirectory': wd_dir,
                      'clientId': 'local0',
                      'iteration': 1}
            }
    covariates = [28, 0]
#    the fist 10 values (rounded) for 5th-Ventricle in the freesurfer file
    data = [0.27451, 0.27451, 0.27059, 0.27059, 0.27059, 0.27059, 0.26667, 0.26667, 0.26667, 0.26275]
    x, y = vbm_parser(args, mask)
#    to compare dataframes in one assert they are converted to 1 D lists
    assert list(itertools.chain(x.values.flatten(),  np.around(y.values[0][0:10], 5))) == list(itertools.chain(covariates, data))
