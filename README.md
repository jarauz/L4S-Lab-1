# L4S-Lab-1
The building and creation of a small network that uses TCP Reno and TCP Cubic to compare to L4S-Lab-2

# Task 1

## Network Diagram
![](./images/L4SLab1.drawio.png)

## IP Grid

| Name           | Interface     | Address/Mask     |
|----------------|---------------|------------------|
| **WAN** | | 
| Ubuntu-CLI-Router    | ens3 |DHCP
||
| **Client LAN** ||192.168.1.0/24
| Ubuntu-CLI-Router        |ens4 |192.168.1.254/24
| Ubuntu-CLI-VBR-Client    |ens3 |192.168.1.1
| Ubuntu-CLI-CBR-Client    |ens3 |192.168.1.2
| |
| **Server LAN**       ||192.168.2.0/24
| Ubuntu-CLI-Router        |ens5|192.168.2.254/24
| Ubuntu-CLI-VBR-Server    |ens3|192.168.2.1
| Ubuntu-CLI-CBR-Server    |ens3|192.168.2.2

## Configuration
1. Start a new blank project in GNS3 called "L4S-Lab1" and create the network shown in the diagram above
3. Right click on the Ubuntu-CLI-Router and enter the Configuration window
4. Click on the network tab and change "Adapters" to 3
5. Start the Ubuntu-CLI-Router and give it a hostname and run the following command,

   ```
   sudo nmcli general hostname Ubuntu-CLI-Router
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

8. Use ```ip a``` to verify all three interfaces got an address

9. Apply a NAT to allow client and server machines to download new kernel

   ```
   sudo iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
   sudo iptables -A FORWARD -i ens4 -o ens3 -j ACCEPT
   sudo iptables -A FORWARD -i ens5 -o ens3 -j ACCEPT
   sudo iptables -A FORWARD -i ens3 -m state --state RELATED,ESTABLISHED -j ACCEPT
   ```

10. Now you need to enable IPv4 forwarding so it can act as a router

   ```
   sudo nano /etc/sysctl.conf
   ```

11. Find the line that looks like ```#net.ipv4.ip_forward=1``` and uncomment it and load the new changes

    ```
    sudo sysctl -p
    ```

12. Start and configure all client and server Ubuntu devices

    ```
    sudo nmcli general hostname Ubuntu-CLI-<CHECK IP GRID>
    sudo nmcli con mod "Wired connection 1" ipv4.addresses <CHECK IP GRID/MASK>
    sudo nmcli con mod "Wired connection 1" ipv4.gateway <CHECK IP GRID>
    sudo nmcli con mod "Wired connection 1" ipv4.dns 8.8.8.8,8.8.4.4
    sudo nmcli con mod "Wired connection 1" ipv4.method manual
    sudo nmcli connection down "Wired connection 1"
    sudo nmcli connection up "Wired connection 1"
    ```

13. At this point all devices are able to reach each other and a reliable IP address (Ask instructor for help if this isn't working for you)

# Task 2

## Download TCP Prague Kernel (All steps need to be done on every machine)

14. Download all tools needed

    ```
    sudo apt-get update && sudo apt install unzip -y
    ```

15. Download the TCP Prague kernel

    ```
    wget https://github.com/L4STeam/linux/releases/download/testing-build/l4s-testing.zip
    ```

16. Unzip the downloaded zip file

    ```
    unzip l4s-testing.zip -d l4s-kernel
    ```

17. Install the packages

    ```
    cd ~/l4s-kernel
    sudo dpkg --install debian_build/*
    sudo update-grub
    ```

18. Reboot the machine and when the GNU Grub Menu appears, Use the arrow keys to select "Advanced options for Ubuntu" and select the newly installed kernel named "Ubuntu, with Linux 5.15.72-8ac01b97f-prague-121"

19. Use this command to see what kernel is being used. You should see the newly installed kernel

    ```
    uname -r
    ```

20. Load the required modules

    ```
    sudo modprobe sch_dualpi2
    sudo modprobe tcp_prague
    ```

# Task 3

## IP Header and ECN

21. Explicit Congestion Notification (ECN) is a networking extension that allows routers to signal impending network congestion to end-hosts without dropping packets. ECN is set in the IPv4 header of the packet in the Differentiated Services Field using the last two bits to set ECN

| ECN Codepoint       | Name        | Meaning     |
|----------------|---------------|------------------|
| 00       | Non-ECT   | Not ECN-Capable Transport. The router will drop this packet when there is congestion as a signal
| 01       | ECT-1     | ECN-Capable Transport. In L4S, this identifies a packet from an L4S-aware sender (Using TCP Prague)
| 10       | ECT-0     | ECN-Capable Transport. Used by "Classic" ECN senders (Using Standard TCP)
| 11       | CE        | Congestion Experienced. The router changed the bits to 11 to tell the receiver that the queue is filling up

