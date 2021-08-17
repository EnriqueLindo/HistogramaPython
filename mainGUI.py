import tkinter as Tk
from tkinter.filedialog import askopenfilename

from matplotlib.pyplot import text
import estatistica
import ajuste

class MeuApp(Tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #master.geometry('250x100')
        master.resizable(False, False)
        master.title('Stats')

        self.pack()        
        self.create_widgets()

    def myHelp(self):
        textoAjuda = "Este é o texto de ajuda!\nSelecione o arquivo .txt que você deseja usar no programa utilizando o botão 'Procurar'\n\nEste arquivo deve seguir o seguinte formato:\nvalor1\nvalor2\n...\nvalorx\n\n"
        textoAjuda += "Se precisar adiconar incertezas, utilize ';' para separá-las de seu valor correspondente. Da seguinte forma: valor1;incertezaValor1\n\nNo caso de construção de retas de ajuste, onde se faz necessário "
        textoAjuda += "a presença dos valores x e y, coloque primeiro todos os valores de x e suas incertezas e imediatamente após os valores de y da seguinte forma:\nvalor_x1;incerteza_x1\nvalor_x2;incerteza_x2\nvalor_xk;incerteza_xk\n"
        textoAjuda += "valor_y1;incerteza_y1\nvalor_y2;incerteza_y2\nvalor_yk;incerteza_yk\n\nVale ressaltar que os números devem ser expressos com '.' em vez de ','. Portanto o valor 1,234 está errado, o correto seria 1.234\n\nBom uso do programa! =D"
        self.output.insert('end', textoAjuda)

    def browseFunc(self, destin):
        filename = askopenfilename(filetypes=(("text file", "*.txt"), ("All files", "*.*"),))
        #Insert the path found
        destin.delete(0, 'end')
        destin.insert(0, filename)

    def constructFunc(self, path):
        options = self.getCheckValues()
        
        respEsta = estatistica.execute(path, options)
        
        respAjuste = ajuste.execute(path, options)

        textoResposta = ''

        #Configurar pra abrir uma nova tela e mostrar os resultados
        if options["numDados"]:
            textoResposta += "Número de dados = " + str(respEsta["numDados"]) + "\n"
        if options["media"]:
            textoResposta += "Média = " + str(respEsta["media"]) + "\n"
        if options["moda"]:
            textoResposta += "Moda = " + str(respEsta["moda"]) + "\n"
        if options["mediana"]:
            textoResposta += "Mediana = " + str(respEsta["mediana"]) + "\n"
        if options["dp"]:
            textoResposta += "Desvio-Padrão = " + str(respEsta["dp"]) + "\n"
        if options["dpM"]:
            textoResposta += "Desvio-Padrão da média = " + str(respEsta["dpM"]) + "\n"
        if options["min"]:
            textoResposta += "Valor mínimo = " + str(respEsta["min"]) + "\n"
        if options["max"]:
            textoResposta += "Valor máximo = " + str(respEsta["max"]) + "\n"
        if options["freq"]:
            textoResposta += "\nFrequências: " + "\n" + str(respEsta["freq"]) + "\n"
        if options["ajuste"]:
            textoResposta += "Coeficiente Angular = " + str(respAjuste[0]) + " ± " + str(respAjuste[2]) + "\n" + "Coeficiente linear = " + str(respAjuste[1]) + " ± " + str(respAjuste[3])
        
        self.output.insert('end', textoResposta)

    def create_widgets(self):
        self.titleLabel = Tk.Label(self, text="Selecione o arquivo de dados")

        self.locationLabel = Tk.Label(self, text="Local: ")
        self.escolhasLabel = Tk.Label(self, text='Marque o que desejas calcular:')

        self.titleLabel.grid(row=0, column=1, sticky="N")
        self.locationLabel.grid(row=1, column=0, sticky="E")
        self.escolhasLabel.grid(row=2, column=0, sticky="W")

        #Local path
        self.path = Tk.Entry(self)

        self.path.grid(row=1, column=1, padx=20, sticky="NESW")

        #Buttons
        self.search = Tk.Button(self, text='Procurar', command=lambda: self.browseFunc(self.path))
        self.construct = Tk.Button(self, text="Calcular!", command=lambda: self.constructFunc(self.path.get()))

        self.search.grid(row=1, column=2, sticky="W")
        self.construct.grid(row=8, column=1, sticky="N")

        self.helpBtn = Tk.Button(self, text="ajuda?", command=self.myHelp)
        self.helpBtn.grid(row=8, column=2, sticky="E", padx=10, pady=10)

        self.output = Tk.Text(self, height=10, padx=10, pady=10)
        self.output.grid(row=9, column=0, columnspan=3, padx=20, pady=20)

        self.credits = Tk.Label(self, text="©EnriqueThomaz / contato: enriquetd@id.uff.br")
        self.credits.grid(row=10, column=0, sticky="W", columnspan=2)

        self.createCheckBoxes(3)
    
    def createCheckBoxes(self, startRow):
        #Creating the variables
        self.vars = []
        for c in range(12):
            self.vars.append(Tk.BooleanVar())
        
        #Creating the widgets
        self.numDados = Tk.Checkbutton(self, text='Número de Dados', var=self.vars[0])
        self.media = Tk.Checkbutton(self, text='Média', var=self.vars[1])
        self.moda = Tk.Checkbutton(self, text='Moda', var=self.vars[2])
        self.mediana = Tk.Checkbutton(self, text='Mediana', var=self.vars[3])
        self.desvioPadrao = Tk.Checkbutton(self, text='Desvio Padrão', var=self.vars[4])

        self.valMin = Tk.Checkbutton(self, text='Desvio Padrão da Média', var=self.vars[5])
        self.valMax = Tk.Checkbutton(self, text='Valor Mínimo', var=self.vars[6])        
        self.frequencia = Tk.Checkbutton(self, text='Valor Máximo', var=self.vars[7])
        self.dpMedia = Tk.Checkbutton(self, text='Frequência', var=self.vars[8])
        self.histograma = Tk.Checkbutton(self, text='Histograma', var=self.vars[9])

        self.ajuste = Tk.Checkbutton(self, text="Reta de ajuste", var=self.vars[10])
        self.residuos = Tk.Checkbutton(self, text="Gráfico de Resíduos", var=self.vars[11])


        def check():            
            self.numDados.select()  
            self.media.select()
            self.moda.select()
            self.mediana.select() 
            self.desvioPadrao.select() 
            self.valMin.select() 
            self.valMax.select() 
            self.frequencia.select() 
            self.dpMedia.select() 
            self.histograma.select()
            self.ajuste.select()
            self.residuos.select()
             
        self.checkAll = Tk.Checkbutton(self, text='Selecionar Todos', command=check)    
        
        #Showing the widgets
        self.numDados.grid(row=startRow, column=0, sticky='W')
        self.media.grid(row=startRow+1, column=0, sticky='W')
        self.moda.grid(row=startRow+2, column=0, sticky='W')
        self.mediana.grid(row=startRow+3, column=0, sticky='W')
        self.desvioPadrao.grid(row=startRow+4, column=0, sticky='W')

        self.valMin.grid(row=startRow, column=1, sticky='W')
        self.valMax.grid(row=startRow+1, column=1, sticky='W')
        self.frequencia.grid(row=startRow+2, column=1, sticky='W')
        self.dpMedia.grid(row=startRow+3, column=1, sticky='W')
        self.histograma.grid(row=startRow+4, column=1, sticky='W')

        self.ajuste.grid(row=startRow, column=2, sticky='W')
        self.residuos.grid(row=startRow+1, column=2, sticky='W')
        self.checkAll.grid(row=startRow+2, column=2, sticky='W')
    
    def getCheckValues(self):
        self.values = {}
        opts = ["numDados", "media", "moda", "mediana", "dp", "dpM", "min", "max", "freq", "hist", "ajuste", "grafResi"]
        for c in range(len(self.vars)):
            self.values[opts[c]] = self.vars[c].get()
        return self.values


root = Tk.Tk()
app = MeuApp(master=root)
app.mainloop()
