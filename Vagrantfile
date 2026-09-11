Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/jammy64"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt update
    sudo apt install python3-pip -y
    python3 -m pip install grpcio protobuf
  SHELL

  # SERVIDOR
  config.vm.define "servidor" do |server|
    server.vm.hostname = "servidor"
    server.vm.network "private_network", ip: "192.168.56.10"

    server.vm.provider "virtualbox" do |vb|
      vb.name = "SDI-Servidor"
      vb.memory = 1024
      vb.cpus = 1
    end
  end

  # CLIENTE 1
  config.vm.define "cliente1" do |client1|
    client1.vm.hostname = "cliente1"
    client1.vm.network "private_network", ip: "192.168.56.11"

    client1.vm.provider "virtualbox" do |vb|
      vb.name = "SDI-Cliente1"
      vb.memory = 1024
      vb.cpus = 1
    end
  end

  # CLIENTE 2
  config.vm.define "cliente2" do |client2|
    client2.vm.hostname = "cliente2"
    client2.vm.network "private_network", ip: "192.168.56.12"

    client2.vm.provider "virtualbox" do |vb|
      vb.name = "SDI-Cliente2"
      vb.memory = 1024
      vb.cpus = 1
    end
  end

end