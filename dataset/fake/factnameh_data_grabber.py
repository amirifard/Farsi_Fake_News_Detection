import requests

def fetch_factcheck_data(variables):
    endpoint = "https://factnameh.com/graphql/"
    
    # Define the GraphQL query
    query = """
    query getFactcheckArticlePreviews(
  $claimPersonalityId: ID
  $dateGte: Date
  $first: Int!
  $localeCode: String!
  $offset: Int
  $orderBy: [String]
  $pks: [String]
  $ratingIsNull: Boolean
  $ratingSlug: String
  $tagSlugs: [String]
) {
  factcheckArticles(
    claim_Personality_Id_Iexact: $claimPersonalityId
    published_Gte: $dateGte
    first: $first
    id_In: $pks
    locale_LanguageCode: $localeCode
    offset: $offset
    orderBy: $orderBy
    rating_Isnull: $ratingIsNull
    rating_Slug_Iexact: $ratingSlug
    tags_In: $tagSlugs
  ) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        ...FactcheckArticlePreview
        claim {
          ...ClaimDetails
        }
      }
    }
  }
  claimsNodeConnection {
    edges {
      node {
        ...ClaimDetails
      }
    }
  }
}

fragment FactcheckArticlePreview on FactcheckArticleNode {
  __typename
  rating {
    ...FactcheckArticlePreviewRating
  }
  featuredImage {
    ...ArticlePreviewFeaturedImage
  }
  featuredYouTubeVideo {
    ...FeaturedYouTubeVideoMinimal
  }
  id
  pk
  published
  slug
  synopsis
  title
}

fragment ClaimDetails on ClaimNode {
  id
  locale
  statement
  link
  source
  factcheckArticle {
    # Include any fields you want from the FactcheckArticleNode here
  }
}

fragment FactcheckArticlePreviewRating on RatingNode {
  colour
  icon {
    rendition(format: "png" width: 300) {
      ...FnImageRendition
    }
  }
  titleEn
  titleFa
}

fragment FnImageRendition on ImageRendition {
  height
  id
  url
  width
}

fragment ArticlePreviewFeaturedImage on CaptionedImageNode {
  rendition(format: "jpeg" width: 600) {
    ...FnImageRendition
  }
}

fragment FeaturedYouTubeVideoMinimal on FeaturedYouTubeVideoNode {
  id
}

    """
    
    # Send the request
    response = requests.post(endpoint, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

articles = []
for i in range (1,6):
    article_var = {
        "first": 300,
        "localeCode": "fa",
        "offset": 300*(i-1),
        "orderBy": "-published",
        "ratingSlug": None,
        "tagSlugs": None
    }
    factnameh_data = fetch_factcheck_data(article_var)

    with open (f"allfacts_{i}.txt", "w") as file:
        file.write(str(factnameh_data))