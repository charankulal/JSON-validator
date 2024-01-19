import JSONValidator
validator = JSONValidator.JsonValidator()
result=validator.validate_schema('example.json', 'example_schema.json')
print(result)