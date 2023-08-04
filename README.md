# Dread
Dread (Decision Rule Engine for Actioning Data) is a python package for creating, managing, executing a pythonic rule engine to make data driven decisions and take actions on those decisions.

Please note, this documentation is still a work in progress...

# Dependencies
Work in progress...

# Installation
Install from github
```
pip install git+https://github.com/No-Reality-Shows/Dread.git
``` 
or just clone to working directory, sometimes I think this is easier
```
git clone https://github.com/No-Reality-Shows/Dread.git
```

#### Dread Decision Engine Components and Structure

First, the basics. Dread decision engines are comprised of a handful of core components in a hierarchical structure. All components can be used seperately, but the "engine" is all of them working together. Below is the hierarchical structure and components of a Dread decision engine.

#### Decision Engine Hierarchy
```
L1 - DataModel
        L2 - Attributes
        L2 - Expressions
L1 - DataPipelines
L1 - LogicModel
        L2 - RuleSet
                L3 - Rule
L1 - LogicPipelines
```

#### Decision Engine Components
- **DataModel** - The DataModel is an object comprised of attributes and expressions. It is meant to provide the means to extract, transform, and format data within the input dictionary object to make it suitable for the LogicModels. Only data extracted by the DataModel can be used within the LogicModel.
  - Attributes - Attributes are objects that extract and format data from the input dictionary object. Attributes can "climb the tree" of the dictionary object by specifying the path as a list. (I tried dot notation, but couldn't quite get it to work without more dependencies, but's effectively the same thing in list format)
  - Expressions - Expressions are objects that take data from the input dictionary object or configured attributes and do something with it to create an output. They can apply Dread configured functions (see Dread component Dread.functions below), logic, do math, and make other maniupuations to get the input data in the desired format. Although expressions are used within a try/except block, they are to be used with caution and tested thoroughly.
- **DataPipelines** - DataPipelines control what attributes and expressions from the DataModel are executed along with their priority. Attributes and Expressions must exist in a DataPipeline in order to be used within the engine.
- **LogicModel**  - The LogicModel is an object comprised of RuleSets, which are comprised of Rules. It holds all of the logic that gets applied within the decision engine. There can be many RuleSets within a LogicModel.
  - RuleSet - RuleSets are objects comprised of one or more Rule objects kept in priority order.
     - Rule - Rules are objects that contain the core logic being executed within the decision engine along with any associated score values and flags that are applied when evaluated. 
- **LogicPipelines** - LogicPipelines control what RuleSets from the LogicModel are executed along with their priority. A RuleSet must exist in a LogicPipeline in order to be used within the engine.

#### Other Dread Modules
- **Dread.config** - Used to configure decision engine and its execution.
- **Dread.functions** - Used as a placeholder to put custom functions which can use other packages and libraries.
- **Dread.utils** - Utility functions for the Dread package.

# Getting Started

Dread can be used within any .py file to build and configure decision engines, however this can be cumbersome and on the more advanced side, so there is a built-in file based approach to make building and configuring decision engines easier. It is suggested you use the file based approach first and then go from there. I'm a big proponent of learning by doing, so let's do something.

### File Based

#### Helpful Notes

The file based approach keeps all of the configurations for the decision engine in .csv files. These files can be manipulated followed by running the engine_build.build function to generate a new decision engine. The required files must keep a particular structure in order for the engine build process to work properly.

#### File types and Formating by directory

***Any filename wrapped in square brackets means the name of the file is dynamic and can change. This is generally because of one to many relationships for the objects within the decision engine. The only filenames that CANNOT change are those within the DataModel directory, the attributes.csv and expressions.csv files.***

DataModel - Files in the /DataModel directory are used to create the DataModel within the decision engine. The names of these files CANNOT change.
 - attributes.csv - Entries in this file create Attribute objects in the DataModel within the decision engine.
   - name (required) - The name of the attribute (e.g. example_attribute_str).
   - attribute_path (required) - The path to the attribute in the input data dictionary as a comma seperated list (e.g. level1,level2,string).
   - dtype (required) - The python datatype for the attribute (e.g. str).
   - default - The default value for the attribute. This is applied if the attribute does not exist in the input dictionary data or there is an error while extracting or casting the datatype. If a default is not provided Nonetype is used.
 - expressions.csv - Entries in this file create Expression objects in the DataModel within the decision engine.
   - name (required) - The name of the attribute (e.g. example_expression_format_str).
   - expression (required) - The expression string to evaluate (e.g. data['example_attribute_str'].upper()). See 'Writing Expressions" below for more details.
   - dtype (required) - The python datatype for the expression result (e.g. str).
   - default - The default value for the expression. This is applied if the expression evaluation fails. If a default is not provided Nonetype is used.

