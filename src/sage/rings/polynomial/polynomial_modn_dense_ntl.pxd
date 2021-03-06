from sage.structure.element cimport Element, ModuleElement, RingElement
from sage.rings.polynomial.polynomial_element cimport Polynomial

from sage.libs.ntl.ntl_ZZ_p cimport ntl_ZZ_p
from sage.libs.ntl.ntl_ZZ_pX cimport ntl_ZZ_pX
from sage.libs.ntl.ntl_ZZ_pContext cimport ntl_ZZ_pContext_class

from sage.libs.ntl.ntl_lzz_p cimport ntl_zz_p
from sage.libs.ntl.ntl_lzz_pX cimport ntl_zz_pX
from sage.libs.ntl.ntl_lzz_pContext cimport ntl_zz_pContext_class

from sage.rings.integer cimport Integer

from sage.libs.ntl.ntl_ZZ_pX_decl cimport *, ZZ_pX_c, ZZ_pX_Modulus_c
from sage.libs.ntl.ntl_lzz_pX_decl cimport *, zz_pX_c, zz_pX_Modulus_c

#include "sage/libs/ntl/decl.pxi"

#cdef extern from "ntl_wrap.h":
#    struct zz_pX

cdef class Polynomial_dense_mod_n(Polynomial):
    cdef object __poly
    cdef object __singular
    cpdef ModuleElement _rmul_(self, RingElement c)
    cpdef ModuleElement _lmul_(self, RingElement c)

cdef class Polynomial_dense_modn_ntl_zz(Polynomial_dense_mod_n):
    cdef zz_pX_c x
    cdef ntl_zz_pContext_class c
    cdef Polynomial_dense_modn_ntl_zz _new(self)
    cpdef Polynomial_dense_modn_ntl_zz _mul_trunc(self, Polynomial_dense_modn_ntl_zz right, long n)

cdef class Polynomial_dense_modn_ntl_ZZ(Polynomial_dense_mod_n):
    cdef ZZ_pX_c x
    cdef ntl_ZZ_pContext_class c
    cdef Polynomial_dense_modn_ntl_ZZ _new(self)
    cpdef Polynomial_dense_modn_ntl_ZZ _mul_trunc(self, Polynomial_dense_modn_ntl_ZZ right, long n)

cdef class Polynomial_dense_mod_p(Polynomial_dense_mod_n):
    pass
