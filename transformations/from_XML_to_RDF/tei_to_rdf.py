from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import DC, RDF, FOAF, XSD
from rdflib import Namespace

SCHEMA = Namespace("http://schema.org/")

# get the xml
xml_file = 'transformations/from_XML_to_HTML/dialogo.xml'

# parse the xml with lxml and find the root (TEI)
tree = etree.parse(xml_file)
root = tree.getroot()

# create an empty graph
g = Graph()

# personalized namespace for our item
EX = Namespace("http://example.org/dialogo/")

g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("ex", EX)

# define the tei namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# find the title element
title_elem = root.find('.//tei:title', namespaces=ns)
title_text = title_elem.text if title_elem is not None else "Titolo sconosciuto"

# create an uri for our item
doc_uri = EX['dialogo']

# adding the first rdf: relation between the document uri and its title taken directly from tei:title
g.add((doc_uri, DC.title, Literal(title_text)))

# estract the author name
author_elem = root.find('.//tei:author/tei:persName', namespaces=ns)
if author_elem is not None:
    # take forename and surname
    forename = author_elem.find('tei:forename', namespaces=ns)
    surname = author_elem.find('tei:surname', namespaces=ns)
    if forename is not None and surname is not None:
        author_name = f"{forename.text} {surname.text}"
        author_uri = EX['galileo']

        # adding another node to our rdf: our author uri as a FOAF:person and its name take directly from tei:author/tei:persName
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author_name)))
        # adding another rdf connecting the document uri to the author uri, its creator
        g.add((doc_uri, DC.creator, author_uri))

# looking for the publishing date inside the editionStmt
date_elem = root.find('.//tei:editionStmt/tei:edition/tei:date', namespaces=ns)
if date_elem is not None:
    date_val = date_elem.get('when') or date_elem.text
    # adding the publishing date to our graph: our document uri and its date expressed in years
    g.add((doc_uri, DC.date, Literal(date_val, datatype=XSD.gYear)))

# find the encoders
enc_elems = root.findall('.//tei:respStmt/tei:persName', namespaces=ns)
if enc_elems is not None:
    enc_elem1 = enc_elems[0]
    enc_elem2 = enc_elems[1]

    enc_uri1 = EX[enc_elem1.text.replace(" ", "")]
    g.add((enc_uri1, RDF.type, FOAF.Person))
    g.add((enc_uri1, FOAF.name, Literal(enc_elem1.text)))
    g.add((enc_uri1, SCHEMA.hasOccupation, SCHEMA.Role))
    g.add((SCHEMA.Role, RDF.type, enc_uri1))

    enc_uri2 = EX[enc_elem1.text.replace(" ", "")]
    g.add((enc_uri2, RDF.type, FOAF.Person))
    g.add((enc_uri2, FOAF.name, Literal(enc_elem1.text)))
    g.add((doc_uri, enc_uri1))


# saving the file in the chosen destination
g.serialize(destination="from_XML_to_RDF/dialogo.ttl", format="turtle")
