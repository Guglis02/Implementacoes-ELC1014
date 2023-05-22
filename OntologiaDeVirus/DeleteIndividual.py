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

    class BaltimoreGroup(Thing):
        pass

    class GenomeType(Thing):
        pass

    class Host(Species):
        pass

    class Realm(Thing):
        pass

    class Subrealm(Realm):
        pass

    class Kingdom(Subrealm):
        pass

    class Subkingdom(Kingdom):
        pass

    class Phylum(Subkingdom):
        pass

    class Subphylum(Phylum):
        pass

    class Class(Subphylum):
        pass

    class Subclass(Class):
        pass

    class Order(Subclass):
        pass

    class Suborder(Order):
        pass

    class Family(Suborder):
        pass

    class Subfamily(Family):
        pass

    class Genus(Subfamily):
        pass

    class Subgenus(Genus):
        pass

    class HostCategory(Thing):
        pass

    # Propriedades
    class HasForScientificName(DataProperty):
        domain = [Species]
        range = [str]

    class HasForAbbreviatedName(DataProperty):
        domain = [Virus]
        range = [str]

    class FromLineage(ObjectProperty):
        domain = [Virus]
        range = [Realm]

    class FromBaltimoreGroup(ObjectProperty):
        domain = [Virus]
        range = [BaltimoreGroup]
        inverse_property = onto.BelongsToThisGroup

    class HasGenomeType(ObjectProperty):
        domain = [Virus]
        range = [GenomeType]
        inverse_property = onto.BelongsToGenomeType

    class HasHost(ObjectProperty):
        domain = [Virus]
        range = [Host]
        inverse_property = onto.HostThoseVirus

    class HasHostOfThisCategory(ObjectProperty):
        domain = [Virus]
        range = [HostCategory]

    # Propriedadas inversas
    class BelongsToThisGroup(ObjectProperty):
        domain = [BaltimoreGroup]
        range = [Virus]
        inverse_property = onto.FromBaltimoreGroup

    class HasThisGenomeType(ObjectProperty):
        domain = [GenomeType]
        range = [Virus]
        inverse_property = onto.HasGenomeType

    class HostThoseVirus(ObjectProperty):
        domain = [Host]
        range = [Virus]
        inverse_property = onto.HasHost

    for individual in tqdm(Virus.instances()):
        if len(individual.HasHost) < 2:
            if Host("Homo_sapiens") in individual.HasHost:
                print(individual)
            else:
                destroy_entity(individual)
    # Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")

