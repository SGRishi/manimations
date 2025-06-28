from manim import *
import numpy as np

# Use Roboto for all text
config.font = "Roboto"

class FallWithTension(Scene):
    def construct(self):
        mass = 5  # kg
        g = 9.8   # m/s^2
        rope_length = 2
        ceiling_start_y = 3
        total_time = 4

        t = ValueTracker(0.0)

        def ceiling_y():
            tau = t.get_value()
            if tau <= 1.0:
                return ceiling_start_y
            dt = tau - 1.0
            return ceiling_start_y - 0.5 * g * dt ** 2

        def object_y():
            return ceiling_y() - rope_length

        ceiling = Rectangle(width=4, height=0.3, fill_opacity=1, color=GRAY)
        obj = Square(side_length=0.5, fill_opacity=1, color=BLUE)

        ceiling.add_updater(lambda m: m.move_to(UP * ceiling_y()))
        obj.add_updater(lambda m: m.move_to(UP * object_y()))
        rope = always_redraw(lambda: Line(ceiling.get_bottom(), obj.get_top(), color=WHITE))

        mass_label = always_redraw(lambda: Text("5 kg", font_size=24).next_to(obj, RIGHT))

        self.play(FadeIn(ceiling, obj, rope, mass_label))

        # Axes for tension graph
        ax = Axes(
            x_range=[0, total_time, 1],
            y_range=[0, mass * g + 1, mass * g / 2],
            x_length=5,
            y_length=3,
        ).to_corner(UR)
        ax_labels = ax.get_axis_labels(Text("t (s)"), Text("T (N)"))
        self.play(Create(ax), FadeIn(ax_labels))

        def tension_func(tau):
            if tau <= 1.0:
                return mass * g
            else:
                return 0.0

        tension_graph = always_redraw(
            lambda: ax.plot(
                tension_func,
                x_range=[0, max(t.get_value(), 0.001)],
                color=RED,
            )
        )
        self.play(FadeIn(tension_graph))

        self.play(t.animate.set_value(total_time), run_time=total_time, rate_func=linear)
        self.wait()

