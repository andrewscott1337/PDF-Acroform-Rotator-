import argparse
import os
import glob
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NumberObject, NameObject

def orient_fields_from_values(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        if "/Annots" in page:
            for annot_ref in page["/Annots"]:
                annot = annot_ref.get_object()

                if annot.get("/Subtype") == "/Widget":
                    field_value = annot.get("/V")

                    if field_value:
                        val_str = str(field_value).strip()

                        if val_str in ["0", "90", "180", "270"]:
                            rotation_int = int(val_str)

                            if "/MK" not in annot:
                                annot[NameObject("/MK")] = DictionaryObject()

                            mk_dict = annot["/MK"].get_object()
                            mk_dict[NameObject("/R")] = NumberObject(rotation_int)

                            # Clear the field value after rotating so it is ready for production
                            del annot[NameObject("/V")]

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Successfully processed and oriented fields from {input_path} to {output_path}")

def process_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        output_path = os.path.join(output_dir, filename)
        orient_fields_from_values(pdf_file, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamically rotate PDF AcroForms based on inputted degree values.")
    parser.add_argument("--input", help="Path to the input PDF hardware sheet")
    parser.add_argument("--output", help="Path to save the oriented PDF")
    parser.add_argument("--input_dir", help="Path to the directory containing input PDF hardware sheets")
    parser.add_argument("--output_dir", help="Path to the directory to save the oriented PDFs")

    args = parser.parse_args()

    if args.input and args.output:
        orient_fields_from_values(args.input, args.output)
    elif args.input_dir and args.output_dir:
        process_directory(args.input_dir, args.output_dir)
    else:
        parser.error("You must provide either --input and --output, or --input_dir and --output_dir.")
