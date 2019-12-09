class Observation:

    def __init__(self, subject):
        self.subject = subject
        self.measures = []
        self.dimensions = []

    def getSubject(self):
        return self.subject

    def addMeasure(self, p, o):
        obj = o if o != "" else "0"
        self.measures.append((p, obj))

    def addDimension(self, p, o):
        obj = o if o != "" else "0"
        self.measures.append((p, obj))

    def getRDF(self, dsName):
        sub = self.subject
        space = " "
        end = " ;\n"
        final = ".\n"
        tab = "\t"

        rdf = sub + "a qb:Observation" + end
        if dsName: rdf += tab + "qb:dataSet %s" % dsName + end
        for d in self.dimensions:
            rdf += tab + d[0] + space + d[1] + end

        for m in self.measures:
            rdf += ("%s %s %s \"%s\" %s" % (tab, m[0], space, m[1], end))

        rdf += final

        return rdf
