from __future__ import annotations

import pydantic
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

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
    url: pydantic.AnyHttpUrl = Query(
        ...,
        description='URL to a zarr store',
        example='https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/HadISST-feedstock/hadisst.zarr',
    )
):

    import xarray as xr

    with xr.open_dataset(url, engine='zarr', chunks={}) as ds:
        html = ds._repr_html_().strip()

    del ds

    return {'html': html, 'dataset': url}
