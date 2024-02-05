import logging
import os
import time
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler

import boto3
from config import Config, config
from tracking import get_tracking_context

cloudwatch = boto3.client(
    "cloudwatch",
    region_name=config.get_aws_region(),
    aws_access_key_id=config.get_aws_access_key_id(),
    aws_secret_access_key=config.get_aws_secret_access_key(),
)


def get_full_function_name(func):
    if hasattr(func, "__qualname__"):
        return func.__qualname__
    return func.__name__


class MetricsLogger:
    def __init__(self, config: Config):
        metrics_file = config.get_metrics_path() + "/epictales-metrics.log"

        metrics_directory = os.path.dirname(metrics_file)
        if not os.path.exists(metrics_directory):
            os.makedirs(metrics_directory)

        self.logger = logging.getLogger("EpicTalesMetrics")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = (
            False  # Prevent the logger from propagating messages to the root logger
        )

        handler = RotatingFileHandler(
            metrics_file, maxBytes=30 * 1024 * 1024, backupCount=50
        )
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_metric(self, metric_name, value, **tags):
        tag_str = ", ".join([f'{key}="{value}"' for key, value in tags.items()])
        self.logger.info(f"{metric_name}={value}, {tag_str}")

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


def publish_voice_messages_processed(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "VoiceMessagesProcessed",
                "Dimensions": [
                    {"Name": "Feature", "Value": "VoiceProcessing"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_articles_summarized(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "ArticlesSummarized",
                "Dimensions": [
                    {"Name": "Feature", "Value": "ArticleSummarization"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_videos_watched(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "VideosWatched",
                "Dimensions": [
                    {"Name": "Feature", "Value": "VideoSummarization"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_request_success_rate(count, is_success=True):
    context = get_tracking_context()
    metric_name = "RequestSuccessRate" if is_success else "RequestErrorRate"
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": metric_name,
                "Dimensions": [
                    {"Name": "Feature", "Value": "General"},
                    {"Name": "Type", "Value": "Success" if is_success else "Error"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_voice_message_duration(duration_in_seconds):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "VoiceMessageDuration",
                "Dimensions": [
                    {"Name": "Feature", "Value": "VoiceProcessing"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": duration_in_seconds,
                "Unit": "Seconds",
            },
        ],
    )


def publish_processed_time(time_taken_seconds):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "VoiceMessageProccedTime",
                "Dimensions": [
                    {"Name": "Feature", "Value": "VoiceProcessedTime"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": time_taken_seconds,
                "Unit": "Seconds",
            },
        ],
    )


def publish_start_command_used(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "Start"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_version_command_used(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "version"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_unknown_command_used(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "unknown"},
                    {"Name": "Environment", "Value": config.get_environment()},
                    {"Name": "User", "Value": str(context.user_id)},
                    {"Name": "Chat", "Value": str(context.chat_id)},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_process_start_command_used(count=1):
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "Process",
                "Dimensions": [
                    {"Name": "State", "Value": "Start"},
                    {"Name": "Environment", "Value": config.get_environment()},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_channel_not_supported_message(count=1):
    cloudwatch.put_metric_data(
        Namespace="EpicTalesBot",
        MetricData=[
            {
                "MetricName": "Warning",
                "Dimensions": [
                    {"Name": "ChannelNotSupported", "Value": "SendMessage"},
                    {"Name": "Environment", "Value": config.get_environment()},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )
