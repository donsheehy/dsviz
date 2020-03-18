# Designing ds_viz

## Goals

I want a library that makes it easy to generate vector graphics figures using Python.

It should have a good list of primitives: point, line, circle, rectangle, polygon, text, etc.

It should be able to support a robust style mechanism.

It should be able to easily compose figures into larger figures.

It should be able to output to many formats, thinly wrapping around other libraries so as to not be too dependent on any one of them.

## Principles

### Primitive Shapes
These primitive shapes are created via methods on the Canvas.

- point
- text
- paths
  - line
  - polyline
  - circular arc
  - bezier curve
- shapes
  - circle
  - ellipse
  - rectangle
  - polygon

The primitives are mapped to a much smaller number of Drawing Primitives that are processed by the Image Engines:

- circle
- line
- polygon
- text

### Canvases

A canvas provides the drawing primitives and has the ability to write output as a string or to a file.

The canvas interface provides methods for drawing the primitives.

A style string is pass to the primitives.

The canvas stores a dictionary of styles associated with strings.

The canvas buffers all the primitives that are drawn and attempts to order them by z-order (which may be part of the style).

### Figure Elements
An element is a shape or a group of elements.  
Every element has
- a parent element (except for the root)
- a style
- a coordinate system
- a position in the parent's coordinate system
- a width
- a height
- a dictionary of anchors in the local coordinate system (see below)
- a function that returns anchors in the parent coordinate system.
- tags (set of strings)
- a draw function that takes **only** a canvas argument.

### Anchors

Figure elements provide natural attachment points called anchors that can be used for composing figures from multiple elements.

The anchors are stored with respect to the local coordinate system.

Anchors usually have a string name.

A function provides access to the anchors in the parent's coordinate system.


### Groups of Elements

A group of elements can be combined into a single element.

All the elements in the group have the group itself as a parent.

### Boxes

Putting a box around something is quite natural.  
Boxes have both padding and margin.  
Sometimes the boxes have width or height that is determined based on something in its parent element.  For example, in a vertical list, the width of the boxes, depends on the max width of any box in the list.

### The Figure

The figure is a tree of elements.  
The root is a group.  
There is a total order on the primitive elements so they can be drawn consistently.  

The canvas order Elements lexicographically by:
- The z-order of their style.
- The creation order.

Elements will often be placed with respect to each others' anchors.

### Models for Data Structure Visualization

To visualize a data structure, one implements a class that extends `ds_viz.Element`.
Ideally, the initializer takes a single instance of the class to be visualized.

The initializer might wrap the data structure in a separately tested wrapper that exposes some of the private attributes of the class.

### Styles

Styles are lists of dictionaries.

The standard way to describe styles is in TOML.

An object with a particular style will (usually) generate one primitive per style.

Styles properties can be split into drawing properties and layout properties.

Drawing properties are those that will be assigned to the drawing primitive and can be passed (more or less) directly to the drawing engine.

Layout properties will affect how the primitives are defined.  These could include the radius of a point, the padding around a box, the z order, etc.

### Image Engines

An `ImageEngine` provides a thin wrapper for translating primitives into whatever form is needed to produce an image file.


---

---

## Brainstorm

### The figure

A hierarchy of shapes
groups have their own coordinate system
transform an entire group
elements have positions, but also (a dict of) anchors for other elements to interact with.
elements keep track of their width and height

elements can also have tags
transform or style by tags (this allows pushing a tag to the back)

mechanisms for elements in a group to arrange themselves into a bigger picture.

Figures like a list drawn with boxes should be possible without hardcoding the sizes.

### Drawing order

The canvas gets drawn all in one go (in what order?).
DFS with children ordered by creation order.
This might not play nice with z order.
For example, if I was drawing a tree, I might want the subtrees to be their own elements.
This makes it hard to draw all the edges first.

The canvas should manage drawing order.

### Transformations

It is possible to apply a transformation to a group or an individual element.
These include:
- style overrides
- z-order shifting (both relative and absolute)
- translation
- rotation
- scaling (with consideration for strokes)

### Styles

Styles as dictionaries.  
Dealing with defaults
Lists of styles
support z order as a style feature.

A arrow heads part of the style?

### Drawing Data Structures

When subclassing a data structure to draw it, it might be better to create an `Exposed` class that provides access to the private members.
Then, the exposed data structure is tested only to see that the assumptions hold.
That is, it uses the exposed attributes and makes sure they behave as expected.

A typical example would be a stack.  There is no way to see inside the stack except the top element.
However, the Exposed version would give access to the list.
One would test the `ExposedStack` by pushing some elements and checking that the exposed list has the right elements in the right order.

Let's favor composition over inheritance.
That way, we can simply wrap the object that we want to use.
I don't know if it's better to reproduce the public interface in the new class, or just access the object.


This idea might be more generally useful, especially if there are special methods that are useful for drawing.
For example, it might make sense to provide an ordered list of attributes of a class, along with their names.

```python {cmd}
class DataStructure:
    def __init__(self, a, b):
        self.a = a
        self._b = b

class ExposedDataStructure:
    def __init__(self, ds):
        self.ds = ds

    @property
    def a(self):
        return self.ds.a

    @property
    def b(self):
        return self.ds._b

    _b = b

from ds_viz.element import Element
class VizDataStructure(Element):
    def __init__(self, ds):
        self.ds = ExposedDataStructure(ds)

    def draw(self, canvas):
        print("pretend this is a drawing")

X = DataStructure(2,3)
Y = ExposedDataStructure(X)
Z = VizDataStructure(X)
# print(Y.b)
print(Z.ds.a, Z.ds.b)
# Z.draw(None)
```