#### 1. What's the average number of input tokens across these 3 calls?

- 1353.0 ~ 1400

#### 2. After running text_search for it, what's the filename of the first result?

- 01-agentic-rag/lessons/03-rag.md

#### 3. After running vector_search for the same question, what's the filename of the first result?

- 01-agentic-rag/lessons/01-intro.md

#### 4. Evaluate text_search on the ground truth data. What's the Hit Rate?

- 0.8416666666666667 ~ 0.88

#### 5. Now evaluate vector_search - the part we left for the homework, since the module only evaluated keyword search. What's the MRR?

- 0.5646472663139328 ~ 0.55

#### 6. Evaluate hybrid_search over the full ground truth dataset for k values 1, 50, 100, and 200. Compare the MRR values for these runs. Which k gives the best MRR?

- 1 (mrr=0.648194)
