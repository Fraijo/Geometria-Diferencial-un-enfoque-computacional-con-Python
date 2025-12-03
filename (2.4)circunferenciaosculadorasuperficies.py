from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class triedroOsculadora(ThreeDScene):

    #función    
    def func(self, u):
        return np.array([
            0.2 * u * np.cos(u) ,
            0.2 * u * np.sin(u),
            0.2 * u
            ])

    #calculando la circunferencia osculadora
    def func1(self, u, t):
        x = sy.symbols('x')
        fan = (0.2 * x * sy.cos(x), 0.2 * x * sy.sin(x), 0.2 * x) #función
        d1_num = np.array([sy.diff(fan[i], x).evalf(subs={x:t}) for i in range(3)], dtype=float) #primera derivada
        d2_num = np.array([sy.diff(fan[i], x, 2).evalf(subs={x:t}) for i in range(3)], dtype=float) #segunda derivada

        r = np.array([fan[i].evalf(subs={x: t}) for i in range(3)], dtype=float)

        norm_d1 = np.linalg.norm(d1_num)
        U = d1_num / norm_d1
        cross_d1_d2 = np.cross(d1_num, d2_num)
        norm_cross = np.linalg.norm(cross_d1_d2)
        if norm_cross == 0:
            v = np.array([0., 0., 0.])
            k = 0.0
        else:
            v = cross_d1_d2 / norm_cross
            k = norm_cross / (norm_d1 ** 3)
             
        w = np.cross(v, U)

        
        if k == 0:
            R = np.inf
            C = np.array([np.inf, np.inf, np.inf])
        else:
            R = np.float64(1.0 / k) 
            C = r + R * w
            
        xc = np.float64(C[0] + R * (np.cos(u) * U[0] + np.sin(u) *w[0]))
        yc = np.float64(C[1] + R * (np.cos(u) * U[1] + np.sin(u) *w[1]))
        zc = np.float64(C[2] + R * (np.cos(u) * U[2] + np.sin(u) *w[2]))
        
        
        return [r, U, v, w, xc, yc, zc]

    def construct(self):
        L = 5.5
        axes = ThreeDAxes(
            x_range=[-L,L,1], x_length=config.frame_height-0.5,
            y_range=[-L,L,1], y_length=config.frame_height-0.5,
            z_range=[-L,L,1], z_length=config.frame_height-0.5
            ).set_color(BLACK)
        self.add(axes)

        sup = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func(u)),
            t_range=[0.0001, 8*PI],
            color = ORANGE
        ))
        self.add(sup)

        s = ValueTracker(0.0001)
        punto = always_redraw(
            lambda: Dot3D(
                axes.c2p(*(self.func(s.get_value()))),
                color = RED,
                radius = 0.08
            )
        )
        self.add(punto)

        tangente = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.func1(0, s.get_value())[1]),
                color = BLUE
            ))
        
        binormal = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.func1(0, s.get_value())[2]),
                color = GREEN
            ))
        
        normal = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.func1(0, s.get_value())[3]),
                color = RED
            ))
        triedro = VGroup(tangente, normal, binormal)
        self.add(triedro)

        osculadora = always_redraw(
            lambda: ParametricFunction(
            lambda u: axes.c2p(*self.func1(u, s.get_value())[4:7]),
            t_range=[0.0001, 2*PI],
            color = PURPLE
        ))
        self.add(osculadora)


        self.renderer.camera.light_source.move_to(3*IN) 
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate = 30*DEGREES, about = "theta")
        self.play(s.animate.set_value(8*PI),  run_time= 9, rate_func=linear)
        self.wait()

