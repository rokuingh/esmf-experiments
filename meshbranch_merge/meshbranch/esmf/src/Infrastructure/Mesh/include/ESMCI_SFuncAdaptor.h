<<<<<<< ESMCI_SFuncAdaptor.h
=======
//
// Earth System Modeling Framework
// Copyright 2002-2010, University Corporation for Atmospheric Research, 
// Massachusetts Institute of Technology, Geophysical Fluid Dynamics 
// Laboratory, University of Michigan, National Centers for Environmental 
// Prediction, Los Alamos National Laboratory, Argonne National Laboratory, 
// NASA Goddard Space Flight Center.
// Licensed under the University of Illinois-NCSA License.

//
//-----------------------------------------------------------------------------
>>>>>>> 1.3
#ifndef ESMCI_SFuncAdaptor_h
#define ESMCI_SFuncAdaptor_h

#include <Mesh/include/ESMCI_MeshTypes.h>
#include <Mesh/include/ESMCI_ShapeFunc.h>
#include <Mesh/include/ESMCI_Exception.h>

#include <string>

namespace ESMCI {


/**
 * Adapt these low level shape functions to the ShapeFunc interface.
 * @ingroup shapefunc
 */
template<typename SFUNC>
class SFuncAdaptor : public ShapeFunc {
private:
  SFuncAdaptor() : ShapeFunc(), m_name("SFunc_Adapt_" + SFUNC::name) {}
  static SFuncAdaptor *classInstance;
public:
  static SFuncAdaptor *instance();
  ~SFuncAdaptor() {}
  UInt NumFunctions() const { return SFUNC::ndofs; }
  UInt ParametricDim() const { return SFUNC::pdim; }
  UInt IntgOrder() const { return SFUNC::iorder; }

  void shape(UInt npts, const double pcoord[], double results[]) const {
    SFUNC::shape(npts, pcoord, results);
  }

  void shape(UInt npts, const fad_type pcoord[], fad_type results[]) const {
    SFUNC::shape(npts, pcoord, results);
  }

  void shape_grads(UInt npts, const double pcoord[], double results[]) const {
    SFUNC::shape_grads(npts, pcoord, results);
  }

  void shape_grads(UInt npts, const fad_type pcoord[], fad_type results[]) const {
    SFUNC::shape_grads(npts, pcoord, results);
  }

  ShapeFunc *side_shape(UInt side_num) const;

  const std::string &name() const { return m_name; }

  bool is_nodal() const { return SFUNC::is_nodal(); }
  
  UInt orientation() const {  return SFUNC::is_nodal() ?
                ShapeFunc::ME_NODAL : ShapeFunc::ME_ELEMENTAL; }

  const int *edge_perm(bool) const {
    Throw() << "no edge perm for SFuncAdaptor";
  }

  const int *face_perm(UInt,bool) const {
    Throw() << "no face perm for SFuncAdaptor";
  }

  UInt NumInterp() const { return SFUNC::NumInterp; }

  const double *InterpPoints() const { return SFUNC::ipoints; }

  void Interpolate(const double fvals[], double mcoef[]) const {
    std::copy(fvals, fvals+NumFunctions(), mcoef);
  }
  void Interpolate(const fad_type fvals[], fad_type mcoef[]) const {
    std::copy(fvals, fvals+NumFunctions(), mcoef);
  }

  const int *DofDescriptionTable() const { return &SFUNC::dof_description[0][0]; }

private:
  std::string m_name;
};

} // namespace

#endif