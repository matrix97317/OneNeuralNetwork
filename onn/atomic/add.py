# -*- coding: utf-8 -*-
"""ONN atomic operator-Add."""
import torch

from onn.slot import TRITON


class Add(torch.autograd.Function):  # pylint: disable=abstract-method
    """Add Op."""

    backend = "triton"
    arch = "sm80"
    device = "cuda"
    op = None

    def __init__(self, backend="triton", arch="sm80", device="cuda"):
        """init."""
        super().__init__()
        Add.backend = backend
        Add.arch = arch
        Add.device = device
        Add.op = TRITON.pop("onn.atomic.backend.triton.add.TritonAdd")()

    @staticmethod
    def forward(ctx, a, b):
        """Forward."""
        ctx.op = Add.op
        ctx.save_for_backward(a, b)
        return ctx.op.forward(a, b)

    @staticmethod
    def backward(ctx, grad_output):
        """Backward."""
        (
            _,  # a
            _,  # b
        ) = ctx.saved_tensors
        grad_a = ctx.op.backward(grad_output) * grad_output
        grad_b = ctx.op.backward(grad_output) * grad_output
        return grad_a, grad_b
