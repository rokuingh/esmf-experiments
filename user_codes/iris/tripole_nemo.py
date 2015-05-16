# This example demonstrates how to use ESMPy with MetOffice tripole grids.

import ESMF
import numpy
import netCDF4 as nc
import os

g1 = "nemo"
g2 = "nemo"

grids = {}
# filename, filetype, addcornerstagger, coordnames, addmask, varname, srclons, srclats, srclonbnds, srclatbnds
grids["nemo"] = ("data/nemo_025_sample_grid.nc",
                 ESMF.FileFormat.GRIDSPEC, True, False, "",
                 "nav_lon", "nav_lat", "nav_lon_bnds", "nav_lat_bnds")
grids["orca"] = ("data/ORCA2_1d_00010101_00010101_grid_T_0000.nc",
                 ESMF.FileFormat.GRIDSPEC, True, False, "",
                 "nav_lon", "nav_lat", "nav_lon_bnds", "nav_lat_bnds")
grids["pop"] = ("data/tx0.1v2_070911.nc",
                ESMF.FileFormat.SCRIP, True, True, "grid_imask",
                "grid_center_lon", "grid_center_lat", "grid_corner_lon", "grid_corner_lat")
grids["ll1deg"] = ("data/ll1deg_grid.nc",
                   ESMF.FileFormat.SCRIP, True, False, "",
                   "grid_center_lon", "grid_center_lat", "grid_corner_lon", "grid_corner_lat")
grids["ll2.5deg"] = ("data/ll2.5deg_grid.nc",
                   ESMF.FileFormat.SCRIP, True, False, "",
                   "grid_center_lon", "grid_center_lat", "grid_corner_lon", "grid_corner_lat")


def create_grid(g):

    grid = ESMF.Grid(filename=grids[g][0], filetype=grids[g][1], add_corner_stagger=grids[g][2],
              add_mask=grids[g][3], varname=grids[g][4], coord_names=[grids[g][5], grids[g][6]])

    return grid

def initialize_field(field):

    # realistic source data
    # f = nc.Dataset(grids[g1][0])
    # sohefldo = f.variables['sohefldo']
    # sohefldo = sohefldo[:]
    # # transpose because this data is represented as lat/lon
    # srcfield.data[...] = sohefldo[0, :, :].T

    # get the coordinate pointers and set the coordinates
    [lon, lat] = [0, 1]
    gridXCoord = field.grid.get_coords(lon, ESMF.StaggerLoc.CENTER)
    gridYCoord = field.grid.get_coords(lat, ESMF.StaggerLoc.CENTER)

    deg2rad = 3.14159 / 180

    field.data[...] = 10.0 + (gridXCoord * deg2rad) ** 2 + (gridYCoord * deg2rad) ** 2

def validate(srcfield, dstfield, xctfield, srcfracfield, dstfracfield):
    # get the area fields
    srcareafield = ESMF.Field(srcfield.grid, name='srcareafield')
    dstareafield = ESMF.Field(dstfield.grid, name='dstareafield')

    srcareafield.get_area()
    dstareafield.get_area()

    csrverr = 0
    srcmass = numpy.sum(numpy.abs(srcareafield.data * srcfracfield.data * srcfield.data))
    dstmass = numpy.sum(numpy.abs(dstareafield.data * dstfield.data))
    if dstmass is not 0:
        csrverr = numpy.abs(srcmass - dstmass) / dstmass

    # compute the mean relative interpolation and conservation error
    from operator import mul

    ind = numpy.where((dstfield.data != 1e20) & (xctfield.data != 0) & (dstfracfield.data > .999))
    num_nodes = reduce(mul, xctfield[ind].shape)
    relerr = numpy.sum(
        numpy.abs(dstfield.data[ind] / dstfracfield.data[ind] - xctfield.data[ind]) / numpy.abs(xctfield.data[ind]))
    meanrelerr = relerr / num_nodes

    # handle the parallel case
    if ESMF.pet_count() > 1:
        try:
            from mpi4py import MPI
        except:
            raise ImportError
        comm = MPI.COMM_WORLD
        relerr = comm.reduce(relerr, op=MPI.SUM)
        num_nodes = comm.reduce(num_nodes, op=MPI.SUM)
        srcmass = comm.reduce(srcmass, op=MPI.SUM)
        dstmass = comm.reduce(dstmass, op=MPI.SUM)

    # output the results from one processor only
    if ESMF.local_pet() is 0:
        meanrelerr = relerr / num_nodes
        csrverr = numpy.abs(srcmass - dstmass) / dstmass

        print "ESMPy Tripole Regridding Example"
        print "  interpolation mean relative error = {0}".format(meanrelerr)
        print "  mass conservation relative error  = {0}".format(csrverr)

    srcareafield.destroy()
    dstareafield.destroy()

