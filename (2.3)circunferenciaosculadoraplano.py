from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080



class osculadora(Scene):
    
    #función otra vez
    def func(self, u, t):
        return np.array([
            u,
            np.sin(u),
            0
            ])

    def func1(self, u, t):
        x = sy.symbols('x')
        fan = (x, sy.sin(x), 0) #función
        d1 = [sy.diff(fan[i], x).evalf(subs={x:t}) for i in range(0,3)] #derivada primera
        d2 = [sy.diff(fan[i], x, 2).evalf(subs={x:t}) for i in range(0,3)] #derivada segunda

        num = (d1[0]*d2[1] - d1[1]*d2[0] )/(((d1[0])**2 + (d1[1])**2 )**(3/2))
        #num = sy.sqrt(np.cross(d1,d2).T @ np.cross(d1,d2)) #norma del producto cruz
        #den = sy.sqrt(np.array(d1).T @ np.array(d1)) #denominador
        #res = num/(den)**3 #curvatura

        k = np.float64(num) #curvatura formateada

        if k == 0:
            k = np.inf
        else:
            k = np.float64(num)
        
        r = np.float64(sy.sqrt((d1[0])**2 + (d1[1])**2 )) #radio
        
        xc = np.float64(fan[0].evalf(subs={x:t}) - (d1[1]/(k*r))) #xc
        yc = np.float64(fan[1].evalf(subs={x:t}) + (d1[0]/(k*r))) #yc
        
        return np.array([
            np.cos(u)/k + xc,
            np.sin(u)/k + yc,
            0
            ])
    
    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 8 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        #ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )#.add_coordinates()
        axes.set_color(BLACK)
        self.add(axes)
        
        s = ValueTracker(-2*PI) #tiempo t en 0
        
        #función verde
        C = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func(u, s.get_value())),
            t_range=[-2*PI, 2*PI],
            color = GREEN
        ))

        #circunferencia osculadora
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())),
            t_range=[-2*PI, 2*PI],
            color = PURPLE
        ))

        #punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(axes.c2p(*self.func(s.get_value(), 0))))

        #radio 
        line = Line(c.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(c.get_center(),ball.get_center(), color= BLACK)))

        self.add(C, c, ball, line)        
        self.play(s.animate.set_value(2*PI), rate_func=linear, run_time=10)