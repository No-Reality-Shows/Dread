# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:00:06 2022

@author: Travis Jones
https://github.com/No-Reality-Shows
"""


import os
import re
import joblib
import json
from Dread import utils
#from dread import decision_engine

##############################################################################
#function to build rule engine using config files
##############################################################################

def test(directory=None):
    try:
        #get inputs if no directory specified
        if directory == None:
            #get inputs
            engine_dir = input('Please specify DIRECTORY for decision engine (ENTER to skip and use current directory): ')
            #edit inputs
            engine_dir = str(os.getcwd()).replace('\\','/') if engine_dir == '' else engine_dir
        else:
            engine_dir = str(directory).replace('\\','/')
            
        engine_name = re.sub('.*/','',engine_dir)
        test_dir = '/'.join([engine_dir,'TestData'])
        engine_pickle = '/'.join([engine_dir,engine_name])+'_engine.pkl'
        
        print("Testing decision engine '{ENGINE}' against files in '{DIR}'".format(ENGINE=engine_name, DIR=test_dir))
        
        #import decision engine
        engine = joblib.load(engine_pickle)
        
        #get test folder files
        files = os.listdir(test_dir)
        
        #loop through folder files and apply engine
        for file in files:
            try:
                file_path = '/'.join([test_dir, file])
                if os.path.isfile(file_path) and bool(re.match('.*.json$', file_path)):
                    #load json file
                    data = json.load(open(file_path))
                    #pass data through engine engine
                    output = engine.execute(data)
                    #convert output to json
                    out_json = json.dumps(output)
                    #write output
                    with open('/'.join([test_dir, 'TestResults', 'result_'+file]), 'w') as f:
                        f.write(out_json)
                    print("Test file '{FILE}' processed".format(FILE=file))
            except:
                print("ERROR: An error occured while processing test file '{FILE}', continue to next file".format(FILE=file))
                continue
                utils.logger.exception('An error occured while processing test file')
                
        print("Decision engine testing complete, navigate to '/TestResults' directory to review results of test files")
    
    except:
        utils.logger.exception('An error occured while testing decision engine')
        
        