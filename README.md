# Kernel Gateway Bundlers

Collection of reference implementation bundlers that convert, package, and deploy notebooks as standalone HTTP microservices beyond a kernel gateway.

## What It Gives You

* *File &rarr; Download as &rarr; Microservice Docker bundle (.zip)* menu item to get a zip bundle that you can build into a notebook-as-a-microservice Docker image

## Prerequisites

* Jupyter Notebook 4.0.x running on Python 3.x or Python 2.7.x
* jupyter_cms>=0.3.0
* Edge Chrome, Firefox, or Safari

## Install It

`pip install jupyter_kernel_gateeway_bundlers`

Restart your Notebook server if you did not have `jupyter_cms` previously installed.

## Use It

Currently, there is only one download bundler available in this package. To use it:

1. Write a notebook that includes microservice metadata (TODO: need link to format in kernel_gateway repo)
2. Click *File &rarr; Download as &rarr; Microservice Docker bundle (.zip)*
3. Follow the README in the downloaded bundle.
