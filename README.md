[![PyPI version](https://badge.fury.io/py/jupyter_kernel_gateway_bundlers.svg)](https://badge.fury.io/py/jupyter_dashboards) [![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/jupyter)

# Jupyter Kernel Gateway Bundlers

Collection of reference implementation bundlers that convert, package, and deploy notebooks as standalone HTTP microservices behind a kernel gateway.

## What It Gives You

* *File &rarr; Download as &rarr; Microservice Docker bundle (.zip)* menu item to get a zip bundle that you can build into a notebook-as-a-microservice Docker image

## Prerequisites

* Jupyter Notebook 4.0.x running on Python 3.x or Python 2.7.x
* jupyter_cms>=0.3.0
* Edge Chrome, Firefox, or Safari

## Install It

`pip install jupyter_kernel_gateway_bundlers`

Restart your Notebook server if you did not have `jupyter_cms` previously installed.

## Use It

Currently, there is only one download bundler available in this package. To use it:

1. Write a notebook that includes metadata for the [kernel gateway notebook-http mode](https://github.com/jupyter-incubator/kernel_gateway#notebook-http-mode)
2. Click *File &rarr; Download as &rarr; Microservice Docker bundle (.zip)*
3. Follow the README in the downloaded bundle.
