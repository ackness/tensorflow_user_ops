import tensorflow as tf
from tensorflow.python.framework import ops
import mask_resize_op

@tf.RegisterShape("PSRoiPool")
def _psroi_pool_shape(op):
  """Shape function for the RoiPool op.

  """
  dims_data = op.inputs[0].get_shape().as_list()
  channels = dims_data[1]

  dims_rois = op.inputs[1].get_shape().as_list()
  num_rois = dims_rois[0]

  output_dim = op.get_attr('output_dim')
  pooled_height = op.get_attr('pooled_height')
  pooled_width = op.get_attr('pooled_width')

  output_shape = tf.TensorShape([num_rois, output_dim, pooled_height, pooled_width])
  return [output_shape, output_shape]

@ops.RegisterGradient("PSRoiPool")
def _psroi_pool_grad(op, grad, _):
  """The gradients for `roi_pool`.
  Args:
    op: The `roi_pool` `Operation` that we are differentiating, which we can use
      to find the inputs and outputs of the original op.
    grad: Gradient with respect to the output of the `roi_pool` op.
  Returns:
    Gradients with respect to the input of `zero_out`.
  """
  #data = op.inputs[0]
  rois = op.inputs[1]
  mapping_channel = op.outputs[1]
  pooled_height = op.get_attr('pooled_height')
  pooled_width = op.get_attr('pooled_width')
  output_dim = op.get_attr('output_dim')
  spatial_scale = op.get_attr('spatial_scale')

  # compute gradient
  #data_grad = psroi_pooling_op.psroi_pool_grad(data, rois, argmax, grad, pooled_height, pooled_width, spatial_scale)
  data_grad = psroi_pooling_op.psroi_pool_grad(grad, mapping_channel, pooled_height, pooled_width, output_dim, spatial_scale)  

  return [data_grad, None]  # List of one Tensor, since we have one input
