# https://github.com/THUDM/CodeGeeX/blob/61529ba61de8e51c520dc67a3ce4bd62278770df/codegeex/docker/Dockerfile#L31
mkdir -p /workspace/download/
curl -o /workspace/download/jdk.tar.gz -SL https://download.oracle.com/java/18/archive/jdk-18_linux-x64_bin.tar.gz \
    && mkdir /usr/java && tar -zxf /workspace/download/jdk.tar.gz -C /usr/java && rm /workspace/download/jdk.tar.gz \
    && java_path=`ls /usr/java/${path}` && echo "export JAVA_HOME=/usr/java/${java_path}" >> ~/.profile
