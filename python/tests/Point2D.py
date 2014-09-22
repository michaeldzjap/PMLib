from numbers import Number

class Point2D(object):

  def __init__(self,x=0,y=0):
    self._x = x
    self._y = y

  @property
  def x(self):
    """x-coordinate"""
    return self._x

  @property
  def y(self):
    """y-coordinate"""
    return self._y

  @x.setter
  def x(self,newX):
    self._x = newX

  @y.setter
  def y(self,newY):
    self._y = newY

  def __lt__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x < other.x and self._y < other.y else False
    elif isinstance(other,Number):
      bl = True if self._x < other and self._y < other else False

    return bl

  def __le__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x <= other.x and self._y <= other.y else False
    elif isinstance(other,Number):
      bl = True if self._x <= other and self._y <= other else False

    return bl

  def __eq__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x == other.x and self._y == other.y else False
    elif isinstance(other,Number):
      bl = True if self._x == other and self._y == other else False

    return bl

  def __ne__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x != other.x or self._y != other.y else False
    elif isinstance(other,Number):
      bl = True if self._x != other or self._y != other else False

    return bl

  def __gt__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x > other.x and self._y > other.y else False
    elif isinstance(other,Number):
      bl = True if self._x > other and self._y > other else False

    return bl

  def __ge__(self,other):
    bl = None
    if isinstance(other,self.__class__):
      bl = True if self._x >= other.x and self._y >= other.y else False
    elif isinstance(other,Number):
      bl = True if self._x >= other and self._y >= other else False

    return bl
