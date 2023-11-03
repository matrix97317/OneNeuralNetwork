#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests."""
# pylint: disable=no-member,import-error
import torch

import onn


def test_add():
    """Test Add."""
    a_tensor = torch.ones((2, 4), requires_grad=True)
    a_tensor_device = a_tensor.cuda()
    b_tensor = torch.ones((2, 4), requires_grad=True)
    b_tensor_device = b_tensor.cuda()
    b_tensor_v2 = b_tensor_device * 3

    out = onn.Add().apply(a_tensor_device, b_tensor_v2)
    out = torch.sum(out)
    out.backward()

    assert torch.allclose(a_tensor.grad.data, torch.ones((2, 4)))
    assert torch.allclose(b_tensor.grad.data, torch.ones((2, 4)) * 3)


if __name__ == "__main__":
    test_add()
