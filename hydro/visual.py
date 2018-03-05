

def contour_2d(P, fig, extent=[0,1,0,1], caption=None):

    assert len(P.shape) is 2

    from numpy import linspace, logspace, log10
    from pylab import contour, figure, title

    Nx, Ny = P.shape
    P = P[2:Nx-2,2:Ny-2]
    Nx, Ny = P.shape

    X = linspace(-1, 1, Nx)
    Y = linspace(-1, 1, Ny)
    levels = logspace(log10(P.min()), log10(P.max()), 30)

    ax1 = fig.add_subplot(1,1,1)
    contour(X, Y, P, levels, extent=extent)
    ax1.set_aspect('equal')

    if title is not None:
        title(caption)


def four_pane_2d(P, *args, **kwargs):

    if P.shape[-1] is 1: scl_four_pane_2d(P, *args, **kwargs)
    if P.shape[-1] is 5: hyd_four_pane_2d(P, *args, **kwargs)
    if P.shape[-1] is 8: mhd_four_pane_2d(P, *args, **kwargs)


def scl_four_pane_2d(P, extent=[0,1,0,1], do_quiver=True, cmap=None, **kwargs):
    pass

def hyd_four_pane_2d(P, extent=[0,1,0,1], do_quiver=True, cmap=None, **kwargs):

    from pylab import flipud, subplot, title, colorbar, cm, imshow, quiver, matplotlib
    from numpy import sqrt, linspace, meshgrid

    rho, pre   = P[:,:,0], P[:,:,1]
    vx, vy, vz = P[:,:,2], P[:,:,3], P[:,:,4]

    if type(cmap) is str:
        from pickle import load
        cmap = load(open('rmhd/data/cmaps.pk'))[cmap]
    elif isinstance(cmap, matplotlib.colors.Colormap):
        pass
    else:
        cmap = cm.hot

    imargs = {'extent':extent, 'cmap':cmap, 'interpolation':'bilinear'}
    imargs.update(kwargs)

    tr = lambda x: flipud(x.T)

    subplot(2,2,1)
    imshow(tr(rho), **imargs)
    colorbar()
    title("Density")

    subplot(2,2,2)
    imshow(tr(pre), **imargs)
    colorbar()
    title("Pressure")

    subplot(2,2,3)
    imshow(tr(vx), **imargs)
    colorbar()
    title("X-Velocity")

    subplot(2,2,4)
    imshow(tr(vy), **imargs)
    colorbar()
    title("Y-Velocity")


def mhd_four_pane_2d(P, extent=[0,1,0,1], do_quiver=True, cmap=None, **kwargs):

    from pylab import flipud, subplot, title, colorbar, cm, imshow, quiver, matplotlib
    from numpy import sqrt, linspace, meshgrid

    rho, pre   = P[:,:,0], P[:,:,1]
    vx, vy, vz = P[:,:,2], P[:,:,3], P[:,:,4]
    Bx, By, Bz = P[:,:,5], P[:,:,6], P[:,:,7]

    B2 = Bx**2 + By**2 + Bz**2
    v2 = vx**2 + vy**2 + vz**2
    W  = 1.0 / sqrt(1.0 - v2)

    if type(cmap) is str:
        from pickle import load
        cmap = load(open('rmhd/data/cmaps.pk'))[cmap]
    elif isinstance(cmap, matplotlib.colors.Colormap):
        pass
    else:
        cmap = cm.hot

    imargs = {'extent':extent, 'cmap':cmap, 'interpolation':'bilinear'}
    imargs.update(kwargs)

    tr = lambda x: flipud(x.T)

    subplot(2,2,1)
    imshow(tr(rho), **imargs)
    colorbar()
    title("Density")

    subplot(2,2,2)
    imshow(tr(pre), **imargs)
    colorbar()
    title("Pressure")

    subplot(2,2,3)
    imshow(tr(B2), **imargs)
    colorbar()
    title("Magnetic Pressure")

    subplot(2,2,4)
    imshow(tr(W), **imargs)
    colorbar()
    title("Lorentz Factor")

    if do_quiver:
        N = 10
        X,Y = meshgrid(linspace(extent[0],extent[1],W.shape[0]),
                       linspace(extent[2],extent[3],W.shape[1]))
        quiver(X[::N,::N], Y[::N,::N], Bx[::N,::N].T, By[::N,::N].T, color='y')

    """
    Don't mess with the way the data are transposed here, I have checked carefully
    and for whatever reason (ask the matplotlib people) this is what gets consistent
    representation of the data in imshow and quiver.

    See link for examples on how to use quiver:
    http://matplotlib.sourceforge.net/examples/pylab_examples/quiver_demo.html
    """


def show():

    from pylab import show
    show()


def shocktube(P, *args, **kwargs):

    if P.shape[-1] is 1: scl_shocktube(P, *args, **kwargs)
    if P.shape[-1] is 5: hyd_shocktube(P, *args, **kwargs)
    if P.shape[-1] is 8: mhd_shocktube(P, *args, **kwargs)


