validator
=========

A simple python3 script which validates a yaml model against a schema (as shown in the diagram below) by:

1. reading a **yaml model** from stdin,
2. determining the top-level **schema** attribute,  
3. searching for a matching **json-schema** in the schema subdirectory and
4. validating the model against the schema.



````
               schema/<schema>.json
                     |
                     |
                     v
yaml (schema) ==> validate.py ==> List of errors

````

Errors are reported to stdout and lead to a return code 1.
The script will send a return code 0 if no errors are encountered.

To invoke the validator issue following command:

````
> cat model.yml | ./validate.py
````

Author: Bernard Tsai (bernard@tsai.eu)
