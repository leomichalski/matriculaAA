matriculaAA
===========

A Helm chart to deploy the matriculaAA project on Kubernetes.


## Configuration

The following table lists the configurable parameters of the matriculaAA chart and their default values.

| Parameter                | Description             | Default        |
| ------------------------ | ----------------------- | -------------- |
| `debug` | Useful to speed up local debugging. | `false` |
| `kafkaTopicName` |  | `"vaga_disponivel"` |
| `endpoint` | Required. The DNS or IP that should host the admin panel. | `` |
| `externalAccess.enabled` |  | `true` |
| `externalAccess.issuer.enabled` |  | `true` |
| `externalAccess.issuer.name` |  | `"letsencrypt-prod"` |
| `externalAccess.issuer.email` | Required. | `` |
| `externalAccess.issuer.server` |  | `"https://acme-v02.api.letsencrypt.org/directory"` |
| `externalAccess.issuer.secretName` |  | `"letsencrypt-secret-prod"` |
| `externalAccess.ingress.enabled` |  | `true` |
| `django.enabled` | Enable the Django admin panel. | `true` |
| `django.container.imagePullPolicy` |  | `"Always"` |
| `django.container.image` |  | `"api_production_django"` |
| `django.container.tag` |  | `"latest"` |
| `django.container.requests.cpu` |  | `"100m"` |
| `django.container.requests.memory` |  | `"60Mi"` |
| `django.container.limits.cpu` |  | `"500m"` |
| `django.container.limits.memory` |  | `"500Mi"` |
| `django.container.port` |  | `5000` |
| `django.service.port` |  | `80` |
| `django.replicas` |  | `3` |
| `django.rollingUpdate.maxSurge` |  | `1` |
| `django.rollingUpdate.maxUnavailable` |  | `0` |
| `django.secretKey` | Required. | `` |
| `django.superuser.password` | Required. | `` |
| `django.superuser.email` | Required. | `` |
| `strimzi.clusterName` |  | `"kafka-cluster"` |
| `strimzi.enabled` | Enables standalone strimzi-kafka-operator install. | `"false"` |
| `strimzi.kafka.version` |  | `"3.6.0"` |
| `strimzi.kafka.replicas` |  | `1` |
| `strimzi.kafka.listener.name` |  | `"plain"` |
| `strimzi.kafka.listener.port` |  | `9092` |
| `strimzi.kafka.listener.type` |  | `"internal"` |
| `strimzi.kafka.listener.tls` |  | `false` |
| `strimzi.kafka.config.offsetsTopicReplicationFactor` |  | `1` |
| `strimzi.kafka.config.transactionStateLogReplicationFactor` |  | `1` |
| `strimzi.kafka.config.transactionStateLogMinIsr` |  | `1` |
| `strimzi.kafka.config.defaultReplicationFactor` |  | `1` |
| `strimzi.kafka.config.minInsyncReplicas` |  | `1` |
| `strimzi.kafka.config.interBrokerProtocolVersion` |  | `"3.6"` |
| `strimzi.zookeeper.replicas` |  | `1` |
| `detectorDeVagas.enabled` |  | `true` |
| `detectorDeVagas.replicas` |  | `1` |
| `detectorDeVagas.rollingUpdate.maxSurge` |  | `1` |
| `detectorDeVagas.rollingUpdate.maxUnavailable` |  | `0` |
| `detectorDeVagas.container.imagePullPolicy` |  | `"Always"` |
| `detectorDeVagas.container.image` |  | `"matriculaaa-detector-de-vagas"` |
| `detectorDeVagas.container.tag` |  | `"latest"` |
| `detectorDeVagas.container.requests.cpu` |  | `"1000m"` |
| `detectorDeVagas.container.requests.memory` |  | `"600Mi"` |
| `detectorDeVagas.container.limits.cpu` |  | `"1000m"` |
| `detectorDeVagas.container.limits.memory` |  | `"600Mi"` |
| `realizadorDeMatriculas.enabled` |  | `true` |
| `realizadorDeMatriculas.replicas` |  | `1` |
| `realizadorDeMatriculas.rollingUpdate.maxSurge` |  | `1` |
| `realizadorDeMatriculas.rollingUpdate.maxUnavailable` |  | `0` |
| `realizadorDeMatriculas.container.imagePullPolicy` |  | `"Always"` |
| `realizadorDeMatriculas.container.image` |  | `"matriculaaa-realizador-de-matriculas"` |
| `realizadorDeMatriculas.container.tag` |  | `"latest"` |
| `realizadorDeMatriculas.container.requests.cpu` |  | `"1000m"` |
| `realizadorDeMatriculas.container.requests.memory` |  | `"600Mi"` |
| `realizadorDeMatriculas.container.limits.cpu` |  | `"1000m"` |
| `realizadorDeMatriculas.container.limits.memory` |  | `"600Mi"` |
| `postgres.db` | Required. This chart doesn't include a PostgreSQL server. | `` |
| `postgres.host` | Required. This chart doesn't include a PostgreSQL server. | `` |
| `postgres.password` | Required. This chart doesn't include a PostgreSQL server. | `` |
| `postgres.port` | Required. This chart doesn't include a PostgreSQL server. | `` |
| `postgres.user` | Required. This chart doesn't include a PostgreSQL server. | `` |

---
_Documentation generated by [Frigate](https://frigate.readthedocs.io)._
