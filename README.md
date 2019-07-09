# panda-dataset
### Pakistani News Dataset

### Notes
- Clone repo
- BeautifulSoup? Required?
$ pip install beautifulsoup4
- Yaml
$ pip install pyyaml


### How to generate Dataset
Change the paths in the **create-articles.yaml** file in **configurations** folder

$> cd [repo]

$> cd scripts/create-articles/

$> python3 create-articles.py ../../configurations/create-articles.yaml > log.txt

For windows run the following command
~~~
python [path to create-articles.yaml file] > [log filename.txt]
~~~


This will generate a log.txt file in scripts/create-articles folder

This will generate dataset.yaml in artifacts/articles folder


## Data Exploration (Python Dataframe)
This section provides details on how to consume the articles data and explore it for analysis. Following are the are ways to do it.
1. Make sure that you have the articles folder made after running the above steps. it should be the `outputFolderPath`.
2. Find the folder `artifacts/articles/`. where you will find the articles data files in `{files}.yaml` format.
3. Open the `Yaml-to-Dataframe.ipynb` notebook and give the path to the folder mentioned in Step-2. Follow rest of the instructions within the notebook, and you will have a `pandas` dataframe for exploration.

### Quick Way: (Incase you dont want to run the parser to get the latest data)
1. Download the data file from the [LINK](https://drive.google.com/file/d/1BEqCRIxm1lb2BZGv_qHRSYq8-eUZKwHx/view?usp=sharing) - This data has articles uptill `31-12-2017`
2. Extract the compressed file using 7zip.
3. Paste the data file in the working directory.
4. Open the `Yaml-to-Dataframe.ipynb` notebook, Scroll down to the `Quick Way : Load data file`
5. Execute the cell and you will have the dataframe to explore.

