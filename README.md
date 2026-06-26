# Adobe AcroForm Rotator

This tool allows you to easily rotate AcroForm fields in your PDF documents.

## How It Works

The logic is simple:
1. Open your PDF and type `0`, `90`, `180`, or `270` directly into the AcroForm fields you want to rotate.
2. The script reads this number, rotates the field counter-clockwise by that many degrees, and clears the text so the field is blank and ready for production use.

## Step-by-Step Usage Instructions

1. Upload your modified PDFs (with the rotation values entered in the fields) to the `PDFs` folder in this repository.
2. Navigate to the GitHub "Actions" tab.
3. Select the "AcroForm Dynamic Rotator Function" workflow and click "Run workflow".
4. Once the job completes, download the resulting rotated PDFs from the artifacts section at the bottom of the workflow summary.
