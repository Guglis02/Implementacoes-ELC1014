from bs4 import BeautifulSoup
from owlready2 import *
from tqdm import tqdm
import openpyxl
from unidecode import unidecode

# Criação/Carregamento da ontologia
onto = get_ontology("file://virus_host_ontology.owl").load()

with onto:
    # Classes
    class Species(Thing):
        pass

    class Virus(Species):
        pass

    # Propriedades
    class HasForScientificName(DataProperty):
        domain = [Species]
        range = [str]

    class HasForAbbreviatedName(DataProperty):
        domain = [Virus]
        range = [str]

    for individual in tqdm(Virus.instances()):
        if individual.HasForAbbreviatedName == [''] or []:
            print(individual.HasForAbbreviatedName)
            individual.HasForAbbreviatedName.remove(individual.HasForAbbreviatedName.first())
        if len(individual.HasForAbbreviatedName) > 1:
            print(individual.HasForAbbreviatedName)
            individual.HasForAbbreviatedName.remove(individual.HasForAbbreviatedName.first())
    # Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")

