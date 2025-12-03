from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080



class evolvente(Scene):
    
    #función 
    def func(self, u, t):
        return np.array([
            (np.cos(u))**3,
            (np.sin(u))**3,
            0
            ])

    def func1(self, u, t):
        x = sy.symbols('x')
        fan = ((sy.cos(x))**3, (sy.sin(x))**3, 0) #función
        d1 = np.array([sy.diff(fan[i], x).evalf(subs={x:t}) for i in range(0,3)], dtype = float) #derivada primera
        d2 = np.array([sy.diff(fan[i], x, 2).evalf(subs={x:t}) for i in range(0,3)], dtype = float) #derivada segunda

        num = np.float64((d1[0]*d2[1] - d1[1]*d2[0] )/(((d1[0])**2 + (d1[1])**2 )**(3/2)))

        k = np.float64(num) #curvatura formateada
        r = np.float64(sy.sqrt((d1[0])**2 + (d1[1])**2 )) #radio
        
        xc = np.float64(fan[0].evalf(subs={x:t}) - (d1[1]/(k*r))) #xc
        yc = np.float64(fan[1].evalf(subs={x:t}) + (d1[0]/(k*r))) #yc
        
        return np.array([np.cos(u)/k + xc, np.sin(u)/k + yc, xc, yc])
    
    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 4 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        #ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )#.add_coordinates()
        axes.set_color(BLACK)
        self.add(axes)
        
        s = ValueTracker(0.001) #tiempo t en 0
        
        #función verde
        C = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func(u, s.get_value())[0:2]),
            t_range=[0, 2*PI],
            color = GREEN
        ))

        #circunferencia osculadora
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())[0:2]),
            t_range=[0, 2*PI],
            color = PURPLE
        ))

        #evoluta
        ev = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())[2:4]),
            t_range=[0, 2*PI],
            color = RED
        ))

        #punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(axes.c2p(*self.func(s.get_value(), 0)[0:2])))

        #radio 
        line = Line(c.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(c.get_center(),ball.get_center(), color= BLACK)))

        bola = Dot(radius=0.05, color = BLACK)
        bola.add_updater(lambda x: x.move_to(c.get_center()))

        #definimos la traza 
        path = VMobject()
        path.set_points_as_corners([bola.get_center(), bola.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([bola.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        path.set_color(ORANGE)

        #agrupamos
        movil = VGroup(bola,path)
        movil.move_to(c.get_start())

        self.add(C, c, ball, line, ev, movil)        
        self.play(s.animate.set_value(2*PI), rate_func=linear, run_time=10)

