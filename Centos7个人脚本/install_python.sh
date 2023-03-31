#python下载地址 https://registry.npmmirror.com/binary.html?path=python/
#去python下载地址.直接替换version可以安装任意版本
#https://registry.npmmirror.com/-/binary/python/2.4.6/Python-2.4.6.tgz
#https://registry.npmmirror.com/-/binary/python/2.7/Python-2.7.tgz
#https://registry.npmmirror.com/-/binary/python/3.9.4/Python-3.9.4.tgz

version=3.9.4
python_version=python${version}
rm -rf /etc/${python_version}
mkdir -p /etc/${python_version}
yum install -y wget
wget -P /etc/${python_version} https://registry.npmmirror.com/-/binary/python/${version}/Python-${version}.tgz --no-check-certificate
yum install -y wget tar zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
tar -zxvf /etc/${python_version}/Python-${version}.tgz -C /etc/${python_version}
cd /etc/${python_version}/Python-${version}
./configure prefix=/usr/local/${python_version}
make -j8
make install -j8
if [ ${version:0:1} == "2" ]
then
  rm -rf /usr/bin/${python_version}
  ln -s /usr/local/${python_version}/bin/python /usr/bin/${python_version}
  rm -rf /usr/bin/python2
  ln -s /usr/local/${python_version}/bin/python /usr/bin/python2
  rm -rf /usr/bin/python
  ln -s /usr/local/${python_version}/bin/python /usr/bin/python
else
  rm -rf /usr/bin/${python_version}
  ln -s /usr/local/${python_version}/bin/python3 /usr/bin/${python_version}
  rm -rf /usr/bin/python3
  ln -s /usr/local/${python_version}/bin/python3 /usr/bin/python3
fi
#如果下载的是python2版本, 则软链接是python2 和 python 和 python${version}
#如果下载的是python3版本, 则软链接是python3 和 python${version}