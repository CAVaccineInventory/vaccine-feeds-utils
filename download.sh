#!/usr/bin/env bash

# exit when a command fails instead of blindly blundering forward
set -e
# treat unset variables as an error and exit immediately
set -u
# don't hide exit codes when pipeline output to another command
set -o pipefail

PUBLIC_TIMESTAMP="2021-08-03T13:16:29"
PRIVATE_TIMESTAMP="2021-08-03T11:04:28"

echo "Clearing existing feed-locations.ndjson and api-locations.geojson"

echo > feed-locations.ndjson
echo > api-locations.geojson

echo "Downloading feed-locations.ndjson"

# Download latest normalized locations in all public feeds
for f in $(gsutil ls "gs://vaccine-feeds/locations/*/*/normalized/${PUBLIC_TIMESTAMP}/*.normalized.ndjson")
do
    echo "Appending locations from $f"
    gsutil cat "$f" >> feed-locations.ndjson
    echo >> feed-locations.ndjson
done

# Download latest normalized locations for vaccinefinder_org
for f in $(gsutil ls "gs://vaccine-feeds-private/us/vaccinefinder_org/normalized/${PRIVATE_TIMESTAMP}/*.normalized.ndjson")
do
    echo "Appending locations from $f"
    gsutil cat "$f" >> feed-locations.ndjson
    echo >> feed-locations.ndjson
done

wc -l feed-locations.ndjson

echo "Downloading api-locations.geojson"

curl "https://api.vaccinatethestates.com/v0/locations.geojson" --output api-locations.geojson

jq ".features | length" api-locations.geojson
