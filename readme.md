# DComEX Framework Prototype

The Prototype integration of the DComEX framework, to be deployed on CSCS' HPC systems.

Directory structure:
* `/korali`: git submodule for the version of korali used in the framework.
* `/msolve`: NuGet configuration
* `/integration`: Python code and configuration data used for integration of Msolve and Korali.
* `/graph.py`: A module to sample Bayesian graphs.
* `/ci`: definition of containerised build, test and deployment pipelines via CI/CD at CSCS.
* `/tests`: unit and integration tests.
* `/docs`: Sphinx documentation

Online documentation is available at [ReadTheDocs](https://dcomex-framework-prototype.readthedocs.io/en/latest/).
