# global
import weakref

# local
import ivy
from ivy import with_unsupported_dtypes
import ivy.functional.frontends.tensorflow as tf_frontend
from ivy.functional.frontends.tensorflow.func_wrapper import _to_ivy_array
from ivy.functional.frontends.numpy.creation_routines.from_existing_data import array


class EagerTensor:
    def __init__(self, array):
        self._ivy_array = (
            ivy.array(array) if not isinstance(array, ivy.Array) else array
        )

    def __repr__(self):
        return (
            repr(self.ivy_array).replace(
                "ivy.array", "ivy.frontends.tensorflow.EagerTensor"
            )[:-1]
            + ", shape="
            + str(self.shape)
            + ", dtype="
            + str(self.ivy_array.dtype)
            + ")"
        )

    # Properties #
    # ---------- #

    @property
    def ivy_array(self):
        return self._ivy_array

    @property
    def device(self):
        return self.ivy_array.device

    @property
    def dtype(self):
        return tf_frontend.DType(
            tf_frontend.tensorflow_type_to_enum[self.ivy_array.dtype]
        )

    @property
    def shape(self):
        return tuple(self.ivy_array.shape.shape)

    # Instance Methods #
    # ---------------- #

    def get_shape(self):
        return tf_frontend.raw_ops.Shape(input=self)

    def set_shape(self, shape):
        if shape is None:
            return

        x_shape = self.shape
        if len(x_shape) != len(shape):
            raise ValueError(
                f"Tensor's shape {x_shape} is not compatible with supplied shape "
                f"{shape}."
            )
        for i, v in enumerate(x_shape):
            if v != shape[i] and (shape[i] is not None):
                raise ValueError(
                    f"Tensor's shape {x_shape} is not compatible with supplied shape "
                    f"{shape}."
                )

    def numpy(self):
        return array(self.ivy_array)

    def __add__(self, y, name="add"):
        return self.__radd__(y)

    def __div__(self, y, name="div"):
        if "int" in self._ivy_array.dtype:
            return tf_frontend.raw_ops.FloorDiv(x=self, y=y, name=name)
        ret = tf_frontend.math.divide(self, y, name=name)
        return tf_frontend.cast(ret, self.dtype)

    def __and__(self, y, name="and"):
        return self.__rand__(y)

    def __array__(self, dtype=None, name="array"):
        if not dtype:
            return ivy.to_numpy(self.ivy_array)
        return ivy.to_numpy(self.ivy_array).astype(dtype)

    def __bool__(self, name="bool"):
        temp = ivy.squeeze(self.ivy_array, axis=None)
        if temp.shape != ():
            raise ValueError(
                "The truth value of an array with more than one element is ambiguous. "
                "Use a.any() or a.all()"
            )
        return temp != 0

    def __eq__(self, other):
        return tf_frontend.raw_ops.Equal(
            x=self, y=other, incompatible_shape_error=False
        )

    def __floordiv__(self, y, name="floordiv"):
        return tf_frontend.raw_ops.FloorDiv(x=self, y=y, name=name)

    @with_unsupported_dtypes(
        {"2.14.0 and below": ("complex",)},
        "tensorflow",
    )
    def __ge__(self, y, name="ge"):
        return tf_frontend.raw_ops.GreaterEqual(x=self, y=y, name=name)

    def __getitem__(self, slice_spec, var=None, name="getitem"):
        ivy_args = ivy.nested_map(_to_ivy_array, [self, slice_spec])
        ret = ivy.get_item(*ivy_args)
        return EagerTensor(ret)

    @with_unsupported_dtypes(
        {"2.14.0 and below": ("complex",)},
        "tensorflow",
    )
    def __gt__(self, y, name="gt"):
        return tf_frontend.raw_ops.Greater(x=self, y=y, name=name)

    def __invert__(self, name="invert"):
        return tf_frontend.raw_ops.Invert(x=self, name=name)

    @with_unsupported_dtypes(
        {"2.14.0 and below": ("complex",)},
        "tensorflow",
    )
    def __le__(self, y, name="le"):
        return tf_frontend.raw_ops.LessEqual(x=self, y=y, name=name)

    @with_unsupported_dtypes(
        {"2.14.0 and below": ("complex",)},
        "tensorflow",
    )
    def __lt__(self, y, name="lt"):
        return tf_frontend.raw_ops.Less(x=self, y=y, name=name)

    def __matmul__(self, y, name="matmul"):
        return tf_frontend.linalg.matmul(a=self, b=y, name=name)

    def __mul__(self, y, name="mul"):
        return tf_frontend.math.multiply(self, y, name=name)

    @with_unsupported_dtypes(
        {"2.14.0 and below": ("complex",)},
        "tensorflow",
    )
    def __mod__(self, y, name="mod"):
        return tf_frontend.floormod(self, y, name=name)

    def __ne__(self, other):
        return tf_frontend.raw_ops.NotEqual(
            x=self, y=other, incompatible_shape_error=False
        )

    def __neg__(self, name="neg"):
        return tf_frontend.raw_ops.Neg(x=self, name=name)

    __nonzero__ = __bool__

    def __or__(self, y, name="or"):
        return self.__ror__(y)

    def __pow__(self, y, name="pow"):
        return tf_frontend.math.pow(x=self, y=y, name=name)

    def __radd__(self, x, name="radd"):
        return tf_frontend.math.add(self, x, name=name)

    def __rand__(self, x, name="rand"):
        return tf_frontend.raw_ops.BitwiseAnd(y=self, x=x, name=name)

    def __rfloordiv__(self, x, name="rfloordiv"):
        return tf_frontend.raw_ops.FloorDiv(x=x, y=self, name=name)

    def __rmatmul__(self, x, name="rmatmul"):
        return tf_frontend.linalg.matmul(a=x, b=self, name=name)

    def __rmul__(self, x, name="rmul"):
        return tf_frontend.raw_ops.Mul(x=self, y=x, name=name)

    def __ror__(self, x, name="ror"):
        return tf_frontend.raw_ops.BitwiseOr(x=self, y=x, name=name)

    def __rpow__(self, x, name="rpow"):
        return tf_frontend.math.pow(x=x, y=self, name=name)

    def __rsub__(self, x, name="rsub"):
        return tf_frontend.math.subtract(x, self, name=name)

    def __rtruediv__(self, x, name="rtruediv"):
        return tf_frontend.math.truediv(x, self, name=name)

    def __rxor__(self, x, name="rxor"):
        return tf_frontend.raw_ops.BitwiseXor(x=self, y=x, name=name)

    def __sub__(self, y, name="sub"):
        return tf_frontend.math.subtract(self, y, name=name)

    def __truediv__(self, y, name="truediv"):
        return tf_frontend.math.truediv(self, y, name=name)

    def __len__(self):
        return len(self.ivy_array)

    def __xor__(self, y, name="xor"):
        return self.__rxor__(y)

    def __setitem__(self, key, value):
        raise ivy.utils.exceptions.IvyException(
            "ivy.functional.frontends.tensorflow.EagerTensor object "
            "doesn't support assignment"
        )

    def __iter__(self):
        ndim = len(self.shape)
        if ndim == 0:
            raise TypeError("iteration over a 0-d tensor not supported")
        for i in range(self.shape[0]):
            yield self[i]


