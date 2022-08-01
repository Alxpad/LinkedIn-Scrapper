class ClaseOferta:
    def __init__ (self):
        self.titulo =""
        self.empresa=""

    def mostrar(self, num):
        print(str(num) + '. '+ self.empresa + ':' + self.titulo)