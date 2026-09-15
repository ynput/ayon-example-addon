name = "example"
title = "Example"
version = "2.1.0"

services = {
    "ExampleService": {"image": "ynput/ayon-example-service"},
    "TestService": {"image": "harbor.ynput.team/testing/test-service:latest"},
}

plugin_for = ["ayon_server"]
build_command = ""