def plot(srcfield, interpfield):
    # source data
    f = nc.Dataset(grids[g1][0])
    srclons = f.variables[grids[g1][5]][:]
    srclats = f.variables[grids[g1][6]][:]

    # read grid coordinates
    f2 = nc.Dataset(grids[g2][0])
    dstlons = f2.variables[grids[g2][5]][:]
    dstlats = f2.variables[grids[g2][6]][:]

    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except:
        raise ImportError("matplotlib is not available on this machine")

    fig = plt.figure(1, (15, 6))
    fig.suptitle('ESMPy Conservative Regridding', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(1, 2, 1)
    im = ax.imshow(srcfield.T, cmap='gist_ncar', aspect='auto',
                   extent=[numpy.min(srclons), numpy.max(srclons), numpy.min(srclats), numpy.max(srclats)])
    ax.set_xbound(lower=numpy.min(srclons), upper=numpy.max(srclons))
    ax.set_ybound(lower=numpy.min(srclats), upper=numpy.max(srclats))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Source Data")

    ax = fig.add_subplot(1, 2, 2)
    im = ax.imshow(interpfield.T, cmap='gist_ncar', aspect='auto',
                   extent=[numpy.min(dstlons), numpy.max(dstlons), numpy.min(dstlats), numpy.max(dstlats)])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Conservative Regrid Solution")

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.9, 0.1, 0.01, 0.8])
    fig.colorbar(im, cax=cbar_ax)

    plt.show()

###################################################################################

# this will enable ESMF logging
ESMF.Manager(debug=True)

# Create a grid1
grid1 = create_grid(g1)
# fix the wonky coords in the nemo grid
if g1 == "nemo":
    grid1.coords[0][1][:, 498] = 0

# Create a grid2
grid2 = create_grid(g2)
# fix the wonky coords in the nemo agrid
if g2 == "nemo":
    grid2.coords[0][1][:, 498] = 0

# create a field on the center stagger locations of the source grid
srcfield = ESMF.Field(grid1, name='srcfield', staggerloc=ESMF.StaggerLoc.CENTER)

# create fields on the center stagger locations of the other grid
dstfield = ESMF.Field(grid2, name='dstfield', staggerloc=ESMF.StaggerLoc.CENTER)
xctfield = ESMF.Field(grid2, name='xctfield', staggerloc=ESMF.StaggerLoc.CENTER)

# create fields needed to analyze accuracy of conservative regridding
srcfracfield = ESMF.Field(grid1, name='srcfracfield')
dstfracfield = ESMF.Field(grid2, name='dstfracfield')

initialize_field(srcfield)
initialize_field(xctfield)
dstfield.data[...] = 1e20

# create an object to regrid data from the source to the destination field
regrid = ESMF.Regrid(srcfield, dstfield,
                     regrid_method=ESMF.RegridMethod.CONSERVE,
                     unmapped_action=ESMF.UnmappedAction.IGNORE,
                     src_frac_field=srcfracfield,
                     dst_frac_field=dstfracfield)

# do the regridding from source to destination field
dstfield = regrid(srcfield, dstfield)

validate(srcfield, dstfield, xctfield, srcfracfield, dstfracfield)

plot(srcfield, dstfield)

# clean up
srcfield.destroy()
dstfield.destroy()
xctfield.destroy()
srcfracfield.destroy()
dstfracfield.destroy()
grid1.destroy()
grid2.destroy()