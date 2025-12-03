from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE
config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class longituddearco(Scene):

    def func(self, t):
        a = 0.3 / 2
        b = 0.5 / 2
        c = 5
        d = 3
        #return (a * np.cos(t) * np.exp(b*t), a * np.sin(t) * np.exp(b*t) , 0)
        #return (np.cos(t)/(1+ (np.sin(t))**2), np.cos(t) * np.sin(t)/(1+ (np.sin(t))**2), 0)
        return (c* np.cos(t), d * np.sin(t), 0)

    def construct(self):

        t0 = 0
        s = ValueTracker(t0)

        # cálculo de la curvatura
        x = sy.Symbol('x')
        c = 5
        d = 3

        fx = c*sy.cos(x)
        fy = d*sy.sin(x)

        fx1 = sy.diff(fx, x)
        fy1 = sy.diff(fy, x)

        fx2 = sy.diff(fx1, x)
        fy2 = sy.diff(fy1, x)

        num = sy.Abs(fx1*fy2 - fy1*fx2)
        den = (fx1**2 + fy1**2)**sy.Rational(3,2)
        k_sym = sy.simplify(num / den)

        curvature = sy.lambdify(x, k_sym, "numpy")

        # cálculo de longitud
        def long(t):
            if t <= 0:
                return 0
            n = 200
            u = np.linspace(0, t, n)
            speed = np.sqrt(25*np.sin(u)**2 + 9*np.cos(u)**2)
            return np.trapz(speed, u)


        # gráfica de la función (elipse)
        ax = Axes(
            x_range=[-5.1, 5.1, 1], x_length=config.frame_height-1,
            y_range=[-5.1, 5.1, 1], y_length=config.frame_height-1,
            axis_config={"numbers_to_include": np.arange(-5.1, 5.1, 1), "font_size": 20},
            tips=False
        ).set_color(BLACK)

        curva = ax.plot_parametric_curve(self.func, t_range=[0, 2*np.pi], color='#DB2E2C')
        caja = SurroundingRectangle(ax, color=BLACK, buff=0.2)
        grafica = VGroup(ax, curva, caja).move_to(np.array([-3.25,0,0]))
        self.add(grafica)

        textocurva = MathTex(r'f(t) = \left(5\cos t, 3\sin t \right)', color=BLACK, font_size=40)
        textocurva.move_to(np.array([4.5,3.85,0]))
        self.add(textocurva)

        # recorrido de la bola
        ball = Dot(radius=0.05, color=BLUE_E)
        ball.add_updater(lambda y: y.move_to(ax.c2p(*self.func(s.get_value())[:2])))

        path = VMobject().set_color(BLUE_E)
        path.set_points_as_corners([ball.get_center(), ball.get_center()])
        path.add_updater(lambda p: p.add_points_as_corners([ball.get_center()]))

        m1 = VGroup(ball, path)
        m1.move_to(ax.c2p(*self.func(s.get_value())[:2]))

        self.add(m1)

        # gráfica curvatura
        ax2 = Axes(
            x_range=[-0.1, 6.6, 1], x_length=(config.frame_width-1)/2.75,
            x_axis_config={"numbers_to_include": np.arange(-0.1, 6.6, 1), "font_size": 20,},
            y_range=[-0.1, 1.1, 0.5], y_length=(config.frame_height-1)/2.75,
            y_axis_config={"numbers_to_include": np.arange(-0, 1.1, 0.5), "font_size": 20,},
            tips=False,
        ).set_color(BLACK)
        caja2 = SurroundingRectangle(ax2, color=BLACK, buff=0.2)
        grafica2 = VGroup(ax2, caja2).move_to(np.array([4.5,-2.375,0]))
        self.add(grafica2)

        ball2 = Dot(radius=0.05, color=BLUE_E)
        ball2.add_updater(lambda y: y.move_to(ax2.c2p(s.get_value(), curvature(s.get_value()))))

        path2 = VMobject().set_color(BLUE_E)
        path2.set_points_as_corners([ball2.get_center(), ball2.get_center()])
        path2.add_updater(lambda p: p.add_points_as_corners([ball2.get_center()]))

        m2 = VGroup(ball2, path2)
        m2.move_to(ax2.c2p(s.get_value(), curvature(s.get_value())))

        self.add(m2)

        # Gráfica longitud
        ax3 = Axes(
            x_range=[-0.1, 6.6, 1], x_length=(config.frame_width-1)/2.75,
            y_range=[-0.1, 25.6, 5], y_length=(config.frame_height-1)/2.75,
            x_axis_config={"numbers_to_include": np.arange(-0.1, 6.6, 1), "font_size": 20,},
            y_axis_config={"numbers_to_include": np.arange(-0.1, 25.6, 5), "font_size": 20,},
            tips=False,
        ).set_color(BLACK)
        caja3 = SurroundingRectangle(ax3, color=BLACK, buff=0.2)
        grafica3 = VGroup(ax3, caja3).move_to(np.array([4.5,1.35,0]))
        self.add(grafica3)

        ball3 = Dot(radius=0.05, color=BLUE_E)
        ball3.add_updater(lambda y: y.move_to(ax3.c2p(s.get_value(), long(s.get_value()))))

        path3 = VMobject().set_color(BLUE_E)
        path3.set_points_as_corners([ball3.get_center(), ball3.get_center()])
        path3.add_updater(lambda p: p.add_points_as_corners([ball3.get_center()]))

        m3 = VGroup(ball3, path3)
        m3.move_to(ax3.c2p(s.get_value(), long(s.get_value())))

        self.add(m3)

        #contador
        lon = DecimalNumber(0, num_decimal_places=2).set_color(BLACK)
        lon.add_updater(lambda d: d.set_value(long(s.get_value())))
        lon.add_updater(lambda d: d.next_to(ball3, 1.2 * UR))
        self.add(lon)

        #texto
        self.add(MathTex(r'\ell', font_size=40, color=BLACK).next_to(caja3.get_right(), 1.5*LEFT+5*UP))
        self.add(MathTex(r'\kappa', font_size=40, color=BLACK).next_to(caja2.get_right(), 1.5*LEFT+5*UP))

        # animación
        self.play(s.animate.set_value(TAU), run_time=6, rate_func=linear)
        self.wait()