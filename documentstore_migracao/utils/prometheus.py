""" """
from time import time
from documentstore_migracao import config
from prometheus_client import CollectorRegistry, push_to_gateway, Summary, Histogram

PUSH_GATEWAY = config.get("PROMETHEUS_PUSH_GATEWAY")
REGISTRY = CollectorRegistry()


SUCCESS = Histogram(
    "documentstore_migracao_success_unixtime", 
    "(Document-Store Migração) Last time of success",
    ["func_name"],
)
RUN_TIME = Summary(
    "documentstore_migracao_runtime_seconds", 
    "(Document-Store Migração) time to job run",
    ["func_name"],
)

# You need to register all of the metrics with your registry.  I like doing it
# this way, but you can also pass the registry when you create your metrics.
REGISTRY.register(SUCCESS)
REGISTRY.register(RUN_TIME)

def monitor_time_run(func):
    """
        Monitoramento do tempo e quantidate de requisições
    """
    def wrapper(*args, **kwargs):
        start = time()
        try:
            response = func(*args, **kwargs)
            return response

        finally:
            duration = time() - start
            func_name = func.__name__
            
            RUN_TIME.labels(func_name).observe(duration)
            SUCCESS.labels(func_name).observe(duration)
        
            push_to_gateway(PUSH_GATEWAY, job='documentstore_migracao', registry=REGISTRY)
    return wrapper
