from enum import StrEnum


class StageEnum(StrEnum):
    dev = "dev"
    ci_runtests = "ci.runtests"
    local_runtests = "local.runtests"
    production = "production"
