import sys
import fitz


def change_pdf_metadata(pdf_path, field, new_value):
    doc = fitz.open(pdf_path)

    # Update metadata
    metadata = doc.metadata
    metadata[field] = new_value

    # Save the modified PDF
    doc.save('output.pdf')
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 pdfmetadata.py <input_pdf> <field> <value>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    metadata_field = sys.argv[2]
    new_value = sys.argv[3]

    change_pdf_metadata(input_pdf, metadata_field, new_value)
    print(f"Metadata field '{metadata_field}' changed to '{new_value}'. Output saved to 'output.pdf'.")
