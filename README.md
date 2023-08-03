# Dread
Dread (Decision Rule Engine for Actioning Data) is a python package for creating, managing, executing a pythonic rule engine to make data driven decisions and take actions on those decisions.

Please note, this documentation is still a work in progress...

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
L1 - DataModel
        L2 - Attributes
        L2 - Expressions
L1 - DataPipelines
L1 - LogicModel
        L2 - RuleSet
                L3 - Rule
L1 - LogicPipelines

#### Decision Engine Components
- **DataModel** - The DataModel is an object comprised of attributes and expressions. It is meant to provide the means to extract, transform, and format data within the input dictionary object to make it suitable for the LogicModels. Only data extracted by the DataModel can be used within the LogicModel.
  - Attributes - Attributes are objects that extract and format data from the input dictionary object. Attributes can "climb the tree" of the dictionary object by specifying the path as a list. (I tried dot notation, but couldn't quite get it to work without more dependencies, but's effectively the same thing in list format)
  - Expressions - Expressions are objects that take data from the input dictionary object or attributes and do something with it to create an output. They can apply Dread configured functions (see Dread component Dread.functions below), logic, do math, and make other maniupuations to get the input data in the desired format. Although expressions are used within a try/except block, they are to be used with caution and tested thoroughly.
- **DataPipelines** - DataPipelines control what attributes and expressions from the DataModel are executed along with their priority. Attributes and Expressions must exist in a DataPipeline in order to be used by the LogicModel.
- **LogicModel**  - The LogicModel is an object comprised of RuleSets, which are comprised of Rules. It holds all of the logic that gets applied within the decision engine. There can be many RuleSets within a LogicModel.
  - RuleSet - RuleSets are objects comprised of Rule objects kept in priority order.
     - Rule - Rules are objects that contain the core logic being executed within the decision engine along with any associated score values and flags that are applied when evaluated to True. 
- **LogicPipelines** - LogicPipelines control what RuleSets from the LogicModel are executed along with their priority. A RuleSet must exist in a LogicPipeline in order to be used by the LogicModel.

#### Other Dread Modules
- **Dread.config** - Used to configure decision engine and its execution.
- **Dread.functions** - Used as a placeholder to put custom functions which can use other packages and libraries.
- **Dread.utils** - Utility functions for the Dread package.

# Getting Started

Dread can be used within any .py file to build and configure decision engines, however this can be cumbersome and on the more advanced side, so there is a built-in file based approach to make building and configuring decision engines easier. It is suggested you use the file based approach first and then go from there. I'm a big proponent of learning by doing, so let's do something.

### File Based

#### Notes on File Based Approach

The file based approach keeps all of the configurations for the decision engine in .csv files. These files can be manipulated followed by an engine build to generate a new decision engine. The required files must keep a particular structure in order for the engine build process to work properly.

#### File types and Formating by directory

***Any filename wrapped in square brackets means the name of the file is dynamic and can change. This generally because of the one to many relationshp for the objects within the decision engine. The only filenames that CANNOT change are those within the DataModel directory. The attributes.csv and expressions.csv files.***

DataModel - Files in the /DataModel directory are used to create the DataModel within the decision engine. The names of these files CANNOT change.
 - attributes.csv
 - expressions.csv
DataPipelines - Files in the /DataPipelines directory create the data pipeline objects within the decision engine. The filenames can change and will become the name of the pipeline within the decision engine. 
 - [DATA_PIPELINE_NAME].csv
LogicModel - Files in the /LogicModel directory are used to create the LogicModel within the decision engine. The filenames can change and will become the name of the pipeline within the decision engine. 
- [RULESET_NAME].csv
LogicPipelines- Files in the /LogicPipeline directory create the logic pipelines for the decision engine. The filenames can change and will become the name of the pipeline within the decision engine. 
- ['LOGIC_PIPELINE_NAME'].csv - Files in the DataPipeline directory create the data pipelines for the decision engine. The filenames can change and become the name of the pipeline within the decision engine.  

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
...Please specify NAME for decision engine (REQUIRED): test_engine
...Please specify DIRECTORY for build configuration files (ENTER to skip and use current directory): [ENTER]

OUTPUT:
Creating directories for build configuration files for test_engine decision engine
Creating template files for build configuration files for test_engine decision engine
Directories and template files created for test_engine
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
        5:) From python, build decision engine which will create the decision engine file test_engine.pkl
                - "from Dread.engine_build import build"
                - "build('test_engine')"
        Yay, your first decision engine was built, now it's time to test it.
        6:)From python, test rule engine against test files in the TestData directory
                - 'Dread.engine_test.test' requires JSON formatted data which is read into a python dictionary object which the engine accepts
                - The outputs from the test execution will be placed in the /TestData/TestResults directory
                - "from Dread.engine_test import test"
                - "test('test_engine')"
```

#### 4.) Build your first decision engine. 

Follow the steps in the README.txt file. There are template files provided in the associated directories and the 'Templates' directory to make this easier. You can build your first engine only using these files.

from python, run ...
```
from Dread.engine_build import build

build('test_engine')

