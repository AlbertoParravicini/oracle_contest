# oracle_contest
Repository of the Oracle graph analytics contest in collaboration with Politecnico di Milano

## Task 1

This folder contains source code and data for the Vertex Classification task.

The code is defined as a Gradle project:
* `data` contains the compressed data required for the project. You will work with the `ppi` dataset, but you can use `pubmed` for further experiments.   
All the data required for the contest, with format and description, can be found on the [Kaggle](https://www.kaggle.com/c/oracle-polimi-contest/data) page of the contest.
* `docs` contains the papers mentioned in the [Kaggle](https://www.kaggle.com/c/oracle-polimi-contest#Documents) page.
* `src` contains the **Scala** and **Python** code required for the project.  
The Scala code allows you to create vertex embeddings using **DeepWalk** and **Pgx**.  
The Python code creates the graphs from their original format (we did that already, you don't need this code), and defines a couple of example **classifiers** that you can reuse or take inspiration from.

All the data files (graphs and embeddings) should be placed in `task_1/data/pgx-graphs/ppi`.
