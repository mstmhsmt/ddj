FROM codinuum/cca:devel

MAINTAINER mstmhsmt

COPY cca /opt/cca/
COPY regression_examples /opt/cca/regression_examples/
COPY configs /opt/cca/configs/

RUN set -x && \
    cd /root && \
    apt-get update && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gnupg ca-certificates && \
    echo "deb https://downloads.skewed.de/apt focal main" > /etc/apt/sources.list.d/gt.list && \
    apt-key adv --no-tty --keyserver keys.openpgp.org --recv-key 612DEFB798507F25 && \
    apt-get update && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            psmisc time \
            locales locales-all nkf \
            ant ant-optional maven pcregrep \
            python3-distutils \
            python3-psutil \
            python3-graph-tool \
            curl subversion && \
    pip3 install simplejson ortools

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64

# For installing Defects4J

RUN set -x && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libdbi-perl libdbd-csv-perl liburi-perl libjson-perl libjson-parse-perl && \
    cd /opt && \
    git clone https://github.com/rjust/defects4j.git && \
    cd defects4j && \
    ./init.sh

ENV PATH $PATH:/opt/defects4j/framework/bin

# For install helper scripts

COPY python /root/python

RUN set -x && \
    cd /root/python && \
    python3 -m build && \
    pip3 install dist/ddj-*.tar.gz && \
    cd /root && \
    rm -r python

# Cleanup

RUN set -x && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
