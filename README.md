# oracle_contest
Repository of the Oracle graph analytics contest in collaboration with Politecnico di Milano

## Task 1

This folder contains source code and data for the Vertex Classification task.

The code is defined as a Gradle project:
* `data` contains the compressed data required for the project. You will work with the `ppi` dataset, but you can use `pubmed` for further experiments.   
All the data required for the contest, with format and description, can be found on the [Kaggle](https://www.kaggle.com/c/oracle-polimi-contest/data) page of the contest. The same data are in the repo, in a compressed format. Only the example embeddings are missing, you can get them on Kaggle.
* `docs` contains the papers mentioned in the [Kaggle](https://www.kaggle.com/c/oracle-polimi-contest#Documents) page.
* `src` contains the **Scala** and **Python** code required for the project.  
The Scala code allows you to create vertex embeddings using **DeepWalk** and **Pgx**.  
The Python code creates the graphs from their original format (we did that already, you don't need this code), and defines a couple of example **classifiers** that you can reuse or take inspiration from.

All the data files (graphs and embeddings) should be placed in `task_1/data/pgx-graphs/ppi`.


***

To run the Python code, a standard Python 3.x installation with Anaconda should be enough. 
Make sure to have `numpy`, `pandas`, `scikit-learn`, and optionally `networkx` and `keras` with a `tensorflow` backend.
It is recommended to run it inside and IDE like **Spyder** or **pyCharm** (you can obtain the full version for free, as a Polimi student).

***

Running the `scala` code is also very simple.
* Go to the `task_1` folder.
* Execute `./gradlew run`: this will download the required dependencies and run `task_1/src/main/scala/Main.scala`.

We tested it with Centos 7, Ubuntu 16.04 and Ubuntu 16.04 inside the Windows 10 Linux Subsystem.
With the Linux Subsystem you might get some `mbind: Function not implemented` messages when loading the graph: don't get scared, it will still work!

***

**Important:** please do not redistribute any of the `jars` in the `libs` folder, they are intender for personal use only!
This also means that they shouldn't be in your repository, if you plan to make it public.
Advice: add `libs/*.jar` to your `.gitignore` file.
