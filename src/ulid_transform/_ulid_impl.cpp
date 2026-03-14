#include "Python.h"
#include "ulid_wrapper.h"

/* ulid_hex() -> str */
static PyObject*
py_ulid_hex(PyObject* module, PyObject* Py_UNUSED(ignored))
{
    uint8_t buf[16];
    char hex[32];
    _cpp_ulid_bytes(buf);
    _cpp_hexlify_16(buf, hex);
    return PyUnicode_DecodeASCII(hex, 32, NULL);
}

/* ulid_now_bytes() -> bytes */
static PyObject*
py_ulid_now_bytes(PyObject* module, PyObject* Py_UNUSED(ignored))
{
    uint8_t buf[16];
    _cpp_ulid_bytes(buf);
    return PyBytes_FromStringAndSize((const char*)buf, 16);
}

/* ulid_at_time_bytes(timestamp) -> bytes */
static PyObject*
py_ulid_at_time_bytes(PyObject* module, PyObject* arg)
{
    double ts = PyFloat_AsDouble(arg);
    if (ts == -1.0 && PyErr_Occurred())
        return NULL;
    uint8_t buf[16];
    _cpp_ulid_at_time_bytes(ts, buf);
    return PyBytes_FromStringAndSize((const char*)buf, 16);
}

/* ulid_now() -> str */
static PyObject*
py_ulid_now(PyObject* module, PyObject* Py_UNUSED(ignored))
{
    char buf[26];
    _cpp_ulid(buf);
    return PyUnicode_DecodeASCII(buf, 26, NULL);
}

/* ulid_at_time(timestamp) -> str */
static PyObject*
py_ulid_at_time(PyObject* module, PyObject* arg)
{
    double ts = PyFloat_AsDouble(arg);
    if (ts == -1.0 && PyErr_Occurred())
        return NULL;
    char buf[26];
    _cpp_ulid_at_time(ts, buf);
    return PyUnicode_DecodeASCII(buf, 26, NULL);
}

/* ulid_to_bytes(value) -> bytes */
static PyObject*
py_ulid_to_bytes(PyObject* module, PyObject* arg)
{
    if (!PyUnicode_Check(arg)) {
        PyErr_Format(PyExc_TypeError,
            "ULID must be a string, not %.200s",
            Py_TYPE(arg)->tp_name);
        return NULL;
    }
    Py_ssize_t len;
    const char* str = PyUnicode_AsUTF8AndSize(arg, &len);
    if (!str)
        return NULL;
    if (len != 26) {
        PyErr_Format(PyExc_ValueError,
            "ULID must be a 26 character string: %R", arg);
        return NULL;
    }
    uint8_t buf[16];
    _cpp_ulid_to_bytes(str, buf);
    return PyBytes_FromStringAndSize((const char*)buf, 16);
}

/* bytes_to_ulid(value) -> str */
static PyObject*
py_bytes_to_ulid(PyObject* module, PyObject* arg)
{
    if (!PyBytes_Check(arg)) {
        PyErr_Format(PyExc_TypeError,
            "ULID bytes must be bytes, not %.200s",
            Py_TYPE(arg)->tp_name);
        return NULL;
    }
    if (PyBytes_GET_SIZE(arg) != 16) {
        PyErr_Format(PyExc_ValueError,
            "ULID bytes must be 16 bytes: %R", arg);
        return NULL;
    }
    char buf[26];
    _cpp_bytes_to_ulid((const uint8_t*)PyBytes_AS_STRING(arg), buf);
    return PyUnicode_DecodeASCII(buf, 26, NULL);
}

/* ulid_to_bytes_or_none(ulid) -> bytes | None */
static PyObject*
py_ulid_to_bytes_or_none(PyObject* module, PyObject* arg)
{
    if (arg == Py_None || !PyUnicode_Check(arg))
        Py_RETURN_NONE;
    Py_ssize_t len;
    const char* str = PyUnicode_AsUTF8AndSize(arg, &len);
    if (!str)
        return NULL;
    if (len != 26)
        Py_RETURN_NONE;
    uint8_t buf[16];
    _cpp_ulid_to_bytes(str, buf);
    return PyBytes_FromStringAndSize((const char*)buf, 16);
}

/* bytes_to_ulid_or_none(ulid_bytes) -> str | None */
static PyObject*
py_bytes_to_ulid_or_none(PyObject* module, PyObject* arg)
{
    if (arg == Py_None || !PyBytes_Check(arg) || PyBytes_GET_SIZE(arg) != 16)
        Py_RETURN_NONE;
    char buf[26];
    _cpp_bytes_to_ulid((const uint8_t*)PyBytes_AS_STRING(arg), buf);
    return PyUnicode_DecodeASCII(buf, 26, NULL);
}

