Installation Note:

* Install Doodba as normal, make sure to use postgres 9.6
* To install Java 7 add following in apt.txt, and run > invoke img-build

```
openjdk-7-jdk
```

* To restore database

```
# copy file into postgres container
docker cp <file path> <postgres container name>:<file path>

# Move into postgres container
docker exec -it -u 0 <postgres container name> bash
```

* Ininstall Jasper Report and Java 7 on your local machine

Download `jdk-7u80-linux-x64.tar.gz` from https://files-cdn.liferay.com/mirrors/download.oracle.com/otn-pub/java/jdk/7u80-b15/

Navigate to ~/Downloads:

```
sudo mkdir -p /usr/local/java
sudo cp -r jdk-7u80-linux-x64.tar.gz /usr/local/java/
cd /usr/local/java
sudo tar xvzf jdk-7u80-linux-x64.tar.gz
ls –a    #you should see jdk1.7.0_80 
```

Edit profile

```
sudo nano /etc/profile
```
Scroll down to the end of the file using arrow keys and add the following lines below to the end of /etc/profile file:
```
JAVA_HOME=/usr/local/java/jdk1.7.0_80
JRE_HOME=/usr/local/java/jdk1.7.0_80 
PATH=$PATH:$JRE_HOME/bin:$JAVA_HOME/bin
export JAVA_HOME
export JRE_HOME
export PATH
```

Update alternatives:

```
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/local/java/jdk1.7.0_80/bin/java" 1
sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/local/java/jdk1.7.0_80/bin/javac" 1
sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/local/java/jdk1.7.0_80/bin/javaws" 1
sudo update-alternatives --set java /usr/local/java/jdk1.7.0_80/bin/java
sudo update-alternatives --set javac /usr/local/java/jdk1.7.0_80/bin/javac
sudo update-alternatives --set javaws /usr/local/java/jdk1.7.0_80/bin/javaws
```
Reload profile:
```
source /etc/profile
```
Verify installation:
```
java -version
```
