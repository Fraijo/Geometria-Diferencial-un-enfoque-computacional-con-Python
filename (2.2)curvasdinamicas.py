from manim import*
import numpy as np

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080


class cicloide(Scene):

    #función circunferencia
    def func1(self, u, theta):
        return np.array([
                    np.cos(u) + theta,
                    np.sin(u) + 1,
                    0
            ])

    #función cicloide
    def func2(self, u, theta):
        return np.array([
                    theta - np.sin(theta),
                    1 - np.cos(theta),
                    0
            ])

    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 7.5 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        #ejes
        axes = Axes(
            x_range = [0,r,e], x_length = l/2,
            y_range = [0, r/2,e], y_length = l/4,
            )#.add_coordinates()
        axes.set_color(BLACK)
        
        s = ValueTracker(0) #tiempo t en 0

        #circunferencia que se mueve
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())),
            t_range=[0, 2*PI],
            color = ORANGE
        ))

        #cicloide, no lo dibujamos como tal, este es el camino que seguirá la pelota
        A = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func2(u, s.get_value())),
            t_range=[0, 2*PI],
            color = ORANGE
        ))

        #punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(A))

        #definimos la traza 
        path = VMobject()
        path.set_points_as_corners([ball.get_center(), ball.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([ball.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        path.set_color(BLACK)

        #agrupamos
        movil = VGroup(ball,path)
        movil.move_to(A.get_start())

        #radio 
        line = Line(c.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(c.get_center(),ball.get_center(), color= BLACK)))

        #añadimos los objetos a la escena en orden

        todo = VGroup(axes, c, A, movil, line, path)
        todo.scale(1.5)

        self.add(todo)
        
        self.play(s.animate.set_value(2*PI), rate_func=linear, run_time=5)


class deltoide(Scene):

    #función circunferencia de radio 2
    def func1(self, u, theta):
        return np.array([
                    2 * np.cos(theta) + np.cos(u),
                    2 * np.sin(theta) + np.sin(u),
                    0
            ])

    #función 
    def func2(self, u, theta):
        return np.array([
                    2 * np.cos(theta) + np.cos(-2*theta),
                    2 * np.sin(theta) + np.sin(-2*theta),
                    0
            ])

    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 3.5 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        #ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )#.add_coordinates()
        axes.set_color(BLACK)
        
        s = ValueTracker(0) #tiempo t en 0
        
        #circunferencia de radio 3 centrada en el origen
        C = axes.plot_implicit_curve(lambda x, y: x**2 + y**2 - 9, color=GREEN)

        #circunferencia que se mueve
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())),
            t_range=[0, 2*PI],
            color = RED
        ))

        #Astroide, no lo dibujamos como tal, este es el camino que seguirá la pelota
        A = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func2(u, s.get_value())),
            t_range=[0, 2*PI],
            color = RED
        ))

        #punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(A))

        #definimos la traza 
        path = VMobject()
        path.set_points_as_corners([ball.get_center(), ball.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([ball.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        path.set_color(BLACK)

        #agrupamos
        movil = VGroup(ball,path)
        movil.move_to(A.get_start())

        #radio 
        line = Line(c.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(c.get_center(),ball.get_center(), color= BLACK)))

        #añadimos los objetos a la escena en orden
        self.add(axes, C, c, A, ball, line, path)
        self.play(s.animate.set_value(2*PI), rate_func=linear, run_time=5)


class astroide(Scene):

    #función circunferencia de radio 3
    def func1(self, u, theta):
        return np.array([
                    3 * np.cos(theta) + np.cos(u),
                    3 * np.sin(theta) + np.sin(u),
                    0
            ])

    #función astroide
    def func2(self, u, theta):
        return np.array([
                    3 * np.cos(theta) + np.cos(-3*theta),
                    3 * np.sin(theta) + np.sin(-3*theta),
                    0
            ])

    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 4.5 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        #ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )#.add_coordinates()
        axes.set_color(BLACK)
        
        s = ValueTracker(0) #tiempo t en 0
        
        #circunferencia de radio 4 centrada en el origen
        C = axes.plot_implicit_curve(lambda x, y: x**2 + y**2 - 16, color=BLUE)

        #circunferencia que se mueve de radio 3
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())),
            t_range=[0, 2*PI],
            color = ORANGE
        ))

        #Astroide, no lo dibujamos como tal, este es el camino que seguirá la pelota
        A = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func2(u, s.get_value())),
            t_range=[0, 2*PI],
            color = ORANGE
        ))

        #punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(A))

        #definimos la traza 
        path = VMobject()
        path.set_points_as_corners([ball.get_center(), ball.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([ball.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        path.set_color(BLACK)

        #agrupamos
        movil = VGroup(ball,path)
        movil.move_to(A.get_start())

        #radio 
        line = Line(c.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(c.get_center(),ball.get_center(), color= BLACK)))

        #añadimos los objetos a la escena en orden
        self.add(axes, C, c, A, ball, line, path)
        self.play(s.animate.set_value(2*PI), rate_func=linear, run_time=5)

