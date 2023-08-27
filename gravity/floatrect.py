class FloatRect:
    def __init__(
        self,
        left: float | int,
        top: float | int,
        width: float | int,
        height: float | int,
    ):
        self.left = float(left)
        self.top = float(top)
        self.width = float(width)
        self.height = float(height)
