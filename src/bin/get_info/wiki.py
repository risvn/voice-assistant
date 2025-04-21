import wikipedia
import sys


def get_summary(qurey):
    summary = wikipedia.summary(qurey, sentences=12)
    return summary

print(get_summary(sys.argv[1]))

