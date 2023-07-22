#!/bin/bash

### JavaScript ###

# Create directory for Node.js download
mkdir -p /workspace/download/

# Download and install Node.js
curl -o /workspace/download/node.tar.gz -SL https://nodejs.org/download/release/v16.14.0/node-v16.14.0-linux-x64.tar.gz \
    && mkdir -p /usr/local/lib/nodejs \
    && tar -zxf /workspace/download/node.tar.gz -C /usr/local/lib/nodejs \
    && mv /usr/local/lib/nodejs/node-v16.14.0-linux-x64 /usr/local/lib/nodejs/node \
    && rm /workspace/download/node.tar.gz \
    && npm install -g js-md5@0.7.3

# Reinstall js-md5 locally and move to the right location
npm install js-md5@0.7.3
mkdir /usr/local/lib/node_modules
mv node_modules/* /usr/local/lib/node_modules/


### Java ###

# Create directory for Java download
mkdir -p /workspace/download/

# Download and install JDK
curl -o /workspace/download/jdk.tar.gz -SL https://download.oracle.com/java/18/archive/jdk-18_linux-x64_bin.tar.gz \
    && mkdir /usr/java \
    && tar -zxf /workspace/download/jdk.tar.gz -C /usr/java \
    && rm /workspace/download/jdk.tar.gz \
    && java_path=$(ls /usr/java/) \
    && echo "export JAVA_HOME=/usr/java/${java_path}" >> ~/.profile

# Set Java path
export PATH="/usr/java/jdk-18/bin:${PATH}"


### Go ###


# Create directory for Go download
mkdir -p /workspace/download

# Download and install Go
curl -o /workspace/download/go.tar.gz -SL https://go.dev/dl/go1.18.4.linux-amd64.tar.gz \
    && tar -zxf /workspace/download/go.tar.gz -C /usr/local \
    && rm /workspace/download/go.tar.gz

# Download vendor dependencies (optional)
wget https://github.com/THUDM/CodeGeeX/raw/07b8d7f10fe544890f9e665473998aed4e831314/codegeex/benchmark/humaneval-x/go/evaluation/vendor.tar.gz \
    && tar -zxf vendor.tar.gz -C ./

# Set Go environment variables
export PATH="/bin:/usr/local/go/bin:${PATH}"
export GOFLAGS="-mod=mod"

# Install testify/assert for Go
go get github.com/stretchr/testify/assert

# Create go.mod file for Go
cat > go.mod <<EOF
module humanEval
go 1.18

require (
    github.com/go-openapi/inflect v0.19.0
    github.com/stretchr/testify v1.8.0
)

require (
    github.com/davecgh/go-spew v1.1.1 // indirect
    github.com/pmezard/go-difflib v1.0.0 // indirect
    gopkg.in/yaml.v3 v3.0.1 // indirect
)
EOF


### Rust ###

# Download and install Rust using rustup
curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal --default-toolchain stable -y

# Set Rust path
export PATH="/root/.cargo/bin:${PATH}"
