def cartopy_crs(ds):
    """Converts a pyproj.Proj to a cartopy.crs.Projection
    Parameters
    ----------
    proj: pyproj.Proj
        the projection to convert
    Returns
    -------
    a cartopy.crs.Projection object
    """
    from osgeo import osr
    import cartopy.crs as ccrs

    proj = ds.GetProjection()
    inproj = osr.SpatialReference()
    inproj.ImportFromWkt(proj)
    srs = inproj.ExportToProj4()

    km_proj = {
        "lon_0": "central_longitude",
        "lat_0": "central_latitude",
        "x_0": "false_easting",
        "y_0": "false_northing",
        "k": "scale_factor",
        "zone": "zone",
    }
    km_globe = {
        "a": "semimajor_axis",
        "b": "semiminor_axis",
    }
    km_std = {
        "lat_1": "lat_1",
        "lat_2": "lat_2",
    }
    kw_proj = dict()
    kw_globe = dict()
    kw_std = dict()
    for s in srs.split("+"):
        s = s.split("=")
        if len(s) != 2:
            continue
        k = s[0].strip()
        v = s[1].strip()
        try:
            v = float(v)
        except BaseException:
            pass
        if k == "proj":
            if v == "tmerc":
                pycl = ccrs.TransverseMercator
            if v == "lcc":
                pycl = ccrs.LambertConformal
            if v == "merc":
                pycl = ccrs.Mercator
            if v == "utm":
                pycl = ccrs.UTM
            if v == "aea":
                pycl = ccrs.AlbersEqualArea
        if k in km_proj:
            kw_proj[km_proj[k]] = v
        if k in km_globe:
            kw_globe[km_globe[k]] = v
        if k in km_std:
            kw_std[km_std[k]] = v

    globe = None
    if kw_globe:
        globe = ccrs.Globe(**kw_globe)
    if kw_std:
        kw_proj["standard_parallels"] = (kw_std["lat_1"], kw_std["lat_2"])

    # mercatoooor
    if pycl.__name__ == "Mercator":
        kw_proj.pop("false_easting", None)
        kw_proj.pop("false_northing", None)

    return pycl(globe=globe, **kw_proj)
