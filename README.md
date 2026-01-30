# Introduction
This custom integration allows Home Assistant to communicate with **Inim Prime alarm panels** via the PrimeLAN network interface.   
It provides monitoring and limited control of panels, partitions, zones, diagnostics, and event logs by using the official Inim Web API.   
This project is **community-developed**, **not affiliated with INIM Electronics**, and is intended to complement — not replace — the official Inim software.   

# Disclaimer   
This integration is provided **as-is** and is currently under active development.   
It should be considered **experimental**.   
Not all Inim Prime panel features are supported, some behaviors may be incomplete or incorrect, and **breaking changes may occur at any time** without notice.   
This integration interacts with a **security/alarm system**.   
Use it **at your own risk** and **do not rely on it as the sole control or monitoring system** for your alarm panel.   
The author takes **no responsibility** for:   
- Malfunctions or unexpected behavior   
- Missed or delayed events   
- Incorrect panel states   
- Any damage, loss, or security issues resulting from the use of this integration   
   
Always verify critical operations directly on the Inim Prime panel or through official Inim software.   
# Security notes   
- The PrimeLAN HTTPS implementation uses outdated TLS   
- It is strongly recommended to use this integration **only on a trusted LAN**   
- Never expose the panel directly to the internet   
   
# Configure the Inim Prime Panel   
## Requirements   
In order to use this integration you need an Inim Prime panel with the PrimeLAN network card. If you have an Inim Prime panel, but you do not have the PrimeLAN card you CANNOT use this integration. Anyway, you can buy it and try to install it on your own or by contacting an installer.   
The manual for the setup of the Inim PrimeLAN card can be found there: [Inim PrimeLAN manual](https://www.manualslib.com/manual/3494645/Inim-Primelan.html?page=4#manual).   
## Prepare the Inim Prime panel   
In order to use this integration, you need to edit you panel configuration. You can do so by installing the Prime/STUDIO software on Windows.   
You can download the latest version of the software there: [Inim Prime/STUDIO](https://download.sicurit.cz/EZS/INIM/_Prime/Prime%20Studio/).   
### Connect to the panel   
Once you have installed the software, open it, and you should have this view:   
!  
Click on `Open panel connected`, and then select `Prime LAN`:   
!   
Type the panel IP and password and click on `Next`.   
Once the communication channel has been checked, you should be able to see that a panel as been detected, the firmware version and the serial number.   
It is **FUNDAMENTAL** to copy the serial number correctly from that view and store it, since it will be needed later on during the configuration in Home Assistant.   
Once you have copied the serial number, you can click on `Open the panel`.   
### Make a backup of the configuration   
The first thing I strongly advise you to do, if you haven't already is making a copy of your panel configuration.   
To do so, first download the current configuration by clicking on the `Download` icon in the upper left corner.   
!  
It will take a while, but once it has finished you can click on `Save`, choose a name and click `OK`.   
Now you have saved your config, and in case you mess up with something, you can just click on `Open`, choose the saved configuration, open it and then press on the `Upload` icon in order to restore the old setup.   
Before doing any operation, I suggest to read the current config.   
### Check network settings   
Once you have backed up the panel, click on `Control panel parameters` on the left panel:   
!
Then click on IP connection parameters:   
!   
There you should check if your panel has `Obtain an IP address automatically` enabled.   
In case it is enabled, your panel will be using connection parameters obtained from the DHCP.    
That could cause problems later, since in Home Assistant we need a static IP or at least a hostname.   
If you want to keep DHCP enabled, you should reserve a static IP address for your Inim Prime panel in your DHCP server. Bear in mind, if you are not very familiar with networking, that usually is your router that act also as a DHCP server and that if you change options there, you should be changing them in case you replace it.   
If you prefer to disable DHCP or you already have it disabled, you can just set your preferred parameters and take note of the IP address in order to use it later in the integration configuration.   
Once you have made the changes, be sure to upload the updated configuration by clicking on `Upload` in the upper bar:   
!
### Upgrade the firmware   
Once you have checked you connection parameters, I suggest to update the firmware of the Inim Prime panel, by clicking on:   
!  
which is placed in the upper right corner. The update procedure is simple.   
### Configure PrimeLAN settings   
Once the panel is updated click on `PrimeLAN settings` on the left panel:   
!  
Before performing any operations, load the current configuration, by clicking on the download icon in the upper left corner (it might take a while):   
!
Once the configuration has been loaded click on `Web API` in the upper right corner:   
!    
There you should firstly enable the `API HTTP/HTTPS enable` toggle, then click on `Generates` to create a new API Key.   
You will need the API Key later for the Home Assistant configuration. Bear in mind that the API Key gives access to most of the panel's features, so if you believe it might have been compromised, you can go back there and generate a new one (remember that you will also need to upload the new configuration after!).   
Once you have generated the key, you should select which `Code` the Web API will use in order to perform the operations. My suggestion is to create a Web API code that will be used only for that scope. The creation of a new code will not be covered here, but it's pretty simple, just remember to load the current configuration before making changes and to upload the new one once you have finished.   
I suggest to enable `Only Allow connections via HTTPS`, that way the communications with the panel will be encrypted. Honestly the encryption uses an old protocol that is not really considered secure anymore, but since you will probably perform the operations on your LAN, you should be ok.   
The option `Not allow disalarm` is up to you. If you enable it, some of the operations will fail, and the Home Assistant integration does not really support having this option disabled at the moment.   
Once you have completed the configuration click on the `Upload` icon to update the new configuration.   
# Install the integration in Home Assistant   
## Install the integration using HACS (recommended)   
The recommended way to install this integration is by using HACS since it will take care of the updates.   
### Requirements   
In order to install the integration through HACS, you need to install HACS in you Home Assistant setup.    
If you haven't installed HACS yet, you can do so by following the guide available there:   
[https://www.hacs.xyz/docs/use/](https://www.hacs.xyz/docs/use/)    
### Adding the custom repository   
Once you have installed HACS in your Home Assistant setup, you have to add this repository to it.   
Firstly, open the HACS dashboard, which should be reachable by clicking on `HACS` sidebar on the left. Then click on the three dots in the upper right corner and press `Custom repositories`.    
There you should have a field labelled `Repository` in which you have to paste the link of this repository, `https://github.com/Pitscheider/ha_inim_prime`. Then, in the `Type` menu, choose `Integration`.   
Press `ADD` and you should be able to see the added repository in the list.   
You can then close the `Custom repositories` window.   
### Install the integration   
Once you have added the custom repository, in the HACS dashboard you should search `Inim Prime`.   
If you set up the repository correctly, you should be able to see an integration called `Inim Prime`.   
Click on it, press `DOWNLOAD` and then `DOWNLOAD` again.   
### Reboot Home Assistant   
Once the integration has been downloaded, in the Home Assistant `Settings` you should have a repair warning that says `Restart required`. Just restart your Home Assistant instance to finish the installation.   
## Install the integration manually (not recommended)   
If you want to install the integration manually (bear in mind that you will not receive update notifications, and you will not be able to perform update automatically), you can do so by downloading the latest release source code here: [https://github.com/Pitscheider/ha_inim_prime/releases/latest](https://github.com/Pitscheider/ha_inim_prime/releases/latest)    
Once you have downloaded the source code, you can copy the `custom_components` in your Home Assistant `config` directory.   
In case you already have a `custom_components` folder there, you can simply copy the `inim_prime` folder inside the downloaded one and copy it there.   
Reboot your Home Assistant instance and the integration should be installed.   
# Configure the integration in Home Assistant   
Once you have installed the integration following the steps above, you can proceed with its configuration in Home Assistant.   
### Add the integration   
To add the integration go to `Settings` → `Devices & services` and click on `Add integration`. There, search for `Inim Prime` and click on the integration.   
### Initial configuration   
In order to add the integration, some information regarding the panel and the integration behaviour are required.   
Firstly, paste the serial number you have obtained during the panel configuration in the `serial_number` field. Double check it, as it is important that you have written it correctly.   
Then, in the `host` you should type the IP address or the hostname of your Inim Prime panel.   
In case your Inim Prime panel uses DHCP, be sure to reserve a static IP for the panel or set up a DNS record for it (read the `Check network settings` section above).   
I suggest to keep the `use_https` flag enabled as it enables encrypted communication between Home Assistant and the Inim Prime panel.   
In the `api_key` field just paste the API Key you obtained in Prime/STUDIO as described above.   
Regarding the `panel_log_events_fetch_limit` selector, you should probably use the default value.   
Changing this value affects how many logs are obtained at each scan in case new logs are fetched. Don't worry, in case the value chosen here is not enough, the integration will fetch the maximum number of events that is allowed, in order to find the maximum number of new logs.   
Once you have filled all the mandatory fields, just press on `Submit`.   
The initial configuration might take a while. It is expected, as the Inim Prime panel is not exactly fast 😅.   
### Finishing the setup   
Once the initial configuration has been completed you should be able to see all the devices created by the integration that you might rename and assign to a Home Assistant Area. Once you have finished, just press on `Finish`.   
# Reconfigure the integration   
In case you need to update one of those fields:   
- `host`   
- `use_https`   
- `api_key`   
   
Open the integration, click the three dots on the left corresponding to your panel (its default name is `INIM Prime (serial_number)`) and press `Reconfigure`.   
There you should be able to change the desired parameters.   
# Change integration options   
In case you want to update some of the available options of the integration, click on the gear icon on the left corresponding to your panel (its default name is `INIM Prime (serial_number)`).   
There you should be able to update the desired parameters.   
# Devices available   
This section provides a list of the devices that are created by the integration with their entities.   
The devices do not currently support all the Inim Prime functions provided by the API, since it does not work correctly with the current firmware version.   
In the future the devices might change as well as their entities, paraphs with new features.   
Information regarding the state of the panel are updated every 10 seconds for most of the entities.   
An exception is the Log Events one, that is updated every 20 seconds.   
## Inim Prime Panel   
This device represents the panel itself and provides different entities related to it.   
### Sensors   
- **Excluded Zones**   
    This numerical sensor is a helper that shows the number of currently excluded zones.   
   
### Events   
- **Log Events**   
    This event logger is used to track the logs provided by the panel.
It DOES NOT provide events in real time, since those are added asynchronously every 20 seconds.
Log Events are provided with the panel in a non-optimal way, in fact every fetch needs to specify a number of logs that should be retrieved and there is no way to only ask for new events.
In order to determine which logs are new, the integration perform a check between the last fetch and the current one, picking only the new logs. The logic is pretty complex, but is described quite well in the source code.
To reduce the number of logs retrieved at the end of every cycle, the integration only fetch 3 logs per cycle. It uses this small pool of logs to determine if new logs appeared. This way most of the time, when no new log will be there, the operation will be fast.
In case it determines that new logs are there, it performs a new request asking for a number of logs equal to `panel_log_events_fetch_limit`.
In the rare case that `panel_log_events_fetch_limit` value is completely filled with new logs, the integration will perform a new request asking for the safe maximum amount of logs, which is currently 100.
It is important to note that every log has the same category `generic`, since I haven't been able to map all the possible categories. So, the actual information of the logs, are contained in attributes. Home Assistant do not provide an embedded way to show those logs correctly, but by using a custom UI component, it is possible to see them in order. Check the `Log Events` section to discover how to enable that.
The event entity has been chosen, since it is the most suitable across the Home Assistant one. Still, it is a workaround to store logs, since Home Assistant does not have a better way to do so (or at least I haven't found it).   
   
### Configuration   
- **Clear All Alarm Memories**   
    This button clears all the partitions alarm memories. It is a helper.   
- **Include All Zones**   
    This button include every excluded zone. It is a helper.   
   
### Diagnostic   
- **Panel faults**   
    The panel device has 14 fault detection diagnostic sensors, that are provided by the API. I tested some of them, and they were correctly updated, but I wasn't able to trigger all of them.
If you test one of them, and it correctly appears (or not) in Home Assistant, please create an Issue to let me know.   
- **Supply Voltage**   
    This diagnostic sensor shows the current voltage of the panel.   
   
## GSM   
This device represents the GSM, and it provides some information regarding it.   
### Diagnostic   
- **Credit**   
    This entity should show the credit of the GSM SIM. It currently is a String since I have not been able to test it with an actual value.
If you see a value that differs from `Unknown` please make an issue so that I can map it to a numerical value.   
- **Operator**   
    This entity shows the current GSM Operator as a string.   
- **Signal Strength**   
    This entity shows the GSM signal strength in percentage.   
- **Supply Voltage**   
    This entity shows the current voltage of the GSM.   
   
## 
Zone   
This device type represents a zone of the Inim Prime alarm panel. The device will be named this way: `Zone zone_name`.   
You can definitely change the name of every zone to make it represent better what it is. Zones have their own ids, so name changing is absolutely possible.   
### Controls   
- **Exclusion**   
    This switch shows the state of exclusion of the entity. It also permits to change the exclusion status.   
   
### Sensors   
- **State**   
    This sensor shows one of the 4 possible zone states:
   
    - FAULT   
    - READY   
    - ALARM   
    - SHORT_CIRCUIT   
   
    The API, in fact, provides those 4 possible states.   
- **Binary sensor**   
    This binary sensor, which automatically gets the same name of the device, represents a helper for the state entity.   
    In fact, it is probably more useful for users to just have a binary sensor for each zone that represents Open/Closed, Detected/Not Detected, etc.   
    It is advised to change this entity type for each zone and adapt it to its real role. It is possible to do so by clicking on the entity, pressing the gear icon and then select the right type in `Show as` menu. Once you have updated the entity just press on `Update`.   
   
### Diagnostic   
- **Alarm Memory**   
    This entity shows if the zone has an active Alarm Memory.   
   
## Partition   
This device type represents a partition of the Inim Prime alarm panel. The device will be named this way: `Partition partition_name`.   
You can definitely change the name of every partition to make it represent better what it is. Partitions have their own ids, so name changing is absolutely possible.   
### Controls   
- **Clear Alarm Memory**   
    This button clear the partition's alarm memory.   
- **Mode**   
    This entity shows the partitions current mode. It also allows to specify a new mode.   
    There are 4 possible modes:   
    - DISARMED   
    - INSTANT   
    - PARTIAL   
    - TOTAL   
   
### Sensors   
- **State**   
    This entity represents the state of the partition.   
    Three values are possible:   
    - ALARM   
    - READY   
    - SABOTAGE   
   
### Diagnostic   
- **Alarm Memory**   
    This sensor represents if the partition has an active Alarm Memory.   
   
# Suggested configuration   
Once you have completed the initial configuration of the integration, I suggest to complete a few other steps that will improve your experience with the integration.   
## Rename device   
You should probably rename Zones and Partitions to a name that better suites their real functions. Don't worry, every device works with ids, so you can freely change names.   
## Disable unused devices   
This integration add every Zone and Partition by default. However, it might be possible that some of them are not actually used in your alarm setup. You can just click on the three dots of the corresponding device and disable it!   
## Choose the right entity type for zone binary sensor   
As described above, every Zone has a binary sensor that acts as a helper and has the same name of the device. You should probably change how those binary sensors appear in Home Assistant depending on the real function of each Zone.   
To do so open the binary sensor of a zone, click on the gear icon and choose a device type under `Show as` menu. You might want to choose Door, Window, Motion, etc.   
Than just click update.   
## Configure the Log Events History UI card   
In order to be able to see the logs provided by the panel, you need to install a custom UI component.   
You can install it from HACS by searching `Logbook card`.   
Once you have installed it, in your desired overview section create a new `Logbook Card`. Click on `Show code editor` and paste:   
```
type: custom:logbook-card
entity: event.log_events
custom_logs: true
attributes:
  - value: timestamp
    label: Time
    type: date
  - value: type
    label: Event
  - value: location
    label: Location
  - value: agent
    label: Agent
show:
  state: false
  duration: false
  start_date: false
  end_date: false
  icon: false
  separator: true
  entity_name: true
desc: true
hidden_state:
  - unavailable
  - ""
```
Then press on `Show visual editor` and select the `log
_events` entity of your panel. Then click on `Save`.   
You should now be able to see a list of logs with their related attributes.   
You can obviously change the card options as you desire, the one I provided is a basic configuration that should work.   
# About the API   
This integration communicates with the Inim Prime panel using a Python library I created and that is available:   
https://github.com/Pitscheider/inim_prime_api   
You can use it to test you Inim Prime panel API at a lower level or to create something new!   
# About the development of this integration   
This is the first Home Assistant integration I've ever developed. I tried to be as careful as I could during the development, but bear in mind that there is some more work that needs to be done to make it better. Some functionality (mainly due to problems with the API) are missing and there might be bad practices in the logic I used under the hood.   
Again, I tried my best, but still, this is my first integration.   
If you have any suggestion, report or critic, please make an issue and I will be glad to answer you.   
# Trademarks   
INIM and Inim Prime are trademarks or registered trademarks of INIM Electronics S.r.l.   
This project is **not affiliated with, endorsed by, or supported by INIM Electronics S.r.l.**   
# License   
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.   
You are free to use, modify, and redistribute this software under the terms of the GPL-3.0 license.
See the `LICENSE` file for full details.