DataPipelines - Files in the /DataPipelines directory create the DataPipeline objects within the decision engine. The filenames can change and will become the name of the pipeline within the decision engine. 
 - [DATA_PIPELINE_NAME].csv
   - type (required) - The type of data pipeline object (e.g. attributes). This is either "attributes" or "expressions". The build will fail if any other value is used.
   - name (required) - The name of the data model object (e.g. example_attribute_str) to add to the pipeline.
- Items in the data pipeline file are added in priority order. In the filebased approch the priority is determined by the row number, excluding the header row. Priority is important when you are trying to apply expressions to attributes or results of other expressions in the data pipeline.

LogicModel - Files in the /LogicModel directory are used to create RuleSets in the LogicModel of the decision engine. They contain the rule logic and are essentially decision tables if you're familiar with other types rule engines, but more flexible. The filenames can change and will become the name of the RuleSet within the decision engine. 
- [RULESET_NAME].csv
  - name (required) - The name of the rule (e.g. example_rule1).
  - score - The score to apply if the rule evalutes to True (e.g. 1000). If no score is provided 0 is used.
  - flag - The flag to apply if the rule evaluates to True (e.g. example_flag). If no flag is provided Nonetype is used.
  - logic (required) - The logic to evalute (e.g. data['example_attribute_str'] == 'test_data'). See 'Writing Rules" below for more details.
- In the file based approach Rule logic can be provided in multiple columns of the RuleSet file if desired. This makes organizing logic easier. Simply add another column and input the logic in the desired rule row. Multiple columns of logic are joined together with an "AND" condition. The name for the logic columns does not really matter, but they cannot be "name", "score", or "flag". However, I suggest keeping it simple and continue to use "logic" for the header of additional columns.
- EXAMPLE - A new column of logic was added for "example_rule2". This rule will be interpreted as "(data['example_expression_math'] < 1) and (ata['example_attribute_int'] > 0)"
```
|    | name          |   score | flag         | logic                                        | logic                             |
|---:|:--------------|--------:|:-------------|:---------------------------------------------|:----------------------------------|
|  0 | example_rule1 |     100 | example_flag | data['example_attribute_str'] == 'test_data' |                                   |
|  1 | example_rule2 |      50 |              | data['example_expression_math'] < 1          | data['example_attribute_int'] > 0 |
```

LogicPipelines- Files in the /LogicPipeline directory create the logic pipelines for the decision engine. The filenames can change and will become the name of the pipeline within the decision engine. 
- ['LOGIC_PIPELINE_NAME'].csv
  - ruleset (required) - The name of the ruleset (e.g. ruleset_template). In the file based approach this should be the name of the file/s in the /LogicModel directory.
  - action - The name of the action to execute if the rule evalutes to True (e.g. get_time).
  - score_override - The score to apply if the RuleSet evalutes to True (e.g. 1000). This will override any score values for individual rules. If no score is provided 0 is used.
  - flag_override - The flag to apply if the RuleSet evaluates to True (e.g. example_flag). This will override any flag values for individual rules. If no flag is provided Nonetype is used.
  - apply_all - An additional parameter to control whether all rules within the RuleSet should be applied. If no value is provided False is used, meaning the RuleSet execution stops following the first True evaluation.


#### 1.) Create and navigate to directory.
```
#create directory
mkdir dread_test

#navigate to dir
cd dread_test
```
#### 2.) Run python from working directory
```
python
```
#### 3.) Initiate engine. 

This will create subdirectories and files to configure your decision engine.

