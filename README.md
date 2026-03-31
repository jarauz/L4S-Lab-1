# L4S-Lab-1
The building and creation of a small network that uses TCP Reno and TCP Cubic to compare to L4S-Lab-2

# Task 1

## Network Diagram
![](./images/L4SLab1.drawio.png)

## Configuration
1. Start a new blank project in GNS3 called "L4S-Lab1" and create the network shown in the diagram above
3. Right click on the Ubuntu-CLI-Router and enter the Configuration window
4. Click on the network tab and change "Adapters" to 3
5. Start the Ubuntu-CLI-Router and apply the following commands,
   ```
   sudo nano /etc/netplan/50-cloud-init.yaml
   ```
6. And have your .yaml file look like this,
   ```
   network:
     version: 2
     renderer: NetworkManager
     ethernets:
       ens3:
         dhcp4: yes
         dhcp4-overrides:
           use-dns: true
           use-routes: true
       ens4:
         dhcp4: no
         addresses:
           - 192.168.1.254/24
       ens5:
         dhcp4: no
         addresses:
           - 192.168.2.254/24
     ```
