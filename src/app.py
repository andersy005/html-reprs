from __future__ import annotations

import pydantic
from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

origins = ['*']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def index():
    return {'message': 'Hello World!'}


@app.get('/xarray/')
def xarray(
    url: pydantic.AnyUrl = Query(
        ...,
        description='URL to a zarr store',
        example='https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/HadISST-feedstock/hadisst.zarr',
    )
):

    import xarray as xr
    import zarr

    try:

        with xr.open_dataset(url, engine='zarr', chunks={}) as ds:
            html = ds._repr_html_().strip()

        del ds

        return {'html': html, 'dataset': url}

    except (zarr.errors.GroupNotFoundError, FileNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': f'Dataset not found. Check the URL: {url}'},
        )

    except PermissionError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'message': f'Permission denied. Check the URL: {url}.'},
        )
