import argparse
import concurrent.futures
import os
import signal
import time
from subprocess import Popen, PIPE, TimeoutExpired

import requests

processes = []
framework_pids = []

runtimes = {"HelidonSE": "frameworks/helidonSE/target/helidon-se.jar",
            "HelidonMP": "frameworks/helidonMP/target/helidon-mp.jar",
            "Nima": "frameworks/nima/target/helidon-nima.jar",
            "SpringBoot": "frameworks/springboot/target/spring.jar"}


class PerformanceRunner:

    def __init__(self):
        self.process = None
        self.start_time = 0.0
        self.end_time = 0.0
        self.framework_pid = None

    def run_java(self, jar_file):
        params = ["java"]
        params.extend(["--enable-preview"])
        params.extend(["-jar", jar_file])

        self.start_time = time.perf_counter()
        process = Popen(params, stdout=PIPE, stderr=PIPE)
        processes.append(process)
        self.framework_pid = process.pid
        self.process = process

    def see_rss(self):
        process = Popen(["ps", "-o", "rss", "-p", str(self.framework_pid)], stdout=PIPE, stderr=PIPE)
        processes.append(process)
        try:
            out, err = process.communicate(timeout=10)
        except TimeoutExpired:
            process.kill()
            out, err = process.communicate()
            print(err.decode())

        rss_mem = out.decode().split("\n")[1]
        print("RSS = {mem}".format(mem=rss_mem))

    def wait_for(self, params):
        if self.framework_pid == -1:
            return False
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.wait_for_response, params)
            (status, self.end_time) = future.result()
        return status

    def wait_for_response(self, params):
        time.sleep(0.05)
        start_time = time.time()
        result = True
        duration = 0.0
        full_url = "GET http://localhost:8080/greet"
        while True:
            try:
                response = requests.get("http://localhost:8080/greet")
                if response.status_code == 200:
                    duration = time.perf_counter()
                    break
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(0.05)
            if time.time() - start_time >= 10:
                print("Timeout reached for {url}".format(url=full_url))
                result = False
                break
        return result, duration

    def measure_first_response(self):
        duration = (self.end_time - self.start_time) * 1000
        print("First Response in: %.2f ms" % duration)

    def terminate(self):
        if self.process.pid != self.framework_pid:
            os.kill(self.framework_pid, signal.SIGKILL)
            framework_pids.remove(self.framework_pid)
        self.process.terminate()
        self.process.communicate()


def get_program_arguments():
    parser = argparse.ArgumentParser(
        prog='Test framework start time')

    parser.add_argument("-f", "--framework", choices=["HelidonSE", "HelidonMP", "Nima", "SpringBoot"], required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_program_arguments()
    print("{runtime} First Response Measurement".format(runtime=args.framework))
    framework = runtimes[args.framework]
    for n in range(10):
        runner = PerformanceRunner()
        runner.run_java(framework)

        running = runner.wait_for({"framework": framework})
        if running:
            runner.measure_first_response()
            runner.see_rss()
        else:
            print("Could not start process")
            break
        runner.terminate()
