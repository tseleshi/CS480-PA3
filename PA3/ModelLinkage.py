"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random
import math

from Component import Component
from Shapes import Cube
from Shapes import Cylinder
from Shapes import Sphere
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Linkage(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    position = None #added this line

    def __init__(self, parent, position, shaderProg):
        super(Linkage, self).__init__(position)
        self.components = []
        #create anteater
        body = Cube(Point((0, 0, 0)), shaderProg, [0.3, 0.3, 0.3], color=Ct.ORANGE)
        arm1 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2 = ModelArm(parent, Point((0, 0, 0)), shaderProg, .3)
        arm2.setDefaultAngle(205, arm2.vAxis)
        arm3 = ModelArm(parent, Point((0, 0, 0)), shaderProg, .3)
        arm3.setDefaultAngle(145, arm3.vAxis)

        self.components = [body, arm1, arm2, arm3]
        self.addChild(body)
        self.addChild(arm1)
        self.addChild(arm2)
        self.addChild(arm3)

        self.rotation_speed = []
        for comp in self.components:

            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.5, 0, 0])

        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1

        #create ant1
        # Create the main body spheres
        body1 = Sphere(Point((-0.055, 1, 0)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        body2 = Sphere(Point((0, 1, 0)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        body3 = Sphere(Point((0.055, 1, 0)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)             

        # Create cylinders (legs) for each body
        leg1 = Cylinder(Point((-.055, 1, -.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg2 = Cylinder(Point((0, 1, -.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg3 = Cylinder(Point((0.055, 1, -.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)

        leg4 = Cylinder(Point((-0.055, 1, 0.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg5 = Cylinder(Point((0, 1, 0.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg6 = Cylinder(Point((0.055, 1, 0.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)

        # Set up the linkage components
        self.components = [body1, body2, body3, leg1, leg2, leg3, leg4, leg5, leg6]
        self.addChild(body1)
        self.addChild(body2)
        self.addChild(body3)
        self.addChild(leg1)
        self.addChild(leg2)
        self.addChild(leg3)
        self.addChild(leg4)
        self.addChild(leg5)
        self.addChild(leg6)

        #create ant2
        # Create the main body spheres
        body4 = Sphere(Point((.5, 1, 1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        body5 = Sphere(Point((.555, 1, 1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        body6 = Sphere(Point((.61, 1, 1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)             

        # Create cylinders (legs) for each body
        leg7 = Cylinder(Point((.5, 1, .9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg8 = Cylinder(Point((.555, 1, .9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg9 = Cylinder(Point((.61, 1, .9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)

        leg10 = Cylinder(Point((.5, 1, 1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg11 = Cylinder(Point((.555, 1, 1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg12 = Cylinder(Point((.61, 1, 1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)

        # Set up the linkage components
        self.components = [body4, body5, body6, leg7, leg8, leg9, leg10, leg11, leg12]
        self.addChild(body4)
        self.addChild(body5)
        self.addChild(body6)
        self.addChild(leg7)
        self.addChild(leg8)
        self.addChild(leg9)
        self.addChild(leg10)
        self.addChild(leg11)
        self.addChild(leg12)

    def getAnt1Components(self):
        return self.components[:6]  # Components for ant1

    def getAnt2Components(self):
        return self.components[6:]  # Components for ant2

    def setAnt1Position(self):
        ant1_components = self.getAnt1Components()
        average_position = sum(comp.getPosition() for comp in ant1_components) / len(ant1_components)
        self.position = average_position

    def setAnt2Position(self):
        ant2_components = self.getAnt2Components()
        average_position = sum(comp.getPosition() for comp in ant2_components) / len(ant2_components)
        self.position = average_position

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        for i, comp in enumerate(self.components):
            if isinstance(comp, Cylinder):
                # Rotate the leg back and forth to crawl
                rotation_angle = 25 * (1 + math.sin(0.1))
                #pivot_point = Point(0,0,0)
                #comp.rotate(rotation_angle, pivot_point, comp.uAxis)

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        #self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. Ths means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

       pass


class ModelArm(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]
