from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080


x_sym = sy.symbols('x')

#función
fan_sym = sy.Matrix([
    (sy.cos(x_sym))**3,
    (sy.sin(x_sym))**3,
    0
])

d1_sym = sy.diff(fan_sym, x_sym, 1) # Derivada primera simbólica
d2_sym = sy.diff(fan_sym, x_sym, 2) # Derivada segunda simbólica


fan_func = sy.lambdify(x_sym, fan_sym, "numpy")
d1_func = sy.lambdify(x_sym, d1_sym, "numpy")
d2_func = sy.lambdify(x_sym, d2_sym, "numpy")

class evolvente(Scene):
    
    # Función para la curva
    def func(self, u, t):
        return np.array([
            (np.cos(u))**3,
            (np.sin(u))**3,
            0
            ])

    # Función para la circunferencia osculadora y el centro de curvatura
    def func1(self, u, t):
        ft = fan_func(t).flatten()
        d1 = d1_func(t).flatten()
        d2 = d2_func(t).flatten()

        num = np.float64(d1[0] * d2[1] - d1[1] * d2[0])
        mod_d1_sq = d1[0]**2 + d1[1]**2
        den = np.power(mod_d1_sq, 3/2)

        epsilon = 1e-6 
        k = np.float64(num / (den if den > epsilon else epsilon)) 

        r = np.float64(1.0 / k) 
        
        factor = mod_d1_sq / num
        
        xc = np.float64(ft[0] - d1[1] * factor) 
        yc = np.float64(ft[1] + d1[0] * factor) 
        
        R_circulo = np.float64(abs(r))

        # Ecuación de la circunferencia osculadora
        circle_x = R_circulo * np.cos(u) + xc
        circle_y = R_circulo * np.sin(u) + yc
        
        return np.array([circle_x, circle_y, xc, yc])
    
    def construct(self):

        # Parámetros
        l = config.frame_height-0.5
        r = 4
        e = 2

        # Ejes
        axes = Axes(
            x_range = [-r,r,e], x_length = l,
            y_range = [-r,r,e], y_length = l,
            )
        axes.set_color(BLACK)
        self.add(axes)
        
        s = ValueTracker(0.001)

        # Curva
        C = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func(u, s.get_value())[0:2]),
            t_range=[0, 2*PI],
            color = GREEN
        ))

        # Circunferencia osculadora
        c = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())[0:2]),
            t_range=[0, 2*PI],
            color = PURPLE
        ))
        
        # Evoluta
        ev_dot = always_redraw(
            lambda: Dot(
                axes.c2p(*self.func1(0, s.get_value())[2:4]),
                color = RED,
                radius = 0.05
            )
        )

        # Punto que dibuja
        ball = Dot(radius=0.05, color = BLACK)
        ball.add_updater(lambda x: x.move_to(axes.c2p(*self.func(s.get_value(), 0)[0:2])))

        # Punto del centro de curvatura
        bola = Dot(radius=0.05, color = BLACK)
        bola.add_updater(lambda x: x.move_to(axes.c2p(*self.func1(0, s.get_value())[2:4])))

        # Radio
        line = Line(bola.get_center(),ball.get_center(), color= BLACK)
        line.add_updater(lambda x: x.become(Line(bola.get_center(),ball.get_center(), color= BLACK)))

        # Definimos la traza (evolvente)
        path = VMobject()
        path.set_points_as_corners([bola.get_center(), bola.get_center()])

        def update_path(path_obj):
            previous_path = path_obj.copy()
            previous_path.add_points_as_corners([bola.get_center()])
            path_obj.become(previous_path)
        path.add_updater(update_path)
        path.set_color(ORANGE)

        # Agrupamos
        movil = VGroup(bola,path)
        movil.move_to(axes.c2p(*self.func1(0, s.get_value())[2:4]))
        
        self.add(C, c, ev_dot, ball, line, movil)
        self.play(s.animate.set_value(2 * PI), rate_func=linear, run_time=5)