OUTPUT:
Building test_engine decision engine from 'test_engine'
Engine intitiated
        Configuring DataModel
                Attribute 'example_attr_name' added to data model
                Expression 'example_expr_name' added to data model
        Configuring LogicModel
                RuleSet 'ruleset_template' added to LogicModel
        Configuring DataPipelines
                DataPipeline 'data_pipeline_template' added to Engine
        Configuring LogicPipelines
                LogicPipeline 'logic_pipeline_template' added to Engine
Engine build complete
Engine saved to 'test_engine/test_engine_engine.pkl'
```

Congrats, you built your first Dread decision engine. You can see your new engine in a serialized pickle file within your directory. When you finally go to use your decision engine, this is the file you will import to create your Engine object. You can then execute this engine to apply your data and logic models on new data, but we'll get to that.

#### 5.) Test your newly created decision engine.

Follow the steps in the README.txt file. There is already a template test file 'template_test_data.json' provided in the TestData directory to make this easier. You can test your first engine only using this file.

from python, run ...
```
from Dread.engine_test import test

test('test_engine')

OUTPUT:
Testing decision engine 'test_engine' against files in 'test_engine/TestData'
Test file 'template_test_data.json' processed
Decision engine testing complete, navigate to '/TestResults' directory to review results of test files
```

#### Examine Results
Cool, test complete. So what the f*ck just happened?

First, when the test script is run, it simply imports your engine, executes it on the data data, and writes the output back out as a .json file. The test data files are .json files, but when read in with the json.loads() method it creates a python dictionary object. ***IMPORTANT: The Dread decision engine always expects the input to be a python dictionary object***.

Now that we know what happened, let's talk about the test results. If you open and format the result "result_template_test_data.json" file, you will see a hierarchy appear. I'll do my best to explain this. Since this is JSON, I will use dot notation to refer to specific places in the JSON object.

#### Decision Engine Output
- **.input** - This is the raw imput the decision engine recieved. It will look exactly like the data in the 'template_test_data.json' file.
- **.processed_data** - This is the data after it is processed by the data pipeline. I will explain exactly how this works below, but this is ultimately the data that is fed into the decision engine.
  - .processed_data.datamodel_errors - This is a list that captures any errors while processing the components of your data model.
  - .processed_data.pipeline_errors - This is a list that captures any fatal data pipeline errors, meaning the entire data pipeline fails for some reason. Hopefully you never see anything in here, but if you do, something bad happened.
  - .processed_data.example_attr_name - This is an attribute extracted from your input data. In this case we simply extracted the data in the "level3" file of the input data.
  - .processed_data.example_expr_name - This is an expression extracted from your input data. In this case we simply applied the str.upper() method on the attribute "example_attr_name"
  - .processed_data.audit_trail - This is the audit trail from the decision engine. It exists here so you can refer to prior rules, actions, flags, and other components of the DataPipelines and LogicPipelines as the decision engine is processing. This can be a very powerful tool and allow you to chain decisions and actions together.
- **.audit_trail** - As mentioned above, this is the audit trail from the decision engine. It shows the final results of the decision engine on the input data.
  - .audit_trail.result - The final result of the decision engine. It is a boolean value indicating if any rule within the decision engine was triggered. A value of "True" means at least one rule was triggered.
  - .audit_trail.actions - A list of actions trigged by the decision engine. Actions are functions configured in the Dread.config module. Actions can be optionally tied to rulesets. If a rule in a ruleset is triggered, the action will be taken.
  - .audit_trail.action_results - An object of executed actions and their name, parameters, results, and output.
  - .audit_trail.score - This is the summation of all "scores" for executed rules and/or rulesets. You can assign a score to both rules and rulesets when configuring the decision engine.
  - .audit_trail.flags - This is a list of all "flags" for executed rules and/or rulesets. You can assign a flag to both rules and rulesets when configuring the decision engine. Flags can help you identify specific scenarios you may be interest in.
  - .audit_trail.LogicPipelines - An object of all Logic Pipelines executed within the decision engine and their results. The resulting LogicPipeline attributes are mostly the same as the attributes within the top level of .audit_trail, just broken down by pipeline, so I will only go over any differences.
    -  .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].errors - This is a list that captures any errors that occured while processing the LogicPipeline.
    -  .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets - An object of all rulesets executed within the LogicPipeline. The resulting ruleset attributes are mostly the same as the attributes within the top level of .audit_trail and .LogicPipelines sections, just broken down by pipeline, so I will only go over any differences.
      - .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets.[RULESET_NAME].errors - This is a list that captures any errors that occured while processing the ruleset.
      - .audit_trail.LogicPipelines.[LOGIC_PIPELINE_NAME].rulesets.[RULESET_NAME].rules - An object of all rules executed within the ruleset. The rule attributes should be pretty self explainatory at this point.

#### Conclusions
Wow, that was a lot, but I had to go over it. Hopefully you can start to understand the results of the decision engine, but also start to understand how the decision engine works along with its benefits and limitations. 

# Advanced - Pure Python Implementation

Coming soon...maybe...you can figure it out, I believe in you
    


