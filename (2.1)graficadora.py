from manim import*
import numpy as np


config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class graficadora(Scene):
    
    #función a graficar
    def func(self, u):
        return np.array([np.cos(u), np.sin(u), 0])

    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 1.3 #rango de los ejes
        e = 0.5 #espaciado entre las marcas de los ejes
        #ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )#.add_coordinates() #por si queremos agregar los números
        axes.set_color(BLACK) #cambiar el color de ejes
        #etiquetas
        labels = axes.get_axis_labels(
            MathTex(r'x'), MathTex(r'y')
        ).set_color(BLACK) #cambiar color de etiquetas
        #función
        funcion = ParametricFunction(
            lambda u: axes.c2p(*self.func(u)),
            t_range=[0, 2*PI], #rango de la función
            color = ORANGE #color
        )
        #añadimos los objetos a la escena en orden
        self.add(axes, labels, funcion)