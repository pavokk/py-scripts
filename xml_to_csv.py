import xml.etree.ElementTree as EL
import pandas as pd

# If the xml-file contains url-encoding we use the function unquote from urllib
import urllib.parse


def get_xml_columns(sourcefile: str) -> list:

    """
    Adds all tags from XML-file to a list
    :param sourcefile: String of relative or full path to xml-file
    :return: List with all unique tags
    """

    tree = EL.parse(sourcefile)
    output_cols = []

    for elem in tree.iter():
        output_cols.append(elem.tag)

    # now I remove duplicities - by conversion to set and back to list
    output_cols = list(set(output_cols))

    return output_cols


def xml_to_csv(sourcefile: str) -> pd.DataFrame:

    """
    Tries to convert an XML-file to a pandas Dataframe. Can get messy if file has lots of nesting.
    :param sourcefile: String of relative or full path to xml-file
    :return: Pandas Dataframe with tags as columns, each iteration as rows.
    """

    cols = get_xml_columns(sourcefile)
    rows = []
    tree = EL.parse(sourcefile)
    root = tree.getroot()

    for product in root:
        dictlist = {}
        for tag in cols:
            if product.find(tag) is None:
                dictlist[tag] = ""
            else:
                content = product.find(tag).text

                if isinstance(content, str):
                    dictlist[tag] = urllib.parse.unquote(content.replace("+", " "))
                else:
                    dictlist[tag] = content

        rows.append(dictlist)

    return pd.DataFrame(rows, columns=cols)


if __name__ == '__main__':
    xml_to_csv('data/xml/oslobunaden.xml').to_csv('data/output/oslobunaden-links.csv', index=False)
