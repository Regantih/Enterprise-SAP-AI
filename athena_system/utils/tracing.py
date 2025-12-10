import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name="athena-system"):
    """
    Configures OpenTelemetry tracing.
    Exports to Console for now (can be switched to OTLP).
    """
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    
    # Use Console Exporter for immediate visibility in CLI
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)

def get_tracer(name):
    return trace.get_tracer(name)
