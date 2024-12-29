use pyo3::prelude::*;
use pyo3::types::{PyByteArray, PyBytes, PyDict, PyList, PyMemoryView, PyString};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use thiserror::Error;

use pyo3::create_exception;

create_exception!(o3json5, DecodeError, pyo3::exceptions::PyValueError);

#[derive(Serialize, Deserialize, PartialEq, Debug)]
#[serde(untagged)]
pub enum Val {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<Val>),
    Object(HashMap<String, Val>),
}

#[derive(Error, Debug)]
pub enum JsonError {
    #[error("Invalid type: expected {expected}, got {got}")]
    TypeError { expected: String, got: String },

    #[error("Failed to parse JSON5: {msg}")]
    ParsingError {
        msg: String,
        location: Option<(usize, usize)>,
    },
}

impl From<PyErr> for JsonError {
    fn from(err: PyErr) -> Self {
        JsonError::ParsingError {
            msg: err.to_string(),
            location: None,
        }
    }
}

impl From<JsonError> for PyErr {
    fn from(err: JsonError) -> Self {
        match err {
            JsonError::TypeError { expected, got } => pyo3::exceptions::PyTypeError::new_err(
                format!("expected {}, got {}", expected, got),
            ),
            JsonError::ParsingError { msg, location } => {
                let error_msg = match location {
                    Some((line, col)) => format!("{} at line {}, column {}", msg, line, col),
                    None => format!("{} at unknown location", msg),
                };
                DecodeError::new_err(error_msg)
            }
        }
    }
}

/// Converts our Val enum into a Python object
pub fn val_to_python<'py>(py: Python<'py>, value: &Val) -> Result<Bound<'py, PyAny>, JsonError> {
    let obj: PyObject = match value {
        Val::Null => py.None().into(),
        Val::Bool(b) => b.into_py(py),
        Val::Number(n) => {
            // Convert to integer if the number is integral
            if n.fract() == 0.0 && n.is_finite() {
                if *n >= (i64::MIN as f64) && *n <= (i64::MAX as f64) {
                    (*n as i64).to_object(py)
                } else {
                    n.to_object(py)
                }
            } else {
                n.to_object(py)
            }
        }
        Val::String(s) => s.into_py(py),
        Val::Array(arr) => {
            let list = PyList::empty(py);
            for item in arr {
                let item_obj = val_to_python(py, item)?;
                list.append(item_obj.as_ref())?;
            }
            list.into()
        }
        Val::Object(map) => {
            let dict = PyDict::new(py);
            for (key, value) in map {
                let value_obj = val_to_python(py, value)?;
                dict.set_item(key, value_obj.as_ref())?;
            }
            dict.into()
        }
    };
    Ok(obj.extract(py)?)
}

pub fn loads_str<'py>(
    py: Python<'py>,
    obj: &Bound<'py, PyString>,
) -> Result<Bound<'py, PyAny>, JsonError> {
    let input_str = obj.to_string();
    let value = py
        .allow_threads(|| json5::from_str::<Val>(&input_str))
        .map_err(|e| match e {
            json5::Error::Message { msg, location } => JsonError::ParsingError {
                msg,
                location: location.map(|loc| (loc.line, loc.column)),
            },
        })?;

    val_to_python(py, &value)
}

pub fn loads_bytes<'py>(
    py: Python<'py>,
    obj: &Bound<'py, PyBytes>,
) -> Result<Bound<'py, PyAny>, JsonError> {
    let str_slice = std::str::from_utf8(obj.as_bytes()).map_err(|_| JsonError::TypeError {
        expected: "valid UTF-8 bytes".to_string(),
        got: "invalid UTF-8 bytes".to_string(),
    })?;

    let value = py
        .allow_threads(|| json5::from_str::<Val>(str_slice))
        .map_err(|e| match e {
            json5::Error::Message { msg, location } => JsonError::ParsingError {
                msg,
                location: location.map(|loc| (loc.line, loc.column)),
            },
        })?;

    val_to_python(py, &value)
}

#[pyfunction]
pub fn loads<'py>(
    py: Python<'py>,
    obj: &Bound<'py, PyAny>,
) -> Result<Bound<'py, PyAny>, JsonError> {
    // Try zero-copy paths first
    if let Ok(s) = obj.downcast::<PyString>() {
        return loads_str(py, s);
    }
    if let Ok(b) = obj.downcast::<PyBytes>() {
        return loads_bytes(py, b);
    }

    // Handle other bytes-like objects
    let value = if let Ok(bytearray) = obj.downcast::<PyByteArray>() {
        // SAFETY: We hold the GIL and have a valid PyByteArray reference
        let str_slice = std::str::from_utf8(unsafe { bytearray.as_bytes() }).map_err(|_| {
            JsonError::TypeError {
                expected: "valid UTF-8 bytes".to_string(),
                got: "invalid UTF-8 bytes".to_string(),
            }
        })?;

        py.allow_threads(|| json5::from_str::<Val>(str_slice))
    } else {
        let input_str = obj.extract::<String>().map_err(|_| JsonError::TypeError {
            expected: "string or bytes-like object".to_string(),
            got: obj
                .get_type()
                .name()
                .map(|s| s.to_string())
                .unwrap_or("unknown".to_string()),
        })?;

        py.allow_threads(|| json5::from_str::<Val>(&input_str))
    }
    .map_err(|e| match e {
        json5::Error::Message { msg, location } => JsonError::ParsingError {
            msg,
            location: location.map(|loc| (loc.line, loc.column)),
        },
    })?;

    val_to_python(py, &value)
}
