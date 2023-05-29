import random
import requests
from bs4 import BeautifulSoup
from owlready2 import *
from tqdm import tqdm

# Criação/Carregamento da ontologia
onto = get_ontology("file://virus_host_ontology.owl").load()

# Url de onde foram extraidos os dados

baseUrl = "https://www.genome.jp/"

def cleanScientificName(string):
    return string.split(" [TAX:")[0]

def cleanBaltimoreGroup(string):
    if string is None:
        return "unknown"

    if ":" in string:
        cleaned_string = string.split(":")[1]
    else:
        cleaned_string = string
    
    return cleaned_string.strip()

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

# Função para obter os dados dos vírus
def GetVirusData():
    url = "virushostdb/index/virus/all"
    # response = requests.get(baseUrl + url)

    with open("response.txt", "r") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    virus_table = soup.find("table", {"class": "view"})
    virus_rows = virus_table.find_all("tr")[2:]  # Ignorar o cabeçalho da tabela

    viruses = random.sample(virus_rows, 200)

    virus_data = []
    for virus_row in tqdm(viruses):
        link = virus_row.find("a").get("href")
        response = requests.get(baseUrl + link)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "info"})

        data = {}
        for row in table.find_all("tr"):
            header = row.find("th").text.strip()
            value = row.find("td").text.strip()
            data[header] = value

        hosts = []
        for span in soup.find_all("span"):
            if "Known hosts" in span.text:
                n = int(span.text.split("(")[1].split(")")[0])
                info_tables = span.find_all_next("table", class_="info")

                for table in info_tables:
                    row = table.find_next("tr")
                    cell = row.find_next("td")
                    info = cell.text.strip()
                    hosts.append(cleanScientificName(info))

        scientific_name = cleanScientificName(data.get("Scientific Name"))
        #print("Scientific Name:", scientific_name)
        lineage = data.get("Lineage").split("; ")[1:]
        baltimore_group = cleanBaltimoreGroup(data.get("Baltimore Group"))
        genome_type = data.get("Genome Type")

        virus_data.append((scientific_name, lineage, baltimore_group, genome_type, hosts))

        # print("Lineage:", lineage)
        # print("Baltimore Group:", baltimore_group)
        # print("Genome Type:", genome_type)
        # print("Hosts:", hosts)

    return virus_data

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

    # Propriedades
    class HasForScientificName(DataProperty):
        domain = [Species]
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

    # Dados dos vírus
    virus_data = GetVirusData()
    for scientific_name, lineage, baltimore_group, genome_type, hosts in virus_data:
        virus = Virus(scientific_name.replace(' ', '_'))
        virus.HasForScientificName.append(scientific_name)

        for entry in lineage:
            if GetLineage(entry) is None:
                continue
            virus.FromLineage.append(GetLineage(entry))

        baltimoreGroup = BaltimoreGroup(baltimore_group)
        virus.FromBaltimoreGroup.append(baltimoreGroup)
        baltimoreGroup.BelongsToThisGroup.append(virus)

        genomeType = GenomeType(genome_type)
        virus.HasGenomeType.append(genomeType)
        genomeType.HasThisGenomeType.append(virus)

        for entry in hosts:
            host = Host(entry.replace(' ', '_'))
            virus.HasHost.append(host)
            host.HasForScientificName.append(entry)
            host.HostThoseVirus.append(virus)

# Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")