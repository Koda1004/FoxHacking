from lxml import etree
from hashlib import sha384

class XMLPackage(object):

    # isError indicates if value is an error or not
    @staticmethod
    def server_package(version, status, value, isError):
        # create XML
        root = etree.Element('request')

        version_elm = etree.Element('version')
        version_elm.text = str(version)
        root.append(version_elm)

        status_elm = etree.Element('status')
        status_elm.text = str(status)
        root.append(status_elm)

        if isError:
            message_elm = etree.Element('error')
        else:
            message_elm = etree.Element('value')
        message_elm.text = str(value)
        root.append(message_elm)

        without_checksum = etree.tostring(root)

        # get a checksum of everything without checksum tag
        pre_checksum = etree.tostring(root)
        checksum = sha384(pre_checksum)

        checksum_elm = etree.Element('checksum')
        # convert binary to hex
        checksum_elm.text = checksum.hexdigest()
        root.append(checksum_elm)

        s = etree.tostring(root)

        return s
