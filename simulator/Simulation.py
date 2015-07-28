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
    def __init__(self, simulation_name=None):
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

        # INTERNAL STATES
        self.init_ok = False
        """ To avoid run of a simulation wihtout initialization
        """

        self._disks = dict()
        """ The created disks to be executed
        """

        self._stats = dict()
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
        self._stats[name] = {'samples': 1,  # integer (starts from 1 as there is the first empty row)
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
            fp = self.sim_path.joinpath("stats_{}.csv".format(d))

            # disk information
            with fp.open('wt') as f:
                # first line
                f.write("time,iops,datarate,amplification,host_write,host_read,disk_write,disk_read,block_erased,"
                        "failures\n")

                # data
                for i in range(0, self._stats[d]['samples']):
                    # columns
                    for s in ('time', 'iops', 'datarate', 'amplification', 'host_write', 'host_read', 'disk_write',
                              'disk_read', 'failures'):
                        f.write("{},".format(self._stats[d][s][i]))

                    # last column
                    f.write('{}\n'.format(self._stats[d]['failures'][i]))

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
    def execute_one_simulation_step(self, step_sample):
        """

        :return:
        """
        # write of a single page in a block
        for d in self._disks:
            self._disks[d].host_write_page(block=step_sample[0], page=step_sample[1])

    @check_init
    def extract_and_store_stats(self):
        """

        :return:
        """
        # for every disk read the data and store it in internal array for further SciPy manipulation
        for d in self._disks:
            stats = self._disks[d].get_stats()
            self._stats[d]['samples'] += 1
            self._stats[d]['time'] = np.append(self._stats[d]['time'], [stats[0]])
            self._stats[d]['iops'] = np.append(self._stats[d]['iops'], [stats[1]])
            self._stats[d]['datarate'] = np.append(self._stats[d]['datarate'], [stats[2]])
            self._stats[d]['amplification'] = np.append(self._stats[d]['amplification'], [stats[3]])
            self._stats[d]['host_write'] = np.append(self._stats[d]['host_write'], [stats[4]])
            self._stats[d]['host_read'] = np.append(self._stats[d]['host_read'], [stats[5]])
            self._stats[d]['disk_write'] = np.append(self._stats[d]['disk_write'], [stats[6]])
            self._stats[d]['disk_read'] = np.append(self._stats[d]['disk_read'], [stats[7]])
            self._stats[d]['block_erased'] = np.append(self._stats[d]['block_erased'], [stats[8]])
            self._stats[d]['failures'] = np.append(self._stats[d]['failures'], [stats[9]])

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

        sample_size = 1000
        sampling_data = 100
        blocks = randint.rvs(0, 256, size=sample_size)
        pages = randint.rvs(0, 64, size=sample_size)

        print(Fore.GREEN + "OK")
        print(Style.RESET_ALL, end="")

        # run the simulation and gather statistics
        quantum_progress = int((5 * sample_size) / 100)  # for the progress indicator

        print("RUNNING ... ", end="", flush=True)
        start_time = datetime.now()
        for i in range(0, sample_size):
            # progress
            if i % quantum_progress == 0:
                elapsed_time = datetime.now() - start_time
                print('\rRUNNING ... {} % \t Elapsed: {}'.format(qd(Decimal(i * 100 / sample_size)),
                                                                 elapsed_time),
                      end="", flush=True)

            # execution
            self.execute_one_simulation_step((blocks[i], pages[i]))

            # extract statistics
            if i > 0 and i % sampling_data == 0:
                self.extract_and_store_stats()

        # compute the total execution time
        final_elapsed_time = datetime.now() - start_time

        # extract final statistics
        self.extract_and_store_stats()

        print('\rRUNNING ... ', end="", flush=True)
        print(Fore.GREEN + "DONE", flush=True)
        print(Style.RESET_ALL, end="")

        print('Total simulation time: {}\n\n'.format(final_elapsed_time))

        # output the end disks information
        self.output_disks("_results")

        # output the stats
        self.output_stats()
