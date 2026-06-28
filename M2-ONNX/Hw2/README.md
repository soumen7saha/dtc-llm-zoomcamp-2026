#### Q1 
Embed the following query:

How does approximate nearest neighbor search work?
The embedder returns a vector of 384 numbers. What's the first value (v[0])?

- -0.02

#### Q2
The embedder returns normalized vectors, so the dot product between two of them is their cosine similarity.

Take the page 02-vector-search/lessons/07-sqlitesearch-vector.md, embed its content, and compute the cosine similarity with the query vector from Q1.

What do you get?

- 0.37

#### Q3
Which file does the highest-scoring chunk belong to (its filename)?

- 02-vector-search/lessons/07-sqlitesearch-vector.md

#### Q4
We've done vector search by hand, which is good for learning, but it's not what we do in practice. In practice we use libraries.

Let's use VectorSearch from minsearch and run a search for the following query:

    What metric do we use to evaluate a search engine?

Which file is the filename of the first result?

- 04-evaluation/lessons/05-search-metrics.md

#### Q5
Vector search matches by meaning, keyword search by exact words.

Let's compare them. Index the same chunks with Index from minsearch. Use content as a text field.

Run both searches for this query:

    How do I store vectors in PostgreSQL?

Take the top 5 results from each method. Which file shows up in the vector results but not in the text results?

- 02-vector-search/lessons/08-pgvector.md

#### Q6
Which file is ranked first after RRF?

- 01-agentic-rag/lessons/13-function-calling.md
