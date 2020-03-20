from zmqnode import *
import random
from queue import Queue
import pandas as pd

class ExpCspZmqNode(CspZmqNode):
    def __init__(self, node, hub_ip='localhost', in_port="8001", out_port="8002", monitor=True, console=False):
        CspZmqNode.__init__(self, node, hub_ip, in_port, out_port, monitor, console)
        self.messages_queue = Queue()

    def read_message(self, message, header=None):
        """ This method is called from the _reader thread"""
        self.messages_queue.put([message.decode('ASCII', 'ignore')])

    def filter_cmd_result_list(self):
        """
        Choose messages indicating that is either running a command or returning a command result
        :param n_cmds: Number of commands to be run
        :return:
        """
        _messages_list = []

        # Read all messages from the queue
        while not self.messages_queue.empty():
            _messages_list.extend(self.messages_queue.get())

        # print(_messages_list)
        cmds = [cmd for cmd in _messages_list if 'Running' in cmd]
        results = [result for result in _messages_list if 'Command result' in result]

        return cmds, results


def write_to_file(cmds_lst, results_lst):
    # Check lists length
    print("Largos")
    print(len(cmds_lst), len(results_lst))
    while len(results_lst) < len(cmds_lst):
        results_lst.append(0)
    d = {'Commands sent': cmds_lst, 'Results': results_lst}
    df = pd.DataFrame(data=d)
    df.to_csv('/home/tamara/PycharmProjects/Memoria/results_report.txt', index=False, sep=' ')
    print(df)


def parm_type_fail(process, n_random_cmds):
    """
    First experiment where the value of the parameters could fail for each case
    :return:
    """
    # Send commands to FS through zmq
    args = get_parameters()
    dest = "1"
    port = "10"
    cmds_list = ["com_ping ", "com_set_node ", "test ", "drp_ebf ", "drp_add_hrs_alive ", "drp_set_deployed ", "tm_get_last ",
                 "tm_send_status "]
    parms_list = ["", "1", "1010"]
    node = ExpCspZmqNode(int(args.node), args.ip, args.in_port, args.out_port, args.nmon, args.ncon)
    node.start()

    # Send five commands chosen randomly
    selected_cmd_list = []
    selected_parm_list = []
    for i in range(0, n_random_cmds):
        cmd = random.choice(cmds_list)
        selected_cmd_list.append(cmd)
        parm = random.choice(parms_list)
        selected_parm_list.append(parm)
        time.sleep(0.5)  # Give some time to zmqnode threads (writer and reader)
        # print("node send:", cmd + parm)
        hdr = CspHeader(src_node=int(args.node), dst_node=int(dest), dst_port=int(port), src_port=55)
        node.send_message(cmd + parm, hdr)

    # Exit SUCHAI process
    hdr = CspHeader(src_node=int(args.node), dst_node=int(dest), dst_port=int(port), src_port=55)
    node.send_message("obc_reset", hdr)

    # Get SUCHAI process return code
    return_code = process.wait()
    print("Return code: ", return_code)

    # Get results
    cmds, results = node.filter_cmd_result_list()  # Filter sent commands and obc_reset command
    results.append(return_code)
    write_to_file(cmds, results)
    print(selected_cmd_list)
    print(selected_parm_list)
    node.stop()
