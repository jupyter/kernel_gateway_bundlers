# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from notebook.nbconvert.handlers import respond_zip

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
CMD [ \
    "--KernelGatewayApp.ip=0.0.0.0", \
    "--KernelGatewayApp.seed_uri=/srv/microservice_definition.ipynb" \
    "--KernelGatewayApp.api=notebook-http"
]
'''

README_TMPL = '''

'''

def bundle(handler, abs_nb_path):
    '''
    Creates a zip file containing the original notebook, a Dockerfile, and a 
    README explaining how to build the bundle. Does not automagically determine
    what base image, kernels, or libraries the notebook needs (yet?). Has the 
    handler respond with the zip file.
    '''
    handler.finish('bundle invoked!')
