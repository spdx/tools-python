import xmltodict
from spdx import document
from spdx.parsers import jsonyamlxml
from collections import OrderedDict

class Parser(jsonyamlxml.Parser):
    """
    Wrapper class for jsonyamlxml.Parser to provide an interface similar to 
    RDF and TV Parser classes (i.e., spdx.parsers.<format name>.Parser) for XML parser.
    It also avoids to repeat jsonyamlxml.Parser.parse code for JSON, YAML and XML parsers
    """    
    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)
        self.LIST_LIKE_FIELDS = {
            'creators', 'externalDocumentRefs', 'extractedLicenseInfos', 
            'seeAlso', 'annotations', 'snippets', 'licenseInfoFromSnippet', 'reviewers', 'fileTypes', 
            'licenseInfoFromFiles', 'artifactOf', 'fileContributors', 'fileDependencies', 
            'excludedFilesNames', 'files', 'documentDescribes'
        }

    def parse(self, file):
        parsed_xml = xmltodict.parse(file.read(), strip_whitespace=False)
        fixed_object = self._set_in_list(parsed_xml, self.LIST_LIKE_FIELDS)
        self.document_object = fixed_object.get('SpdxDocument').get('Document')
        return super(Parser, self).parse()

    def _set_in_list(self, data, keys):
        """
        xmltodict parse list-like fields in different way when there is only one 
        of them than when there are several of them.
        Set in lists those fields that are expected to be in them.
        """
        if isinstance(data, dict):
            new_data = OrderedDict()
            for k, v in data.items():
                if k in keys and not isinstance(v, list):
                    new_data[k] = [self._set_in_list(v, keys)]
                else:
                    new_data[k] = self._set_in_list(v, keys)
            return new_data
        elif isinstance(data, list):
            new_data = []
            for element in data:
                new_data.append(self._set_in_list(element, keys))
            return new_data
        return data
