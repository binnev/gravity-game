from pygame import Rect

from gravity.viewport_handler import FloatRect


class Transform:
    """
    Convert from xy (game coords) -> uv (screen coords) and back
    """

    scale: float
    u_offset: float
    v_offset: float

    def __init__(self, viewport_rect_xy: Rect, image_rect_uv: Rect):
        image_u, image_v, image_width_u, image_height_v = image_rect_uv
        viewport_x, viewport_y, viewport_width_x, viewport_height_y = viewport_rect_xy
        x_scale = image_width_u / viewport_width_x
        y_scale = image_height_v / viewport_height_y
        scale = min(x_scale, y_scale)
        self.scale = scale

        viewport_width_u = viewport_width_x * scale
        viewport_height_v = viewport_height_y * scale
        delta_u = (image_width_u - viewport_width_u) / 2
        delta_v = (image_height_v - viewport_height_v) / 2
        self.u_offset = delta_u - viewport_x * self.scale
        self.v_offset = delta_v - viewport_y * self.scale

    def length(self, length_xy: float) -> float:
        return length_xy * self.scale

    def point(self, point_xy: tuple[float, float]) -> tuple[float, float]:
        x, y = point_xy
        u = x * self.scale + self.u_offset
        v = y * self.scale + self.v_offset
        return u, v

    def rect(self, rect_xy: Rect) -> Rect:
        return Rect(*self.floatrect(rect_xy))

    def floatrect(self, rect_xy: FloatRect | Rect) -> FloatRect:
        x, y, width_x, height_y = rect_xy
        u, v = self.point((x, y))
        width_u = self.length(width_x)
        height_v = self.length(height_y)
        return u, v, width_u, height_v
