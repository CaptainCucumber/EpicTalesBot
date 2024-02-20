from datetime import datetime

import boto3
from config import config
from tracking import get_tracking_context

cloudwatch = boto3.client(
    "cloudwatch",
    region_name=config.aws_region,
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
)

CLOUDWATCH_NAMESPACE = "EpicTalesBot-1.5.1"


def publish_articles_summarized(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "ArticlesSummarized",
                "Dimensions": [
                    {"Name": "Environment", "Value": config.environment},
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
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "VideosWatched",
                "Dimensions": [
                    {"Name": "Environment", "Value": config.environment},
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
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": metric_name,
                "Dimensions": [
                    {"Name": "Type", "Value": "Success" if is_success else "Error"},
                    {"Name": "Environment", "Value": config.environment},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_voice_message_processed(type, duration, processed_time, compute_time):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "VoiceMessageDuration",
                "Dimensions": [
                    {"Name": "Type", "Value": type},
                    {"Name": "Environment", "Value": config.environment},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": duration,
                "Unit": "Seconds",
            },
            {
                "MetricName": "VoiceMessageProccedTime",
                "Dimensions": [
                    {"Name": "Type", "Value": type},
                    {"Name": "Environment", "Value": config.environment},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": processed_time,
                "Unit": "Seconds",
            },
            {
                "MetricName": "VoiceMessageComputeTime",
                "Dimensions": [
                    {"Name": "Type", "Value": type},
                    {"Name": "Environment", "Value": config.environment},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": compute_time,
                "Unit": "Seconds",
            },
        ],
    )


def publish_start_command_used(count=1):
    context = get_tracking_context()
    cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "start"},
                    {"Name": "Environment", "Value": config.environment},
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
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "version"},
                    {"Name": "Environment", "Value": config.environment},
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
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "Command",
                "Dimensions": [
                    {"Name": "CommandName", "Value": "unknown"},
                    {"Name": "Environment", "Value": config.environment},
                    {"Name": "ChatType", "Value": context.chat_type},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_channel_not_supported_message(count=1):
    cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "Warning",
                "Dimensions": [
                    {"Name": "ChannelNotSupported", "Value": "SendMessage"},
                    {"Name": "Environment", "Value": config.environment},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )


def publish_process_started(count=1):
    cloudwatch.put_metric_data(
        Namespace=CLOUDWATCH_NAMESPACE,
        MetricData=[
            {
                "MetricName": "ProcessStarted",
                "Dimensions": [
                    {"Name": "Environment", "Value": config.environment},
                ],
                "Timestamp": datetime.utcnow(),
                "Value": count,
                "Unit": "Count",
            },
        ],
    )