class TensorArray:
    def __init__(
        self,
        dtype,
        size=None,
        dynamic_size=None,
        clear_after_read=None,
        tensor_array_name=None,
        handle=None,
        flow=None,
        infer_shape=True,
        element_shape=None,
        colocate_with_first_write_call=True,
        name=None,
    ):
        del (flow, tensor_array_name, name)
        self._handle = None
        self._flow = tf_frontend.constant(0, dtype=tf_frontend.int32)
        self._infer_shape = infer_shape
        self._element_shape = (
            ivy.Shape(element_shape) if element_shape is not None else element_shape
        )
        self._colocate_with_first_write_call = colocate_with_first_write_call
        self._dtype = tf_frontend.as_dtype(dtype)
        self._dynamic_size = dynamic_size or False
        self._clear_after_read = True if clear_after_read is None else clear_after_read
        self._previously_read_indices = []

        if isinstance(size, EagerTensor):
            size = size.ivy_array
        self._tensor_array = [None for _ in range(size)]
        self._parent = weakref.ref(self)

    @property
    def flow(self):
        return self._flow

    @property
    def dtype(self):
        return self._dtype

    @property
    def handle(self):
        return self._handle

    @property
    def element_shape(self):
        return self._element_shape

    def identity(self):
        return self._parent()

    def grad(self, source, flow=None, name=None):
        raise NotImplementedError(
            "TensorArray.grad is not supported when executing eagerly; eager's "
            "gradient implementation does not use/need this function to compute "
            "gradients of operations that use TensorArrays."
        )

    @property
    def dynamic_size(self):
        return self._dynamic_size

    @property
    def infer_shape(self):
        return self._infer_shape

    def read(self, index, name=None):
        if isinstance(index, EagerTensor):
            index = ivy.to_scalar(index.ivy_array)

        if index < 0:
            raise IndexError(f"Reading from negative indices {index} is not allowed.")

        if index >= len(self._tensor_array):
            raise IndexError(
                f"Tried to read from index {index} but array size is:"
                f" {len(self._tensor_array)} "
            )

        tensor = self._tensor_array[index]
        if tensor is None:
            if index in self._previously_read_indices:
                raise ValueError(
                    f"Could not read index {index} twice because it was cleared after a"
                    " previous read (perhaps try setting clear_after_read = false?)"
                )
            else:
                tensor = self._tensor_array[index] = tf_frontend.zeros(
                    shape=self._element_shape, dtype=self._dtype
                )

        if self._clear_after_read:
            self._tensor_array[index] = None
            self._previously_read_indices.append(index)
        return tensor

    def _write(self, index, value, name=None):
        if isinstance(index, EagerTensor):
            index = ivy.to_scalar(index.ivy_array)

        if index < 0:
            raise IndexError(f"Reading from negative indices {index} is not allowed.")

        size = len(self._tensor_array)
        if index >= size:
            if not self._dynamic_size:
                raise IndexError(
                    "Tried to write to index {index} but array is not resizeable and"
                    " size is: {size}"
                )
            self._tensor_array.extend(None for _ in range(index - size + 1))

        if not isinstance(value, EagerTensor):
            value = tf_frontend.cast(value, self.dtype)

        if self._dtype != value.dtype:
            raise ValueError(
                f"TensorArray dtype is {self._dtype} but Op is trying to write dtype"
                f" {value.dtype} "
            )

        if self._infer_shape:
            self._element_shape = self._merge_shape(value)

        self._tensor_array[index] = value

    def _merge_shape(self, value):
        if self._element_shape is None:
            return value.shape
        if len(self._element_shape) != len(value.shape):
            raise ValueError("Shapes not compatible")
        shape = []
        for a, b in zip(self._element_shape, value.shape):
            if a == b or a is None:
                shape.append(b)
            else:
                raise ValueError("Shapes not compatible")
        return tuple(shape)

    def write(self, index, value, name=None):
        self._write(index, value)
        return self._parent()

    def stack(self, name=None):
        if self._tensor_array:
            for ix in range(len(self._tensor_array)):
                if self._tensor_array[ix] is None:
                    self._tensor_array[ix] = tf_frontend.zeros(
                        shape=self._element_shape, dtype=self._dtype
                    )
        if not self._tensor_array and self._element_shape.is_fully_defined():
            return tf_frontend.constant(
                [0] + list(self.element_shape), dtype=self._dtype
            )
        else:
            return tf_frontend.stack(self._tensor_array)

    def _maybe_zero(self, ix):
        val = self._tensor_array[ix]
        if val is None:
            val = self._tensor_array[ix] = tf_frontend.zeros(
                shape=self._element_shape, dtype=self._dtype
            )
        return val

    def gather(self, indices, name=None):
        if isinstance(indices, EagerTensor):
            indices = indices.ivy_array
        return tf_frontend.stack([self._maybe_zero(i) for i in indices])

    def concat(self, name=None):
        return tf_frontend.concat(
            [self._maybe_zero(ix) for ix in range(len(self._tensor_array))],
            0,
            name=name,
        )

    def unstack(self, value, name=None):
        tensors = tf_frontend.unstack(value, name=name)
        if len(tensors) > len(self._tensor_array) and not self._dynamic_size:
            raise ValueError(
                f"Cannot unstack {len(tensors)} tensors into a TensorArray of static"
                f" size {len(self._tensor_array)} "
            )
        self._tensor_array = tensors
        return self._parent()

    def scatter(self, indices, value, name=None):
        if isinstance(indices, EagerTensor):
            indices = indices.ivy_array
        for index, val in zip(indices, tf_frontend.unstack(value)):
            self._write(index, val)
        return self._parent()

    def size(self, name=None):
        return tf_frontend.constant(len(self._tensor_array))

    def close(self, name=None):
        del self._tensor_array[:]

    def split(self, value, lengths, name=None):
        value = tf_frontend.cast(value, self.dtype)
        lengths = (
            tf_frontend.constant(lengths)
            if not isinstance(lengths, EagerTensor)
            else lengths
        )
        self._tensor_array = tf_frontend.split(value, lengths, name=name)
        return self._parent()


# Dummy Tensor class to help with compilation, don't add methods here
class Tensor(EagerTensor):
    pass
