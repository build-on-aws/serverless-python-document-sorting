# GOALZ

## Background
- Brian has thousands of PDFs
- All scanned and stored in a folder named RAW
- Cannot get rid of the docs
- What are they?
- Considered using human labor to organize them

## Means
- Python as the language
- Serverless on AWS
    - S3 as storage
    - DynamoDB as metadata storage
- AI Services from AWS (Textract)

## Approaches

### Detecting Duplicates
- Textract extract text and compare
- Convert PDF to image and compare images
- Get the total bytes value and compare

## End goal
[x] Check for duplicates
[ ] Tag them based on context
[ ] Ability to search