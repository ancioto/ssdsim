# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the main simulation class.
"""

# IMPORTS
from datetime import datetime
from decimal import Decimal, getcontext
from colorama import init, Fore, Style
from pathlib import Path
from scipy.stats import randint
import numpy as np
from simulator.NAND.common import DECIMAL_PRECISION
from simulator.NAND.common import get_quantized_decimal as qd


# SIMULATION TYPES (THE DISTRIBUTION)
SIM_UNIFORM_RANDOM_PAGE_WRITE = 'SIM_RNDUNIF_PAGE_WRITE'
""" This simulates a random uniform distribution of page writes at the maximum disk capability.
"""

# SIMULATION SAMPLING TYPES
SIM_SAMPLING_HOST_WRITE = 'SIM_SAMPLING_HOSTWRITE'
""" The statistics are collected every self.sim_sampling page write REQUESTED by the host.
    This occurs regardless of the actual disk data being written, so be careful that the time unit of the results
    may be different depending on the disk performances.
"""

SIM_SAMPLING_ELAPSED_TIME = 'SIM_SAMPLING_TIME'
""" The statistics are collected every self.sim_sampling microseconds of the ACTUAL simulation time for the
    specific disk. This occurs regardless of the actual activity of the disk, ie: data may not have the same
    number of samples if a disk stop working (ie: disk full).
