#!/usr/bin/env python

"""
Entry point for running vaccine feed runners
"""
import pathlib
import json

import click


@click.group()
def cli():
    """Run commands"""

@cli.command()
@click.option("--feed-locations", "feed_locations", type=str, default="feed-locations.ndjson")
@click.option("--api-locations", "api_locations", type=str, default="api-locations.geojson")
@click.option("--output-locations", "output_locations", type=str, default="output-locations.geojson")
def filter_api(
    feed_locations: str,
    api_locations: str,
    output_locations: str,
) -> None:
    """Filter API locations to locations that exist in feed locations"""
    feed_locations_path = pathlib.Path(feed_locations)
    api_locations_path = pathlib.Path(api_locations)
    output_locations_path = pathlib.Path(output_locations)

    source_ids = set()
    with feed_locations_path.open() as feed_locations_file:
        for line in feed_locations_file:
            line = line.strip()
            if not line:
                continue

            try:
                feed_location = json.loads(line)
            except json.JSONDecodeError as err:
                print(err, line)
                raise

            source_ids.add(feed_location["id"])

    with api_locations_path.open() as api_locations_file:
        api_locations = json.load(api_locations_file)

    original_num_api_locations = len(api_locations["features"])

    api_locations["features"] = [
        feature for feature in api_locations["features"]
        if set(feature["properties"].get("concordances", [])) & source_ids
    ]

    api_locations_json = json.dumps(api_locations)
    output_locations_path.write_text(api_locations_json)

    print(f"Filtered {original_num_api_locations} to "
          f"{len(api_locations['features'])}")


@cli.command()
def version() -> None:
    """Get the library version."""
    click.echo(click.style("0.1.0", bold=True))


if __name__ == "__main__":
    cli()
