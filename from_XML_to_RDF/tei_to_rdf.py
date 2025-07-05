from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import DC, RDF, FOAF, XSD

# Percorso file XML (modifica se serve)
xml_file = 'from_XML_to_HTML/dialogo.xml'

# Parsing XML con lxml
tree = etree.parse(xml_file)
root = tree.getroot()

# Creo un grafo RDF
g = Graph()

# Namespace personalizzato per la risorsa (ipotizziamo URI base)
EX = Namespace("http://example.org/dialogo/")

g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("ex", EX)

# Estraggo il titolo dal TEI (path xpath)
# Nota: XML ha namespace, per semplicità definiamo un dict
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

title_elem = root.find('.//tei:title', namespaces=ns)
title_text = title_elem.text if title_elem is not None else "Titolo sconosciuto"

# Creo URI per il documento
doc_uri = EX['dialogo']

# Aggiungo titolo come proprietà DC:title
g.add((doc_uri, DC.title, Literal(title_text)))

# Estraggo autore (per semplicità il primo autore)
author_elem = root.find('.//tei:author/tei:persName', namespaces=ns)
if author_elem is not None:
    # Provo a prendere nome e cognome
    forename = author_elem.find('tei:forename', namespaces=ns)
    surname = author_elem.find('tei:surname', namespaces=ns)
    if forename is not None and surname is not None:
        author_name = f"{forename.text} {surname.text}"
        author_uri = EX['galileo']
        # Aggiungo autore come FOAF:Person
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author_name)))
        # Collegamento autore - documento
        g.add((doc_uri, DC.creator, author_uri))

# Estraggo anno edizione (dalla data in editionStmt)
date_elem = root.find('.//tei:editionStmt/tei:edition/tei:date', namespaces=ns)
if date_elem is not None:
    date_val = date_elem.get('when') or date_elem.text
    g.add((doc_uri, DC.date, Literal(date_val, datatype=XSD.gYear)))

# Salvo il grafo RDF in formato Turtle
g.serialize(destination="dialogo.ttl", format="turtle")

print("File RDF dialogo.ttl creato con successo!")