# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:17:48 2022

@author: JonTr003
"""

import os
import pandas as pd
from Dread import utils

##############################################################################
#template files
##############################################################################

def init(name=None, directory=None):
    try:
        if name == None:
            #get inputs
            engine_name = input('Please specify NAME for decision engine (REQUIRED): ')
            build_dir = input('Please specify DIRECTORY for build configuration files (ENTER to skip and use current directory): ')
            
            #edit inputs
            build_dir = str(os.getcwd()).replace('\\','/') if build_dir == '' else build_dir
        else:
            build_dir = str(directory).replace('\\','/')
            engine_name = str(name)
            
        if engine_name == '':
            print('No decision engine name specified, goodbye')
            pass
        else:
            ######################################################################
            #create directories
            ######################################################################
            
            print('Creating directories for build configuration files for {ENGINE} decision engine'.format(ENGINE=engine_name))
            #create engine directory
            os.mkdir('/'.join([build_dir, engine_name]))
            #create LogicModel directory
            os.mkdir('/'.join([build_dir, engine_name, 'LogicModel']))
            #create DataModel directory
            os.mkdir('/'.join([build_dir, engine_name, 'DataModel']))
            #create LogicPipelines directory
            os.mkdir('/'.join([build_dir, engine_name, 'LogicPipelines']))
            #create DataPipelines directory
            os.mkdir('/'.join([build_dir, engine_name, 'DataPipelines']))
            #create template directory
            os.mkdir('/'.join([build_dir, engine_name, 'Templates']))
            #create Test directory
            os.mkdir('/'.join([build_dir, engine_name, 'TestData']))
            #create TestResults directory
            os.mkdir('/'.join([build_dir, engine_name, 'TestData', 'TestResults']))
            print('Creating template files for build configuration files for {ENGINE} decision engine'.format(ENGINE=engine_name))
            #ruleset template
            pd.DataFrame(utils.RULESET_TEMPLATE).to_csv('/'.join([build_dir, engine_name, 'Templates','ruleset_template.csv']), index=False)
            #attribute template
            pd.DataFrame(utils.ATTRIBUTE_TEMPLATE).to_csv('/'.join([build_dir, engine_name, 'DataModel','attributes.csv']), index=False)
            #expression template
            pd.DataFrame(utils.EXPRESSION_TEMPLATE).to_csv('/'.join([build_dir, engine_name, 'DataModel','expressions.csv']), index=False)
            #data_pipeline temaplte
            pd.DataFrame(utils.DATA_PIPELINE_TEMPLATE).to_csv('/'.join([build_dir, engine_name, 'Templates','data_pipeline_template.csv']), index=False)
            #logic_pipeline template
            pd.DataFrame(utils.LOGIC_PIPELINE_TEMPLATE).to_csv('/'.join([build_dir, engine_name, 'Templates','logic_pipeline_template.csv']), index=False)
            #template test data
            pd.DataFrame(utils.TEMPLATE_TEST_DATA).to_json('/'.join([build_dir, engine_name,'TestData','template_test_data.json']))
            print('Directories and template files created for {ENGINE}'.format(ENGINE=engine_name))
            
            steps = """NEXT STEPS:
\t1:) Create DataModel by adding entries to 'DataModel/attributes.csv' and 'DataModel/expressions.csv' files
\t2:) Create LogicModel by creating ruleset '.csv' files in 'LogicModel/' directory
\t\t- A template ruleset file can be found in 'Templates/ruleset_template.csv' directory
\t3:) Create DataPipeline by creating data pipeline '.csv' files in 'DataPipelines/' directory
\t\t- A template data pipeline file can be found in 'Templates/data_pipeline_template.csv' directory
\t\t- Multiple files will result multiple DataPipelines within the rule engine
\t4:) Create LogicPipeline by creating logic pipeline '.csv' files in 'LogicPipelines/' directory
\t\t- A template data pipeline file can be found in 'Templates/data_pipeline_template.csv' directory
\t\t- Multiple files will result multiple LogicPipelines within the rule engine
\t5:) From python, build decision engine which will create the decision engine file {ENGINE}.pkl
\t\t"from Dread.engine_build import build"
\t\t"build('{ENGINE}')"
\tYay, your first decision engine was built, now it's time to test it.
\t6:)From python, test rule engine against test files in the TestData directory
\t\t- 'Dread.engine_test.test' requires JSON formatted data which is read into a python dictionary object which the engine accepts
\t\t- The outputs from the test execution will be placed in the /TestData/TestResults direcotry
\t\t"from Dread.engine_test import test"
\t\t"test('{ENGINE}')"
""".format(ENGINE = engine_name)
            print(steps)
            #write steps to file
            with open('/'.join([build_dir, engine_name,'README.txt']), 'w') as f:
                f.write(steps)
    except:
        utils.logger.exception('An error occured while initiating decision engine')
        
if __name__ == '__main__':
    init()