import ruamel.yaml as yaml
from spdx.parsers import jsonyaml

class Parser(jsonyaml.Parser):
    """
    Wrapper class for jsonyaml.Parser to provide an interface similar to 
    RDF and TV Parser classes (i.e., spdx.parsers.<format name>.Parser) for YAML parser.
    It also avoids to repeat jsonyaml.Parser.parse code for JSON and YAML parsers
    """
    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)
    
    def parse(self, file):
        self.document_object = yaml.safe_load(file).get('Document')
        return super(Parser, self).parse()