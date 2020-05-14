### samsungtv_H
Samsung have used a different (encrypted) type of interface for 2014 (H) model series.
To use custom component [samsungtv_H](https://github.com/Kuzj/Home-AssistantConfig/tree/master/custom_components/samsungtv_H) you must reinstall the encryption-enabled package [samsungctl](https://github.com/Kuzj/samsungctl) and pairing with your TV.
```sh
source /srv/homeassistant/bin/activate
pip uninstall samsungctl
git clone https://github.com/Kuzj/samsungctl.git
cd samsungctl
python setup.py install
samsungctl --pair
```
After pairing add *session_id* and *session_key* to [configuration.yaml](https://github.com/Kuzj/Home-AssistantConfig/blob/master/configuration.yaml)
For reinitialize your TV, remove integration from settings of Home Assistant and reload.