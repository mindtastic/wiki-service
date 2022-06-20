from typing import Dict, List
from .wikiEntry import MAX_LENGTH_OF_TITLE
from pymongo import CursorType
import re

# currently 57 (see validator in wikiEntry.py)
LEN_OF_SEARCH_SECTION = MAX_LENGTH_OF_TITLE + 7


def createTitleToIdDict(entries: CursorType) -> Dict:
    titleToID = {}
    for article in entries:
        titleToID[article.get("title")] = str(article.get("_id"))
    return titleToID


def checkIfLinksHaveToBeAdded(paragraph: Dict) -> List:
    contentString = paragraph.get("text")
    searchString = "siehe "
    indexesOfOccurences = [m.start() for m in re.finditer(searchString, contentString)]
    return indexesOfOccurences


def addLinks(paragraph: Dict, indexesOfOccurences: List, titleToID: Dict) -> Dict:
    updatedParagraph = {}
    contentString = paragraph.get("text")
    # stores the point, until the original text has already been stored again
    progressStoredTextIndex = 0

    for i, indexOfOccurence in enumerate(indexesOfOccurences):

        # reference is in the middle of the content
        if len(contentString) > indexOfOccurence + LEN_OF_SEARCH_SECTION:
            searchSection = contentString[indexOfOccurence:indexOfOccurence + LEN_OF_SEARCH_SECTION]
        # reference is at the end of the content
        else:
            searchSection = contentString[indexOfOccurence:len(contentString) - 1]

        indexEndOfRefArticle = searchSection.find(")")
        # shortens the searchSection ("siehe ABC-Modell). Man kann sie sich") to "ABC-Modell"
        refArticleName = searchSection[6:indexEndOfRefArticle]
        refArticleID = titleToID.get(refArticleName)
        newTextKey = "text" + str(i)
        updatedParagraph[newTextKey] = contentString[progressStoredTextIndex:indexOfOccurence + 5]

        # set progress to the ")" after the article title
        progressStoredTextIndex = indexOfOccurence + indexEndOfRefArticle

        newLinkKey = "link" + str(i)
        updatedParagraph[newLinkKey] = {
            "refArticleName": refArticleName,
            "refArticleID": refArticleID
        }
        if i == len(indexesOfOccurences) - 1:
            newTextKey = "text" + str(i + 1)
            updatedParagraph[newTextKey] = contentString[progressStoredTextIndex:len(contentString)]

    return updatedParagraph
