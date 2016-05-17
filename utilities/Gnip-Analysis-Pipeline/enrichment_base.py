
class BaseEnrichment(object):
    """ 
    Classes that add data to a single tweet (enrichments)
    inherit from this class. These derived enrichment classes
    must implement the function 'enrichment value', which
    accepts a tweet dictionary as the single argument, and
    returns the enrichment value. This value must be JSON-
    serializable.
    """
    def __init__(self):
        pass
    def enrich(self,tweet):
        if "enrichments" not in tweet:
            tweet['enrichments'] = {}
        tweet['enrichments'][self.__class__.__name__] = self.enrichment_value(tweet)


