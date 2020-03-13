use pyo3::prelude::*;
use tantivy as tv;

/// Tantivy schema.
///
/// The schema is very strict. To build the schema the `SchemaBuilder` class is
/// provided.
#[pyclass]
pub(crate) struct Schema {
    pub(crate) inner: tv::schema::Schema,
}

#[pymethods]
impl Schema {

    fn get_field(
        &mut self,
        field_name: &str
    )-> PyResult<Field> {
        let inner = self.inner.get_field(field_name).unwrap();
        Ok(Field { inner })
    }
}


#[pyclass]
pub(crate) struct Field {
    pub(crate) inner: tv::schema::Field,
}

#[pymethods]
impl Field {

    fn field_id(&mut self) -> PyResult<String> {
        let s: String = self.inner.field_id().to_string();

        Ok(s)
    }

}


