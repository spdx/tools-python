class Package(object):
    """Represents an analyzed Package.
    Fields:
        name : Mandatory, string.
        version: Optional, string.
        file_name: Optional, string.
        supplier: Optional, Organization or Person
        originator: Optional, Organization or Person.
        download_location: Mandatory, URL as string.
    """
    def __init__(self, name, download_location,version="", file_name="", 
            supplier=None, originator=None):
        super(Package, self).__init__()
        self.name = name
        self.version = version
        self.file_name = file_name
        self.supplier = supplier
        self.originator = originator
        self.download_location = download_location