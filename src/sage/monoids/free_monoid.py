r"""
Free Monoids

AUTHORS:

- David Kohel (2005-09)
- Simon King (2011-04): Put free monoids into the category framework

Sage supports free monoids on any prescribed finite number
`n\geq 0` of generators. Use the ``FreeMonoid``
function to create a free monoid, and the ``gen`` and
``gens`` functions to obtain the corresponding
generators. You can print the generators as arbitrary strings using
the optional ``names`` argument to the
``FreeMonoid`` function.
"""

#*****************************************************************************
#  Copyright (C) 2005 David Kohel <kohel@maths.usyd.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty
#    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License for more details; the full text
#  is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.rings.integer import Integer
from sage.structure.parent_gens import normalize_names
from free_monoid_element import FreeMonoidElement

from monoid import Monoid_class


from sage.structure.factory import UniqueFactory
from sage.misc.cachefunc import cached_method

class FreeMonoidFactory(UniqueFactory):
    """
    Returns a free monoid on `n` generators.

    INPUT:


    -  ``n`` - integer

    -  ``names`` - names of generators


    OUTPUT: free abelian monoid

    EXAMPLES::

        sage: FreeMonoid(0,'')
        Free monoid on 0 generators ()
        sage: F.<a,b,c,d,e> = FreeMonoid(5); F
        Free monoid on 5 generators (a, b, c, d, e)
        sage: F(1)
        1
        sage: mul([ a, b, a, c, b, d, c, d ], F(1))
        a*b*a*c*b*d*c*d
    """
    def create_key(self, n, names):
        n = int(n)
        names = normalize_names(n, names)
        return (n, names)

    def create_object(self, version, key):
        return FreeMonoid_class(*key)

FreeMonoid = FreeMonoidFactory("FreeMonoid")


def is_FreeMonoid(x):
    """
    Return True if `x` is a free monoid.

    EXAMPLES::

        sage: from sage.monoids.free_monoid import is_FreeMonoid
        sage: is_FreeMonoid(5)
        False
        sage: is_FreeMonoid(FreeMonoid(7,'a'))
        True
        sage: is_FreeMonoid(FreeAbelianMonoid(7,'a'))
        False
        sage: is_FreeMonoid(FreeAbelianMonoid(0,''))
        False
    """
    return isinstance(x, FreeMonoid_class)

class FreeMonoid_class(Monoid_class):
    """
    The free monoid on `n` generators.
    """
    Element = FreeMonoidElement
    def __init__(self, n, names=None):
        """
        Create free monoid on `n` generators.

        INPUT:

        -  ``n`` - integer

        -  ``names`` - (optional) variable name or list of
           variable names


        EXAMPLES::

            sage: F = FreeMonoid(3,'x'); F
            Free monoid on 3 generators (x0, x1, x2)
            sage: x = F.gens()
            sage: x[0]*x[1]**5 * (x[0]*x[2])
            x0*x1^5*x0*x2
            sage: F = FreeMonoid(3, 'a')
            sage: F
            Free monoid on 3 generators (a0, a1, a2)

        ::

            sage: M = FreeMonoid(3, names=['a','b','c'])
            sage: TestSuite(M).run()
        """
        if not isinstance(n, (int, long, Integer)):
            raise TypeError, "n (=%s) must be an integer."%n
        if n < 0:
            raise ValueError, "n (=%s) must be nonnegative."%n
        self.__ngens = int(n)
        #self._assign_names(names)
        Monoid_class.__init__(self,names)

    def __cmp__(self, other):
        if not isinstance(other, FreeMonoid_class):
            return -1
        c = cmp(self.__ngens, other.__ngens)
        if c: return c
        if self.variable_names() == other.variable_names():
            return 0
        return 1

    def _repr_(self):
        return "Free monoid on %s generators %s"%(self.__ngens,self.gens())

    def _element_constructor_(self, x, check=True):
        """
        Return `x` coerced into this free monoid.

        One can create a free monoid from the integer 1 and from a list of
        2-tuples of integers `(i,j)`, where `(i,j)`
        corresponds to `x_i^j`, where `x_i` is the
        `i`th generator.

        EXAMPLES::

            sage: F = FreeMonoid(3, 'a')
            sage: F(1)
            1
            sage: F(F.gen(0))
            a0
            sage: F(0)
            Traceback (most recent call last):
            ...
            TypeError: Argument x (= 0) is of the wrong type.

        ::

            sage: F([(0,5),(1,2),(0,10),(0,2),(1,2)])
            a0^5*a1^2*a0^12*a1^2
        """
        ## There should really some careful type checking here...
        if isinstance(x, FreeMonoidElement) and x.parent() is self:
                return x
        if isinstance(x, FreeMonoidElement) and x.parent() == self:
            return self.element_class(self,x._element_list,check)
        elif isinstance(x, (int, long, Integer)) and x == 1:
            return self.element_class(self, x, check)
        elif isinstance(x, list):
            return self.element_class(self, x, check)
        else:
            raise TypeError, "Argument x (= %s) is of the wrong type."%x

    def __contains__(self, x):
        return isinstance(x, FreeMonoidElement) and x.parent() == self

    def gen(self,i=0):
        """
        The `i`-th generator of the monoid.

        INPUT:

        -  ``i`` - integer (default: 0)

        EXAMPLES::

            sage: F = FreeMonoid(3, 'a')
            sage: F.gen(1)
            a1
            sage: F.gen(2)
            a2
            sage: F.gen(5)
            Traceback (most recent call last):
            ...
            IndexError: Argument i (= 5) must be between 0 and 2.
        """
        n = self.__ngens
        if i < 0 or not i < n:
            raise IndexError, "Argument i (= %s) must be between 0 and %s."%(i, n-1)
        return self.element_class(self,[(Integer(i),Integer(1))])

    def ngens(self):
        """
        The number of free generators of the monoid.

        EXAMPLES::

            sage: F = FreeMonoid(2005, 'a')
            sage: F.ngens()
            2005
        """
        return self.__ngens

    @cached_method
    def one_element(self):
        """
        Returns the identity element in this monoid.

        EXAMPLES::

            sage: F = FreeMonoid(2005, 'a')
            sage: F.one_element()
            1
        """
        return self(1)
