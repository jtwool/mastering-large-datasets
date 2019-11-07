from mrjob.job import MRJob
import json

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        j = json.loads(line)
        vehicles = j['Number of Vehicles Involved']
        yield vehicles, 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()
