class Simulation:
    def __init__(self, afd, sfPoint, test):
        self.afd = afd
        self.start = sfPoint[0]
        self.end = sfPoint[1]
        self.tokens = sfPoint[2]
        self.test = test
        # print(self.start)
        # print(self.end)
        # print(self.tokens)
        self.result = []
        
    def simulate(self):
        text = ""
        position = self.start[0]
        for x in self.test:
            # print(x)
            for l in x:
                seguir = True
                notExist = True
                val = ord(l)
                # print("++++++++++")
                # print(val)
                # print("palabra: ", chr(val))
                while(seguir):
                    # print("position: ", position)
                    
                    for pos in self.afd:
                        if pos[0] == position and pos[1] == str(val):
                            text += chr(val)
                            position = pos[2]
                            # print("=====================")
                            # print("existe")
                            # print(pos[0])
                            # print(pos[1])
                            # print(pos[2])
                            # print("text: ", text)
                            # print("=====================")
                            notExist = False
                            seguir = False
                            break
                
                    if notExist:
                        # print("No existe")
                        if position == self.start[0]:
                            self.result.append(["error lexico",l])
                            text = ""
                            seguir = False
                        else:
                            indice = self.end.index(position)
                            self.result.append([self.tokens[indice].replace("#",""),text])
                            # print("result: ",self.result)
                            text = ""
                            position = self.start[0]
                            # print("new position: ", position)
                    # input()
        if text:
            if position == self.start[0]:
                self.result.append(["error lexico",text])
                text = ""
            else:
                indice = self.end.index(position)
                self.result.append([self.tokens[indice].replace("#",""),text])
                text = ""
                position = self.start[0]
            
                        
        # print("\n",self.result)
        return self.result
                        