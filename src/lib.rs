use pyo3::prelude::*;
mod core;

use crate::core::{loads, DecodeError};

/// A Python module implemented in Rust.
#[pymodule]
fn o3json5(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(loads, m)?)?;
    m.add("DecodeError", py.get_type::<DecodeError>())?;
    Ok(())
}
