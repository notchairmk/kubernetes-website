#!/usr/bin/env python

import os
import json

import click
import requests
from jinja2 import Template

QUERY_BY_LABEL = """
query Test($labels: [String!]){
  repository(name: "website", owner: "kubernetes") {
    pullRequests(states:MERGED, last: 10, labels: $labels) {
      edges {
        node {
          labels(first: 10) {
            edges {
              node {
                name
              }
            }
          }
          reviews(first: 10) {
            edges {
              node {
                id
              }
            }
          }
          merged
        }
      }
    }
  }
}
"""

QUERY_BY_LABEL_VARS = """
{
  "labels": [
    "sig/auth",
    "sig/autoscaling",
    "sig/cli",
    "sig/cloud-provider",
    "sig/cluster-lifecycle",
    "sig/contributor-experience",
    "sig/multicluster",
    "sig/network",
    "sig/node",
    "sig/release",
    "sig/scalability",
    "sig/scheduling",
    "sig/security",
    "sig/service-catalog",
    "sig/storage",
    "sig/testing",
    "sig/ui",
    "sig/usability",
    "sig/windows"
  ]
}
"""

QUERY_BY_FILE = """
query Test{
  repository(name: "website", owner: "kubernetes") {
    object(expression: "HEAD:") {
      ... on Tree {
        entries {
          name
          type
          mode
          object {
            ... on Blob {
              byteSize
              # text
              isBinary
            }
          }
        }
      }
    }
  }
}
"""


@click.command()
@click.option("--token",
              help="GitHub API token. (Default env variable GITHUB_TOKEN)",
              default=os.environ.get("GITHUB_TOKEN", ""))
def main(token: string):
    """
    Find GitHub pull requests touch a given file.

    ex:
    ./last_review.py
    """

    if not token:
        print("GitHub token not provided (required)")
        exit(1)

    query = Template("""

    """).render()

    variables = """

    """

    print(query)

    try:
        r = requests.post("https://api.github.com/graphql",
                          json={"query": query, "variables": variables},
                          headers={
                              "Authorization": "Bearer %s" % token,
                              "Accept": "application/vnd.github.ocelot-preview+json",
                              "Accept-Encoding": "gzip"
                          })
        r.raise_for_status()

        reply = r.json()
        # prs = reply['data']['repository']['pullRequests']['edges']

        print(reply)

    except requests.exceptions.HTTPError as err:
        gh_err_response = json.loads(err.response.text)
        print("HTTP Error: %d %s" % (err.response.status_code, gh_err_response['message']))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting: %s" % err)
    except requests.exceptions.Timeout as err:
        print("Timeout Error: %s" % err)
    except requests.exceptions.RequestException as err:
        print("Oops, another error occurred: %s" % err)

if __name__ == '__main__':
    main()