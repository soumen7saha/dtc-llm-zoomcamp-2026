import time
from dataclasses import dataclass, field

from rag_helper import RAGBase

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

import sqlite3
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


provider = TracerProvider()
# provider.add_span_processor(
#     SimpleSpanProcessor(ConsoleSpanExporter())
# )

class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self):
        return True        


provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("Hw5")

def calculate_cost(model, usage):
    cost = 0
    if "gpt-5.4-mini" in model:
        cost = (usage.input_tokens * 0.75 + usage.output_tokens * 4.50) / 1_000_000
    return cost

class RAGTraced(RAGBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search") as span:
            start_time = time.time()
            results = self.index.search(query, num_results=num_results)
            search_time = time.time() - start_time
            span.set_attribute("search_time", search_time)
            return results

    def _call_llm(self, prompt):
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]
        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )
        return response
    
    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            start_time = time.time()
            response = self._call_llm(prompt)
            response_time = time.time() - start_time
            self._log_response(prompt, response, response_time, span)
            return response
    
    def _log_response(self, prompt, response, response_time, span):
        usage = response.usage
        cost = calculate_cost(self.model, usage)

        span.set_attribute("model", self.model)
        # span.set_attribute("prompt", prompt)
        span.set_attribute("instruction", self.instructions)
        span.set_attribute("answer", response.output_text)
        span.set_attribute("response_time", response_time)
        span.set_attribute("input_tokens", usage.input_tokens)
        span.set_attribute("output_tokens", usage.output_tokens)
        span.set_attribute("total_tokens", usage.total_tokens)
        span.set_attribute("cost", cost)

    def rag(self, query):
        with tracer.start_as_current_span("rag") as span:
            span.set_attribute("rag_trace_start_time", time.time())
            search_results = self.search(query)
            prompt = self.build_prompt(query, search_results)
            response = self.llm(prompt)
            span.set_attribute("rag_trace_end_time", time.time())
            return response.output_text

