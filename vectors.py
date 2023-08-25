import math

class Vector:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)): # If a list containing a list of coordinates is submitted, get the coordinates from that list.
            self.components = args[0]
        else:
            self.components = args
        self.components = list(self.components)
        self.dimensions = len(self.components)
    
    def __repr__(self):
        return f"{[component for component in self.components]}"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i+other for i in self.components])
        elif isinstance(other, (list, tuple)):
            return [self.components[i]+otherVal for i, otherVal in enumerate(other)]
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError("Vector dimensions do not match.")
            return Vector([self.components[i]+other.components[i] for i in range(self.dimensions)])
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i-other for i in self.components])
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError(f"Vector dimensions do not match. {self.dimensions, other.dimensions}")
            return Vector([self.components[i]-other.components[i] for i in range(self.dimensions)])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i*other for i in self.components])
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError("Vector dimensions do not match.")
            return Vector([self.components[i]*other.components[i] for i in range(self.dimensions)])
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector([i/other for i in self.components])
        elif isinstance(other, Vector):
            if self.dimensions != other.dimensions:
                raise ValueError("Vector dimensions do not match.")
            return Vector([self.components[i]/other.components[i] for i in range(self.dimensions)])
    
    def __abs__(self):
        return math.sqrt(sum(i**2 for i in self.components))
    
    def __setitem__(self, key, value):
        self.components[key] = value
    
    def __getitem__(self, key):
        return self.components[key]
    
    def direction(self):
        if self[1] >= 0:
            return math.acos(self[0] / abs(self))
        else:
            return math.pi*2 - math.acos(self[0] / abs(self))
    
    def rotatePygame(self, angle=0, rotateTo=0):
        if not rotateTo:
            rotateTo = self.direction() + angle
        length = abs(self)
        self.components = [math.cos(rotateTo) * length, -1 * math.sin(rotateTo) * length]
        return self

    def rotate(self, angle=0, rotateTo=0):
        """Only supports 2D!"""
        if not rotateTo:
            rotateTo = self.direction() + angle
        length = abs(self)
        self.components = [math.cos(rotateTo) * length, math.sin(rotateTo) * length]
        return self


def dotProduct(v1 : Vector, v2 : Vector):
    if v1.dimensions != v2.dimensions:
        raise ValueError("Vector Dimensions do not match.")
    return sum([v1.components[i]*v2.components[i] for i in range(v1.dimensions)])


if __name__ == "__main__":
    print(Vector(-2, 0).rotate(rotateTo=math.pi/2, debug=True))