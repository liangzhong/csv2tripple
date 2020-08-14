import csv
import os
import constant

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

def header():
    return """
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

def url_format(doi):
    # print("%%%%%%" + doi + "%%%%%%%%%\n")
    a, b = doi.split('-', 1)
    return "ttps://digital.lib.usf.edu/?" + a + "." + b 

# https://stackoverflow.com/questions/41059264/simple-csv-to-xml-conversion-python
# print '\n'.join([convert_row(row) for row in data[1:]])

def convert_row(row):
    dic={}

    def providedCHO_dcSubjects(row):
        xml=""
        dic[row[40]] = row[41]
        dic[row[42]] = row[43]
        dic[row[44]] = row[45]
        dic[row[46]] = row[47]
        for k in dic:
            # print(k+" ^^^^^^^ \n")
            if dic[k]:
               xml += """<dc:subject rdf:resource="%s"/>
            """ % (dic[k])
            else:
                xml += """<dc:subject>%s</dc:subject>
            """ % (k)
        return xml
    
    def providedCHO_edmCurrentLocation():
        dic[row[35]] = row[36]
        return"""
            <edm:currentLocation>%s</edm:currentLocation>""" % (row[36])
 
    def convert_providedCHO(row, url, subjects):
        edmCurrentLocation = providedCHO_edmCurrentLocation()
        return """
        <edm:ProvidedCHO rdf:about="%s">
            <dc:creator rdf:resource="%s" />
            <dc:title>%s</dc:title>
            <dc:type>%s</dc:type>
            <dc:description>%s</dc:description>%s<dcterms:extent>%s</dcterms:extent>%s
        </edm:ProvidedCHO>
        """ % (url, row[8], row[1], constant.RESOURCE_TYPE[str(row[9]).lower()], row[16], subjects, constant.DCTERMEXTENT[str(row[12]).lower()], edmCurrentLocation)

    def skos_concept_dccreator(row):
        return """
        <skos:concept rdf:about="%s" >   
            <skos:prefLabel xml:lang="en">%s</skos:prefLabel>
        </skos:concept>
        """ % (row[8], row[7])
    
    # def skos_concept_edmcurrentlocation(row):
    #     return """
    #     <skos:concept rdf:about="%s" >   
    #         <skos:prefLabel xml:lang="en">%s</skos:prefLabel>
    #     </skos:concept>
    #     """ % (row[36], row[35])    

    def skos_concetp_dcsubject(dic):
        xml = ""
        for k in dic:
           if dic[k]:
               xml += """
        <skos:concept rdf:about="%s">
            <skos:prefLabel xml:lang="en">%s</skos:prefLabel>
        </skos:concept>
               """ % (dic[k], k)
        return xml    

    def edm_taxon(row):
        xml=""
        if row[24]:
            dic[row[23]] = "http://www.wikidata.org/entity/" + row[24]
            xml += """<dwc:phylum rdf:resource="http://www.wikidata.org/entity/%s"/>
            """ % (row[24])
        else:
            xml += """<dwc:phylum>%s</dwc:phylum>
            """ % (row[23])

        if row[26]:
            dic[row[25]] = "http://www.wikidata.org/entity/" + row[26]
            xml += """<dwc:class rdf:resource="http://www.wikidata.org/entity/%s"/>
            """ % (row[26])
        else:
            xml += """<dwc:class>%s</dwc:class>
            """ % (row[25])

        if row[28]:
            dic[row[27]] = "http://www.wikidata.org/entity/" + row[28]
            xml += """<dwc:order rdf:resource="http://www.wikidata.org/entity/%s"/>
            """ % (row[28])
        else:
            xml += """<dwc:>%s</dwc:>
            """ % (row[27])

        if row[30]:
            dic[row[29]] = "http://www.wikidata.org/entity/" + row[30]
            xml += """<dwc:family rdf:resource="http://www.wikidata.org/entity/%s"/>
            """ % (row[30])
        else:
            xml += """<dwc:family>%s</dwc:family>
            """ % (row[29])
            
        if row[32]:
            dic[row[31]] = "http://www.wikidata.org/entity/" + row[32]
            xml += """<dwc:genus rdf:resource="http://www.wikidata.org/entity/%s"/>
            """ % (row[32])
        else:
            xml += """<dwc:genus>%s</dwc:genus>
            """ % (row[31])

        if row[34]:
            dic[row[33]] = "http://www.wikidata.org/entity/" + row[34]
            xml += """<dwc:subgenus rdf:resource="http://www.wikidata.org/entity/%s"/>""" % (row[34])
        else:
            xml += """<dwc:subgenus>%s</dwc:subgenus>""" % (row[33])
        return xml    

    def convert_rdfDescription(url, edm_taxon):
        return"""
        <dwc:Organism rdf:about="%s">
            <dwc:vernacularName>%s</dwc:vernacularName>
        </dwc:Organism>
        <dwc:taxon rdf:about="%s">
            <dwc:kingdom>%s</dwc:kingdom>%s
        </dwc:taxon>
        """ %(url, row[20], url, row[22], edm_taxon)

    def edm_WebResource(url):
        return """
        <edm:WebResource rdf:about="%s">
            <edm:rights>TBD</edm:rights>
            <edm:type>%s</edm:type>
        </edm:WebResource>
        """ %(url, constant.RESOURCE_TYPE[str(row[9]).lower()])

    def ore_Aggregation(url):
        return """
        <ore:Aggregation rdf:about="%s">
            <edm:aggregatedCHO rdf:resource="%s" />
            <edm:dataProvider>%s</edm:dataProvider>
            <edm:isShownAt rdf:resource="%s" />
            <edm:datasetName>%s</edm:datasetName>
        </ore:Aggregation>""" %(url, url, row[35], url, row[6])

    ####### top function #########    
    url = url_format(row[4])
    providedCHO_subjects = providedCHO_dcSubjects(row)
    provodedCHO = convert_providedCHO(row, url, providedCHO_subjects)
    edm_taxons = edm_taxon(row)
    rdfDescription = convert_rdfDescription(url, edm_taxons)
    skos_concetp_dccreater = skos_concept_dccreator(row)
    skos_concetp_dcsubjects = skos_concetp_dcsubject(dic)
    edm_webResource = edm_WebResource(url)
    ore_aggregation = ore_Aggregation(url)
    xml = provodedCHO + rdfDescription + skos_concetp_dccreater + skos_concetp_dcsubjects + edm_webResource + ore_aggregation
    
    return xml


###################################################
##    Main program
###################################################


path = '/Users/liangzhong/projects/csv2tripple'
# csv_file = path + '/tmp/' + 'a.csv'
csv_file = path + '/a.csv.bak'
dir = path + '/tmp/out/'

# print ('\n'.join([convert_row(row) for row in read_file(csv_file)]))

header=header()
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
print ("    </rdf:RDF>")