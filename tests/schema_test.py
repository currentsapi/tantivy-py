import tantivy
import pytest
from datetime import datetime
from tantivy import Document, Index, SchemaBuilder, Schema, DocAddress


def schema():
    schema_builder = SchemaBuilder()
    schema_builder.add_text_field("title", stored=True)
    schema_builder.add_text_field("body")
    schema = schema_builder.build()

    field = schema.get_field('title')
    print(field.field_id())
    field = schema.get_field('body')
    print(field.field_id())
    # field = schema.get_field('timestamp')
    # print(field.field_id())

    return schema



def create_index(dir=None):
    # assume all tests will use the same documents for now
    # other methods may set up function-local indexes
    schema_ = schema()
    index = Index(schema_, dir)
    writer = index.writer()

    # 2 ways of adding documents
    # 1
    doc = Document()
    # create a document instance
    # add field-value pairs
    doc.add_text("title", "The Old Man and the Sea")
    doc.add_text(
        "body",
        (
            "He was an old man who fished alone in a skiff in"
            "the Gulf Stream and he had gone eighty-four days "
            "now without taking a fish."
        ),
    )
    # print( int( datetime.timestamp(datetime.utcnow())) % 2**64 )
    # doc.add_integer("timestamp", int(int( datetime.timestamp(datetime.utcnow())) % 2**64 ))
    writer.add_document(doc)

    # 2 use the built-in json support
    # keys need to coincide with field names
    doc = Document.from_dict(
        {
            "title": "Of Mice and Men",
            "body": (
                "A few miles south of Soledad, the Salinas River drops "
                "in close to the hillside bank and runs deep and "
                "green. The water is warm too, for it has slipped "
                "twinkling over the yellow sands in the sunlight "
                "before reaching the narrow pool. On one side of the "
                "river the golden foothill slopes curve up to the "
                "strong and rocky Gabilan Mountains, but on the valley "
                "side the water is lined with trees—willows fresh and "
                "green with every spring, carrying in their lower leaf "
                "junctures the debris of the winter’s flooding; and "
                "sycamores with mottled, white, recumbent limbs and "
                "branches that arch over the pool"
            ),
        }
    )
    writer.add_document(doc)
    doc = Document.from_dict(
        {
            "title": ["Frankenstein", "The Modern Prometheus"],
            "body": (
                "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings.  I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking. "
            ),
        }
    )
    writer.add_document(doc)
    writer.commit()

    index.reload()
    return index, schema_


def test_new_doc():
    doc = DocAddress(32, 65)

    print(doc)

if __name__ == "__main__":
    index,schema_ = create_index()
    query = index.parse_query("sea whale", ["title", "body"])
    # timestamp_field = schema_.get_field("timestamp")
    # print(timestamp_field.field_id())

    result = index.searcher().search(query, 10)
    print(result.hits)
    # test_new_doc()
    doc = DocAddress(result.hits[0][1].segment_ord, result.hits[0][1].doc)
    print( index.searcher().doc(doc)['title'] )