import oracle.pgx.api.{Pgx, PgxGraph, PgxSession}
import oracle.pgx.api.beta.mllib.DeepWalkModel

object Main {

  def main(args: Array[String]): Unit = {

    val graphName = "pubmed"

    val graphPath = s"data/pgx-graphs/$graphName/${graphName}_no_prop.json"

    // Load the graph. The graph must be undirected to compute the embeddings;
    val session: PgxSession = Pgx.createSession("session_1")
    val graph: PgxGraph = session.readGraphWithProperties(graphPath).undirect()
    println(graph)

    // Create an analyst to create the embeddings;
    val analyst = session.createAnalyst

    // Create a DeepWalk model.
    // Parameters might depend on the graph, and are chosen according to these papers:
    //   https://cs.stanford.edu/~jure/pubs/node2vec-kdd16.pdf
    //   https://arxiv.org/pdf/1403.6652.pdf
    val model: DeepWalkModel = analyst.deepWalkModelBuilder()
      .setMinWordFrequency(1)
      .setBatchSize(512)
      .setNumEpochs(1)
      .setLayerSize(128)
      .setLearningRate(0.05)
      .setMinLearningRate(0.0001)
      .setWindowSize(10)
      .setWalksPerVertex(10)
      .setWalkLength(8)
      .setSampleRate(0.00001)
      .setNegativeSample(5)
      .setValidationFraction(0.01)
      .build

    println("Started embeddings generation...")
    model.fit(graph)
    println("Embeddings generation completed!")
    println(s"\tLoss: ${model.getLoss}")

    // Store the embeddings in a csv;
    val vertexVectors = model.getTrainedVertexVectors.flattenAll
    vertexVectors.write.overwrite(true).csv.separator(',').store(s"data/pgx-graphs/$graphName/embeddings.csv")
    println(f"Embeddings stored in data/pgx-graphs/$graphName/embeddings.csv")
  }
}