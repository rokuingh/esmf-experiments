<<<<<<< ESMCI_GlobalIds.h
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
>>>>>>> 1.4
#ifndef ESMCI_GlobalIds_h
#define ESMCI_GlobalIds_h
#include <Mesh/include/ESMCI_MeshObj.h>

#include <vector>

namespace ESMCI {

// Retrieve a list of new global ids, given the set of current ids
void GlobalIds(const std::vector<MeshObj::id_type> &current_ids,
                          std::vector<MeshObj::id_type> &new_ids);


} // namespace

#endif