class Dinosaur:
    def __init__(self, response, name, time):
        self.name = name
        self.collected_date = time
        self.species = response["data"][0]["name"]
        self.description = response["data"][0]["description"]
        self.imageURL = response["data"][0]["image"]["imageURL"]
        self.period = response["data"][0]["temporalRange"]
        self.movement = response["data"][0]["locomotionType"]
        
    # { 
    #   "count": 5,
    #   "data": [
    #     {
    #       "id": 1118,
    #       "name": "Zephyrosaurus",
    #       "temporalRange": "Early Cretaceous, ~113 Ma",
    #       "diet": "herbivore",
    #       "locomotionType": "biped",
    #       "description": "...",
    #       "classificationInfo": {...},
    #       "image": {...},
    #       "source": {...}
    #     }
    #   ]
    # }