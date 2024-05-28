import logging
import numpy as np
import math
from utils.misc_utils import get_valid_data


class ValidRangesChecker:
    """
    Check that data values are in a given range 
    """

    def __init__(self, dschecker):

        # Read only attributes
        self.file = dschecker.file
        self.data_source = dschecker.data_source
        self.directory = dschecker.directory
        self.ds = dschecker.ds
        self.variable = dschecker.variable
        self.variable_list = dschecker.variable_list 
        self.boundaries = dschecker.boundaries
        self.variable = dschecker.variable
        self.reference_file = dschecker.reference_file

        self.results = {}

    def check_allowed_values(self, min_value, max_value, var):
       
        logging.debug(
            f'Found variable {var} '
        )

        data_array = self.ds[var]
        self.results['boundaries_min'] = 0
        self.results['boundaries_max'] = 0

        if min_value is not None: 
            min_value = round(min_value,7)
        if max_value is not None:
            max_value = round(max_value,7)
        
        if 'time' in list(data_array.dims): 
            for _, timestep in data_array.groupby('time'):
                data = timestep.values
               
                data_min = np.nanmin(data)
                data_max = np.nanmax(data)
                if min_value is not None:
                    if (data_min < min_value) and (not np.isclose(data_min, min_value, rtol = 0.0001)):
                        self.results['boundaries_min'] = -1

                if max_value is not None:
                    if (data_max > max_value) and (not np.isclose(data_min, min_value, rtol = 0.0001)):
                        self.results['boundaries_max'] = 1
                        
        else:
            data = data_array.values
            data_min = np.nanmin(data)
            data_max = np.nanmax(data)

            if min_value is not None:
                if (data_min < min_value) and (not np.isclose(data_min, min_value, rtol = 0.0001)):
                    self.results['boundaries_min'] = -1
                    
            if max_value is not None:
                if (data_max > max_value) and (not np.isclose(data_min, min_value, rtol = 0.0001)):
                    self.results['boundaries_max'] = 1
                    
        if (self.results['boundaries_max'] == 1):
            logging.error(
                f'Invalid values of {var} '
                f'in file {self.file.name}: data_max = {data_max} > required max = {max_value}'
                f'diff = {data_max-max_value} '
                )
        if (self.results['boundaries_min'] == -1):
            logging.error(
                f'Invalid values of {var} '
                f'in file {self.file.name}: data_min = {data_min} < required min = {min_value}'
                )
        if (self.results['boundaries_max'] == 0 and self.results['boundaries_min'] == 0):
            logging.info(
                f'Correct values of {var}'
                )
            

    def run_checker(self):
        """
        Run valid ranges check
        """
       
        if self.boundaries is None:
            self.results['boundaries_max'] = 2
            self.results['boundaries_min'] = -2
            logging.debug(
                f'No boundaries to check for variable {self.variable}'
            )

        else:

            for var in self.variable_list:
                if var in self.boundaries:
                    min_allowed, max_allowed = self.boundaries[var]
                    self.check_allowed_values(min_allowed, max_allowed, var)
                else:
                    logging.warning(
                    f'No valid ranges information for variable {var}'
                )

    