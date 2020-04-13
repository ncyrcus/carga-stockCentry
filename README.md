## Carga de stock masiva Multi-hilo

Este repo permite la carga de stock a multiples cuentas de centry mediante archivo config

## Requisitos

Para usar este repo mediante el comando ./Run.sh  se debe tener Docker instalado
[DockerHub](https://docs.docker.com/get-docker/)

## Formato Configs.json

```json
[
    {
        "app_id"          : "{{app_id}}",
        "secret_id"       : "{{secret_id}}",
        "redirect_uri"    : "{{redirect_app_uri}}",
        "url_data"        : "{{Decarga de información}}"  // url con json  
    },
]
```

## Formato de inyección de datos

```json
[
    {
        "9003629_900362901_6194":{  // lo que que estime conveniente.
            "id_variante_centry":  "{{id_variante}}",  // id_variante_centry
            "stock":  0 // Stock final
            }
    }

]
```

## Limitaciones

    * única bodega en centry.
