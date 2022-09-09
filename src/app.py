from __future__ import annotations

import pydantic
import xarray as xr
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'message': 'Hello World!'}


@app.get('/xarray/')
def xarray(dataset: pydantic.AnyHttpUrl = None):

    ds = xr.open_dataset(dataset, engine='zarr', chunks={})

    return {'repr': ds._repr_html_().strip(), 'dataset': dataset}
