# oracle_contest
Repository of the Oracle graph analytics contest in collaboration with Politecnico di Milano


## Task 1

This folder contains source code of the checker for the PR values as well as the scripts to download and unzip the datasets and the truth values of PR computed with the NVIDIA nvgraph pragerank implementation (https://docs.nvidia.com/cuda/nvgraph/index.html#nvgraph-pagerank-example) that can be found in the samples code in /usr/local/cuda-9.0/samples/7_CUDALibraries/nvgraph_Pagerank.

Instructions to run the checker are provided in the checker folder.

### Setup your environment to run code on the slurm cluster

1. Connect to the NECSTLab VPN (we will provide a bundle)
2. Login with name.surname to slurm-cuda-entrypoint.local.necst.it
3. edit your .bashrc file to set the CUDA version you are running with
```
export CUDA_9_0_HOME=/usr/local/cuda-9.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${CUDA_9_0_HOME}/lib64
export PATH=${PATH}:${CUDA_9_0_HOME}/bin
```
4. Move to your shared folder (it is located at /home/shared_data/name.surname on all the cluster machines)
5. Download the datasets in the shared folder using the scripts inside the task_2 folder of this repository
6. start running tasks on slurm
7. If you have trouble launching tasks on the cluster (e.g. missing dependencies and libraries, issues with files, etc.), please contact us

### Slurm cluster facilities

The slurm cluster is a small cluster built for the purpose of this contest. After the contest everything will be deleted, so remember to save all your important files somewhere else.

The cluster is composed of 5 nodes:
* **slurm-cuda-entrypoint** this is the machine where you log-in and where you compile code and launch tasks on the cluster. Remember to put the datasets inside your shared folder, otherwise you will not see them when you launch the task on a GPU node. Moreover, this machine has just 50GB of local storage, please do not fill it.
* **slurm-cuda-master** this is the slurm master, it provides 10 cores and 100GB of RAM, so it may be useful if you want to convert the datasets format.
* **dwarf1, dwarf6, dwarf7** these are the GPU nodes, they provide a GTX 960 with 2GB of RAM, an 8 cores Intel core i7 each and 32GB of RAM.

### Output files and competition submission

The submission is your code, so help us run it! :)
We will download the code from your repository in the state it was at the last commit before the deadline.

Try to script the various steps of the computation (a.k.a. graph transformation, compilation and parametric execution). Try also to create code that accepts dataset paths as command line input.

The Pagerank implementation should provide as output two files (provided as input the dataset needed for a single computation of PR):

1. Pagerank Scores, filename `pagerank_gpu`, one vertex per line formatted as `vertex_name PR_score`
2. Execution time, filename `execution_time_gpu`, one line with the execution time

***

## Task 2

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
