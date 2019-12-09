from classes.observation import Observation


class Dataset:
    observations: Observation = []

    def __init__(self, name):
        self.name = name

    def addObservation(self, obs: Observation):
        self.observations.append(obs)

    def getRDF(self):
        observations = ""
        rdf = ""
        space = " "
        end = " ;\n"
        final = " .\n"
        datacubeNs = "qb: <http://purl.org/linked-data/cube#>"
        generalNs = "eg: <http://example.org/ns#>"
        dbpediaNs = "dbpedia: <http://dbpedia.org/ontology/>"
        cboNs = "cbo: <http://comicmeta.org/cbo/>"
        m3liteNs = "cf-feature: <http://purl.oclc.org/NET/ssnx/cf/cf-feature#>"

        prefixes = "@prefix " + datacubeNs + final
        prefixes += "@prefix " + generalNs + final
        prefixes += "@prefix " + dbpediaNs + final
        prefixes += "@prefix " + cboNs + final
        prefixes += "@prefix " + m3liteNs + final

        o: Observation
        for o in self.observations:
            observations += o.getRDF(self.name)

        rdf += prefixes + "\n" + observations

        return rdf

    def saveToDisk(self, path):
        rdf = self.getRDF()

        with open(path, "w") as text_file:
            text_file.write(rdf)