import os
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# 1. Cartella dove si trovano i CSV
csv_folder = "transformations/from_CSV_to_RDF/CSV_items"

# 2. Dizionario dei namespace usati
BASE = Namespace('https://galileoarchive.org/ISCHGalileo/')
namespaces = {
    "crm": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "owl": OWL,
    "schema": Namespace("http://schema.org/"),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
    "rdf": RDF
}

# Creazione del grafo RDF
g = Graph()
for prefix, ns in namespaces.items():
    g.bind(prefix, ns)

def clean_pred(predicate):
    prefix, local = predicate.split(":", 1)
    return namespaces[prefix][local]

def clean_obj(object):
    object = object.strip().strip('"').strip()
    if ":" in object and not object.startswith("http"):
        prefix, local = object.split(":", 1)
        if prefix in namespaces:
            return namespaces[prefix][local]
    if object.startswith("http"):
        return URIRef(object)
    return Literal(object) 


#lista CSV
all_csv = os.listdir(csv_folder)
all_path = []

for file in all_csv:
    all_path.append(os.path.join(csv_folder,file).replace("\\", "/"))

for file in all_path:
    df = pd.read_csv((file), sep=";", encoding="latin1")
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    for index, row in df.iterrows():
        subj = URIRef(row["subject"])
        pred = clean_pred(row["predicate"])
        obj = clean_obj(row["object"])
        g.add((subj, pred, obj))
    

# 6. Serializzazione finale
output_file = "transformations/from_CSV_to_RDF/output.ttl"
g.serialize(destination=output_file, base=BASE, format="turtle")

print(f"Conversione completata. RDF salvato in: {output_file}")
