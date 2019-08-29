# Architecture du programme

## Base de données

| Table | Contenu | 
| ---- | ----- |
| Chaudiere | 1 entrée à chaque appel du script sensor/create_data.py (toutes les 3 à 5 secondes)|
|ChaudiereMinute|1 entrée par minute (moyenne des données de la table Chaudiere)|

Pour simplifier le code, les deux tables ont la même structure et les mêmes champs. Le champ `phase` n’est pas utilisé dans la table `Chaudiere`.

## Principes de base
### create_data.py
Le script `sensor/create_data.py` tourne en tâche de fond géré par `supervisor`. Il récupère les données des capteur (températures et moteurs) et les enregistre dans la table `Chaudiere` toutes les 3 à 5 secondes environ.

### archive_minute.py
Le script `flask_app/script/archive_minute.py` est appelé toutes les deux minutes (`cron`).

Si de nouvelles données sont présentent dans la table `Chaudiere`, alors il crée une/plusieurs entrées dans la table `ChaudiereMinute` (une entrée pour chaque minute).

La valeur température est la moyenne des températures (sur une minute) de la table `Chaudiere`.

La valeur des moteur est un booléen qui vaut true si au moins une entrée (sur une minute) est vraie.

En mode production, deux minutes sont traitées à chaque appel

### process_phase.py
Le script `flask_app/script/process_phase.py` est appelé toutes les deux minutes (cron). Si de nouvelles entrées sont à traiter dans la table `ChaudiereMinute` alors il exécute un algorithme pour déterminer la phase de fonctionnement de la chaudière au cours de chaque minute qu’il traite.

En mode production, deux minutes sont traitées à chaque appel

Si la température de l’eau de la chaudiere (temp0) passe sous la consigne, alors une alerte mail/sms est générée. Aucun mail/sms n’est envoyé si une alerte à déja été générée dans les 10 minutes précédentes.

## Supervisor


<div class="mermaid">
graph LR
    A[supervisor] --> B(create_data.py)
    A[supervisor] --> E(wsgi_gunicorn.py)
    subgraph sensor
        B --> C[get_watt.py]
        B --> G[get_temp.py]
    end
    subgraph gunicorn
        E
    end
</div>

## Cron
To configure, copy file `config/prod/chaudiere_cron_prod` in directory `/etc/cron.d/`  
This file must be owned by root (`sudo chown root /etc/cron.d/chaudiere_cron_prod`)

`sudo service cron status` - Check if cron is running

```mermaid
graph LR
    A[chaudiere_cron_prod] --> B(archive_minute.py)
    A[chaudiere_cron_prod] --> C(process_phase.py)
    A[chaudiere_cron_prod] --> D(manager.py database rotate Chaudiere)
    A[chaudiere_cron_prod] --> E(manager.py database rotate ChaudiereMinute)
    A[chaudiere_cron_prod] --> F(local_gui.sh)
    subgraph when reboot
        F
    end
    subgraph every day
        D
        E
    end
    subgraph every minute
        B
        C 

    end
```

## Alerts

```mermaid
    graph LR
        A[process_phase.py] --> B(send_email_sms.py)
```

``` Python
    sms_gateway = nexmo.Client(key=app.config['NEXMO_API_KEY'], 
                               secret=app.config['NEXMO_API_SECRET'])

    def send_async_sms(app, sender, recipient, body):
        """ Call nexmo library to send sms """
        with app.app_context():
            sms = {
                'from': sender,
                'to': recipient,
                'text': body
            }
            sms_gateway.send_message(sms)
```

## Retrieve sensor data
```mermaid
graph TD
    A[supervisor] -->|every second| B(create_data.py)
    B --> C[get_watt.py]
    C --> |i2C| E[ADS1115]
    E --> |audio jack| F[Current sensor <br>SCT-013-030 30A-1V]
    B --> G[get_temp.py]
    G --> |1 wire| H[Temperature sensor <br>DS18B20]
```
