from bs4 import BeautifulSoup
from owlready2 import *
from tqdm import tqdm
import openpyxl
from unidecode import unidecode

# Criação/Carregamento da ontologia
onto = get_ontology("file://virus_host_ontology.owl").load()

def GetVirusData():
    wb = openpyxl.load_workbook('VMR_MSL38_v1.xlsx')
    sheet = wb.active
    virus_data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        virus_name = row[18]
        scientific_name = row[16]
        abbreviated_name = row[19]
        lineage = row[2:15]
        baltimore_group = row[24]
        host_category = row[25]

        virus_data.append((virus_name, scientific_name, abbreviated_name, lineage, baltimore_group, host_category))
    return virus_data

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


    virus_data = GetVirusData()
    for virus_name, scientific_name, abbreviated_name, lineage, baltimore_group, host_category in tqdm(virus_data):
        virus = Virus(unidecode(virus_name.replace(' ', '_')))
        virus.HasForScientificName.append(scientific_name)
        virus.HasForAbbreviatedName.append(abbreviated_name)

        for entry in lineage:
            if entry is None or GetLineage(entry) is None:
                continue
            virus.FromLineage.append(GetLineage(entry))

        baltimoreGroup = BaltimoreGroup(baltimore_group)
        virus.FromBaltimoreGroup.append(baltimoreGroup)
        baltimoreGroup.BelongsToThisGroup.append(virus)

        if "," in host_category:
            for host in host_category.split(','):
                virus.HasHostOfThisCategory.append(HostCategory(unidecode(host.replace(' ', ''))))
        else:
            virus.HasHostOfThisCategory.append(HostCategory(unidecode(host_category.replace(' ', ''))))

    # Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")

