import csv
import os

# return a list of list, slicing the first row
def read_file(file):
    entries_list=[]
    try:
        with open(file, mode='r',encoding='utf-8') as file_reader:
            # entries_list = [line.strip().split(',') for line in lines]
            lines = csv.reader(file_reader, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            entries_list = [line for line in lines]
    except Exception as e:
        print(e)
        exit(-1)
    # finally:
    return entries_list[1:]

# https://stackoverflow.com/questions/41059264/simple-csv-to-xml-conversion-python

# def convert_row(row):
#     return """<movietitle="%s">
#     <type>%s</type>
#     <format>%s</format>
#     <year>%s</year>
#     <rating>%s</rating>
#     <stars>%s</stars>
#     <description>%s</description>
# </movie>""" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])

# print '\n'.join([convert_row(row) for row in data[1:]])


def convert_row(row):
    return """
<edm:ProvidedCHO rdf:about="%s">
<dcterms:creator rdf:resource="%s" />
<dcterms:title>%s</dcterms:title>
<dcterms:subject rdf:resource="%s" />
<dcterms:extent>1 color photo[check physical_description to determine]</dcterms:extent>
<edm:type>image[check Resource_type to determine]</edm:type>
<dcterms:description>%s</dcterms:description>
<dcterms:spatial rdf:resource="http://vocab.getty.edu/tgn/7012149" /> 

<dwc:organismName>%s]</dwc:organismName>
<dwc:kingdom>%s</dwc:kingdom>
<dwc:phylum>%s</dwc:phylum>
<dwc:class>%s</dwc:class>
<dwc:order rdf:resource="http://id.loc.gov/authorities/subjects/sh85022628" />
<dwc:family>%s</dwc:family>
<dwc:genus>%s</dwc:genus>
<dwc:subgenus>%s</dwc:subgenus>

</edm:ProvidedCHO>

<edm:WebResource rdf:about="%s">
<edm:rights>TBD</edm:rights>
</edm:WebResource>

<ore:Aggregation rdf:about="%s">
<edm:aggregatedCHO rdf:resource="USFLDC:A64-01041-box8-folder5" />
<edm:dataProvider>University of South Florida Libraries</edm:dataProvider>
<edm:isShownAt rdf:resource="%s" />
</ore:Aggregation>
    """ % (row[0], row[8], row[1], row[38], row[16], row[20], row[22], row[23], 
        row[25], row[29], row[31], row[33], row[0], row[0], row[0])


# def convert_row(row):
#     return """
    
# <?xml version="1.0" encoding="UTF-8"?>
# <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
# xmlns:dc="http://purl.org/dc/elements/1.1"
# xmlns:dcterms="http://http://purl.org/dc/terms"
# xmlns:edm="http://www.europeana.eu/schemas/edm"
# xmlns:skos="http://www.w3.org/2004/02/skos/core#"
# xmlns:owl="http://www.w3.org/2002/07/0wl#"
# xmlns:ore="http://www.openarchives.org/ore/terms/"
# xmlns:rdfs= "http://www.w3.org/2000/01/rdf-schema#"
# xmlns:dwc= "http://rs.tdwg.org/dwc/terms/">

# <edm:ProvidedCHO rdf:about="%s">
# <dcterms:creator rdf:resource="%s" />
# <dcterms:title>%s</dcterms:title>
# <dcterms:subject rdf:resource="%s" />
# <dcterms:extent>1 color photo[check physical_description to determine]</dcterms:extent>
# <edm:type>image[check Resource_type to determine]</edm:type>
# <dcterms:description>%s</dcterms:description>
# <dcterms:spatial rdf:resource="http://vocab.getty.edu/tgn/7012149" /> 

# <dwc:organismName>%s]</dwc:organismName>
# <dwc:kingdom>%s</dwc:kingdom>
# <dwc:phylum>%s</dwc:phylum>
# <dwc:class>%s</dwc:class>
# <dwc:order rdf:resource="http://id.loc.gov/authorities/subjects/sh85022628" />
# <dwc:family>%s</dwc:family>
# <dwc:genus>%s</dwc:genus>
# <dwc:subgenus>%s</dwc:subgenus>

# </edm:ProvidedCHO>

# <edm:WebResource rdf:about="%s">
# <edm:rights>TBD</edm:rights>
# </edm:WebResource>

# <ore:Aggregation rdf:about="%s">
# <edm:aggregatedCHO rdf:resource="USFLDC:A64-01041-box8-folder5" />
# <edm:dataProvider>University of South Florida Libraries</edm:dataProvider>
# <edm:isShownAt rdf:resource="%s" />
# </ore:Aggregation>

# </rdf:RDF>
    
#     """ % (row[0], row[8], row[1], row[38], row[16], row[20], row[22], row[23], 
#         row[25], row[29], row[31], row[33], row[0], row[0], row[0])


path = '/Users/liangzhong/projects/csv2tripple'
csv_file = path + '/' + 'a.csv'
dir = path + '/tmp/out/'

# print ('\n'.join([convert_row(row) for row in read_file(csv_file)]))

header="""
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:dc="http://purl.org/dc/elements/1.1"
xmlns:dcterms="http://http://purl.org/dc/terms"
xmlns:edm="http://www.europeana.eu/schemas/edm"
xmlns:skos="http://www.w3.org/2004/02/skos/core#"
xmlns:owl="http://www.w3.org/2002/07/0wl#"
xmlns:ore="http://www.openarchives.org/ore/terms/"
xmlns:rdfs= "http://www.w3.org/2000/01/rdf-schema#"
xmlns:dwc= "http://rs.tdwg.org/dwc/terms/">
"""
# first_flage = True
# if not os.path.isdir(dir):
#     os.mkdir(dir)
# for row in read_file(csv_file):
#     out_file_name = dir + row[4] + '.rdf'
#     with open(out_file_name, 'w') as f:
#         if first_flage:
#             print(header)
#         print(convert_row(row), file=f)
#     first_flage = False

print (header)
print ('\n'.join([convert_row(row) for row in read_file(csv_file)]))
print ("</rdf:RDF>")