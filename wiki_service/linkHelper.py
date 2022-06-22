from typing import Dict, List, Tuple
from .wikiEntry import MAX_LENGTH_OF_TITLE
from pymongo import CursorType
import re


def createTitleToIdDict(entries: CursorType) -> Dict:
    titleToID = {}
    for article in entries:
        titleToID[article.get("title")] = str(article.get("_id"))
    return titleToID


def searchContentForLinks(content: str) -> List[Tuple]:
    """
    :param content of a wiki article (str containing markdown)
    :return: a list with tuples;
            each tuple contains the start index and the end index
            of the name of a referenced article in the content
    """
    searchString = "siehe "
    # +6 because "siehe " has 6 characters
    startIndexes = [m.start() + 6 for m in re.finditer(searchString, content)]
    indexesOfReferences = []
    for startIndex in startIndexes:
        # reference is in the beginning/middle of the content
        if len(content) > startIndex + MAX_LENGTH_OF_TITLE:
            searchSection = content[startIndex:startIndex + MAX_LENGTH_OF_TITLE]
        # reference is at the end of the content
        else:
            searchSection = content[startIndex:len(content)]

        refArticleLength = searchSection.find(")")
        endIndex = startIndex + refArticleLength
        indexesOfReferences.append(tuple((startIndex, endIndex)))
    return indexesOfReferences


def addLinks(content: str, indexesOfReferences: List[Tuple], titleToID: Dict) -> str:

    for indexOfReference in indexesOfReferences:
        startIndex, endIndex = indexOfReference

        # assemble link
        refArticleName = content[startIndex:endIndex]
        refArticleID = titleToID.get(refArticleName)
        markDownLink = "[{}] (kopfsachen:wiki/{})".format(refArticleName, refArticleID)

        # replace article title with link
        content = content[:startIndex] + markDownLink + content[endIndex:]

    return content
