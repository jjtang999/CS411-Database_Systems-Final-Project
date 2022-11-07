# Installation Guide
1. Do all of the following commands inside this `/server/` directory.
1. Install [Anaconda](https://www.anaconda.com/products/distribution) and create a virtual environment with the `environment.yml` file here as the base.
    ```
    conda env create -f enviornment.yml
    ```
    This will create an environment called `StoredProcedures`
1. Modify `app.py` to set the database password on line 8 ***(DO NOT COMMIT THIS)***
1. Run the Flask server. Press Ctrl-C to quit when done testing.
    ```
    conda activate StoredProcedures
    flask run
    ```
