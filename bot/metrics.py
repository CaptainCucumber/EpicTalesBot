import logging
import os
import time
from functools import wraps
from logging.handlers import RotatingFileHandler

from config import Config, config

def get_full_function_name(func):
    if hasattr(func, '__qualname__'):
        return func.__qualname__
    return func.__name__


class MetricsLogger:
    def __init__(self, config: Config):
        metrics_file = config.get_metrics_path() + '/epictales-metrics.log'

        metrics_directory = os.path.dirname(metrics_file)
        if not os.path.exists(metrics_directory):
            os.makedirs(metrics_directory)

        self.logger = logging.getLogger('EpicTalesMetrics')
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Prevent the logger from propagating messages to the root logger

        handler = RotatingFileHandler(metrics_file, maxBytes=10*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    def log_metric(self, metric_name, value, **tags):
        tag_str = ', '.join([f'{key}="{value}"' for key, value in tags.items()])
        self.logger.info(f'{metric_name}={value}, {tag_str}')

    def function_call(self, function_name, success=True):
        status = "success" if success else "failure"
        self.log_metric("function_call", 1, function_name=function_name, status=status)

    def function_timing(self, function_name, duration):
        self.log_metric("function_timing", duration, function_name=function_name)

metrics_logger = MetricsLogger(config)

def track_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            success = False
            raise
        finally:
            duration = int((time.time() - start_time) * 1000)
            metrics_logger.function_call(get_full_function_name(func), success=success)
            metrics_logger.function_timing(get_full_function_name(func), duration)
        return result
    return wrapper