```
#import init module
from Dread.engine_init import init

#run init, you will be prompted to specify a name for the decision engine and a directory for its contents. 
init()

SPECIFY PARAMETERS:
...Please specify NAME for decision engine (REQUIRED): foo
...Please specify DIRECTORY for build configuration files (ENTER to skip and use current directory): [ENTER]
```
**OUTPUT:**
```
NEXT STEPS:
        1:) Create DataModel by adding entries to 'DataModel/attributes.csv' and 'DataModel/expressions.csv' files
                - Example entries already existing within these files
        2:) Create LogicModel by creating ruleset '.csv' files in the 'LogicModel/' directory
                - A template ruleset file 'ruleset_template.csv' can be found in 'LogicModel/' and 'Templates/' directories
        3:) Create DataPipeline by creating data pipeline '.csv' files in the 'DataPipelines/' directory
                - A template data pipeline file 'data_pipeline_template.csv' can be found in 'DataPipelines' and 'Templates/' directories
                - Multiple files will result multiple DataPipelines within the rule engine
        4:) Create LogicPipeline by creating logic pipeline '.csv' files in the 'LogicPipelines/' directory
                - A template logic pipeline file 'logic_pipeline_template.csv' can be found in 'LogicPipelines/' and 'Templates/' directories
                - Multiple files will result multiple LogicPipelines within the rule engine
        5:) From python, build decision engine which will create the decision engine file foo.pkl
                - "from Dread.engine_build import build"
                - "build('foo')"
        Yay, your first decision engine was built, now it's time to test it.
        6:)From python, test rule engine against test files in the TestData directory
                - 'Dread.engine_test.test' requires JSON formatted data which is read into a python dictionary object which the engine accepts
                - The outputs from the test execution will be placed in the /TestData/TestResults directory
                - "from Dread.engine_test import test"
                - "test('foo')"
```

#### 4.) Build your first decision engine. 

Follow the steps in the README.txt file. There are template files provided in the associated directories and the 'Templates' directory to make this easier. You can build your first engine only using these files.

from python, run ...
```
from Dread.engine_build import build

build('foo')
```
**OUTPUT:**
```
Building foo decision engine from 'foo'
Engine intitiated
        Configuring DataModel
                Attribute 'example_attribute_str' added to data model
                Attribute 'example_attribute_int' added to data model
                Attribute 'example_attribute_float' added to data model
                Expression 'example_expression_format_str' added to data model
                Expression 'example_expression_math' added to data model
        Configuring LogicModel
                RuleSet 'ruleset_template' added to LogicModel
        Configuring DataPipelines
                DataPipeline 'data_pipeline_template' added to Engine
        Configuring LogicPipelines
                LogicPipeline 'logic_pipeline_template' added to Engine
Engine build complete
Engine saved to 'foo/foo_engine.pkl'
```

Congrats, you built your first Dread decision engine. You can see your new engine in a serialized pickle file within your directory. When you finally go to use your decision engine, this is the file you will import to create your Engine object. You can then execute this engine to apply your data and logic models on new data, but we'll get to that.

#### 5.) Test your newly created decision engine.

Follow the steps in the README.txt file. There is already a template test file 'template_test_data.json' provided in the TestData directory to make this easier. You can test your first engine only using this file.

from python, run ...
```
from Dread.engine_test import test

test('foo')
```
**OUTPUT:**
```
Testing decision engine 'foo' against files in 'foo/TestData'
Test file 'template_test_data.json' processed
Decision engine testing complete, navigate to '/TestResults' directory to review results of test files
```

#### Examine Results
Cool, test complete. So what the f*ck just happened?

First, when the test script is run, it simply imports your engine, executes it on the data in the TestData directory, and writes the output back out as a .json file. The test data files are .json files, but when read in with the json.loads() method it creates a python dictionary object. ***IMPORTANT: The Dread decision engine always expects the input to be a python dictionary object***.

Now that we know what happened, let's talk about the test results. If you open and format the result "result_template_test_data.json" file, you will see a hierarchy appear. I'll do my best to explain this. Since this is JSON, I will use dot notation to refer to specific places in the JSON object.

