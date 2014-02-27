from lxml import etree
from hashlib import sha384

class XMLClientPackage(object):

    @staticmethod
    # arguments is a list
    def client_package(version, opcode, arguments):
        # create XML
        root = etree.Element('request')

        version_elm = etree.Element('version')
        version_elm.text = str(version)
        root.append(version_elm)

        opcode_elm = etree.Element('opcode')
        opcode_elm.text = str(opcode)
        root.append(opcode_elm)

        if len(arguments) > 0:
            arguments_elm = etree.Element('arguments')

            for arg in arguments:
                arg_elm = etree.Element('arg')
                arg_elm.text = str(arg)
                arguments_elm.append(arg_elm)

            root.append(arguments_elm)

        # get a checksum of everything without checksum tag
        pre_checksum = etree.tostring(root)
        checksum = sha384(pre_checksum)

        checksum_elm = etree.Element('checksum')
        checksum_elm.text = checksum.hexdigest()
        root.append(checksum_elm)

        s = etree.tostring(root)

        return s