from foursquare.models import UserProfile
from math import sqrt

def _scores_for_mutual_venues(profile_a, profile_b):
    """
    Finds all the mutual venues for two profiles and returns a dictionary
    of the scores.

    The dictionary entries are in the form:
      venue_id: {'a': profile_a_score, 'b': profile_b_score}
    """

    # Get the visits (which contain scores and venues) for both users
    a_visits = profile_a.visit_set.filter(ranked=True)
    b_visits = profile_b.visit_set.filter(ranked=True)

    # Work out the intersection of the visited venues
    a_venue_ids = set([visit.venue_id for visit in a_visits])
    b_venue_ids = set([visit.venue_id for visit in b_visits])
    mutual_venue_ids = a_venue_ids & b_venue_ids

    # Make sure they have something in common
    if len(mutual_venue_ids) == 0:
        return {}

    # Get the scores in a form where they can be accessed by venue_id
    scores_by_venue = {}
    for visit in a_visits:
        if visit.venue_id in mutual_venue_ids:
            scores_by_venue.setdefault(visit.venue_id, {})
            scores_by_venue[visit.venue_id]['a'] = visit.score
    for visit in b_visits:
        if visit.venue_id in mutual_venue_ids:
            scores_by_venue.setdefault(visit.venue_id, {})
            scores_by_venue[visit.venue_id]['b'] = visit.score
    
    return scores_by_venue

def _calculate_pearson_correlation_score(scores_by_venue):
    """
    Takes a dictionary of scores by venue in the form returned by
    _scores_for_mutual_venues and returns the pearson correlations score
    for the two profiles it represents.
    """
    # No overlap means no correlation
    n_mutual_venues = len(scores_by_venue)
    if n_mutual_venues == 0:
        return 0

    # Various summations are required for the correlation score
    a_sum, a_sq_sum = 0, 0
    b_sum, b_sq_sum = 0, 0
    product_sum = 0
    for venue_id in scores_by_venue:
        a_score = scores_by_venue[venue_id]['a']
        b_score = scores_by_venue[venue_id]['b']
        a_sum += a_score
        a_sq_sum += pow(a_score, 2)
        b_sum += b_score
        b_sq_sum += pow(b_score, 2)
        product_sum += a_score * b_score

    # Calculate the correlation score
    denominator = sqrt((a_sq_sum - pow(a_sum, 2) / n_mutual_venues) * \
                       (b_sq_sum - pow(b_sum, 2) / n_mutual_venues))
    if denominator == 0:
        return 0;
    numerator = product_sum - (a_sum * b_sum / n_mutual_venues)
    return numerator / denominator

def pearson_correlation_score(profile_a, profile_b):
    """
    Calculates the similarity in taste of two profiles.
    The return values are on a scale from -1 to 1:
      -1    Perfect negative correlation
       0    No correlation
       1    Perfect positive correlation
    """
    scores_by_venue = _scores_for_mutual_venues(profile_a, profile_b)
    return _calculate_pearson_correlation_score(scores_by_venue)

def similar_profiles(profile):
    """
    Returns a sorted list of score/profile tuples for all profiles that are
    positively correlated with the given profile. Most correlated first.
    """
    other_profiles = UserProfile.objects.exclude(pk=profile.pk)
    similar_profiles = []
    for other in other_profiles:
        score = pearson_correlation_score(profile, other)
        if score > 0:
            similar_profiles.append((score, other, ))
    similar_profiles.sort()
    similar_profiles.reverse()
    return similar_profiles

