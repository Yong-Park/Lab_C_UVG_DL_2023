class SLRPARSING:
    def __init__(self, transitions, conjuntos, numbers):
        self.transitions = transitions
        self.conjuntos = conjuntos
        
        self.state = numbers
        self.action = []
        self.goto = []
        self.table = []
                
    def constructTable(self):
        #primero divirlos por sus secciones correspondietes
        for x in self.transitions:
            if x[1].isupper():
                if x[1] not in self.goto:
                    self.goto.append(x[1])
            else:
                if x[1] not in self.action:
                    self.action.append(x[1])
        self.action.sort(reverse=True)
        print("self.state: ", self.state)
        print("self.action: ",self.action)
        print("self.goto: ",self.goto)