#### Decision Engine Output
- **.input** - This is the raw input the decision engine recieved. It will look exactly like the data in the 'template_test_data.json' file.
- **.processed_data** - This is the data after it is processed by the data pipeline. I will explain exactly how this works below, but this is ultimately the data that is fed into the decision engine.
  - .processed_data.datamodel_errors - This is a list that captures any errors while processing the components of your data model.
  - .processed_data.pipeline_errors - This is a list that captures any fatal data pipeline errors, meaning the entire data pipeline fails for some reason. Hopefully you never see anything in here, but if you do, something bad happened.
  - .processed_data.example_attribute_str - This is a string attribute extracted from your input data. In this case we simply extracted the data in the "string" field of the input data.
  - .processed_data.example_attribute_int - This is an integer attribute extracted from your input data. In this case we simply extracted the data in the "integer" field of the input data.
  - .processed_data.example_attribute_float - This is a float attribute extracted from your input data. In this case we simply extracted the data in the "float" field of the input data.
  - .processed_data.example_expression_format_str - This is an expression extracted from your input data. In this case we simply applied the str.upper() method on the attribute "example_attribute_str"
  - .processed_data.example_expression_math - This is an expression extracted from your input data. In this case we simply did some division on the input attributes "example_attribute_int" and "example_attribute_float" (e.g. 1 / 1.5)
  - .processed_data.audit_trail - This is the audit trail from the decision engine. It exists here so you can refer to prior rules, actions, flags, and other components of the DataPipelines and LogicPipelines as the decision engine is processing. This can be a very powerful tool and allow you to chain decisions and actions together.
- **.audit_trail** - As mentioned above, this is the audit trail from the decision engine. It shows the final results of the decision engine on the input data.
  - .audit_trail.result - The final result of the decision engine. It is a boolean value indicating if any rule within the decision engine was triggered. A value of "True" means at least one rule was triggered.
  - .audit_trail.actions - A list of actions trigged by the decision engine. Actions are functions configured in the Dread.config module. Actions can be optionally tied to rulesets within LogicPipelines. If a rule in a ruleset is triggered, the action will be taken.
  - .audit_trail.action_results - An object of executed actions and their name, parameters, results, and output.
  - .audit_trail.score - This is the summation of all "scores" for executed rules and/or rulesets. You can assign a score to both rules and rulesets when configuring the decision engine.
  - .audit_trail.flags - This is a list of all "flags" for executed rules and/or rulesets. You can assign a flag to both rules and rulesets when configuring the decision engine. Flags can help you identify specific events you may be interest in.
  - .audit_trail.LogicPipelines - An object of all Logic Pipelines executed within the decision engine and their results. The resulting LogicPipeline attributes are mostly the same as the attributes within the top level of .audit_trail, just broken down by pipeline, so I will only go over any differences.
    -  .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].errors - This is a list that captures any errors that occured while processing the LogicPipeline.
    -  .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets - An object of all rulesets executed within the LogicPipeline. The resulting ruleset attributes are mostly the same as the attributes within the top level of .audit_trail and .LogicPipelines sections, just broken down by pipeline, so I will only go over any differences.
      - .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets.[RULESET_NAME].errors - This is a list that captures any errors that occured while processing the ruleset.
      - .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets.[RULESET_NAME].rules - An object of all rules executed within the ruleset. The rule attributes should be pretty self explainatory at this point.

#### Using the decision engine
Now that the decision engine is created, we can now use it to get results from new data. As mentioned, the file based approach saves the decision engine as a serialized pickle file that can be imported into any .py file. 

from python, run...
```
import joblib

#import engine
engine = joblib.load('foo/foo_engine.pkl')

#new data to process
new_data = {
	'level1': {
		'level2': {
			'string': "new_test_data",
			'integer': 5,
			'float': 2
		}
	}
}

#execute engine on new data
result = engine.execute(new_data)

#print result
print(result)
```
**OUTPUT:**
```
{
	'input': {
		'level1': {
			'level2': {
				'string': 'new_test_data',
				'integer': 5,
				'float': 2
			}
		}
	},
	'processed_data': {
		'datamodel_errors': [],
		'pipeline_errors': [],
		'example_attribute_str': 'new_test_data',
		'example_attribute_int': 5,
		'example_attribute_float': 2.0,
		'example_expression_format_str': 'NEW_TEST_DATA',
		'example_expression_math': 2.5,
		'audit_trail': {
			'result': False,
			'actions': [],
			'action_results': {},
			'score': 0,
			'flags': [],
			'LogicPipelines': {
				'logic_pipeline_template': {
					'result': False,
					'actions': [],
					'score': 0,
					'flags': [],
					'errors': [],
					'rulesets': {
						'ruleset_template': {
							'result': False,
							'action': None,
							'score': 0,
							'flags': [],
							'rules': {},
							'errors': []
						}
					}
				}
			}
		}
	},
	'audit_trail': {
		'result': False,
		'actions': [],
		'action_results': {},
		'score': 0,
		'flags': [],
		'LogicPipelines': {
			'logic_pipeline_template': {
				'result': False,
				'actions': [],
				'score': 0,
				'flags': [],
				'errors': [],
				'rulesets': {
					'ruleset_template': {
						'result': False,
						'action': None,
						'score': 0,
						'flags': [],
						'rules': {},
						'errors': []
					}
				}
			}
		}
	}
}
```

