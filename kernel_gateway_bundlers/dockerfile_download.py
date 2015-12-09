# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import io
import zipfile
from ipython_genutils.py3compat import cast_bytes

# Starting simply, keep all assets here in Python
DOCKERFILE_TMPL = '''
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM jupyter/minimal-notebook:latest

USER jovyan

# TODO: add additional kernels and libraries needed here manually for now

# Install Kernel Gateway
RUN pip install jupyter_kernel_gateway
# Add notebook file
COPY {notebook_filename} /srv/microservice_definition.ipynb

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]
CMD [ \\
    "--KernelGatewayApp.ip=0.0.0.0", \\
    "--KernelGatewayApp.seed_uri=/srv/microservice_definition.ipynb" \\
    "--KernelGatewayApp.api=notebook-http" \\
]
'''

MAKEFILE_TMPL = '''
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: help build dev

REPO:={notebook_name}

help:

build:
\tdocker build -t $(REPO) .

dev:
\tdocker run -it --rm -p 8888:8888 $(REPO)
'''

README_TMPL = '''
This bundle includes foundation needed to get the included notebook running
as a Jupyter kernel microservice within a Docker container. To use it:

1. Modify the Dockerfile to install any kernels or kernel libraries your 
notebook needs. The current base image ships with a Python 3 kernel only.
2. Run `make build` to build an image named after the notebook.
3. Run `make dev` to try it locally.

A few caveats:

* The Dockerfile pulls from the kernel gateway master branch for the moment.
The microservice functionality is not yet released.
* It would be nice, of course, if the Dockerfile automatically captured the
Jupyter Notebook server environment (libraries, data, kernels, ...) but this
still remains a "hard problem" outside walled-garden hosted solutions.
'''

def bundle(handler, abs_nb_path):
    '''
    Creates a zip file containing the original notebook, a Dockerfile, and a 
    README explaining how to build the bundle. Does not automagically determine
    what base image, kernels, or libraries the notebook needs (yet?). Has the 
    handler respond with the zip file.
    '''
    # Notebook basename with and without the extension
    notebook_filename = os.path.basename(abs_nb_path)
    notebook_name = os.path.splitext(notebook_filename)[0] 

    # Headers
    zip_filename = os.path.splitext(notebook_name)[0] + '.zip'
    handler.set_header('Content-Disposition',
                       'attachment; filename="%s"' % zip_filename)
    handler.set_header('Content-Type', 'application/zip')

    # Prepare the zip file
    zip_buffer = io.BytesIO()
    zipf = zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED)
    zipf.write(abs_nb_path, notebook_filename)
    zipf.writestr('Dockerfile', DOCKERFILE_TMPL.format(**locals()))
    zipf.writestr('Makefile', MAKEFILE_TMPL.format(**locals()))
    zipf.writestr('README.md', README_TMPL.format(**locals()))
    zipf.close()

    # Return the buffer value as the response
    handler.finish(zip_buffer.getvalue())