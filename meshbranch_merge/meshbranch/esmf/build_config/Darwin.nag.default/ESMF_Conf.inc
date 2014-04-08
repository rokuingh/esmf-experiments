#if 0
$Id: ESMF_Conf.inc,v 1.10 2010/04/23 04:24:31 w6ws Exp $

Earth System Modeling Framework
Copyright 2002-2010, University Corporation for Atmospheric Research,
Massachusetts Institute of Technology, Geophysical Fluid Dynamics
Laboratory, University of Michigan, National Centers for Environmental
Prediction, Los Alamos National Laboratory, Argonne National Laboratory,
NASA Goddard Space Flight Center.
Licensed under the University of Illinois-NCSA License.
#endif

#if 0
Define the proper way to flush Fortran units.  Typically this will
be one of the following:

  * Fortran-2003 FLUSH statement (preferred and default)
  * Two argument FLUSH call
  * One argument FLUSH call

  Use F2003 FLUSH statement from 5.2-onwards NAG, because
  the library call has thread-safety problems.  If a pre-5.2
  compiler is being used, enable the following macros.
#endif
#if 0
#define ESMF_NAG_UNIXIO_MODULE
#define ESMF_IOFlushMacro(unit,status) call flush (unit, status)
#endif

#if 0
In the ESMF_Config.F90 source file, if EOL is defined
as achar(10) (which is the newline character), 
the file cannot be compiled (it will not parse). 
If a bug fix for this is released, the next #define can
be removed.
#endif

#define ESMF_HAS_ACHAR_BUG 1
