class ClaseOferta:      #   Offer object, which includes all the different data from offers
    def __init__ (self):
        self.titulo =""
        self.empresa=""
        self.href = ""
        #TODO: self.description
        #TODO: self.contractType
        #TODO: self.competences
        #TODO: self.experience
        #TODO: self.employees
        
    def mostrar(self, num):     # Optional method to show offer data
        print(str(num+1) + '. '+ self.empresa + ':' + self.titulo)