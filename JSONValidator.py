import json

class JsonValidator:
    # doc string 
    """
        Validate JSON file against a given schema file.
        
        :param json_file: Path to the JSON file for validation
        :type json_file: str
        :param schema_file: Path to the schema file for validation
        :type schema_file: str
        :return: True if validation is success, otherwise False
        :type: boolean
        """
    def validate_schema(self, json_file, schema_file):
        try:
            with open(json_file, 'r') as json_data, open(schema_file, 'r') as schema_data:
                json_obj = json.load(json_data)
                schema = json.load(schema_data)
                flag_mutual_count=0

# to validate that the json file having requie fields 
                required_fields = schema.get("required", [])
                for field in required_fields:
                    if field not in json_obj:
                        print(f"Error: Required field '{field}' is not found.")
                        return False

# to validate that at least one of many fields are present
                one_of_fields = schema.get("oneOf", [])
                field_present = any(field in json_obj for field in one_of_fields)
                if not field_present:
                    print(f"Error: At least one of {one_of_fields} must be present.")
                    return False

# to validate either one field or another field present in json file
                either_or_fields = schema.get("eitherOr", [])
                either_fields_present = sum(field in json_obj for field in either_or_fields) == 1
                if not either_fields_present:
                    print(f"Error: Either one of {either_or_fields} must be present..but not all of them")
                    return False
                
# to validate the mutually exclusive fields present in json file
                exclusive_fields = schema.get("exclusiveFields", [])
                if (field in json_obj for field in exclusive_fields):
                    flag_mutual_count+=1
                
                if flag_mutual_count>1:
                    print(f"Error: Mutually exclusive fields {exclusive_fields} found together.")
                    return False

#to validate field value to be one of a set of values in the  json file
                enum_fields = schema.get("enum", {})
                for field, allowed_values in enum_fields.items():
                    if field in json_obj and json_obj[field] not in allowed_values:
                        print(f"Error: Invalid value for field '{field}'. Allowed values are {allowed_values}.")
                        return False

                print(f"The file {json_file} is valid against the schema provided")
                return True
# Handling the exceptions
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"Error: {e}")
            return False