import pandas as pd
import plotly.plotly as py
from sklearn import preprocessing
from IPython.display import HTML
from metakernel.display import display
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, save
import plotly.offline as offline
from bokeh.io import export_png, output_file
import plotly.graph_objs as go
from bokeh.models import PanTool, WheelZoomTool, LassoSelectTool
colors = ["red", "green", "blue", "grey", "orange", "black", "firebrick", "navy", "olive"]


class ParallelCoordinates:

    # We generate the constructor
    def __init__(self, file, library = 'bokeh', normalization=False, tags=None, remove_legend=False, autosave = False, color_unique = False, save_file_name=None):
        self.file = file
        self.library = library
        self.normalization = normalization
        self.tags = tags
        self.remove_legend = remove_legend
        self.autosave = autosave
        self.color_unique = color_unique
        self.save_file_name = save_file_name

    def plot(self):
        print("Reading data")
        # Vemos cual es la extensión
        exten = self.file.split('.')
        extension = exten[len(exten)-1]
        # Leemos los archivos .tsv
        if extension == 'tsv':
            df = pd.read_table(self.file)
            df = df.drop(list(df)[-1], 1)#Para los archivos .tsv eliminamos la última columna que se suele leer y no tiene nada
            # Calculamos los índices para poder hacer los plots
            print("Calculate indexes")
            par = list(df)
            # Añadimos los índices
            df[len(par)] = df.index
            # Establecemos nombres a las columnas
            df.columns = ["Strike", "TC", "SP", "Index"]
            # Damos opción para indicar tags diferentes
            if self.tags != None:
                dfd = self.tags
                dfd.append("Indice")
                if(len(dfd) == len(list(df))):
                    df.columns = dfd
                else:
                    raise Exception("Number of tags: " + str(len(dfd)-1) + "  missmatched column length  -->   " + str(len(list(df))-1))
        # Leemos archivos que acepta read_csv
        elif (extension == 'csv' or extension == 'txt'):
            df = pd.read_csv(self.file)

        name_data_frame = list(df)
        if self.normalization == True:
            print("Normalizing data")
            # Eliminamos temporalmente ultima columna
            num = df[list(df)[-1]]
            df = df.drop(list(df)[-1], 1)
            # Normalizamos los datos
            x = df.values  # returns a numpy array
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            df = pd.DataFrame(x_scaled)
            # Volvemos a añadir el dataFrame
            df[len(list(df))] = num
            df.columns = name_data_frame
        print("Calculating best ranges")
        # Inicializamos las variables
        max_range_values = []
        min_range_values = []
        final_max_value = 0
        final_min_value = 0
        #Creamos una lista con los nombres de las columnas
        pared = list(df)
        for l in range(0, len(pared)-1):
            max1 = max(df[pared[l]])
            min1 = min(df[pared[l]])
            if l < len(pared)-3:
                max2 = max(df[pared[l + 1]])
                min2 = min(df[pared[l + 1]])
                max_range_values.append(max(int(max1*2), int(max2*1.2)))
                min_range_values.append(min(min1-1, min2-1))
            if l == len(pared)-2:
                max_range_values.append(max(df[pared[l]]*1.2))
                min_range_values.append(min(df[pared[l]]))
                final_max_value = max(max_range_values)
                final_min_value = min(min_range_values)
        print("Plotting data")
        if self.library == 'pyplot':
            division = list(df)[-1]
            # Limpiamos la figura en caso de que tuviesemos algo
            plt.close()
            plt.figure()
            plt.clf()
            # Ofrece la opción de plotear de un solo color
            if self.color_unique ==True:
                fig = parallel_coordinates(df, division, color=('#556270'))
            elif self.color_unique == False:
                fig = parallel_coordinates(df, division)
            # Ofrece la opcion de eliminar la leyenda
            if (self.remove_legend == True):
                plt.gca().legend_.remove()
            # Ofrece la opcion de guardar la gráfica
            if self.autosave == True:
                plt.savefig(self.save_file_name)
            # Mostramos la gráfica
            plt.show()
            fig = df

        elif self.library == 'plotly':
            # Vamos a generar unos indices para poder identificar las columnas en forma de ids
            levels = df[pared[-1]].unique()
            new_column = []
            for o in range(0, len(df[pared[-1]])):
                for q in range(0, len(levels)):
                    if df[pared[-1]][o] == levels[q]:
                        new_column.insert(o, q)
            df[len(list(df))] = new_column
            df = df.rename(columns={len(list(df)) - 1: "autoIndexes"})
            print(len(list(df)))


            if len(list(df)) == 8:
                data = [
                    go.Parcoords(
                        # Añadimos el id y los colores que vamos a usar
                        line=dict(color=df['autoIndexes'],
                                  colorscale=[[0, '#D7C16B'], [0.5, '#23D8C3'], [1, '#F3F10F']]),
                        dimensions=list([
                            # Vamos a añadiendo las diferentes subplots que se añaden al final
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[0], values=df[pared[0]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[1], values=df[pared[1]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[2], values=df[pared[2]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[3], values=df[pared[3]])
                            ,
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[4], values=df[pared[4]])
                            ,
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[5], values=df[pared[5]])
                        ])
                    )
                ]
            #Tenemos esto para diferente numero de colimnas
            if len(list(df)) == 7:
                data = [
                    go.Parcoords(
                        line=dict(color=df['autoIndexes'],
                                  colorscale=[[0, '#D7C16B'], [0.5, '#23D8C3'], [1, '#F3F10F']]),
                        dimensions=list([
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[0], values=df[pared[0]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[1], values=df[pared[1]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[2], values=df[pared[2]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[3], values=df[pared[3]])
                            ,
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[4], values=df[pared[4]])
                        ])
                    )
                ]


            if len(list(df)) == 6:
                data = [
                    go.Parcoords(
                        line=dict(color=df['autoIndexes'],
                                  colorscale=[[0, '#D7C16B'], [0.5, '#23D8C3'], [1, '#F3F10F']]),
                        dimensions=list([
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[0], values=df[pared[0]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[1], values=df[pared[1]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[2], values=df[pared[2]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[3], values=df[pared[3]])
                        ])
                    )
                ]
            if len(list(df)) == 5:
                data = [
                    go.Parcoords(
                        line=dict(color=df['autoIndexes'],
                                  colorscale=[[0, '#D7C16B'], [0.5, '#23D8C3'], [1, '#F3F10F']]),
                        dimensions=list([
                            dict(range=[final_min_value, final_max_value],
                                 constraintrange=[4, 8],
                                 label=pared[0], values=df[pared[0]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[1], values=df[pared[1]]),
                            dict(range=[final_min_value, final_max_value],
                                 label=pared[2], values=df[pared[2]])
                        ])
                    )
                ]

            # Coloreamos el fondo de la figura
            layout = go.Layout(
                plot_bgcolor='#E5E5E5',
                paper_bgcolor='#E5E5E5'
            )
            # Utilizamos la librería offline de plotly para hacer el gráfico
            fig = go.Figure(data=data, layout=layout)
            if self.autosave == True:
                off = offline.plot(fig, image = 'png',output_type='file', image_filename=self.save_file_name, filename=self.save_file_name)
            if self.autosave == False:
                off = offline.iplot(fig)
            display(HTML(off))

        elif self.library == 'bokeh':
            plots = []
            nombres = list(df)
            count = 0
            df.sort_values(nombres[1])
            colourname = []
            for i in range(0, len(nombres)-2):
                # Generamos la figura
                p = figure(x_range=(1, 5),x_axis_label=nombres[i]+'       '+nombres[i+1], y_range=(final_min_value, final_max_value), plot_width=400, plot_height=400)
                xs = []
                ys = []
                # Coloreamos  25%-25%-25%-25%
                for j in range(0, len(df[nombres])):
                    if i == 0:
                        if j < len(df[nombres[i]])/4:
                            colourname.append(colors[1])
                        elif j>= len(df[nombres[i]])/4 and j< (2*len(df[nombres[i]])/4):
                            colourname.append(colors[2])
                        elif j>= 2*len(df[nombres[i]])/4 and j< 3*len(df[nombres[i]])/4:
                            colourname.append(colors[3])
                        elif j>= 3*len(df[nombres[i]])/4 and j< 4*len(df[nombres[i]])/4:
                            colourname.append(colors[4])
                            # Añadimos los valores
                    xs.append([1, 5])
                    ys.append([df[nombres[i]][j], df[nombres[i+1]][j]])
                    count += 1
                    # Generamos el plot
                if self.color_unique == True:
                    p.multi_line(xs, ys, line_width=4)
                else:
                    p.multi_line(xs, ys, color=colourname, line_width=4)
                p.add_tools(PanTool(), WheelZoomTool(),LassoSelectTool())
                plots.append(p)
            # Añadimos las diferentes gráficas generadas
            fig = gridplot([plots], sizing_mode='stretch_both')
            if self.autosave == True:
                save(fig)
                export_png(fig, filename=self.save_file_name)
            # Mostramos el total de las gráficas generadas
            show(fig)
        return fig

    def save(self, fig ):
        exten = self.save_file_name.split('.')
        print("Guardamos los valores")
        if self.library == 'bokeh':
            if exten[-1] == 'png':
                export_png(fig, filename=self.save_file_name)
            elif exten[-1] == 'html':
                output_file(self.save_file_name)
                save(fig)
            else:
                raise Exception("El formato" + exten[-1]+ " no lo soporta esta aplicacion.\n Tiene que elegir entre .png y .html")

        if self.library == 'plotly':
            if exten[-1] == 'html':
                offline.plot(fig, image='png', output_type='file', image_filename=self.save_file_name,
                               filename=self.save_file_name)
            elif exten[-1] == 'jpeg' or exten[-1] == 'png' or exten[-1] == 'pdf':
                py.image.save_as(fig, filename=self.save_file_name)
                from IPython.display import Image
                Image(self.save_file_name)
            else:
                raise Exception(
                    "El formato" + exten[-1] + " no lo soporta esta aplicacion.\n Tiene que elegir entre .png, .jpeg, .pdf y .html")

        if self.library == 'pyplot':
            division = list(fig)[-1]
            plt.figure()
            if self.color_unique == True:
                parallel_coordinates(fig, division, color=('#556270'))
            else:
                parallel_coordinates(fig, division)
            if (self.remove_legend == True):
                plt.gca().legend_.remove()
            plt.savefig(self.save_file_name)




#bokeh1 = ParallelCoordinates(file='../data/iris.csv', library='bokeh', normalization=False, tags=None, remove_legend= True, autosave=True, color_unique=True, save_file_name="../Results/prueba.png" )
#result = bokeh1.plot()
#bokeh1.save(result)