def scl_shocktube(P, x=(0,1), **kwargs):

    from pylab import sqrt, linspace, subplot, plot, text, xlabel, figure, show
    from pylab import subplots_adjust, setp, gca, LinearLocator, rcParams, legend

    rho = P[:,0]

    plot_args = { }
    plot_args['marker'] = kwargs.get('marker', 'o')
    plot_args['c'     ] = kwargs.get('c'     , 'k')
    plot_args['mfc'   ] = kwargs.get('mfc'   , 'None')

    plot_args.update(kwargs)
    rcParams.update({'axes.labelsize':16, 'ytick.major.pad':8})

    X = linspace(x[0],x[1],P.shape[0])

    ax = subplot(1,1,1)
    plot(X,rho, **plot_args)
    text(0.9,0.85, r"$\rho$", transform = ax.transAxes, fontsize=20)
    if 'label' in plot_args: legend(loc='upper left')


def hyd_shocktube(P, x=(0,1), **kwargs):

    from pylab import sqrt, linspace, subplot, plot, text, xlabel, figure, show
    from pylab import subplots_adjust, setp, gca, LinearLocator, rcParams, legend

    rho, pre   = P[:,0], P[:,1]
    vx, vy, vz = P[:,2], P[:,3], P[:,4]

    plot_args = { }
    plot_args['marker'] = kwargs.get('marker', 'o')
    plot_args['c'     ] = kwargs.get('c'     , 'k')
    plot_args['mfc'   ] = kwargs.get('mfc'   , 'None')

    plot_args.update(kwargs)
    rcParams.update({'axes.labelsize':16, 'ytick.major.pad':8})

    X = linspace(x[0],x[1],P.shape[0])

    ax = subplot(2,2,1)
    plot(X,rho, **plot_args)
    text(0.9,0.85, r"$\rho$", transform = ax.transAxes, fontsize=20)
    setp(ax.get_xticklabels(), visible=False)
    if 'label' in plot_args: legend(loc='upper left')

    ax = subplot(2,2,2)
    plot(X,pre, **plot_args)
    text(0.9,0.85, r"$P$", transform = ax.transAxes, fontsize=20)
    setp(ax.get_xticklabels(), visible=False)

    ax = subplot(2,2,3)
    plot(X, vx, **plot_args)
    text(0.9,0.85, r"$v_x$", transform = ax.transAxes, fontsize=20)
    xlabel(r"$x$")

    ax = subplot(2,2,4)
    plot(X, vy, **plot_args)
    text(0.9,0.85, r"$v_y$", transform = ax.transAxes, fontsize=20)
    xlabel(r"$x$")

    subplots_adjust(hspace=0.15)


def mhd_shocktube(P, x=(0,1), **kwargs):

    from pylab import sqrt, linspace, subplot, plot, text, xlabel, figure, show
    from pylab import subplots_adjust, setp, gca, LinearLocator, rcParams, legend

    rho, pre   = P[:,0], P[:,1]
    vx, vy, vz = P[:,2], P[:,3], P[:,4]
    Bx, By, Bz = P[:,5], P[:,6], P[:,7]

    plot_args = { }
    plot_args['marker'] = kwargs.get('marker', 'o')
    plot_args['c'     ] = kwargs.get('c'     , 'k')
    plot_args['mfc'   ] = kwargs.get('mfc'   , 'None')

    plot_args.update(kwargs)
    rcParams.update({'axes.labelsize':16, 'ytick.major.pad':8})

    X = linspace(x[0],x[1],P.shape[0])
    g = 1 / sqrt(1-(vx**2+vy**2+vz**2))

    ax = subplot(2,3,1)
    plot(X,rho, **plot_args)
    text(0.9,0.85, r"$\rho$", transform = ax.transAxes, fontsize=20)
    setp(ax.get_xticklabels(), visible=False)
    if 'label' in plot_args: legend(loc='upper left')

    ax = subplot(2,3,2)
    plot(X,pre, **plot_args)
    text(0.9,0.85, r"$P$", transform = ax.transAxes, fontsize=20)
    setp(ax.get_xticklabels(), visible=False)

    ax = subplot(2,3,3)
    plot(X, g, **plot_args)
    text(0.9,0.85, r"$\gamma$", transform = ax.transAxes, fontsize=20)
    setp(ax.get_xticklabels(), visible=False)

    ax = subplot(2,3,4)
    plot(X, vx, **plot_args)
    text(0.9,0.85, r"$v_x$", transform = ax.transAxes, fontsize=20)
    xlabel(r"$x$")

    ax = subplot(2,3,5)
    plot(X, vy, **plot_args)
    text(0.9,0.85, r"$v_y$", transform = ax.transAxes, fontsize=20)
    xlabel(r"$x$")

    ax = subplot(2,3,6)
    plot(X, By, **plot_args)
    text(0.9,0.85, r"$B_y$", transform = ax.transAxes, fontsize=20)
    xlabel(r"$x$")

    subplots_adjust(hspace=0.15)
