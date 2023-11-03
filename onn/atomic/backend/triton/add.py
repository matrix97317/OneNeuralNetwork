# -*- coding: utf-8 -*-
"""ONN atomic operator-add."""
import math

import torch
from torch import Tensor
import triton  # pylint: disable=import-error
import triton.language as tl  # pylint: disable=import-error

from onn.slot import TRITON
from onn.operator import Operator


@triton.jit
def add_func(a_ptr, b_ptr, c_ptr, element_size, block_size: tl.constexpr):
    """Triton Func."""
    block_id = tl.program_id(axis=0)
    thread_id = block_id * block_size + tl.arange(0, block_size)
    mask = thread_id < element_size
    a = tl.load(a_ptr + thread_id, mask=mask)
    b = tl.load(b_ptr + thread_id, mask=mask)
    tl.store(c_ptr + thread_id, a + b, mask=mask)


@TRITON.push()
class TritonAdd(Operator):
    """Add Operator."""

    BLOCK_SIZE = 512

    def parse_inputs_data(self, a_tensor: Tensor, b_tensor: Tensor):
        """Parse inputs data."""
        return a_tensor, b_tensor

    def parse_outputs_data(self, out_tensor: Tensor):
        """Parse outputs data."""
        return out_tensor

    def forward(self, a_tensor: Tensor, b_tensor: Tensor):
        """Compute flow."""
        out = torch.zeros_like(  # pylint: disable=no-member
            a_tensor, device=a_tensor.device, dtype=a_tensor.dtype
        )
        gird = (math.ceil(a_tensor.numel() / TritonAdd.BLOCK_SIZE),)
        add_func[gird](a_tensor, b_tensor, out, a_tensor.numel(), TritonAdd.BLOCK_SIZE)
        return out

    def backward(self, input_grad: Tensor):
        """Compute flow."""
        return torch.ones_like(  # pylint: disable=no-member
            input_grad, device=input_grad.device, dtype=input_grad.dtype
        )
