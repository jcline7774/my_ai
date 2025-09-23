import json
import boto3

s3 = boto3.client("s3")
polly = boto3.client("polly")


def lambda_handler(event, context):
    # print(event)
    # print(type(event))
    record = event["Records"][0]

    source_bucket = record["s3"]["bucket"]["name"]
    file_key = record["s3"]["object"]["key"]

    # print(f'source_bucket= {source_bucket}')
    # print(f'file_key = {file_key}')
    response = s3.get_object(Bucket=source_bucket, Key=file_key)
    summary_text = response["Body"].read().decode("utf-8")
    # print(f'summary = {summary_text}')

    polly_response = polly.synthesize_speech(
        Text=summary_text, OutputFormat="mp3", VoiceId="Joanna"
    )

    no_prefix_audio_file_key = file_key.replace("text/", "")
    audio_file_key = no_prefix_audio_file_key.replace(".txt", ".mp3")

    if "AudioStream" in polly_response:
        s3.put_object(
            Bucket=source_bucket,
            Key=f"audio/{audio_file_key}",
            Body=polly_response["AudioStream"].read(),
        )
