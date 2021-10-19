from fuzzingbook.Fuzzer import RandomFuzzer
from flightsoftwarerunner import *
import random

MIN_INT = -2147483648
MAX_INT = 2147483647
MIN_LONG = -9223372036854775808
MAX_LONG = 9223372036854775807
MAX_U_INT = 18446744073709551615
MIN_FLOAT = -3.402823e+38
MAX_FLOAT = 3.402823e+38


class RandomSequenceFuzzer(RandomFuzzer):
    def __init__(self, commands_filename, min_length=10, max_length=100,
                 char_start=33, char_range=93, n_cmds=1):
        RandomFuzzer.__init__(self, min_length, max_length, char_start, char_range)
        self.n_cmds = n_cmds
        self.commands_file = commands_filename
        self.fs_cmds = []
        self.get_commands_names(self.commands_file)
        self.fuzz_funcs = {}

    def get_commands_names(self, commands_list):
        """
        Get command names list and set into the fs_cmds variable.
        :param commands_list: String. File name of the SUCHAI flight software commands.
        :return:
        """
        commands_names = []
        with open(commands_list) as file_list:
            for row in file_list:
                commands_names.append(row.split(', ')[0])
        self.fs_cmds = commands_names

    def fuzz_int(self):
        """
        Produce random integer.
        :return: String. Random integer converted to string.
        """
        # Min. length and max. length are not considered
        return str(random.randint(MIN_INT, MAX_INT))

    def fuzz_long(self):
        """
        Produce random long.
        :return: String. Random long converted to string.
        """
        # Min. length and max. length are not considered
        return str(random.randint(MIN_LONG, MAX_LONG))

    def fuzz_unsigned_int(self):
        """
        Produce random unsigned int.
        :return: String. Random unsigned int converted to string.
        """
        # Min. length and max. length are not considered
        return str(random.randint(0, MAX_U_INT))

    def fuzz_float(self):
        """
        Produce random float.
        :return: String. Random float converted to string.
        """
        # Min. length and max. length are not considered
        return str(random.uniform(MIN_FLOAT, MAX_FLOAT))

    def fuzz_string(self):
        """
        Produce random string between self.min_length and self.max_length size.
        :return: String.
        """
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(self.char_start, self.char_start + self.char_range))
        return out

    def generate_seqs(self, iterations):
        """
        Generate random sequences.
        :param iterations:
        :return: List. List of sequences created (commands and parameters).
        """
        self.fuzz_funcs = [self.fuzz_int, self.fuzz_float, self.fuzz_long, self.fuzz_unsigned_int, self.fuzz_string]
        sequences = []
        for iter in range(iterations):
            seq = []
            for i in range(0, self.n_cmds):
                cmd = random.choice(self.fs_cmds)
                n_params = random.randint(0, 11) # 11 is the max number of params that a cmd has
                fuzz_to_apply = [random.choice(self.fuzz_funcs) for i in range(n_params)]
                params = [fuzz_to_apply[i]() for i in range(n_params)]
                params = " ".join(params)
                seq.append(cmd + " " + params)
            sequences.append(seq)
        return sequences

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list.
        :param runner: Class. Runner.
        :return: Results obtained from running the program with fuzzed input.
        """
        self.fuzz_funcs = [self.fuzz_int, self.fuzz_float, self.fuzz_long, self.fuzz_unsigned_int, self.fuzz_string]
        cmds_to_send = []
        params_to_send = []
        print(self.fs_cmds)
        for i in range(0, self.n_cmds):
            cmds_to_send.append(random.choice(self.fs_cmds))
            n_params = random.randint(0, 11)  # 11 is the max number of params that a cmd has
            fuzz_to_apply = [random.choice(self.fuzz_funcs) for i in range(n_params)]
            params = [fuzz_to_apply[i]() for i in range(n_params)]
            params = " ".join(params)
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)
