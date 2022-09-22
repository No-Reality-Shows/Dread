# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:39:46 2022

@author: JonTr003
"""

#for logging
import logging

#for config
import config

##############################################################################
#logger
##############################################################################

def create_logger(logger_name, logger_level='INFO'):
    # create logger
    logger = logging.getLogger(logger_name)
    
    if logger_level == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif logger_level == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif logger_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif logger_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    
    # create formatter
    formatter = logging.Formatter('{"datetime":"%(asctime)s.%(msecs)03d", "level":"%(levelname)s", "module":"%(name)s", "message":%(message)s}', datefmt='%Y-%m-%d %H:%M:%S')
    
    # add formatter to ch
    ch.setFormatter(formatter)
    
    # add ch to logger
    logger.addHandler(ch)
    return logger

#initiate logger
logger = create_logger(__name__, config.LOGGER_LEVEL)

#prevent logger from propagating
logger.propagate = config.LOGGER_PROPAGATE

#log message
logger.debug('logger configured')

##############################################################################
#import external modules for rule evaluation
##############################################################################

EVAL_CONFIG = {}
for module in config.EXTERNAL_MODULES:
    try:
        EVAL_CONFIG[module] = __import__(module)
        logger.debug("external module '{MODULE}' imported for eval".format(MODULE=module))
    except:
        logger.exception("ERROR: unable to import external module '{MODULE}'".format(MODULE=module))
        
#append allowed builtins for eval        
EVAL_CONFIG.update(config.ALLOWED_BUILTINS)
logger.debug("allowed __builtins__ set for eval")


##############################################################################
#get action config
##############################################################################

AVAILABLE_ACTIONS = config.ACTION_CONFIG

##############################################################################
#get templates
##############################################################################

TEMPLATE_TEST_DATA = config.TEMPLATE_TEST_DATA

ATTRIBUTE_TEMPLATE = config.ATTRIBUTE_TEMPLATE

EXPRESSION_TEMPLATE = config.EXPRESSION_TEMPLATE

RULESET_TEMPLATE = config.RULESET_TEMPLATE

DATA_PIPELINE_TEMPLATE = config.DATA_PIPELINE_TEMPLATE

LOGIC_PIPELINE_TEMPLATE = config.LOGIC_PIPELINE_TEMPLATE