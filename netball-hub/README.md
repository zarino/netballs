# netball-hub

Code relating to the setup of a Raspberry Pi as an MQTT broker and a DMX interface.

## Setting up Raspbian, wifi, and SSH access

Follow the instructions here to get the Pi into a suitable state for provisioning:

<https://zarino.co.uk/post/raspberry-pi-mac-setup/>

Change the Pi’s `hostname` to `netball-hub`, and set up password-less SSH login with `ssh-copy-id`, so that you can SSH right into the Pi with just:

    ssh pi@netball-hub.local

## Provisioning

Install Ansible on your main machine. For example, on a Mac:

    brew install ansible

Or on Ubuntu:

    sudo apt-get install ansible

Then run the provisioner in `ansible-provisioning`:

    cd ansible-provisioning
    ansible-playbook -i inventory.yml playbook.yml

_(Much of the MQTT provisioning has been adapted from instructions at <https://oneguyoneblog.com/2017/06/20/mosquitto-mqtt-node-red-raspberry-pi/>.)_

For now, you’ll need to install the RaspAP wifi access point stuff by hand. SSH into the Pi, then become root, and run the installer:

    ssh pi@netball-hub.local
    sudo su
    wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap
    reboot

Now connect to the Pi’s wifi network:

    SSID      raspi-webgui
    Password  ChangeMe

The RaspAP admin interface should now be accessible at:

    URL       http://netball-hub.local/
    Username  admin
    Password  secret

Visit the [Configure hostspot](http://netball-hub.local/index.php?page=hostapd_conf) page and make the following changes:

* Basic->SSID: `netball-hub-wifi`
* Security->PSK: `bubblino`
* Advanced->Country Code: `United Kingdom`

Press the "Save settings" button, then cross your fingers. The `raspi-webgui` network should disappear, and a new `netball-hub-wifi` should replace it.

The Pi should have access to the wider internet (via its connection as a _client_ to the `DoESLiverpool` wifi network), but it doesn’t seem that devices _connected_ to the Pi’s `netball-hub-wifi` network will get the same internet connection. Annoying.
