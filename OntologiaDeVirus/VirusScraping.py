import random
import requests
from bs4 import BeautifulSoup
from owlready2 import *

# Criação/Carregamento da ontologia
onto = get_ontology("file://H:/My%20Drive/UFSM/7%20semestre/IA/Trabalho%20Ontologias/virus_host_ontology.owl").load()

# Url de onde foram extraidos os dados

baseUrl = "https://www.genome.jp/"

def cleanScientificName(string):
    return string.split(" [TAX:")[0]

def cleanBaltimoreGroup(string):
    if ":" in string:
        cleaned_string = string.split(":")[1]
    else:
        cleaned_string = string
    
    return cleaned_string.replace('\'', '').replace(' ', '')

# Função para obter os dados dos vírus
def GetVirusData():
    url = "virushostdb/index/virus/all"
    # response = requests.get(baseUrl + url)

    with open("response.txt", "r") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    virus_table = soup.find("table", {"class": "view"})
    virus_rows = virus_table.find_all("tr")[2:]  # Ignorar o cabeçalho da tabela

    viruses = random.sample(virus_rows, 5)

    virus_data = []
    for virus_row in viruses:
        link = virus_row.find("a").get("href")
        response = requests.get(baseUrl + link)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "info"})

        data = {}
        for row in table.find_all("tr"):
            header = row.find("th").text.strip()
            value = row.find("td").text.strip()
            data[header] = value

        scientific_name = cleanScientificName(data.get("Scientific Name"))
        lineage = data.get("Lineage").split("; ")
        baltimore_group = cleanBaltimoreGroup(data.get("Baltimore Group"))
        genome_type = data.get("Genome Type")

        virus_data.append((scientific_name, lineage, baltimore_group, genome_type))

        #print("Scientific Name:", scientific_name)
        #print("Lineage:", lineage)
        #print("Baltimore Group:", baltimore_group)
        #print("Genome Type:", genome_type)

    return virus_data

with onto:
    # Classes
    class Virus(Thing):
        pass

    class BaltimoreGroup(Thing):
        pass

    class GenomeType(Thing):
        pass

    class Host(Thing):
        pass

    # Propriedades
    class HasForScientificName(DataProperty):
        domain = [Virus]
        range = [str]

    class FromLineage(DataProperty):
        domain = [Virus]
        range = [str]

    class FromBaltimoreGroup(ObjectProperty):
        domain = [Virus]
        range = [BaltimoreGroup]
        inverse_property = onto.BelongsToThisGroup

    class HasGenomeType(ObjectProperty):
        domain = [Virus]
        range = [GenomeType]
        inverse_property = onto.BelongsToGenomeType

    # Propriedadas inversas  
    class BelongsToThisGroup(ObjectProperty):
        domain = [BaltimoreGroup]
        range = [Virus]
        inverse_property = onto.FromBaltimoreGroup

    class HasThisGenomeType(ObjectProperty):
        domain = [GenomeType]
        range = [Virus]
        inverse_property = onto.HasGenomeType
        

    # Dados dos vírus
    virus_data = GetVirusData()
    for scientific_name, lineage, baltimore_group, genome_type in virus_data:
        virus = Virus(scientific_name.replace(' ', '_'))
        virus.HasForScientificName.append(scientific_name)
        virus.FromLineage.append(lineage[0])
        baltimoreGroup = BaltimoreGroup(baltimore_group)
        virus.FromBaltimoreGroup.append(baltimoreGroup)
        baltimoreGroup.BelongsToThisGroup.append(virus)
        genomeType = GenomeType(genome_type)
        virus.HasGenomeType.append(genomeType)
        genomeType.HasThisGenomeType.append(virus)

# Salvando a ontologia em um arquivo .owl
onto.save(file="virus_host_ontology.owl", format="rdfxml")


# Classificação taxonomica
# Realm (-viria)
# Subrealm (-vira)
# Kingdom (-virae)
# Subkingdom (-virites)
# Phylum (-viricota)
# Subphylum (-viricotina)
# Class (-viricetes)
# Subclass (-viricetidae)
# Order (-virales)
# Suborder (-virineae)
# Family (-viridae)
# Subfamily (-virinae)
# Genus (-virus)
# Subgenus (-virus)
# Species