[![CI](https://github.com/infrasonar/ipflownetwork-probe/workflows/CI/badge.svg)](https://github.com/infrasonar/ipflownetwork-probe/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/ipflownetwork-probe)](https://github.com/infrasonar/ipflownetwork-probe/releases)

# InfraSonar Netflow/IPFIX Probe

Documentation: https://docs.infrasonar.com/collectors/probes/ipflownetwork/

## Environment variable

Variable            | Default                        | Description
------------------- | ------------------------------ | ------------
`AGENTCORE_HOST`    | `127.0.0.1`                    | Hostname or Ip address of the AgentCore.
`AGENTCORE_PORT`    | `8750`                         | AgentCore port to connect to.
`INFRASONAR_CONF`   | `/data/config/infrasonar.yaml` | File with probe and asset configuration like credentials.
`MAX_PACKAGE_SIZE`  | `500`                          | Maximum package size in kilobytes _(1..2000)_.
`MAX_CHECK_TIMEOUT` | `300`                          | Check time-out is 80% of the interval time with `MAX_CHECK_TIMEOUT` in seconds as absolute maximum.
`DRY_RUN`           | _none_                         | Do not run demonized, just return checks and assets specified in the given yaml _(see the [Dry run section](#dry-run) below)_.
`LOG_LEVEL`         | `warning`                      | Log level (`debug`, `info`, `warning`, `error` or `critical`).
`LOG_COLORIZED`     | `0`                            | Log using colors (`0`=disabled, `1`=enabled).
`LOG_FMT`           | `%y%m%d %H:%M:%S`              | Log format prefix.
`LISTEN_PORT`       | `2055`                         | Port to listen to for flow packets
`FORWARD_HOST`      | `127.0.0.1`                    | Forward UDP traffic to this host (only applicable if FORWARD_PORTS is set).
`FORWARD_PORTS`     | _none_                         | Forward UDP traffic to these local ports for other listeners (comma separate for multiple ports).

## Docker build

```
docker build -t ipflownetwork-probe . --no-cache
```

## Dry run

Available checks:
- `network`

Create a yaml file, for example _(test.yaml)_:

```yaml
asset:
  name: "foo.local"
  check: "network"
  config:
    network:
      - "192.168.1.0/24"
```

Run the probe with the `DRY_RUN` environment variable set the the yaml file above.

```
DRY_RUN=test.yaml python main.py
```