Awesome, this decision engine is ready to be used for making decisions. 

#### Additional Notes
A couple quick notes...

- You may have noticed the output when applying the decision engine on the "new_data" did not trigger any rules. This is by design. The input data changed and no longer met the criteria of any of the rules within the decision engine.
- You may have noticed only one rule shows as triggered in the audit trail from the original test even though multiple rules should have evaluated to True. This is by design. By default, when a RuleSet is being excuted, the first True evaluation cause the entire RuleSet to evaluate to True and no further rules are applied. This makes the decision engine faster and conforms with how most rule engines work. 
  - This behavior can be modified in the LogicPipeline configuration, so all rules are evaluated. In this scenario, if any of the rules evaluate to True the RuleSet will evalute to True.
- You also may have noticed the "get_time" action was applied during the original test. This is because there is a "get_time" function configured within the Dread.config module and that action is tied to the "ruleset_template" RuleSet within the LogicPipeline. This is how you take actions based on your decisions.
  - If an action is applied but not configured in the Dread.config file, it will still show up in the "actions" within the audit_trail, just nothing will be done, obviously.
  - This can be a very powerful tool. You can also reference the output of actions in other decisions through the "audit_trail". 

#### Conclusions
Wow, that was a lot, but we had to go over it. Hopefully you can start to understand the results of the decision engine, but also start to understand how the decision engine works along with its benefits and limitations. 

# Writing Rules
Writing rules for a Dread decision engine is like writing any logic in python with a few caveats. You can look for conditions, values in lists, apply expressions, compare attributes/expressions, and even apply Dread configured functions directly in rule logic.

- Only attributes and expressions from the DataModel can be used in rules.
- To reference DataModel attributes and expressions simply treat it like a dictionary object with the name "data".
  - EXAMPLE
    - data['example_attribute_str'] will reference the 'example_attribute_str' attribute from our getting started example (data.get('example_attribute_str') will also work).
    - data['example_expression_math'] will reference the 'example_expression_math' expression from our getting started example (data.get('example_expression_math') will also work).
- Be careful with your order of operations. When in doubt use parentheses.
- Be careful with single and double quotes.
- The execution of logic within a Dread decision engine is heavily controlled to prevent misuse. Only methods for the datatypes begin executed are allowed by default (i.e. str.upper) along with a handful of default python libraries.
  - This behavior can be controlled in the Dread.config module by modifying the EXTERNAL_MODULES and ALLOWED_BUILTINS.

Examples of rules
- "data['some_attribute'] >= 5"
- "data['some_attribute'] >= 5 and data['some_attribute'] < 10"
- "(data['some_attribute'] >= 5 and data['some_attribute'] < 10) or (data['some_attribute'] >= 20 and data['some_attribute'] < 30)"
- "data['some_attribute'] == 'some_value'"
- "data['some_attribute'] in data['some_list']"
- "data['some_attribute'].upper() == 'SOME_VALUE'"
- "(data['some_attribute'] / 100) > 1"
- "data['some_attribute'] > data['some_other_attribute']"
- "Dread.functions.some_function(data['some_attribute']) > 1"

# Writing Expressions
Writing expressions for a Dread decision engine is very similar to writing rules and also like writing any expression python with a few caveats.

