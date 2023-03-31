#git下载地址 https://mirrors.edge.kernel.org/pub/software/scm/git/
#去git地址查看版本.直接替换git_version可以安装任意版本
git_version=git-2.38.0
rm -rf /etc/${git_version}
mkdir -p /etc/${git_version}
yum remove -y git
yum install -y wget
wget -P /etc/${git_version} https://mirrors.edge.kernel.org/pub/software/scm/git/${git_version}.tar.gz --no-check-certificate
yum install -y curl-devel expat-devel openssl-devel gcc-c++
tar -zxvf /etc/${git_version}/${git_version}.tar.gz -C /etc/${git_version}
cd /etc/${git_version}/${git_version}
./configure --prefix=/usr/local/git
make -j8
make install -j8
echo "export PATH=$PATH:/usr/local/git/bin" >> /etc/profile
source /etc/profile
git --version