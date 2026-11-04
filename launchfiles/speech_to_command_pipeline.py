"""only for test and debug, not for running with ADORe"""

import os
from pathlib import Path
import sys

from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    SetEnvironmentVariable,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def find_cuda_library_directories():
    search_paths = [Path(path) for path in sys.path if path]
    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        search_paths.extend(
            Path(virtual_env).glob("lib/python3*/site-packages")
        )

    directories = []
    for library in ("cublas", "cudnn"):
        for search_path in search_paths:
            library_directory = search_path / "nvidia" / library / "lib"
            if library_directory.is_dir():
                directories.append(str(library_directory))
                break

    return directories


def generate_launch_description():
    namespace = LaunchConfiguration("namespace")
    model_name = LaunchConfiguration("model_name")
    ollama_base_url = LaunchConfiguration("ollama_base_url")
    enable_stt_correction = LaunchConfiguration("enable_stt_correction")
    ollama_timeout = LaunchConfiguration("ollama_timeout")
    simulation = LaunchConfiguration("simulation")
    only_simulate = LaunchConfiguration("only_simulate")

    whisper_model_size = LaunchConfiguration("whisper_model_size")
    whisper_device = LaunchConfiguration("whisper_device")
    whisper_compute_type = LaunchConfiguration("whisper_compute_type")
    whisper_language = LaunchConfiguration("whisper_language")
    whisper_hotwords = LaunchConfiguration("whisper_hotwords")
    audio_device = LaunchConfiguration("audio_device")
    audio_channels = LaunchConfiguration("audio_channels")
    audio_channel = LaunchConfiguration("audio_channel")
    audio_sample_rate = LaunchConfiguration("audio_sample_rate")
    end_silence_duration = LaunchConfiguration("end_silence_duration")
    max_audio_backlog_seconds = LaunchConfiguration(
        "max_audio_backlog_seconds"
    )
    audio_chunk_duration = LaunchConfiguration("audio_chunk_duration")
    pre_roll_duration = LaunchConfiguration("pre_roll_duration")
    max_utterance_duration = LaunchConfiguration("max_utterance_duration")
    min_audio_rms = LaunchConfiguration("min_audio_rms")
    max_no_speech_probability = LaunchConfiguration(
        "max_no_speech_probability"
    )
    vad_filter = LaunchConfiguration("vad_filter")

    source_directory = os.environ.get("SOURCE_DIRECTORY")
    if source_directory:
        hf_cache = Path(source_directory) / ".cache" / "huggingface"
    else:
        hf_cache = Path.home() / ".cache" / "huggingface"

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value="ego_vehicle",
            description="Namespace for both nodes.",
        ),
        DeclareLaunchArgument(
            "model_name",
            default_value="qwen3.5:4b",
            description="Ollama model used for command interpretation.",
        ),
        DeclareLaunchArgument(
            "ollama_base_url",
            default_value="http://localhost:11434",
            description="Base URL of the Ollama server.",
        ),
        DeclareLaunchArgument(
            "enable_stt_correction",
            default_value="True",
            description="Correct transcripts in the Ollama request.",
        ),
        DeclareLaunchArgument(
            "ollama_timeout",
            default_value="10.0",
            description="Request timeout for the Ollama server in seconds.",
        ),
        DeclareLaunchArgument(
            "simulation",
            default_value="False",
            description="Classify with local rules instead of Ollama.",
        ),
        DeclareLaunchArgument(
            "whisper_model_size",
            default_value="large-v3-turbo",
        ),
        DeclareLaunchArgument("whisper_device", default_value="cuda"),
        DeclareLaunchArgument(
            "whisper_compute_type",
            default_value="float16",
        ),
        DeclareLaunchArgument("whisper_language", default_value="de"),
        DeclareLaunchArgument(
            "whisper_hotwords",
            default_value=(
                "Haltestelle, anhalten, aussteigen, einsteigen, "
                "weiterfahren, Spurwechsel, Kreisverkehr, Abstand, "
                "wenden, Startpunkt"
            ),
        ),
        # PortAudio input device index, -1 for the default
        DeclareLaunchArgument("audio_device", default_value="-1"),
        # channels opened on that device
        DeclareLaunchArgument("audio_channels", default_value="1"),
        # channel used for recognition
        DeclareLaunchArgument("audio_channel", default_value="0"),
        # input sample rate in Hz
        DeclareLaunchArgument("audio_sample_rate", default_value="48000"),
        # length of one captured audio block
        DeclareLaunchArgument("audio_chunk_duration", default_value="0.1"),
        # audio kept before speech is detected
        DeclareLaunchArgument("pre_roll_duration", default_value="0.3"),
        # hard cut for single utterance
        DeclareLaunchArgument("max_utterance_duration", default_value="8.0"),
        # loudness threshold for speech
        DeclareLaunchArgument("min_audio_rms", default_value="0.005"),
        # no-speech threshold
        DeclareLaunchArgument(
            "max_no_speech_probability",
            default_value="0.6",
        ),
        # remove non-speech parts by Whisper
        DeclareLaunchArgument("vad_filter", default_value="True"),
        # read commands from terminal
        DeclareLaunchArgument("only_simulate", default_value="False"),
        DeclareLaunchArgument(
            "end_silence_duration",
            default_value="1.2",
            description="Silence required before an utterance is complete.",
        ),
        DeclareLaunchArgument(
            "max_audio_backlog_seconds",
            default_value="2.0",
            description="Maximum delay before buffered audio is discarded.",
        ),
        SetEnvironmentVariable("HF_HOME", str(hf_cache)),
        SetEnvironmentVariable("HF_HUB_DISABLE_XET", "1"),
        SetEnvironmentVariable("HF_HUB_DOWNLOAD_TIMEOUT", "120"),
        *[
            AppendEnvironmentVariable(
                "LD_LIBRARY_PATH",
                directory,
                prepend=True,
            )
            for directory in find_cuda_library_directories()
        ],
        Node(
            package="passenger_interface",
            executable="speech_to_text",
            name="speech_to_text",
            namespace=namespace,
            output="screen",
            emulate_tty=True,
            parameters=[{
                "only_simulate": ParameterValue(
                    only_simulate,
                    value_type=bool,
                ),
                "whisper_model_size": whisper_model_size,
                "whisper_device": whisper_device,
                "whisper_compute_type": whisper_compute_type,
                "whisper_language": whisper_language,
                "whisper_hotwords": whisper_hotwords,
                "audio_device": ParameterValue(
                    audio_device,
                    value_type=int,
                ),
                "audio_channels": ParameterValue(
                    audio_channels,
                    value_type=int,
                ),
                "audio_channel": ParameterValue(
                    audio_channel,
                    value_type=int,
                ),
                "audio_sample_rate": ParameterValue(
                    audio_sample_rate,
                    value_type=int,
                ),
                "end_silence_duration": ParameterValue(
                    end_silence_duration,
                    value_type=float,
                ),
                "max_audio_backlog_seconds": ParameterValue(
                    max_audio_backlog_seconds,
                    value_type=float,
                ),
                "audio_chunk_duration": ParameterValue(
                    audio_chunk_duration,
                    value_type=float,
                ),
                "pre_roll_duration": ParameterValue(
                    pre_roll_duration,
                    value_type=float,
                ),
                "max_utterance_duration": ParameterValue(
                    max_utterance_duration,
                    value_type=float,
                ),
                "min_audio_rms": ParameterValue(
                    min_audio_rms,
                    value_type=float,
                ),
                "max_no_speech_probability": ParameterValue(
                    max_no_speech_probability,
                    value_type=float,
                ),
                "vad_filter": ParameterValue(
                    vad_filter,
                    value_type=bool,
                ),
            }],
        ),
        Node(
            package="passenger_interface",
            executable="text_to_command",
            name="text_to_command",
            namespace=namespace,
            output="screen",
            emulate_tty=True,
            parameters=[{
                "simulation": ParameterValue(
                    simulation,
                    value_type=bool,
                ),
                "model_name": model_name,
                "ollama_base_url": ollama_base_url,
                "enable_stt_correction": ParameterValue(
                    enable_stt_correction,
                    value_type=bool,
                ),
                "ollama_timeout": ParameterValue(
                    ollama_timeout,
                    value_type=float,
                ),
            }],
        ),
    ])