- Only data from the input dictionary object and prior extracted attributes or expressions from the DataModel can be used in expressions.
- To reference data from the input dictionary objec or DataModel attributes and expressions simply treat it like a dictionary object with the name "data".
  - EXAMPLE
    - data['level1]['level2']['string'] will reference the 'string' field in the input data dictionary from our getting started example.
    - data['example_attribute_str'] will reference the 'example_attribute_str' attribute from our getting started example (data.get('example_attribute_str') will also work).
    - data['example_expression_math'] will reference the 'example_expression_math' expression from our getting started example (data.get('example_expression_math') will also work).
- Be careful with your order of operations. When in doubt use parentheses.
- Be careful with single and double quotes.
- The execution of expressions within a Dread decision engine is heavily controlled to prevent misuse. Only methods for the datatypes begin executed are allowed by default (i.e. str.upper) along with a handful of default python libraries.
  - This behavior can be controlled in the Dread.config module by modifying the EXTERNAL_MODULES and ALLOWED_BUILTINS.

Examples of rules
- "data['some_attribute'] * 10"
- "data['some_attribute'] / data['some_other_attribute']"
- "data['some_attribute'].upper()"
- "Dread.functions.some_function(data['some_attribute'])"

# Advanced - Pure Python Implementation
```
#import Dread decision_engine module
from Dread import decision_engine

##############################################################################
#initiate decision engine
##############################################################################

engine = decision_engine.Engine('foo')

##############################################################################
#add attributes to data model
##############################################################################

#add example_attribute_str attribute
engine.data_model.add_attribute(name='example_attribute_str', 
                                attribute_path = ['level1','level2','string'],
                                dtype = str,
                                default = 'missing')


#add example_attribute_int attribute
engine.data_model.add_attribute(name='example_attribute_int', 
                                attribute_path = ['level1','level2','integer'],
                                dtype = int,
                                default = 0)

#add example_attribute_float attribute using params dictionary
attr_params = {'name':'example_attribute_float',
          'attribute_path': ['level1','level2','float'],
          'dtype': float,
          'default': 0}


engine.data_model.add_attribute(**attr_params)


##############################################################################
#add expressions to data model
##############################################################################

#add example_attribute_str expression
engine.data_model.add_expression(name='example_expression_format_str', 
                                expression = "data['example_attribute_str'].upper()",
                                dtype = str,
                                default = 'MISSING')

#add example_expression_math expression using params dictionary
expr_params = {'name':'example_expression_math',
          'expression': "data['example_attribute_int'] / data['example_attribute_float']",
          'dtype': float,
          'default': 0}

engine.data_model.add_expression(**expr_params)


#print data model
print(engine.data_model.model)

##############################################################################
#add ruleset to logic model
##############################################################################

#add 'rulset_template' ruleset
engine.logic_model.add_ruleset('ruleset_template')

#add 'example_rule1' rule to ruleset
engine.logic_model.model['ruleset_template'].add_rule(name='example_rule1',
                                                     score=100,
                                                     flag='example_flag',
                                                     logic="data['example_attribute_str'] == 'test_data'",
                                                     )

#add 'example_rule1' rule to ruleset using params dictionary
rule_params = {'name':'example_rule2',
          'score': 50,
          'flag': None,
          'logic': "data['example_expression_math'] < 1"}

engine.logic_model.model['ruleset_template'].add_rule(**rule_params)


#print data model
print(engine.logic_model.model)


##############################################################################
#add data pipeline
##############################################################################

#create pipeline
data_pipeline = [
                #attributes
                {'type': 'attributes', 'name': 'example_attribute_str'},
                {'type': 'attributes', 'name': 'example_attribute_int'},
                {'type': 'attributes', 'name': 'example_attribute_float'},
                {'type': 'expressions', 'name': 'example_expression_format_str'},
                {'type': 'expressions', 'name': 'example_expression_math'}
                ]


#add pipeline to engine
engine.add_data_pipeline('data_pipeline_template', data_pipeline)

#print data pipeline
print(engine.data_pipelines)

##############################################################################
#add logic pipeline
##############################################################################

#create pipeline
logic_pipeline = []

logic_pipeline.append({'ruleset':'ruleset_template', 
                   'params':{'action':'get_time', 
                             'score_override':0, 
                             'flag_override':'', 
                             'apply_all':False}})


#add pipeline to engine
engine.add_logic_pipeline('logic_pipeline_template', logic_pipeline)


#print logic pipeline
print(engine.logic_pipelines)

##############################################################################
# Yay, we're done, now let's test it
# testing
##############################################################################

#create test data
test_data = {'level1':{'level2':{'string':'test_data', 'integer':1, 'float':1.5}}}

#run test data through engine
result = engine.execute(test_data)

#print result
print(result)

##############################################################################
# saving and loading decision engine
##############################################################################

import joblib

#save engine to pickle file
joblib.dump(engine, 'foo_engine.pkl')

#delete engine
del engine

#load engine
engine_new = joblib.load('foo_engine.pkl')

#run test data through engine
result_new = engine_new.execute(test_data)

#print result
print(result_new)
```

Coming soon...maybe...you can figure it out, I believe in you
    


