"""
Hyperelliptic curve constructor
"""

#*****************************************************************************
#  Copyright (C) 2006 David Kohel <kohel@maths.usyd.edu>
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.schemes.projective.projective_space import ProjectiveSpace

from hyperelliptic_generic import HyperellipticCurve_generic
from hyperelliptic_finite_field import HyperellipticCurve_finite_field
from hyperelliptic_rational_field import HyperellipticCurve_rational_field
from hyperelliptic_padic_field import HyperellipticCurve_padic_field
from hyperelliptic_g2_generic import HyperellipticCurve_g2_generic
from hyperelliptic_g2_finite_field import HyperellipticCurve_g2_finite_field
from hyperelliptic_g2_rational_field import HyperellipticCurve_g2_rational_field
from hyperelliptic_g2_padic_field import HyperellipticCurve_g2_padic_field

from sage.rings.all import is_FiniteField, is_RationalField, is_Polynomial, is_pAdicField

def HyperellipticCurve(f, h=None, names=None, PP=None, check_squarefree=True):
    r"""
    Returns the hyperelliptic curve `y^2 + h y = f`, for
    univariate polynomials `h` and `f`. If `h`
    is not given, then it defaults to 0.

    INPUT:

    -  ``f`` - univariate polynomial

    -  ``h`` - optional univariate polynomial

    -  ``names``  (default: ``["x","y"]``) - names for the
       coordinate functions

    -  ``check_squarefree`` (default: ``True``) - test if
       the input defines a hyperelliptic curve when f is
       homogenized to degree `2g+2` and h to degree
       `g+1` for some g.

    .. WARNING::

        When setting ``check_squarefree=False`` or using a base ring that is
        not a field, the output curves are not to be trusted. For example, the
        output of ``is_singular`` is always ``False``, without this being
        properly tested in that case.

    .. NOTE::

        The words "hyperelliptic curve" are normally only used for curves of
        genus at least two, but this class allows more general smooth double
        covers of the projective line (conics and elliptic curves), even though
        the class is not meant for those and some outputs may be incorrect.

    EXAMPLES:

    Basic examples::

        sage: R.<x> = QQ[]
        sage: HyperellipticCurve(x^5 + x + 1)
        Hyperelliptic Curve over Rational Field defined by y^2 = x^5 + x + 1
        sage: HyperellipticCurve(x^19 + x + 1, x-2)
        Hyperelliptic Curve over Rational Field defined by y^2 + (x - 2)*y = x^19 + x + 1

        sage: k.<a> = GF(9); R.<x> = k[]
        sage: HyperellipticCurve(x^3 + x - 1, x+a)
        Hyperelliptic Curve over Finite Field in a of size 3^2 defined by y^2 + (x + a)*y = x^3 + x + 2

    Characteristic two::

        sage: P.<x> = GF(8,'a')[]
        sage: HyperellipticCurve(x^7+1, x)
        Hyperelliptic Curve over Finite Field in a of size 2^3 defined by y^2 + x*y = x^7 + 1
        sage: HyperellipticCurve(x^8+x^7+1, x^4+1)
        Hyperelliptic Curve over Finite Field in a of size 2^3 defined by y^2 + (x^4 + 1)*y = x^8 + x^7 + 1

        sage: HyperellipticCurve(x^8+1, x)
        Traceback (most recent call last):
        ...
        ValueError: Not a hyperelliptic curve: highly singular at infinity.

        sage: HyperellipticCurve(x^8+x^7+1, x^4)
        Traceback (most recent call last):
        ...
        ValueError: Not a hyperelliptic curve: singularity in the provided affine patch.

        sage: F.<t> = PowerSeriesRing(FiniteField(2))
        sage: P.<x> = PolynomialRing(FractionField(F))
        sage: HyperellipticCurve(x^5+t, x)
        Hyperelliptic Curve over Laurent Series Ring in t over Finite Field of size 2 defined by y^2 + x*y = x^5 + t

    We can change the names of the variables in the output::

        sage: k.<a> = GF(9); R.<x> = k[]
        sage: HyperellipticCurve(x^3 + x - 1, x+a, names=['X','Y'])
        Hyperelliptic Curve over Finite Field in a of size 3^2 defined by Y^2 + (X + a)*Y = X^3 + X + 2

    This class also allows curves of genus zero or one, which are strictly
    speaking not hyperelliptic::

        sage: P.<x> = QQ[]
        sage: HyperellipticCurve(x^2+1)
        Hyperelliptic Curve over Rational Field defined by y^2 = x^2 + 1
        sage: HyperellipticCurve(x^4-1)
        Hyperelliptic Curve over Rational Field defined by y^2 = x^4 - 1
        sage: HyperellipticCurve(x^3+2*x+2)
        Hyperelliptic Curve over Rational Field defined by y^2 = x^3 + 2*x + 2

    Double roots::

        sage: P.<x> = GF(7)[]
        sage: HyperellipticCurve((x^3-x+2)^2*(x^6-1))
        Traceback (most recent call last):
        ...
        ValueError: Not a hyperelliptic curve: singularity in the provided affine patch.

        sage: HyperellipticCurve((x^3-x+2)^2*(x^6-1), check_squarefree=False)
        Hyperelliptic Curve over Finite Field of size 7 defined by y^2 = x^12 + 5*x^10 + 4*x^9 + x^8 + 3*x^7 + 3*x^6 + 2*x^4 + 3*x^3 + 6*x^2 + 4*x + 3

    The input for a (smooth) hyperelliptic curve of genus `g` should not
    contain polynomials of degree greater than `2g+2`. In the following
    example, the hyperelliptic curve has genus 2 and there exists a model
    `y^2 = F` of degree 6, so the model `y^2 + yh = f` of degree 200 is not
    allowed.::

        sage: P.<x> = QQ[]
        sage: h = x^100
        sage: F = x^6+1
        sage: f = F-h^2/4
        sage: HyperellipticCurve(f, h)
        Traceback (most recent call last):
        ...
        ValueError: Not a hyperelliptic curve: highly singular at infinity.

        sage: HyperellipticCurve(F)
        Hyperelliptic Curve over Rational Field defined by y^2 = x^6 + 1

    An example with a singularity over an inseparable extension of the
    base field::

        sage: F.<t> = GF(5)[]
        sage: P.<x> = F[]
        sage: HyperellipticCurve(x^5+t)
        Traceback (most recent call last):
        ...
        ValueError: Not a hyperelliptic curve: singularity in the provided affine patch.

    Input with integer coefficients creates objects with the integers
    as base ring, but only checks smoothness over `\QQ`, not over Spec(`\ZZ`).
    In other words, it is checked that the discriminant is non-zero, but it is
    not checked whether the discriminant is a unit in `\ZZ^*`.::

        sage: P.<x> = ZZ[]
        sage: HyperellipticCurve(3*x^7+6*x+6)
        Hyperelliptic Curve over Integer Ring defined by y^2 = 3*x^7 + 6*x + 6
    """
    if (not is_Polynomial(f)) or f == 0:
        raise TypeError, "Arguments f (=%s) and h (= %s) must be polynomials " \
                         "and f must be non-zero" % (f,h)
    P = f.parent()
    if h is None:
        h = P(0)
    try:
        h = P(h)
    except TypeError:
        raise TypeError, \
              "Arguments f (=%s) and h (= %s) must be polynomials in the same ring"%(f,h)
    df = f.degree()
    dh_2 = 2*h.degree()
    if dh_2 < df:
        g = (df-1)//2
    else:
        g = (dh_2-1)//2
    if check_squarefree:
        # Assuming we are working over a field, this checks that after
        # resolving the singularity at infinity, we get a smooth double cover
        # of P^1.
        if P(2) == 0:
            # characteristic 2
            if h == 0:
                raise ValueError, \
                   "In characteristic 2, argument h (= %s) must be non-zero."%h
            if h[g+1] == 0 and f[2*g+1]**2 == f[2*g+2]*h[g]**2:
                raise ValueError, "Not a hyperelliptic curve: " \
                                  "highly singular at infinity."
            should_be_coprime = [h, f*h.derivative()**2+f.derivative()**2]
        else:
            # characteristic not 2
            F = f + h**2/4
            if not F.degree() in [2*g+1, 2*g+2]:
                raise ValueError, "Not a hyperelliptic curve: " \
                                  "highly singular at infinity."
            should_be_coprime = [F, F.derivative()]
        try:
            smooth = should_be_coprime[0].gcd(should_be_coprime[1]).degree()==0
        except (AttributeError, NotImplementedError, TypeError):
            try:
                smooth = should_be_coprime[0].resultant(should_be_coprime[1])!=0
            except (AttributeError, NotImplementedError, TypeError):
                raise NotImplementedError, "Cannot determine whether " \
                      "polynomials %s have a common root. Use " \
                      "check_squarefree=False to skip this check." % \
                      should_be_coprime
        if not smooth:
            raise ValueError, "Not a hyperelliptic curve: " \
                              "singularity in the provided affine patch."
    R = P.base_ring()
    PP = ProjectiveSpace(2, R)
    if names is None:
        names = ["x","y"]
    if is_FiniteField(R):
        if g == 2:
            return HyperellipticCurve_g2_finite_field(PP, f, h, names=names, genus=g)
        else:
            return HyperellipticCurve_finite_field(PP, f, h, names=names, genus=g)
    elif is_RationalField(R):
        if g == 2:
            return HyperellipticCurve_g2_rational_field(PP, f, h, names=names, genus=g)
        else:
            return HyperellipticCurve_rational_field(PP, f, h, names=names, genus=g)
    elif is_pAdicField(R):
        if g == 2:
            return HyperellipticCurve_g2_padic_field(PP, f, h, names=names, genus=g)
        else:
            return HyperellipticCurve_padic_field(PP, f, h, names=names, genus=g)
    else:
        if g == 2:
            return HyperellipticCurve_g2_generic(PP, f, h, names=names, genus=g)
        else:
            return HyperellipticCurve_generic(PP, f, h, names=names, genus=g)
