from bs4 import BeautifulSoup
from owlready2 import *
from tqdm import tqdm
import openpyxl
from unidecode import unidecode

# Criação/Carregamento da ontologia
onto = get_ontology("file://virus_host_ontology.owl").load()

def GetLineage(entry):  
    if "viria" in entry:
        return (Realm(entry))
    elif "vira" in entry:
        return (Subrealm(entry))
    elif "virae" in entry:
        return (Kingdom(entry))
    elif "virites" in entry:
        return (Subkingdom(entry))
    elif "viricota" in entry:
        return (Phylum(entry))
    elif "viricotina" in entry:
        return (Subphylum(entry))
    elif "viricetes" in entry:
        return (Class(entry))
    elif "viricetidae" in entry:
        return (Subclass(entry))
    elif "virales" in entry:
        return (Order(entry))
    elif "virineae" in entry:
        return (Suborder(entry))
    elif "viridae" in entry:
        return (Family(entry))
    elif "virinae" in entry:
        return (Subfamily(entry))
    elif "virus" in entry and " " not in entry:
        return (Genus(entry))
    elif "virus" in entry and " " in entry:
        return (Subgenus(entry.replace(" ", "_")))
    else:
        return (Realm("unclassified"))
    
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

    class LineageCategory(Thing):
        pass

    class Realm(LineageCategory):
        pass

    class Subrealm(LineageCategory):
        pass

    class Kingdom(LineageCategory):
        pass

    class Subkingdom(LineageCategory):
        pass

    class Phylum(LineageCategory):
        pass

    class Subphylum(LineageCategory):
        pass

    class Class(LineageCategory):
        pass

    class Subclass(LineageCategory):
        pass

    class Order(LineageCategory):
        pass

    class Suborder(LineageCategory):
        pass

    class Family(LineageCategory):
        pass

    class Subfamily(LineageCategory):
        pass

    class Genus(LineageCategory):
        pass

    class Subgenus(LineageCategory):
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
        # Caso o vírus tenha alguma informação específica
        # (Não necessariamente só funciona pra virus, basta trocar a classe na hora de chamar o instances())
            # Executa determinada alteração

    # Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")

