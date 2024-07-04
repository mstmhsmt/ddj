FROM codinuum/cca:devel2404

MAINTAINER mstmhsmt

COPY cca /opt/cca/
# COPY regression_examples /opt/cca/regression_examples/
COPY configs /opt/cca/configs/

RUN set -x && \
    cd /root && \
    apt-get update && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            psmisc time \
            locales locales-all nkf \
            ant ant-optional maven \
            pcregrep \
            python3-build \
            python3-psutil \
            python3-networkx \
            python3-absl \
            python3-simplejson \
            curl subversion && \
    pip3 install ortools --break-system-packages && \
    cd /usr/lib/jvm && \
    ln -s java-8-openjdk-* java-8-openjdk

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk

# For installing Defects4J

RUN set -x && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libdbi-perl \
        libdbd-csv-perl \
        liburi-perl \
        libjson-perl \
        libjson-parse-perl && \
    cd /opt && \
    git clone https://github.com/rjust/defects4j.git && \
    cd defects4j && \
    ./init.sh

ENV PATH $PATH:/opt/defects4j/framework/bin

# For installing helper scripts

COPY python /root/python

RUN set -x && \
    cd /root/python && \
    python3 -m build && \
    pip3 install dist/ddj-*.tar.gz --break-system-packages && \
    cd /root && \
    rm -r python

# Cleanup

RUN set -x && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
