"""Strict configuration; live transport cannot be enabled in this milestone."""
from dataclasses import dataclass, fields
from pathlib import Path
import json

class ConfigurationError(ValueError):
    pass

@dataclass(frozen=True)
class Config:
    schema_version: int = 1
    mode: str = "dry_run"
    transport_enabled: bool = False
    max_dry_run_drafts: int = 3

    def __post_init__(self):
        if type(self.schema_version) is not int or self.schema_version != 1:
            raise ConfigurationError("unsupported schema version")
        if self.mode != "dry_run" or self.transport_enabled is not False:
            raise ConfigurationError("live transport is disabled")
        if type(self.max_dry_run_drafts) is not int or not 1 <= self.max_dry_run_drafts <= 3:
            raise ConfigurationError("dry-run limit must be 1 to 3")

    @classmethod
    def from_file(cls, path):
        try:
            data = json.loads(Path(path).read_text(encoding="utf8"))
        except (OSError, ValueError) as exc:
            raise ConfigurationError(f"invalid config: {exc}") from exc
        if not isinstance(data, dict) or set(data) - {f.name for f in fields(cls)}:
            raise ConfigurationError("unknown fields or non-object config")
        try:
            return cls(**data)
        except TypeError as exc:
            raise ConfigurationError(str(exc)) from exc