"""


# USEFUL CLASS DECORATOR
def check_init(f):
    """
    A wrapper to validate the simulation initialization.
    """
    def wrapper(s, *args):
        if not s.init_ok:
            raise RuntimeError("Simulation not yet initialized")

        # seems fine, let's proceed
        return f(s, *args)
    return wrapper


# SIMULATION CLASS
class Simulation(object):
    """
    This class ...
    """
    # CONSTRUCTOR

    # METHODS
    def __init__(self, simulation_name=None, sample_size=0, sampling=0, sampling_type=SIM_SAMPLING_HOST_WRITE):
        """

        :return:
        """
        # ATTRIBUTES
        # SIMULATION SETTINGS
        self._sim_base_path = None
        """ Full path to base folder where the simulation results are placed.
        """

        self.sim_name = simulation_name
        """ A string used as folder for this simulation
        """

        self.sim_path = None
        """ Actual full path of the current simulation (base + folder name)
        """

        # SIMULATION PARAMETERS
        self.sim_sample_size = sample_size
        """ Size of the sample (rougly the number of disk operations).
        """

        self.sim_sampling = sampling
        """ This parameter specify how often the statistics must be collected.
        """

        self.sim_sampling_type = sampling_type
        """ This parameter specifies the meaning of the self.sim_sampling parameter.
        """

        self.sim_type = SIM_UNIFORM_RANDOM_PAGE_WRITE
        """ The type of the simulation: distribution of the data, type of operation performed by the host.
            Currently fixed to "random uniform page write" as it is the only simulation available.
        """

        # INTERNAL STATES
        self.init_ok = False
        """ To avoid run of a simulation wihtout initialization
        """

        self._disks = dict()
        """ The created disks to be executed
        """

        self._samples = dict()
        """ Randomly generated samples for every disk (as they may have different specs).
        """

        self.stats = dict()
        """ Store the statistics for each disk. Each disk has a dictionary of variables (es: iops, time, page written).
            Then every variable has a numpy array of the extracted data.
            A special 'samples' column stores the number of written data
        """

    def init_simulation(self, base_path=None):
        """

        :return:
        """
        # avoid multiple initialization
        if self.init_ok:
            raise RuntimeError("Simulation already initialized")

        # initialize colorama
        init(autoreset=True)

        # set the decimal precision
        getcontext().prec = DECIMAL_PRECISION

        # the base path is valid?
        self._sim_base_path = Path(base_path)
        print("Checking '{}' ... ".format(self._sim_base_path), end="")

        if not self._sim_base_path.exists():
            print(Fore.RED + 'INVALID')
            raise IOError("The provided base path is not valid")
        print(Fore.GREEN + 'OK')
        print(Style.RESET_ALL, end="")

        # the simulation path is valid or should be created?
        self.sim_path = self._sim_base_path.joinpath(self.sim_name)
        print("Checking '{}' ... ".format(self.sim_path), end="")

        if self.sim_path.exists():
            # ok, already exists
            print(Fore.GREEN + 'OK')
        else:
            # create it
            self.sim_path.mkdir(parents=False)
            print(Fore.YELLOW + 'CREATED')
        print(Style.RESET_ALL, end="")

        # set init ok
        self.init_ok = True

    @check_init
    def add_disk(self, name, disk):
        """

        :return:
        """
        self._disks[name] = disk
        self.stats[name] = {'samples': 1,  # integer (starts from 1 as there is the first empty row)
                            'extra': None,  # for internal use only
                            'time': np.array([0]),  # microseconds
                            'iops': np.array([0]),
                            'datarate': np.array([0]),  # MiB/s
                            'amplification': np.array([0]),
                            'host_write': np.array([0]),  # pages
                            'host_read': np.array([0]),  # pages
                            'disk_write': np.array([0]),  # pages
                            'disk_read': np.array([0]),  # pages
                            'block_erased': np.array([0]),  # blocks
                            'failures': np.array([0])}  # pages

    @check_init
    def output_stats(self):
        """

        :return:
        """
        # every disk has its own stats
        for d in self._disks:
            # create the file path
            fp = self.sim_path.joinpath("raw_data_{}.csv".format(d))

            # disk information
            with fp.open('wt') as f:
                # first line
                f.write("time,iops,datarate,amplification,host_write,host_read,disk_write,disk_read,"
                        "block_erased,failures\n")

                # data
                for i in range(0, self.stats[d]['samples']):
                    # columns
                    for s in ('time', 'iops', 'datarate', 'amplification', 'host_write', 'host_read',
                              'disk_write', 'disk_read', 'block_erased'):
                        f.write("{},".format(self.stats[d][s][i]))

                    # last column
                    f.write('{}\n'.format(self.stats[d]['failures'][i]))

            # status
            print("Updated file '{}'".format(fp))

    @check_init
    def output_disks(self, extra=""):
        """

        :return:
        """
        # create the file path
        fp = self.sim_path.joinpath("disks{}.txt".format(extra))

        # disk information
        with fp.open('wt') as f:
            for d in self._disks:
                f.write("Disk name: {}\n{}\n\n".format(d, self._disks[d]))

        # status
        print("Updated file '{}'".format(fp))

    @check_init
    def execute_one_simulation_step(self, index):
        """

        :return:
        """
        # write of a single page in a block
        for d in self._disks:
            self._disks[d].host_write_page(block=self._samples[d][0][index],
                                           page=self._samples[d][1][index])

    @check_init
    def extract_and_store_stats(self, current_index):
        """

        :return:
        """
        def store_stat_disk(disk):
            # FOR INTERNAL USE ONLY
            stats = self._disks[disk].get_stats()
            self.stats[disk]['samples'] += 1
            self.stats[disk]['time'] = np.append(self.stats[disk]['time'], [stats[0]])
            self.stats[disk]['iops'] = np.append(self.stats[disk]['iops'], [stats[1]])
            self.stats[disk]['datarate'] = np.append(self.stats[disk]['datarate'], [stats[2]])
            self.stats[disk]['amplification'] = np.append(self.stats[disk]['amplification'], [stats[3]])
            self.stats[disk]['host_write'] = np.append(self.stats[disk]['host_write'], [stats[4]])
            self.stats[disk]['host_read'] = np.append(self.stats[disk]['host_read'], [stats[5]])
            self.stats[disk]['disk_write'] = np.append(self.stats[disk]['disk_write'], [stats[6]])
            self.stats[disk]['disk_read'] = np.append(self.stats[disk]['disk_read'], [stats[7]])
            self.stats[disk]['block_erased'] = np.append(self.stats[disk]['block_erased'], [stats[8]])
            self.stats[disk]['failures'] = np.append(self.stats[disk]['failures'], [stats[9]])

        # depending on the sampling type we need to perform different checks
        if self.sim_sampling_type == SIM_SAMPLING_HOST_WRITE:
            # for SIM_SAMPLING_HOST_WRITE is just a matter of current_index
            if current_index >= self.sim_sample_size or \
                    (current_index > 0 and current_index % self.sim_sampling == 0):
                # for every disk read the data and store it in internal array for further SciPy manipulation
                for d in self._disks:
                    store_stat_disk(d)

                return True
        elif self.sim_sampling_type == SIM_SAMPLING_ELAPSED_TIME:
            # for SIM_SAMPLING_ELAPSED_TIME is we need to check every disk to see if the internal
            # simulation time is enough. We use the 'extra' data in stats to remember the last
            # time we gathered the statistics
            for d in self._disks:
                # get the disk's simulation time
                sim_time = self._disks[d].elapsed_time()

                # check
                if (current_index >= self.sim_sample_size and sim_time - self.stats[d]['extra'] > 0)\
                        or sim_time - self.stats[d]['extra'] >= self.sim_sampling:
                    # get the stats
                    store_stat_disk(d)

                    # save the new time
                    self.stats[d]['extra'] = sim_time
            return True

        return False

    @check_init
    def run(self):
        """

        :return:
        """
        # output the disks information
        self.output_disks("_setup")

        # generate the random sample
        print(Fore.CYAN + "\n\nSimulation being executed")
        print(Style.RESET_ALL, end="")
        print("Sample data generation ... ", end="")

        for d in self._disks:
            # as we have only one type of simulation we don't need any fancy code here
            # just plain random data generation.
            # every disk has a tuple where
            #   the first element is the block index samples
            #   the second element is the page index samples
            self._samples[d] = (randint.rvs(0, self._disks[d].total_blocks, size=self.sim_sample_size),
                                randint.rvs(0, self._disks[d].pages_per_block, size=self.sim_sample_size))

            # in case of SIM_SAMPLING_ELAPSED_TIME we need to remember the last time we gathered the stats
            if self.sim_sampling_type == SIM_SAMPLING_ELAPSED_TIME:
                self.stats[d]['extra'] = 0  # initial value is 0

        print(Fore.GREEN + "OK")
        print(Style.RESET_ALL, end="")

        # run the simulation and gather statistics
        quantum_progress = int((1 * self.sim_sample_size) / 100)  # for the progress indicator

        print("RUNNING ... ", end="", flush=True)
        start_time = datetime.now()
        for i in range(0, self.sim_sample_size):
            # progress
            if i % quantum_progress == 0:
                elapsed_time = datetime.now() - start_time
                print('\rRUNNING ... {} % \t Elapsed: {}'.format(qd(Decimal(i * 100 / self.sim_sample_size)),
                                                                 elapsed_time),
                      end="", flush=True)

            # execution
            self.execute_one_simulation_step(i)

            # extract statistics (if needed)
            self.extract_and_store_stats(i)

        # compute the total execution time
        final_elapsed_time = datetime.now() - start_time

        # extract final statistics
        self.extract_and_store_stats(self.sim_sample_size)

        print('\rRUNNING ... ', end="", flush=True)
        print(Fore.GREEN + "DONE", flush=True)
        print(Style.RESET_ALL, end="")

        print('Total simulation time: {}\n\n'.format(final_elapsed_time))

        # output the end disks information
        self.output_disks("_results")

        # output the stats
        self.output_stats()
