def cpu_stress(command):
    while command == "start":
        print("cpu stress testing")


if __name__ == "__main__":
    cpu_stress("start")
    cpu_stress("stop")