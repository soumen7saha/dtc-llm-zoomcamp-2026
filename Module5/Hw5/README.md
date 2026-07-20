Source file: [Hw5.ipynb](Hw5.ipynb)

#### 1. The console exporter prints every finished span as a dictionary. Count the spans in the console output - each one is a separate ReadableSpan entry. How many spans does the trace produce?

- 3

#### 2. Now re-run the query. How many input tokens do we see?

- 7000

#### 3. For a typical query, roughly how long does the LLM call take?

- Over 2000ms

#### 4. Re-run the query from Q1. Which span names appear in the spans table?

- rag, search, and llm

#### 5. Using SQL (or pandas), compute the total duration for each span name excluding rag. Which span type takes the most total time?

- llm

#### 6. How much do the input tokens vary across these 4 runs?

- They're identical
