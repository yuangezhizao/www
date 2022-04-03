---
title: 树莓派基于 K3s 搭建 Kubernetes 集群
date: 2021-03-06 21:14:51
tags:
  - RaspberryPi
  - K3s
  - Kubernetes
count: 2
os: 1
os_1: Big Sur 11.2.2 (20D80)
browser: 0
browser_1: 89.0.4389.82 Stable
place: 新家
key: 109
---
    闲鱼一百五收了块二手 3B+ 板子
<!-- more -->
## 0x00.前言
终于有两台`rpi`，可以组集群辣

## 0x01.修改`/etc/hosts`文件
①主节点：
``` bash
pi@rpi-master:~ $ sudo echo -e "192.168.25.129\trpi-master" | sudo tee -a /etc/hosts
192.168.25.129  rpi-master
pi@rpi-master:~ $ sudo echo -e "192.168.25.130\trpi-slave" | sudo tee -a /etc/hosts
192.168.25.130  rpi-slave
pi@rpi-master:~ $ cat /etc/hosts
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       rpi-master
192.168.25.129  rpi-master
192.168.25.130  rpi-slave
pi@rpi-master:~ $ ping rpi-slave
PING rpi-slave (192.168.25.130) 56(84) bytes of data.
64 bytes from rpi-slave (192.168.25.130): icmp_seq=1 ttl=64 time=2.35 ms
64 bytes from rpi-slave (192.168.25.130): icmp_seq=2 ttl=64 time=2.50 ms
^C
```
②从节点：
``` bash
pi@rpi-slave:~ $ sudo echo -e "192.168.25.129\trpi-master" | sudo tee -a /etc/hosts
192.168.25.129  rpi-master
pi@rpi-slave:~ $ sudo echo -e "192.168.25.130\trpi-slave" | sudo tee -a /etc/hosts
192.168.25.130  rpi-slave
pi@rpi-slave:~ $ cat /etc/hosts
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       rpi-slave
192.168.25.129  rpi-master
192.168.25.130  rpi-slave
pi@rpi-slave:~ $ ping rpi-master
PING rpi-master (192.168.25.129) 56(84) bytes of data.
64 bytes from rpi-master (192.168.25.129): icmp_seq=1 ttl=64 time=98.3 ms
64 bytes from rpi-master (192.168.25.129): icmp_seq=2 ttl=64 time=2.25 ms
^C
```

## 0x02.[开启 cgroups](https://rancher.com/docs/k3s/latest/en/advanced/#enabling-cgroups-for-raspbian-buster)
修改`/boot/cmdline.txt`：追加`cgroup_memory=1 cgroup_enable=memory`
``` bash
pi@rpi-slave:~ $ sudo vim /boot/cmdline.txt 
pi@rpi-slave:~ $ cat /boot/cmdline.txt 
console=serial0,115200 console=tty1 root=PARTUUID=16fa0840-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles cgroup_memory=1 cgroup_enable=memory
```

## 0x03.[安装 K3s](https://rancher.com/docs/k3s/latest/en/quick-start/)
①主节点：
``` bash
Linux rpi-master 5.10.17-v8+ #1403 SMP PREEMPT Mon Feb 22 11:37:54 GMT 2021 aarch64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  6 21:52:08 2021
pi@rpi-master:~ $ curl -sfL https://get.k3s.io | sh -
[INFO]  Finding release for channel stable
[INFO]  Using v1.20.4+k3s1 as release
[INFO]  Downloading hash https://github.com/k3s-io/k3s/releases/download/v1.20.4+k3s1/sha256sum-arm64.txt
[INFO]  Downloading binary https://github.com/k3s-io/k3s/releases/download/v1.20.4+k3s1/k3s-arm64
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO]  systemd: Starting k3s
pi@rpi-master:~ $ sudo kubectl get nodes
NAME         STATUS   ROLES                  AGE     VERSION
rpi-master   Ready    control-plane,master   9m55s   v1.20.4+k3s1
pi@rpi-master:~ $ sudo kubectl get pods --all-namespaces
NAMESPACE     NAME                                      READY   STATUS      RESTARTS   AGE
kube-system   metrics-server-86cbb8457f-47gqx           1/1     Running     0          20m
kube-system   coredns-854c77959c-xvfzj                  1/1     Running     0          20m
kube-system   helm-install-traefik-98p9q                0/1     Completed   0          20m
kube-system   svclb-traefik-qq6xl                       2/2     Running     0          12m
kube-system   traefik-6f9cbd9bd4-g52z6                  1/1     Running     0          12m
kube-system   local-path-provisioner-5ff76fc89d-m54v8   1/1     Running     2          20m
pi@rpi-master:~ $ sudo cat /var/lib/rancher/k3s/server/node-token
<rm>
pi@rpi-master:~ $ sudo cat /etc/rancher/k3s/k3s.yaml
<rm>
```
②从节点：
``` bash
Linux rpi-slave 5.10.17-v8+ #1403 SMP PREEMPT Mon Feb 22 11:37:54 GMT 2021 aarch64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  6 22:40:54 2021 from 240e:30d:1fb0:4300:81eb:6678:7040:d3c7
pi@rpi-slave:~ $ curl -sfL https://get.k3s.io | K3S_URL=https://192.168.25.129:6443 K3S_TOKEN=<rm> sh -
[INFO]  Finding release for channel stable
[INFO]  Using v1.20.4+k3s1 as release
[INFO]  Downloading hash https://github.com/k3s-io/k3s/releases/download/v1.20.4+k3s1/sha256sum-arm64.txt
[INFO]  Downloading binary https://github.com/k3s-io/k3s/releases/download/v1.20.4+k3s1/k3s-arm64
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Skipping /usr/local/bin/ctr symlink to k3s, command exists in PATH at /usr/bin/ctr
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-agent-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s-agent.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s-agent.service
[INFO]  systemd: Enabling k3s-agent unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s-agent.service → /etc/systemd/system/k3s-agent.service.
[INFO]  systemd: Starting k3s-agent
```
稍等片刻，马上回来
``` bash
pi@rpi-master:~ $ sudo kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
rpi-master   Ready    control-plane,master   47m   v1.20.4+k3s1
rpi-slave    Ready    <none>                 22s   v1.20.4+k3s1
```

