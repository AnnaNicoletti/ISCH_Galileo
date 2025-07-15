from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import DC, RDF, FOAF, XSD, DCTERMS

SCHEMA = Namespace("http://schema.org/")
EX = Namespace("http://example.org/dialogo/")

g = Graph()
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("schema", SCHEMA)
g.bind("ex", EX)

tree = etree.parse('transformations/from_XML_to_HTML/dialogo.xml')
root = tree.getroot()
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

doc_uri = EX['dialogo']

# Titolo
title_elem = root.find('.//tei:titleStmt/tei:title', namespaces=ns)
if title_elem is not None:
    g.add((doc_uri, DC.title, Literal(title_elem.text)))

# Autore
author_elem = root.find('.//tei:author/tei:persName', namespaces=ns)
if author_elem is not None:
    forename = author_elem.find('tei:forename', namespaces=ns)
    surname = author_elem.find('tei:surname', namespaces=ns)
    viaf_id = author_elem.find('tei:idno[@type="VIAF"]', namespaces=ns)
    if forename is not None and surname is not None:
        author_name = f"{forename.text} {surname.text}"
        author_uri = URIRef(viaf_id.text) if viaf_id is not None else EX['galileo']
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author_name)))
        g.add((doc_uri, DC.creator, author_uri))

# Editor
editor_elem = root.find('.//tei:editor/tei:persName', namespaces=ns)
if editor_elem is not None:
    editor_uri = EX[editor_elem.text.replace(" ", "")]
    g.add((editor_uri, RDF.type, FOAF.Person))
    g.add((editor_uri, FOAF.name, Literal(editor_elem.text)))
    g.add((doc_uri, DC.contributor, editor_uri))

# Data pubblicazione
date_elem = root.find('.//tei:editionStmt/tei:edition/tei:date', namespaces=ns)
if date_elem is not None:
    date_val = date_elem.get('when') or date_elem.text
    g.add((doc_uri, DC.date, Literal(date_val, datatype=XSD.gYear)))

# Licenza
licence_elem = root.find('.//tei:licence', namespaces=ns)
if licence_elem is not None and licence_elem.get('target'):
    g.add((doc_uri, DCTERMS.license, URIRef(licence_elem.get('target'))))

# Encoder
enc_elems = root.findall('.//tei:respStmt/tei:persName', namespaces=ns)
for enc_elem in enc_elems:
    enc_name = enc_elem.text
    enc_uri = EX[enc_name.replace(" ", "")]
    g.add((enc_uri, RDF.type, FOAF.Person))
    g.add((enc_uri, FOAF.name, Literal(enc_name)))

    role = BNode()
    g.add((role, RDF.type, SCHEMA.Role))
    g.add((role, SCHEMA.roleName, Literal("Encoder")))
    g.add((role, SCHEMA.performedBy, enc_uri))
    g.add((doc_uri, SCHEMA.hasContributor, role))

# Personaggi
persons = root.findall('.//tei:listPerson/tei:person', namespaces=ns)
for p in persons:
    xml_id = p.get('{http://www.w3.org/XML/1998/namespace}id')
    role = p.get('role')
    char_uri = EX[xml_id]
    g.add((char_uri, RDF.type, FOAF.Person))
    g.add((char_uri, SCHEMA.roleName, Literal(role)))

# --- Aggiunte interessanti ---

# Publisher e luogo di pubblicazione (publicationStmt)
pub_place = root.find('.//tei:publicationStmt/tei:pubPlace', namespaces=ns)
publisher = root.find('.//tei:publicationStmt/tei:publisher', namespaces=ns)

if publisher is not None:
    g.add((doc_uri, DC.publisher, Literal(publisher.text)))
if pub_place is not None:
    g.add((doc_uri, SCHEMA.location, Literal(pub_place.text)))

# Source description - bibliographic source (sourceDesc/bibl)
bibl = root.find('.//tei:sourceDesc/tei:bibl', namespaces=ns)
if bibl is not None:
    bibl_id = bibl.get('{http://www.w3.org/XML/1998/namespace}id', 'source1')
    bibl_uri = EX[bibl_id]
    g.add((bibl_uri, RDF.type, SCHEMA.Book))

    # Titolo della fonte bibliografica
    bibl_title = bibl.find('tei:title', namespaces=ns)
    if bibl_title is not None:
        g.add((bibl_uri, DC.title, Literal(bibl_title.text)))

    # Autore della fonte
    bibl_author = bibl.find('tei:author/tei:persName', namespaces=ns)
    if bibl_author is not None:
        forename = bibl_author.find('tei:forename', namespaces=ns)
        surname = bibl_author.find('tei:surname', namespaces=ns)
        if forename is not None and surname is not None:
            bibl_author_name = f"{forename.text} {surname.text}"
            bibl_author_uri = EX['biblAuthor']
            g.add((bibl_author_uri, RDF.type, FOAF.Person))
            g.add((bibl_author_uri, FOAF.name, Literal(bibl_author_name)))
            g.add((bibl_uri, DC.creator, bibl_author_uri))

    # Editore della fonte
    bibl_publisher = bibl.find('tei:publisher', namespaces=ns)
    if bibl_publisher is not None:
        g.add((bibl_uri, DC.publisher, Literal(bibl_publisher.text)))

    # Luogo di pubblicazione della fonte
    bibl_pub_place = bibl.find('tei:pubPlace', namespaces=ns)
    if bibl_pub_place is not None:
        g.add((bibl_uri, SCHEMA.location, Literal(bibl_pub_place.text)))

    # Data pubblicazione fonte
    bibl_date = bibl.find('tei:date', namespaces=ns)
    if bibl_date is not None:
        bibl_date_val = bibl_date.get('when') or bibl_date.text
        g.add((bibl_uri, DC.date, Literal(bibl_date_val, datatype=XSD.gYear)))

    # Collegamento tra documento e fonte bibliografica
    g.add((doc_uri, DCTERMS.isReferencedBy, bibl_uri))

# Salva file
g.serialize(destination="transformations/from_XML_to_RDF/dialogo.ttl", format="turtle")