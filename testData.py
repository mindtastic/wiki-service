ARTICLES_VALID = {
        "articles": [
            {
                "title": "Test 1",
                "content": "# This is a test article \n ## I hope you like it!"
            },
            {
                "title": "Test 2",
                "content": "This is also a test article. ## This is a H2 Heading"
            }
        ]
    }

ARTICLES_INVALID_V1 = {
        "articles": [
            {
                "title": "T",
                "content": "This is a test article, but it's title is too short :("
            },
            {
                "title": "Test 2",
                "content":  "# This is also a test article. \n This should work"
            }
        ]
    }

ARTICLES_INVALID_V2 = {
        "articles": [
            {
                "title": "Test 1",
                "content": "This is a test article"
            },
            {
                "title": "Test 2",
                "content": ""
            }
        ]
    }
