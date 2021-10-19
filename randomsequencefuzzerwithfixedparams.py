from randomsequencefuzzer import *


class RandomSequenceFuzzerWithFixedParams(RandomSequenceFuzzer):
    def __init__(self, commands_filename, min_length=10, max_length=100,
                 char_start=32, char_range=32, n_cmds=1):
        RandomSequenceFuzzer.__init__(self, commands_filename, min_length, max_length, char_start, char_range, n_cmds)
        self.number_of_params = []
        self.get_parameters_numbers(self.commands_file)

    def get_parameters_numbers(self, commands_list):
        """
        Get list of the number of parameters each command of the SUCHAI flight software receives and set into the
        variable "number_of_params"
        :param commands_list: String. File name of the SUCHAI flight software commands.
        :return:
        """
        parameters_numbers = []
        with open(commands_list) as file_list:
            for row in file_list:
                parameters_numbers.append(int(row.split(', ')[1]))
        self.number_of_params = parameters_numbers

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list
        :param runner: Class. Runner.
        :return: Results obtained from running the program with fuzzed input
        """
        self.fuzz_funcs = [self.fuzz_int, self.fuzz_float, self.fuzz_long, self.fuzz_unsigned_int, self.fuzz_string]
        cmds_to_send = []
        params_to_send = []
        print(self.fs_cmds)
        for i in range(0, self.n_cmds):
            ind_chosen = random.randint(0, len(self.fs_cmds) - 1)
            cmds_to_send.append(self.fs_cmds[ind_chosen])
            n_params = self.number_of_params[ind_chosen]
            fuzz_to_apply = [random.choice(self.fuzz_funcs) for i in range(n_params)]
            params = [fuzz_to_apply[i]() for i in range(n_params)]
            params = " ".join(params)
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)