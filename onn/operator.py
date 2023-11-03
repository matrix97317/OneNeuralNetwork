# -*- coding: utf-8 -*-
"""One Neural Network-Slot."""
import abc


class Operator(abc.ABC):
    """Operator base class."""

    @abc.abstractmethod
    def parse_inputs_data(self, *args, **kwargs):
        """Parse inputs data."""
        raise NotImplementedError

    @abc.abstractmethod
    def parse_outputs_data(self, *args, **kwargs):
        """Parse outputs data."""
        raise NotImplementedError

    @abc.abstractmethod
    def forward(self, *args, **kwargs):
        """Compute data."""
        raise NotImplementedError

    @abc.abstractmethod
    def backward(self, *args, **kwargs):
        """Compute data."""
        raise NotImplementedError
