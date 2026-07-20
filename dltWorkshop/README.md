### dlt Workshop

#### 1. For the query "How do I run Ollama locally?", how many spans does a single agent run produce?

- 1

#### 2. How many tables did dlt create in the agent_traces schema?

- 24 (Source file: [count_tables.py](count_tables.py))

#### 3. What is the range of total input token usage for the agent run from Q1?

- 1500-5000
  (under the logfire dashboard : avg(gen_ai.client.token.usage) by gen_ai.token.type
  )
