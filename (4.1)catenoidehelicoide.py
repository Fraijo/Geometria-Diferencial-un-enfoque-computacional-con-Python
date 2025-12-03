from manim import*

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class catenoide(ThreeDScene):
    def func1(self, u, v):
        c = 5
        return np.array([c * np.cosh(v/c) * np.cos(u), c * np.cosh(v/c) * np.sin(u), v])

    def func2(self, u, v):
        c = 5
        return np.array([u * np.cos(v), u * np.sin(v), c * v])

    def construct(self):
        s = ValueTracker(0)
        axes = ThreeDAxes(
            x_range=[-5,5,2],
            x_length=config.frame_height-0.5,
            y_range=[-5,5,2],
            y_length=config.frame_height-0.5,
            z_range=[-5,5,2],
            z_length=config.frame_height-0.5
            )

        catenoide1 = always_redraw(
            lambda: Surface(
            lambda u, v: axes.c2p(*self.func1(u, v)),
            u_range=[0, s.get_value()],
            v_range=[-5, 5],
            resolution=16,
            fill_opacity = 0.5
        )
        )

        catenoide = always_redraw(
            lambda: Surface(
            lambda u, v: axes.c2p(
                np.cos(s.get_value()) * np.sinh(v) * np.sin(u) + np.sin(s.get_value()) * np.cosh(v) * np.cos(u),
                - np.cos(s.get_value()) * np.sinh(v) * np.cos(u) + np.sin(s.get_value()) * np.cosh(v) * np.sin(u),
                u * np.cos(s.get_value()) + v * np.sin(s.get_value())
            ),
            u_range=[-PI, PI],
            v_range=[-1, 1],
            resolution=32,
            fill_opacity = 0.5
        )
        )
        #orientación cámara
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate = 30*DEGREES, about = "theta")
        #agregar a la escena
        self.add(axes, catenoide)
        self.play(s.animate.set_value(PI/2), rate_func=linear, run_time=9)
        self.wait()