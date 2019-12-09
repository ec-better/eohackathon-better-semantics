import csv
import sys

from classes.observation import Observation
from classes.dataset import Dataset

def getRainfallValues(input, output):
    prefixes = "time : <http://www.w3.org/2006/time#>" \
               "cbo: http://comicmeta.org/cbo/price"
    i = 0
    short_ns = "eg"

    ds_name = "%s:dataset-%s " % (short_ns, "prices")
    ds_chirps = Dataset(ds_name)

    with open(input, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row['Dekad'] == "1"):
                i = i + 1
                subject = "%s:obs%d " % (short_ns, i)
                obs = Observation(subject=subject)
                obs.addDimension(p="dbpedia:month", o=row['Month'])
                obs.addDimension(p="dbpedia:year", o=row['Year'])
                obs.addMeasure(p="cf-feature:rainfall_amount", o=row['Rainfall (mm)'])

                ds_chirps.addObservation(obs)

    ds_chirps.saveToDisk(output)


if __name__ == "__main__":
    # input = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2016/Zimbabwe__Rainfall2016.csv"
    # output = "/home/mmami/FhG/Projects/BETTER/Data/rdf-chirps.ttl"

    input = sys.argv[1]
    output = sys.argv[2]

    getRainfallValues(input, output)