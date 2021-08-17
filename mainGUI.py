import tkinter as Tk
from tkinter.filedialog import askopenfilename
import estatistica
import ajuste

class MeuApp(Tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #master.geometry('250x100')
        master.resizable(False, False)
        master.title('HistoMaker')

        self.pack()        
        self.create_widgets()

    def browseFunc(self, destin):
        filename = askopenfilename(filetypes=(("text file", "*.txt"), ("All files", "*.*"),))
        #Insert the path found
        destin.delete(0, 'end')
        destin.insert(0, filename)

    def constructFunc(self, path):
        options = self.getCheckValues()
        
        respEsta = estatistica.execute(path, options)
        
        respAjuste = ajuste.execute(path, options)

        #Configurar pra abrir uma nova tela e mostrar os resultados
        if options["numDados"]:
            print(respEsta["numDados"])
        if options["media"]:
            print(respEsta["media"])
        if options["moda"]:
            print(respEsta["moda"])
        if options["mediana"]:
            print(respEsta["mediana"])
        if options["dp"]:
            print(respEsta["dp"])
        if options["dpM"]:
            print(respEsta["dpM"])
        if options["min"]:
            print(respEsta["min"])
        if options["max"]:
            print(respEsta["max"])
        if options["freq"]:
            print(respEsta["freq"])
        if options["ajuste"]:
            print(respAjuste)


    def create_widgets(self):
        self.titleLabel = Tk.Label(self, text="Selecione o arquivo de dados")

        self.locationLabel = Tk.Label(self, text="Local: ")
        self.escolhasLabel = Tk.Label(self, text='Marque o que desejas calcular:')

        self.titleLabel.grid(row=0, column=1, columnspan=2, sticky="W")
        self.locationLabel.grid(row=1, column=0, sticky="E")
        self.escolhasLabel.grid(row=2, column=0, sticky="W")

        #Local path
        self.path = Tk.Entry(self)

        self.path.grid(row=1, column=1)

        #Buttons
        self.search = Tk.Button(self, text='Procurar', command=lambda: self.browseFunc(self.path))
        self.construct = Tk.Button(self, text="Calcular!", command=lambda: self.constructFunc(self.path.get()))

        self.search.grid(row=1, column=2, sticky="W")
        self.construct.grid(row=8, column=1)

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
