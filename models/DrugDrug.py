from Model import Model


class DrugDrug(Model):
    """
    A specialized graph class for handling drug-drug interaction data,
    inheriting from the base Model class.
    """
    NAME = "Drug-Drug"

    def __init__(self):
        super().__init__()
        self.set_file_location("graphs/drug_drug_graph.json")
        self.load_graph()
