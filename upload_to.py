import boto3, os, json

# Upload to S3
def s3(filename, file, filetype, folder=""):

    # S3 boto class
    s3 = boto3.client('s3')

    # Content type
    content_type = ""
    if filetype == ".png":
        content_type = "image/png"
    elif filetype == ".json":
        content_type = "application/json"

    # Create object name
    file_name = "questfrens/" + folder + filename + filetype

    s3.put_object(
        Body=file,
        Bucket='punkfrens',
        Key=file_name,
        ContentType=content_type
    )

    # S3_BUCKET = os.environ.get('S3_BUCKET')
    # print(S3_BUCKET)
    # print(filename)

    # file_name = request.args.get(filename)
    # file_type = request.args.get(filetype)

    # s3 = boto3.client('s3')

    # presigned_post = s3.generate_presigned_post(
    #     Bucket = S3_BUCKET,
    #     Body = file,
    #     Key = "questfrens/" + file_name,
    #     Fields = {"acl": "public-read", "Content-Type": file_type},
    #     Conditions = [
    #         {"acl": "public-read"},
    #         {"Content-Type": file_type}
    #     ],
    #     ExpiresIn = 3600
    # )

    # return json.dumps({
    #     'data': presigned_post,
    #     'url': 'https://%s.s3.amazonaws.com/questfrens/%s' % (S3_BUCKET, file_name)
    # })

