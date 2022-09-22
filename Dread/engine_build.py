# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 08:28:43 2022

@author: JonTr003
"""

import os
import pandas as pd
import re
import joblib
from Dread import utils
from Dread import decision_engine

##############################################################################
#function to build rule engine using config files
##############################################################################

def build(directory=None):
    try:
        #get inputs if no directory specified
        if directory == None:
            #get inputs
            build_dir = input('Please specify DIRECTORY for decision engine (ENTER to skip and use current directory): ')
            #edit inputs
            build_dir = str(os.getcwd()).replace('\\','/') if build_dir == '' else build_dir
        else:
            build_dir = str(directory).replace('\\','/')
        
        #get engine name from directory
        engine_name = re.sub('.*/','',build_dir)
        print("Building {ENGINE} decision engine from '{BUILD_DIR}'".format(ENGINE=engine_name,BUILD_DIR=build_dir))
        
        #intitate engine
        try:    
            engine = decision_engine.Engine(engine_name)
            print('Engine intitiated')
        except:
            utils.logger.exception('An error occured while initiating Engine')
        
        ######################################################################
        #build data model
        ######################################################################
        try:
            print('\tConfiguring DataModel')
            ##################################################################
            #add attributes
            ##################################################################
            
            #read in attributes file
            attributes = pd.read_csv('/'.join([build_dir,'DataModel','attributes.csv']))
            #replace np.nan with None
            attributes = attributes.where(pd.notnull(attributes), None)
            #drop empty rows and columns
            attributes = attributes.dropna(axis=0, how = 'all')
            attributes = attributes.dropna(axis=1, how = 'all')
            
            #create attributes
            for index, attribute in attributes.iterrows():
                #get params
                params = attribute.to_dict()
                params['attribute_path'] = re.sub("[^A-Za-z0-9,]",'',params['attribute_path']).split(',')
                params['dtype'] = eval(params['dtype'],{"__builtins__": {}}, utils.EVAL_CONFIG)
                params['default'] = params['dtype'](params['default'])
                #add attribute to engine
                engine.data_model.add_attribute(**params)
                print("\t\tAttribute '{ATTRIBUTE}' added to data model".format(ATTRIBUTE=params['name']))
                
            ##################################################################
            #add expressions
            ##################################################################
                
            #read in attributes file
            expressions = pd.read_csv('/'.join([build_dir,'DataModel','expressions.csv']))
            #replace np.nan with None
            expressions = expressions.where(pd.notnull(expressions), None)
            #drop empty rows and columns
            expressions = expressions.dropna(axis=0, how = 'all')
            expressions = expressions.dropna(axis=1, how = 'all')
            
            #create expressions
            for index, expression in expressions.iterrows():
                #get params
                params = expression.to_dict()
                params['dtype'] = eval(params['dtype'],{"__builtins__": {}}, utils.EVAL_CONFIG)
                params['default'] = params['dtype'](params['default'])
                #add expression to engine
                engine.data_model.add_expression(**params)
                print("\t\tExpression '{EXPRESSION}' added to data model".format(EXPRESSION=params['name']))
                
        except:
            utils.logger.exception('An error occured while building DataModel')
            
        ######################################################################
        #build logic model
        ######################################################################
        try:
            print('\tConfiguring LogicModel')
            ##################################################################
            #add rulesets
            ##################################################################
            
            #get folder files
            path = '/'.join([build_dir,'LogicModel'])
            files = os.listdir(path)
            
            for file in files:
                file_path = '/'.join([path, file])
                if os.path.isfile(file_path) and bool(re.match('.*.csv$', file_path)):
                    #get ruleset name
                    ruleset_name = re.sub('.csv$','',file)
                    #create ruleset
                    engine.logic_model.add_ruleset(ruleset_name)
                    #read ruleset data
                    ruleset = pd.read_csv(file_path)
                    #fill nas with None
                    ruleset = ruleset.where(pd.notnull(ruleset), None)
                    #drop empty rows and columns
                    ruleset = ruleset.dropna(axis=0, how = 'all')
                    ruleset = ruleset.dropna(axis=1, how = 'all')
                    #join rule logic
                    ruleset['logic'] = '('+ruleset.drop(['name', 'score', 'flag'], axis = 1).astype(str).agg(') and ('.join, axis=1)+')'
                    #add rules to ruleset
                    for index, rule in ruleset.iterrows():
                        params = rule[['name', 'score', 'flag','logic']].to_dict()
                        engine.logic_model.model[ruleset_name].add_rule(**params)
                    print("\t\tRuleSet '{RULESET}' added to LogicModel".format(RULESET=ruleset_name))
                
        except:
            utils.logger.exception('An error occured while building LogicModel')
            
        ######################################################################
        #add data pipelines
        ######################################################################
        try:
            print('\tConfiguring DataPipelines')
            ##################################################################
            #add pipelines
            ##################################################################
            
            #get folder files
            path = '/'.join([build_dir,'DataPipelines'])
            files = os.listdir(path)
            
            for file in files:
                file_path = '/'.join([path, file])
                if os.path.isfile(file_path) and bool(re.match('.*.csv$', file_path)):
                    #get ruleset name
                    pipeline_name = re.sub('.csv$','',file)
                    #read in data
                    pipeline = pd.read_csv(file_path)
                    #fill nas with None
                    pipeline = pipeline.where(pd.notnull(pipeline), None)
                    #drop empty rows and columns
                    pipeline = pipeline.dropna(axis=0, how = 'all')
                    pipeline = pipeline.dropna(axis=1, how = 'all')
                    #convert dataframe to dict list
                    pipeline = pipeline.to_dict(orient='records')
                    #add pipeline
                    engine.add_data_pipeline(pipeline_name, pipeline)
                    print("\t\tDataPipeline '{PIPELINE}' added to Engine".format(PIPELINE=pipeline_name))
                
        except:
            utils.logger.exception('An error occured while adding DataPipelines to Engine')
            
        ######################################################################
        #add logic pipelines
        ######################################################################
        try:
            print('\tConfiguring LogicPipelines')
            ##################################################################
            #add pipelines
            ##################################################################
            
            #get folder files
            path = '/'.join([build_dir,'LogicPipelines'])
            files = os.listdir(path)
            
            for file in files:
                file_path = '/'.join([path, file])
                if os.path.isfile(file_path) and bool(re.match('.*.csv$', file_path)):
                    #get ruleset name
                    pipeline_name = re.sub('.csv$','',file)
                    #read in data
                    pipeline = pd.read_csv(file_path, index_col='ruleset')
                    #fill nas with None
                    pipeline = pipeline.where(pd.notnull(pipeline), None)
                    #drop empty rows and columns
                    pipeline = pipeline.dropna(axis=0, how = 'all')
                    pipeline = pipeline.dropna(axis=1, how = 'all')
                    #convert dataframe to dict list
                    pipeline_ls = []
                    for index, ruleset in pipeline.iterrows():
                        pipeline_ls.append({'ruleset':index, 'params':ruleset.to_dict()})
                    engine.add_logic_pipeline(pipeline_name, pipeline_ls)                         
                    print("\t\tLogicPipeline '{PIPELINE}' added to Engine".format(PIPELINE=pipeline_name))
                
        except:
            utils.logger.exception('An error occured while adding DataPipelines to Engine')
        
        print('Engine build complete')
        output_filename = '/'.join([build_dir,engine_name])+'_engine.pkl'
        joblib.dump(engine, output_filename)
        print("Engine saved to '{FILENAME}'".format(FILENAME=output_filename))
        
    except:
        utils.logger.exception('An error occured while building decision engine')
        