# L4S-Lab-1
The building and creation of a small network that uses TCP Reno and TCP Cubic to compare to L4S-Lab-2

# Task 1

## Network Diagram
![](./images/L4SLab1.drawio.png)

## IP Grid

| Name           | Interface     | Address/Mask     |
|----------------|---------------|------------------|
| **WAN** | | 
| VyOS-1         | |132.235.205.**X**/25
| (WAN Gateway)  | |132.235.205.**Y**
||
| **Front Office Network** ||
| DHCP Pool Start        ||
| VPCS                   ||
| Windows                ||
| DHCP Pool Stop         ||
| VyOS-1 (Front Office Gateway)  ||
| |
| **Guest Wi-Fi Network**       ||
| DHCP Pool Start        ||
| VPCS  ||
| Ubuntu-GUI             ||
| DHCP Pool Stop         ||
| VyOS-2 (Guest Wi-Fi Gateway)  ||

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

7. Apply these changes

   ```
   sudo netplan apply
   ```

8. Apply a NAT to allow client and server machines to download new kernel

   ```
   sudo iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
   sudo iptables -A FORWARD -i ens4 -o ens3 -j ACCEPT
   sudo iptables -A FORWARD -i ens5 -o ens3 -j ACCEPT
   sudo iptables -A FORWARD -i ens3 -m state --state RELATED,ESTABLISHED -j ACCEPT
   ```

9. Now you need to enable IPv4 forwarding so it can act as a router

   ```
   sudo nano /etc/sysctl.conf
   ```

10. Find the line that looks like "#net.ipv4.ip_forward=1" and uncomment it and laod the new changes

    ```
    sudo sysctl -p
    ```

11. Start and configure all client and server Ubuntu devices

    ```
    sudo nmcli general hostname Ubuntu-CLI-<CHECK IP GRID>
    sudo nmcli con mod "Wired connection 1" ipv4.addresses <CHECK IP GRID/MASK>
    sudo nmcli con mod "Wired connection 1" ipv4.gateway <CHECK IP GRID>
    sudo nmcli con mod "Wired connection 1" ipv4.dns 8.8.8.8,8.8.4.4
    sudo nmcli con mod "Wired connection 1" ipv4.method manual
    sudo nmcli connection down "Wired connection 1"
    sudo nmcli connection up "Wired connection 1"
    ```

