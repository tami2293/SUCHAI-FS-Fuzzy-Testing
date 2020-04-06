from fuzzingbook.Fuzzer import Runner
from subprocess import Popen, PIPE
from fuzzcspzmqnode import *
from proc_info import *


class FlightSoftwareRunner(Runner):
    def __init__(self, path="../../Git/SUCHAI-Memoria/build_x86/", exec_cmd="./SUCHAI_Flight_Software"):
        self.exec_cmd = exec_cmd

    def run_process(self, cmds_list=[], params_list=[]):
        """
        Runs SUCHAI flight software and send commands to it until the process is done.
        :param cmds_list:
        :param params_list:
        :return: Tuple. List of commands executed, list of results, execution time and memory usage.
        """
        # Each element of params_list matches with a command from the commands list
        assert len(cmds_list) == len(params_list), "Each sequence of parameters must match with a command"

        # Execute flight software
        time.sleep(1)
        init_time = time.time()  # Start measuring execution time of the sequence
        suchai_process = Popen([self.exec_cmd], stdin=PIPE)
        time.sleep(1)

        # Send commands to the flight software through zmq
        args = get_parameters()
        dest = "1"
        port = "10"
        node = FuzzCspZmqNode(int(args.node), args.ip, args.in_port, args.out_port, args.nmon, args.ncon)
        node.start()

        for i in range(0, len(cmds_list)):
            time.sleep(0.5)  # Give some time to zmqnode threads (writer and reader)
            cmd = cmds_list[i]
            params = params_list[i]
            print("node send:", cmd + " " + params)  # For debugging purposes
            header = CspHeader(src_node=int(args.node), dst_node=int(dest), dst_port=int(port), src_port=55)
            node.send_message(cmd + " " + params, header)

        # Get memory usage of the SUCHAI process
        proc_pid = suchai_process.pid
        vm, rm = get_mem_info(proc_pid)

        # Exit SUCHAI process
        hdr = CspHeader(src_node=int(args.node), dst_node=int(dest), dst_port=int(port), src_port=55)
        node.send_message("obc_reset", hdr)

        # Get SUCHAI process return code
        return_code = suchai_process.wait()
        end_time = time.time()  # End measuring execution time of the sequence
        print("Return code: ", return_code)  # For debugging purposes

        # Get commands, results, execution time and memory usage
        executed_cmds = node.filter_cmds_names()
        results = node.filter_results()
        cmds_time = node.filter_cmds_exec_time()
        total_exec_time = end_time - init_time

        node.stop()
        return cmds_list, params_list, executed_cmds, results, cmds_time, return_code, total_exec_time, rm, vm

    def run(self, cmds_list=[], params_list=[]):
        result = self.run_process(cmds_list, params_list)

        if result[5] == 0:
            outcome = self.PASS
        elif result[5] < 0:
            outcome = self.FAIL
        else:
            outcome = self.UNRESOLVED

        return result, outcome
