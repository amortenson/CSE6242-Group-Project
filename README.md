# CSE6242-Group-Project

This repository contains ETL code and experiments performed on 2022 Single Family Census Tract data from Freddie Mac

Documentation for the source data can be found [here](https://www.fhfa.gov/DataTools/Downloads/Documents/Enterprise-PUDB/Single-Family_Census_Tract_File_/2022_Single_Family_Census_Tract_File.pdf). Source data and more can be found [here](https://www.fhfa.gov/DataTools/Downloads/Pages/Public-Use-Databases.aspx).
An interactive visualization of the data based on our analysis can be found [here](https://observablehq.com/@cse6242-demo/bivariate-choropleth)

All code and notebooks should be run using python 3.9. Libraries used include numpy, pandas, matplotlib, seaborn, scikit-learn and shap.

The source code is split up into two parts: a notebook, `housingDataExperimentsFull.ipynb`, to perform exploratory data analysis, cleaning, and experiments; and a python file, `calculate_county_averages.py`, to generate the data used for our visualization. Each of these files contains code to pull and clean the data, and can be run independently.

## Running the Code

### housingDataExperimentsFull.ipynb

This notebook contains code to pull, clean, and analyze Freddie Mac single family home loan data from 2022. It is tested using python version 3.9.

If you are not able to run a jupyter notebook using python version 3.9, you can use the insructions [here](https://poloclub.github.io/cse6242-2024spring-online/hw3/Docker_setup_guide.pdf) to set up a docker conainer and run the notebook in a contained environment locally.

The notebook uses several python libraries. These should be installed automatically when you run the first cell of the notebook. If you do not want to install libraries this way, you can install them manually by running the following command: `pip install pandas matplotlib seaborn scikit-learn shap`. If you do not have pip installed, documentation can be found [here](https://pip.pypa.io/en/stable/installation/). The notebook was tested with the most recent version of these libraries as of March 27, 2024.

### calculate_county_averages.py

This python file contains code to pull, clean, and aggragate Freddie Mac and Fannie Mae single family home loan data from 2018-2022 into county-level averages. It is tested using python version 3.9.

It has the same library dependencies as `housingDataExperimentsFull.ipynb`. You can install these libraries manually by running the following command: `pip install pandas matplotlib seaborn scikit-learn shap`. If you do not have pip installed, documentation can be found [here](https://pip.pypa.io/en/stable/installation/). Alternatively, if you are able to run the notebook above, you can copy the first cell of that notebook into a new notebook, and copy the entire contents of theis file into a new cell in that notebook. This way, you will be able to automatically install dependencies and run the code from a jupyter notebook.

The code has been tested on data from 2018-2022. The federal housing data we use changes over time, so we do not guarantee that this code will work as expected if you simply replace the year `2018` in the code with some earlier year. However, with modifications, you could likely use this code to pull data from earlier years as well.

### Visualization

`calculate_county_averages.py` should generate a file called `county_averages_by_year.csv`. This is used to generate our visualization at [Observable](https://observablehq.com/@cse6242-demo/bivariate-choropleth). This visualization is generated using d3.js, but the observable platform allows us to cut out many of the steps necessary to locally host a d3.js visualization and remove some boilerplate html. 

To create your own visualization or make changes, simply create an [observable account](https://observablehq.com/@observablehq/signing-up-for-an-observable-account), return to our visualization, and locate the "fork this project" button near the upper right hand corner of your window (next to "share"). This will allow you to host your own idential version of our notebook and make changes. To upload your own data, locate the "files" section (a paperclip icon on the right hand side of the window), and click on the "+" icon. To make changes to any of the visualization code, click the "+" icon to the left of any element of the visualization and change the code as desired.