/* ulid_to_timestamp(ulid) -> int */
static PyObject*
py_ulid_to_timestamp(PyObject* module, PyObject* arg)
{
    if (PyBytes_Check(arg)) {
        if (PyBytes_GET_SIZE(arg) != 16) {
            PyErr_Format(PyExc_ValueError,
                "ULID bytes must be 16 bytes: %R", arg);
            return NULL;
        }
        uint64_t ts = _cpp_bytes_to_timestamp(
            (const uint8_t*)PyBytes_AS_STRING(arg));
        return PyLong_FromUnsignedLongLong(ts);
    }
    if (!PyUnicode_Check(arg)) {
        PyErr_Format(PyExc_TypeError,
            "ULID must be a string or bytes, not %.200s",
            Py_TYPE(arg)->tp_name);
        return NULL;
    }
    Py_ssize_t len;
    const char* str = PyUnicode_AsUTF8AndSize(arg, &len);
    if (!str)
        return NULL;
    if (len != 26) {
        PyErr_Format(PyExc_ValueError,
            "ULID must be a 26 character string: %R", arg);
        return NULL;
    }
    uint8_t buf[16];
    _cpp_ulid_to_bytes(str, buf);
    uint64_t ts = _cpp_bytes_to_timestamp(buf);
    return PyLong_FromUnsignedLongLong(ts);
}

static PyMethodDef module_methods[] = {
    { "ulid_hex", py_ulid_hex, METH_NOARGS,
        "ulid_hex()\n--\n\n"
        "Generate a ULID in lowercase hex that will work for a UUID.\n\n"
        "This ulid should not be used for cryptographically secure\n"
        "operations.\n\n"
        "This string can be converted with https://github.com/ahawker/ulid\n\n"
        "ulid.from_uuid(uuid.UUID(ulid_hex))" },
    { "ulid_now_bytes", py_ulid_now_bytes, METH_NOARGS,
        "ulid_now_bytes()\n--\n\n"
        "Generate an ULID as 16 bytes that will work for a UUID." },
    { "ulid_at_time_bytes", py_ulid_at_time_bytes, METH_O,
        "ulid_at_time_bytes($self, timestamp, /)\n--\n\n"
        "Generate an ULID as 16 bytes that will work for a UUID.\n\n"
        "uuid.UUID(bytes=ulid_bytes)" },
    { "ulid_now", py_ulid_now, METH_NOARGS,
        "ulid_now()\n--\n\n"
        "Generate a ULID." },
    { "ulid_at_time", py_ulid_at_time, METH_O,
        "ulid_at_time($self, timestamp, /)\n--\n\n"
        "Generate a ULID.\n\n"
        "This ulid should not be used for cryptographically secure\n"
        "operations.\n\n"
        " 01AN4Z07BY      79KA1307SR9X4MV3\n"
        "|----------|    |----------------|\n"
        " Timestamp          Randomness\n"
        "   48bits             80bits\n\n"
        "This string can be loaded directly with https://github.com/ahawker/ulid\n\n"
        "import ulid_transform as ulid_util\n"
        "import ulid\n"
        "ulid.parse(ulid_util.ulid())" },
    { "ulid_to_bytes", py_ulid_to_bytes, METH_O,
        "ulid_to_bytes($self, value, /)\n--\n\n"
        "Decode a ulid to bytes." },
    { "bytes_to_ulid", py_bytes_to_ulid, METH_O,
        "bytes_to_ulid($self, value, /)\n--\n\n"
        "Encode bytes to a ulid." },
    { "ulid_to_bytes_or_none", py_ulid_to_bytes_or_none, METH_O,
        "ulid_to_bytes_or_none($self, ulid, /)\n--\n\n"
        "Convert an ulid to bytes." },
    { "bytes_to_ulid_or_none", py_bytes_to_ulid_or_none, METH_O,
        "bytes_to_ulid_or_none($self, ulid_bytes, /)\n--\n\n"
        "Convert bytes to a ulid." },
    { "ulid_to_timestamp", py_ulid_to_timestamp, METH_O,
        "ulid_to_timestamp($self, ulid, /)\n--\n\n"
        "Get the timestamp from a ULID.\n"
        "The returned value is in milliseconds since the UNIX epoch." },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "ulid_transform._ulid_impl",
    NULL,
    -1,
    module_methods,
};

PyMODINIT_FUNC
PyInit__ulid_impl(void)
{
    return PyModule_Create(&moduledef);
}
