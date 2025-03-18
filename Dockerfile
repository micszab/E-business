FROM ubuntu:24.04

# Install prerequisites, Java, and other required packages in a single layer
RUN apt-get update && apt-get install -y \
    software-properties-common \
    gcc \
    wget \
    unzip \
    curl \
    openjdk-8-jdk \
    && rm -rf /var/lib/apt/lists/*

# Add the deadsnakes repository to install Python 3.10 specific packages
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-distutils \
    python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install Kotlin
RUN wget https://github.com/JetBrains/kotlin/releases/download/v1.8.20/kotlin-compiler-1.8.20.zip -P /tmp \
    && unzip /tmp/kotlin-compiler-1.8.20.zip -d /opt \
    && rm /tmp/kotlin-compiler-1.8.20.zip

# Install Gradle
RUN wget https://services.gradle.org/distributions/gradle-8.7-bin.zip -P /tmp \
    && unzip -d /opt/gradle /tmp/gradle-8.7-bin.zip \
    && rm /tmp/gradle-8.7-bin.zip

ENV PATH="/opt/gradle/gradle-8.7/bin:/opt/kotlinc/bin:${PATH}"

# Check installation
RUN python3 --version && \
    java -version && \
    kotlinc -version && \
    gradle --version

WORKDIR /app
COPY . /app

CMD ["gradle", "run"]
