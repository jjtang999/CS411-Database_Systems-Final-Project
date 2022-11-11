# Installation Guide
1. Do all of the following commands inside this `/server/` directory.
2. Install [Anaconda](https://www.anaconda.com/products/distribution) and create a virtual environment with the `environment.yml` file here as the base.
    ```
    conda env create -f environment.yml
    ```
    This will create an environment called `StoredProcedures`
3. Create a `.env` file in `server/` and populate it with the following line
    ```
    DB_PASSWORD=<database password>
    ```
This will allow flask to securly access the database

4. Run the Flask server. Press Ctrl-C to quit when done testing.
    ```
    conda activate StoredProcedures
    flask run
    ```
