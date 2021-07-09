import tkinter as Tk
from tkinter.filedialog import askopenfilename
import estatistica

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
        estatistica.execute(path, options)


    def create_widgets(self):
        self.locationLabel = Tk.Label(self, text="Local: ")
        self.escolhasLabel = Tk.Label(self, text='Marque o que desejas calcular:')

        self.locationLabel.grid(row=0, column=1)
        self.escolhasLabel.grid(row=1, column=0)

        #Local path
        self.path = Tk.Entry(self)

        self.path.grid(row=0, column=2)

        #Buttons
        self.search = Tk.Button(self, text='Procurar', command=lambda: self.browseFunc(self.path))
        self.construct = Tk.Button(self, text="Construir!", command=lambda: self.constructFunc(self.path.get()))

        self.search.grid(row=0, column=3)
        self.construct.grid(row=1, column=2)

        self.createCheckBoxes(2)
    
    def createCheckBoxes(self, startRow):
        #Checkboxes
        self.cbRow = startRow

        #Creating the variables
        self.vars = []
        for c in range(10):
            self.vars.append(Tk.BooleanVar())
        #Creating the widgets
        self.numDados = Tk.Checkbutton(self, text='Número de Dados', var=self.vars[0])
        self.media = Tk.Checkbutton(self, text='Média', var=self.vars[1])
        self.moda = Tk.Checkbutton(self, text='Moda', var=self.vars[2])
        self.mediana = Tk.Checkbutton(self, text='Mediana', var=self.vars[3])
        self.desvioPadrao = Tk.Checkbutton(self, text='Desvio Padrão', var=self.vars[4])
        self.valMin = Tk.Checkbutton(self, text='Valor Mínimo', var=self.vars[5])
        self.valMax = Tk.Checkbutton(self, text='Valor Máximo', var=self.vars[6])        
        self.frequencia = Tk.Checkbutton(self, text='Frequência', var=self.vars[7])
        self.dpMedia = Tk.Checkbutton(self, text='Desvio Padrão da Média', var=self.vars[8])
        self.histograma = Tk.Checkbutton(self, text='Histograma', var=self.vars[9])


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
             
        self.checkAll = Tk.Checkbutton(self, text='Selecionar Todos', command=check)    
        
        #Showing the widgets
        self.numDados.grid(row=self.cbRow, column=0, sticky='W')
        self.media.grid(row=self.cbRow+1, column=0, sticky='W')
        self.moda.grid(row=self.cbRow+2, column=0, sticky='W')
        self.mediana.grid(row=self.cbRow+3, column=0, sticky='W')
        self.desvioPadrao.grid(row=self.cbRow+4, column=0, sticky='W')
        self.valMin.grid(row=self.cbRow+5, column=0, sticky='W')
        self.valMax.grid(row=self.cbRow+6, column=0, sticky='W')
        self.frequencia.grid(row=self.cbRow+7, column=0, sticky='W')
        self.dpMedia.grid(row=self.cbRow+8, column=0, sticky='W')
        self.histograma.grid(row=self.cbRow+9, column=0, sticky='W')
        self.checkAll.grid(row=self.cbRow+10, column=0, sticky='W')
    
    def getCheckValues(self):
        self.values = []
        for c in self.vars:
            self.values.append(c.get())
        return self.values


root = Tk.Tk()
app = MeuApp(master=root)
app.mainloop()
