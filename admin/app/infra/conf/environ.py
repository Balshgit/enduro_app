import environ

env = environ.Env(
    DEBUG=(bool, False),
)

env_path = "infra/.envs/.env"

if env("STAGE", str, "dev") in ("runtests", "ci_runtests"):
    env_path = "infra/.envs/.env.local.runtests" if env("LOCALTEST", int, 0) else "infra/.envs/.env.ci.runtests"

environ.Env.read_env(env_path)
