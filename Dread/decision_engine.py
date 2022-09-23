# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:47:18 2022

@author: No-Reality-Shows
"""

#dependencies
import numpy as np
import operator
from functools import reduce
from Dread import utils

###############################################################################
#DataModel class
###############################################################################

class DataModel:
    
    def __init__(self, name=''):
            self.name = name
            self.model = {'attributes':{}, 'expressions':{}}
    
    ###########################################################################
    #attribute class
    ###########################################################################
    
    class Attribute:
        """
        DESCRIPTION:
        This class creates 'Attribute' objects utilized by the DataModel class.
        It is used when extracting data from the input dictionary.
        
        ATTRIBUTES:
        name (str; required) - The name of the attribute.
        
        attribute_path (list; required) - The path to the attribute in the input 
        data.
        
        dtype (type; required) - The desired datatype for the attribute.
        
        default (varies; required) - The default value for the 
        attribute. Should match the attribute datatype.
        """

        def __init__(self, name, attribute_path, dtype, default):
            self.name = name
            self.attribute_path = attribute_path
            self.dtype = dtype
            self.default = default
            
        def execute(self, data):
            output = {'name':self.name,
                      'value':None}
            try:
                output['value'] = self.dtype(reduce(operator.getitem, self.attribute_path, data))
            except Exception as e:
                utils.logger.exception('{{"exception":"an error occured while executing attribute [{ATTRIBUTE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(ATTRIBUTE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
                output['value'] = self.default
                output['error_type'] = str(type(e).__name__)
                output['error'] = str(e)
            return output
    
    # ###########################################################################
    # #expression class
    # ###########################################################################
    
    class Expression:
        """
        DESCRIPTION:
        This class creates 'expression' objects utilized by the data structure 
        class. It is used to apply expressions to create new attributes following 
        attribute extraction.
        
        ATTRIBUTES:
        name (str; required) - The name of the expression.
        
        expression (str; requied) - The expression string to be executed.
        
        default (varies; required) - The default value for the 
        expression. 
        """
        
        def __init__(self, name, expression, dtype, default):
            self.name = name
            self.expression = expression
            self.dtype = dtype
            self.default = default
            
        def execute(self, data):
            output = {'name':self.name,
                      'value':None}
            try:
                utils.EVAL_CONFIG['data'] = data
                output['value'] = self.dtype(eval(self.expression,{"__builtins__": {}}, utils.EVAL_CONFIG))
            except Exception as e:
                utils.logger.exception('{{"exception":"an error occured while executing expression [{EXPRESSION}],"error_type":"{TYPE}","error":"{ERROR}"'.format(EXPRESSION=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
                output['value'] = self.default
                output['error_type'] = str(type(e).__name__)
                output['error'] = str(e)
            return output
        
    ###########################################################################
    #function to add attribute to DataModel
    ###########################################################################
    
    def add_attribute(self, name, attribute_path, dtype, default=None):
        try:
            self.model['attributes'][name] = DataModel.Attribute(name, attribute_path, dtype, default)
            utils.logger.debug("Attribute '{NAME}' added to DataModel".format(NAME=name))
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while adding Attribute [{NAME}] to DataModel,"error_type":"{TYPE}","error":"{ERROR}"'.format(NAME=name,TYPE=str(type(e).__name__), ERROR=str(e)))
            
    ###########################################################################
    #function to add expression to DataModel
    ###########################################################################
    
    def add_expression(self, name, expression, dtype, default):
        try:
            self.model['expressions'][name] = DataModel.Expression(name, expression, dtype, default)
            utils.logger.debug("Expression '{NAME}' added to DataModel".format(NAME=name))
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while adding Expression [{NAME}] to DataModel,"error_type":"{TYPE}","error":"{ERROR}"'.format(NAME=name,TYPE=str(type(e).__name__), ERROR=str(e)))


###############################################################################
#Logic class
###############################################################################
            
#rule class
class LogicModel:
    
    def __init__(self, name=''):
            self.name = name
            self.model = {}
    
    ###########################################################################
    #Rule class
    ###########################################################################
    
    class Rule:
        def __init__(self, name, logic, score, flag):
            self.name = name
            self.logic = logic
            self.score = score
            self.flag = flag
            
        def execute(self, data):
            #set scope for eval
            #default output
            output = {'result':False,
                   'score':0,
                   'flag':None}
            try:
                #set scope for eval
                utils.EVAL_CONFIG['data'] = data
                #evaluate logic
                if eval(self.logic,{"__builtins__": {}}, utils.EVAL_CONFIG):
                    output['result'] = True
                    output['score'] = self.score
                    output['flag']  = self.flag
            except Exception as e:
                #add error details
                output['error_type'] = str(type(e).__name__)
                output['error'] = str(e)
                #log exception
                utils.logger.exception('{{"exception":"an error occured while executing rule [{RULE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(RULE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
            #return output
            return output

    ###########################################################################
    #RuleSet class
    ###########################################################################    

    class RuleSet:
        
        def __init__(self, name):
            self.name = name
            self.rules = np.array([])
    
        def add_rule(self, name, logic, score=0, flag=None):
            try:
                self.rules = np.append(self.rules, LogicModel.Rule(name, logic, score, flag))
                utils.logger.debug("Rule '{NAME}' added to RuleSet '{RULESET}'".format(NAME=name, RULESET=self.name))
            except Exception as e:
                utils.logger.exception('{{"exception":"an error occured while adding rule [{RULE}] to ruleset [{RULESET}],"error_type":"{TYPE}","error":"{ERROR}"'.format(RULE=name,RULESET=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
    
        def execute(self, data, action=None, score_override=None, flag_override=None, apply_all=False):
            #default output
            output = {'result':False,
                      'action':None,
                      'score':0,
                      'flags':[],
                      'rules':{},
                      'errors':[]
                      }
            try:
                #loop through rules
                for rule in self.rules:
                    #execute rule
                    rule_result = rule.execute(data)
                    
                    if rule_result.get('error') is None:                    
                        #check rule fired
                        if rule_result['result']:
                            output['result'] = True
                            output['action'] = action
                            output['score'] = output['score'] + rule_result['score']
                            if rule_result['flag'] is not None:
                                output['flags'].append(rule_result['flag'])
                            output['rules'][rule.name] = rule_result
                            
                            if apply_all == False:
                                #break loop 
                                break
                            else:
                                output['rules'][rule.name] = rule_result
                    else:
                        #add errors to output
                        output['errors'].append({'ruleset':self.name, 'rule':rule.name, 'error':rule_result['error'], 'error_type':rule_result['error_type']})
                            
                #add overrides
                if score_override is not None and output['result']:
                    output['score'] = score_override
                    
                if flag_override is not None and output['result']:
                    output['flags'] = [flag_override]
                    
                #execute actions
                if (output.get('action') is not None):
                    if utils.AVAILABLE_ACTIONS.get(output.get('action')) is not None:
                        action_results = {'name': output.get('action')}
                        try:
                            #get parameters
                            action_results['params'] = eval(utils.AVAILABLE_ACTIONS.get(action_results['name'])['params'],{"__builtins__": {}}, {'data':data})
                            #run action function
                            action_output = utils.AVAILABLE_ACTIONS.get(action_results['name'])['action_function'](**action_results['params'])
                            #append results
                            action_results['result'] = 'success'
                            action_results['action_output'] = action_output
                        except Exception as e:
                            #append errors
                            action_results['error_type'] = str(type(e).__name__)
                            action_results['error'] = str(e)
                            utils.logger.exception('{{"exception":"an error occured while executing action [{ACTION}],"error_type":"{TYPE}","error":"{ERROR}"'.format(ACTION=output.get('action'),TYPE=str(type(e).__name__), ERROR=str(e)))
                    else:
                        action_results = {'name': output.get('action'), 'params':{}, 'result':None, 'action_output':'no action function available'}
                        
                    output['action_result'] = action_results
            except Exception as e:
                output['error_type'] = str(type(e).__name__)
                output['error'] = str(e)
                utils.logger.exception('{{"exception":"an error occured while executing ruleset [{RULESET}],"error_type":"{TYPE}","error":"{ERROR}"'.format(RULESET=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
    
            #return output
            return output
        
    ###########################################################################
    #add Ruleset Function
    ###########################################################################    
    
    def add_ruleset(self, name):
        try:
            self.model[name] = LogicModel.RuleSet(name)
            utils.logger.debug("RuleSet [{RULESET}] added to LogicModel [{LOGIC}]".format(RULESET=name, LOGIC=self.name))
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while adding RuleSet [{RULESET}] to LogicModel [{LOGIC}],"error_type":"{TYPE}","error":"{ERROR}"'.format(RULESET=name,LOGIC=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))

###############################################################################
#Engine class
###############################################################################


class Engine:
    
    def __init__(self, name=''):
            self.name = name
            self.data_model = DataModel('default')
            self.logic_model = LogicModel('default')
            self.data_pipelines = {}
            self.logic_pipelines = {}

    ###########################################################################
    #DataPipeline class
    ###########################################################################   
    
    class DataPipeline:
        """
        DESCRIPTION:
        This class creates 'DataPipeline' objects utilized by the rule engine 
        class. It is used to extract attributes and apply expressions 
        to the input data. 
        
        ATTRIBUTES:
        name (str; required) - The name of the pipeline.
        
        pipeline (list; requied) - A list of dictionaries specifiying the attributes
        and expresseions to apply to the input data.
        """
        
        def __init__(self, name, pipeline=[]):
            self.name = name
            self.pipeline = np.array(pipeline)
            
        def execute(self, data, DataModel):
            
            input_data = data.copy()
            
            output = {'datamodel_errors':[],
                      'pipeline_errors':[]}
            try:
                for item in self.pipeline:
                    result = DataModel.model[item['type']][item['name']].execute(input_data)
                    #add result to data
                    input_data[result['name']] = result['value']
                    #add result to output
                    output[result['name']] = result['value']
                    if result.get('error') is not None:
                        output['datamodel_errors'].append({'pipeline':self.name, 
                                                          'type': item['type'],
                                                          'name': item['name'],
                                                          'error': result.get('error'),
                                                          'error_type': result.get('error_type')})
                    
            except Exception as e:
                utils.logger.exception('{{"exception":"an error occured while executing DataPipeline [{PIPELINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(PIPELINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
                output['pipeline_errors'] = {'pipeline':self.name, 'error':str(e),'error_type': str(type(e).__name__)}
            return output
        
    ###########################################################################
    #add data pipeline function
    ###########################################################################   
    
    def add_data_pipeline(self, name, pipeline=[]):
        try:
            self.data_pipelines[name] = Engine.DataPipeline(name, pipeline)
            utils.logger.debug("DataPipeline [{PIPELINE}] added to Engine [{ENGINE}]".format(PIPELINE=name, ENGINE=self.name))
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while adding DataPipeline [{PIPELINE}] to Engine [{ENGINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(PIPELINE=name,ENGINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))

    ###########################################################################
    #LogicPipeline class
    ###########################################################################

    class LogicPipeline:
        
        def __init__(self, name, pipeline=[]):
            self.name = name
            self.pipeline = np.array(pipeline)
    
        def add_logic_pipeline(self,name, pipeline=[]):
            try:
                self.pipeline = np.append(self.pipeline, pipeline)
                utils.logger.debug("LogicPipeline [{PIPELINE}] added to Engine [{ENGINE}]".format(PIPELINE=name, ENGINE=self.name))
            except Exception as e:
                utils.logger.exception('{{"exception":"an error occured while adding ruleset [{RULESET}] to collection [{PIPELINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(RULESET=name,PIPELINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
    
        def execute(self, data, logic_model, audit_trail={}, apply_all=True):
            #default output
            output = {'result':False,
                      'actions':[],
                      'score':0,
                      'flags':[],
                      'errors':[],
                      'rulesets':{}}
            try:
                #append audit trail to data
                data['audit_trail'] = audit_trail
                
                #loop through rulesets
                for ruleset in self.pipeline:
                    #execute rule
                    ruleset_result = logic_model[ruleset['ruleset']].execute(data, **ruleset['params'])
    
                    #append ruleset result
                    output['rulesets'][ruleset['ruleset']] = ruleset_result
                        
                    #append errors
                    output['errors'] = output['errors'] + ruleset_result['errors']
                    
                    #if ruleset result == True
                    if ruleset_result['result']:
                        #update result
                        output['result'] = True
                        data['audit_trail']['result'] = True
                        #update actions
                        if ruleset_result['action'] is not None:
                            output['actions'].append(ruleset_result['action'])
                            data['audit_trail']['actions'].append(ruleset_result['action'])
                            data['audit_trail']['action_results'][ruleset_result['action']] = ruleset_result['action_result']
                        output['score'] = output['score'] + ruleset_result['score']
                        #update scores
                        data['audit_trail']['score'] = data['audit_trail']['score']  + ruleset_result['score']
                        #update flags
                        output['flags'] = output['flags'] + ruleset_result['flags']
                        data['audit_trail']['flags'] = data['audit_trail']['flags'] + ruleset_result['flags']
                        #update rulesets
                        output['rulesets'][ruleset['ruleset']] = ruleset_result
    
                    #update audit_trail
                    data['audit_trail']['LogicPipelines'][self.name] = output
                    
                    #break loop if apply_all=False
                    if apply_all == False and ruleset_result['result']:
                        break
                        
            except Exception as e:
                output['error_type'] = str(type(e).__name__)
                output['error'] = str(e)
                utils.logger.exception('{{"exception":"an error occured while executing LogicPipeline [{PIPELINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(PIPELINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
    
            #return output
            return data['audit_trail']
        
    ###########################################################################
    #add logic pipeline function
    ###########################################################################
        
    def add_logic_pipeline(self, name, pipeline=[]):
        
        try:
            self.logic_pipelines[name] = Engine.LogicPipeline(name, pipeline)
            utils.logger.debug("LogicPipeline [{PIPELINE}] added to Engine [{ENGINE}]".format(PIPELINE=name, ENGINE=self.name))
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while adding LogicPipeline [{PIPELINE}] to Engine [{ENGINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(PIPELINE=name,ENGINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))

        
    def execute(self, data, data_pipelines=None, logic_pipelines=None):
        
        try:
            
            utils.logger.debug('executing engine')
            
            ######################################################################
            #set attributes
            ######################################################################
            
            #use all data_pipelines if data_pipelines == None
            data_pipelines = list(self.data_pipelines.keys()) if data_pipelines == None else data_pipelines
            
            #use all logic_pipelines if logic_pipelines == None
            logic_pipelines = list(self.logic_pipelines.keys()) if logic_pipelines == None else logic_pipelines
            
            #create audit trail
            audit_trail = {'result':False,
                   'actions':[],
                   'action_results':{},
                   'score':0,
                   'flags':[],
                   'LogicPipelines':{}}
            
            #create output
            input_data = data
            output = {'input':input_data}
            
            ######################################################################
            #run DataPipelines
            ######################################################################
            
            utils.logger.debug('execute data_pipelines')
            
            for pipeline in data_pipelines:
                data = self.data_pipelines[pipeline].execute(data, self.data_model)
                
            processed_data = data
            output['processed_data'] = processed_data    
            
            ######################################################################
            #run LogicPipelines
            ######################################################################
    
            utils.logger.debug('execute logic_pipelines')
            
            for pipeline in logic_pipelines:
                logic_output = self.logic_pipelines[pipeline].execute(processed_data, self.logic_model.model, audit_trail)
                
            output['audit_trail'] = logic_output
        
        except Exception as e:
            utils.logger.exception('{{"exception":"an error occured while executing engine [{ENGINE}],"error_type":"{TYPE}","error":"{ERROR}"'.format(ENGINE=self.name,TYPE=str(type(e).__name__), ERROR=str(e)))
 
        return output