## 0x03.[安装 kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/#install-with-homebrew-on-macos)
``` bash
yuangezhizao@MacMini ~ % brew install kubectl
yuangezhizao@MacMini ~ % vim ~/.kube/config
yuangezhizao@MacMini ~ % chmod 600 ~/.kube/config
yuangezhizao@MacMini ~ % kubectl get nodes
NAME         STATUS   ROLES                  AGE    VERSION
rpi-slave    Ready    <none>                 5m4s   v1.20.4+k3s1
rpi-master   Ready    control-plane,master   51m    v1.20.4+k3s1
yuangezhizao@MacMini ~ % kubectl label node rpi-slave node-role.kubernetes.io/worker=worker
node/rpi-slave labeled
yuangezhizao@MacMini ~ % kubectl get nodes
NAME         STATUS   ROLES                  AGE     VERSION
rpi-master   Ready    control-plane,master   55m     v1.20.4+k3s1
rpi-slave    Ready    worker                 8m50s   v1.20.4+k3s1
```
``` bash
pi@rpi-master:~ $ sudo kubectl get pods --all-namespaces
NAMESPACE     NAME                                      READY   STATUS      RESTARTS   AGE
kube-system   metrics-server-86cbb8457f-47gqx           1/1     Running     0          52m
kube-system   coredns-854c77959c-xvfzj                  1/1     Running     0          52m
kube-system   helm-install-traefik-98p9q                0/1     Completed   0          52m
kube-system   svclb-traefik-qq6xl                       2/2     Running     0          44m
kube-system   traefik-6f9cbd9bd4-g52z6                  1/1     Running     0          44m
kube-system   local-path-provisioner-5ff76fc89d-m54v8   1/1     Running     2          52m
kube-system   svclb-traefik-s9xkl                       2/2     Running     0          5m48s
```

## 0x04.[Kubernetes 仪表盘](https://rancher.com/docs/k3s/latest/en/installation/kube-dashboard/)
``` bash
pi@rpi-master:~ $ sudo k3s kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
pi@rpi-master:~ $ cd Downloads/
pi@rpi-master:~/Downloads $ vim dashboard.admin-user.yml
pi@rpi-master:~/Downloads $ vim dashboard.admin-user-role.yml
pi@rpi-master:~/Downloads $ sudo k3s kubectl create -f dashboard.admin-user.yml -f dashboard.admin-user-role.yml
serviceaccount/admin-user created
clusterrolebinding.rbac.authorization.k8s.io/admin-user created
pi@rpi-master:~/Downloads $ sudo k3s kubectl -n kubernetes-dashboard describe secret admin-user-token | grep ^token
<rm>
pi@rpi-master:~ $ sudo kubectl get deployment --namespace=kubernetes-dashboard kubernetes-dashboard
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-dashboard   1/1     1            1           10m
pi@rpi-master:~ $ sudo kubectl get service --namespace=kubernetes-dashboard kubernetes-dashboard
NAME                   TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
kubernetes-dashboard   ClusterIP   10.43.89.57   <none>        443/TCP   10m
pi@rpi-master:~ $ sudo kubectl --namespace=kubernetes-dashboard get pod -o wide | grep dashboard
dashboard-metrics-scraper-79c5968bdc-fxxjn   1/1     Running   0          10m   10.42.1.4   rpi-slave   <none>           <none>
kubernetes-dashboard-9f9799597-vzqt7         1/1     Running   0          10m   10.42.1.3   rpi-slave   <none>           <none>
```
``` bash
yuangezhizao@MacMini ~ % kubectl proxy
Starting to serve on 127.0.0.1:8001
```
![](https://i1.yuangezhizao.cn/macOS/QQ20210306-232125@2x.png!webp)
![](https://i1.yuangezhizao.cn/macOS/QQ20210306-232717@2x.png!webp)
![](https://i1.yuangezhizao.cn/macOS/QQ20210306-232850@2x.png!webp)
![](https://i1.yuangezhizao.cn/macOS/QQ20210306-232931@2x.png!webp)

## 0x05.后记
就算是`3b+`，毕竟只有`1G`内存，即使不开启交换，搁着一天多就会**黄灯**常亮，还是性能不足？

## 0x06.引用
[访问K8s Dashboard的几种方式](https://segmentfault.com/a/1190000023130407)
