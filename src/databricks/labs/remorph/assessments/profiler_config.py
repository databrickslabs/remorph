from dataclasses import dataclass, field

@dataclass
class PythonConfig:
    requirements: list = field(default_factory=list)
    install_command: str = "pip install"
    env_vars: dict = field(default_factory=dict)

@dataclass
class Step:
    name: str
    type: str | None
    extract_source: str
    mode: str | None
    frequency: str | None
    flag: str | None

    def __post_init__(self):
        if self.frequency is None:
            self.frequency = "once"
        if self.flag is None:
            self.flag = "active"
        if self.mode is None:
            self.mode = "append"


@dataclass
class PipelineConfig:
    name: str
    version: str
    extract_folder: str
    steps: list[Step] = field(default_factory=list)
