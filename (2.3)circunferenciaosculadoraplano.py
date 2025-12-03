from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080
class osculadora2d(Scene):
    
    #función otra vez
    def func(self, u, t):
        return np.array([
            u,
            np.sin(u),
            0
            ])

    def construct(self):

        #parámetros
        l = config.frame_height-0.5 #longitud ejes
        r = 8 #rango de los ejes
        e = 2 #espaciado entre las marcas de los ejes

        self.x_sym = sy.symbols('x')
        fan_sym = (self.x_sym, sy.sin(self.x_sym), 0) #función
        
        # Cálculo de derivadas simbólicas
        d1_sym = [sy.diff(fan_sym[i], self.x_sym) for i in range(0,3)] #derivada primera
        d2_sym = [sy.diff(fan_sym[i], self.x_sym, 2) for i in range(0,3)] #derivada segunda

        self.func_x = sy.lambdify(self.x_sym, fan_sym[0], 'numpy')
        self.func_y = sy.lambdify(self.x_sym, fan_sym[1], 'numpy')
        
        self.d1_0 = sy.lambdify(self.x_sym, d1_sym[0], 'numpy')
        self.d1_1 = sy.lambdify(self.x_sym, d1_sym[1], 'numpy')
        
        self.d2_0 = sy.lambdify(self.x_sym, d2_sym[0], 'numpy')
        self.d2_1 = sy.lambdify(self.x_sym, d2_sym[1], 'numpy')
        
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


    def func1(self, u, t):
        
        d1_0 = self.d1_0(t)
        d1_1 = self.d1_1(t)
        d2_0 = self.d2_0(t)
        d2_1 = self.d2_1(t)

        # Cálculo de la curvatura (k) y radio (R)
        num = (d1_0 * d2_1 - d1_1 * d2_0)
        den = (d1_0**2 + d1_1**2)**(3/2)
        
        # Curvatura
        k = num / den if den != 0 else 0

        if abs(k) < 1e-9:
            k = np.inf
        
        # Radio de curvatura (R = 1/k)
        R = 1/k if k != 0 else np.inf
        
        # Valores de la función en el punto t
        x_at_t = self.func_x(t)
        y_at_t = self.func_y(t)

        if k == np.inf or R == np.inf:
            xc, yc = x_at_t, y_at_t
            return np.array([x_at_t, y_at_t, 0])
        else:
            
            r_val_sq = (d1_0**2 + d1_1**2)
            xc = x_at_t - d1_1 * r_val_sq / num
            yc = y_at_t + d1_0 * r_val_sq / num

            return np.array([
                R*np.cos(u) + xc,
                R*np.sin(u) + yc,
                0
                ])
