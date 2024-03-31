import requests
from scipy.cluster.hierarchy import DisjointSet

URL = "https://artemis.hackillinois.org/challenge"
HEADERS = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImdpdGh1YjkwODg0MjI0IiwiZW1haWwiOm51bGwsInByb3ZpZGVyIjoiZ2l0aHViIiwicm9sZXMiOlsiVVNFUiJdLCJleHAiOjE3MDk2Nzk0NDAuMzI0LCJpYXQiOjE3MDcwODc0NDB9.Drwt8NlE8HczZI_s6XimFDPnQuHhaOs_CUOyXlJziW8",
    "Content-Type": "application/json",
}

j = requests.get(
    URL,
    headers=HEADERS,
).json()

alliances: list[list[str]] = j["alliances"]
wizards: dict[str, int] = j["wizards"]

D = DisjointSet(wizards.keys())
for a, b in alliances:
    D.merge(a, b)

requests.post(
    URL,
    headers=HEADERS,
    json={"max_goodness": max(sum(wizards[w] for w in tribe) for tribe in D.subsets())},
)
