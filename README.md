# Repository Overview

This repository hosts multiple projects, each maintained in its own branch:

- **1_Docker**: Provides Docker images tailored for various development environments.
- **2_Scala**: Implements a web application using the Play framework in Scala 3.
- **3_Kotlin**: Develops a client application in Kotlin using the Ktor framework for integration with Discord.

---

## 1_Docker: Containerized Environments

### Key Features

- Ubuntu-based image with Python 3.10.
- `ubuntu:24.04` image equipped with Java 8 and Kotlin.
- Enhanced environment with the latest Gradle and SQLite JDBC package within a Gradle project (`build.gradle`).
- Includes a `HelloWorld` example, demonstrating execution via CMD and Gradle.
- Integrated `docker-compose` configuration for streamlined deployment.

---

## 2_Scala: Web Application

### Key Features

- A product controller has been created.
- The controller includes endpoints following CRUD principles, with data retrieved from a list.

---

## 3_Kotlin: Discord Client Application

### Key Features

- A client application developed in Kotlin using the Ktor framework, enabling message transmission to Discord.
- Supports bidirectional communication, allowing the application (bot) to receive and respond to user messages from Discord.
