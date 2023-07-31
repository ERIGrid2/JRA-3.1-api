# ERIGrid 2.0 Middleware - Experiment Configuration
# test global config for MVP
- **File format:** YAML

- Global data-exchange config
  - Channel list
  - Routing
  - Directionality
  - Directional Graph

- Definition of participating RIs
  - Endpoints
  - Devices

- Consumers of experiment configuration:
  - Transport operators

## Example

```yaml
nodes:
  rwth:
    description: RWTH Aachen University

    uapi_endpoint: http://uapi.dtu.dk:8080/v2 # Optional

    channels: # This node provides (sources) these channels
    - id: rwth::busbar1:v
      unit: V
      rate: 100.0

    - { id: rwth::ch1.v, unit: V, rate: 100.0 }
    - { id: rwth::ch2.v, unit: V, rate: 100.0 }

    transport:
      type: jander

      # All following attributes are specific to the type of transport
      # and not covered by the global config schema.
      redis:
        host: 10.10.2.1
        port: 123
        username: erigrid
        password: wdsjfsd

  dtu:
    description: Technical University of Denmark

    channels:
    - id: dtu::vsrc.enabled
        type: boolean
        rate: 1.0

  ait:
    transport:
        type: lablink

        # All following attributes are specific to the type of transport
        # and not covered by the global config schema.
        client-type: opal-rt

        mapping:
        - channel: rwth::busbar1:v
        simulink_signal_name:

connections:
- from: rwth::busbar1:v
  to: dtu
- from: rwth::busbar1:v
  to: ait

ri_adapters:
- type: syslab

  nodes:
  - ait

  # All following attributes are specific to the type of adapter
  # and not covered by the global config schema.

  mapping: ...
```
