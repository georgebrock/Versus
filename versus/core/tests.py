from django.test import TestCase
from recommendations import _calculate_pearson_correlation_score, pearson_correlation_score, _scores_for_mutual_venues, similar_profiles
from foursquare.models import UserProfile

class PearsonCorrelationScoreTest(TestCase):
    def test_with_no_overlap(self):
        score = _calculate_pearson_correlation_score({})
        self.assertEqual(0, score)

    def test_with_perfect_positive_correlation(self):
        score = _calculate_pearson_correlation_score({
            1: {'a': 2, 'b': 2},
            2: {'a': 1, 'b': 1},
            3: {'a': -1, 'b': -1},
        })
        self.assertEqual(1, score)

    def test_with_perfect_negative_correlation(self):
        score = _calculate_pearson_correlation_score({
            1: {'a': 2, 'b': -2},
            2: {'a': 0, 'b': 0},
            3: {'a': -2, 'b': 2},
        })
        self.assertEqual(-1, score)

    def test_with_good_correlation(self):
        score = _calculate_pearson_correlation_score({
            1: {'a': 2, 'b': 3},
            2: {'a': 2, 'b': 2},
            3: {'a': 0, 'b': 1},
        })
        self.assertTrue(score > 0.75)


class SimilarityTest(TestCase):
    fixtures = [ 'correlations' ]

    def test_venue_overlap(self):
        p = UserProfile.objects.in_bulk([1,2,3,4])
        self.assertEqual(
            _scores_for_mutual_venues(p[2], p[3]),
            {
                1: {'a': 2, 'b': 1},
                4: {'a': 1, 'b': 4},
            },
        )

    def test_correlation(self):
        p = UserProfile.objects.in_bulk([1,2,3,4])
        self.assertEqual(1, pearson_correlation_score(p[1], p[2]))
        self.assertTrue(pearson_correlation_score(p[1], p[4]) > 0.5)
        self.assertTrue(pearson_correlation_score(p[1], p[3]) < -0.75)

    def test_similarity(self):
        p = UserProfile.objects.in_bulk([1,2,3,4])

        approx_similar = [(round(score,1),pr) for score,pr in similar_profiles(p[1])]
        self.assertEqual([(1.0, p[2]), (0.7, p[4])], approx_similar)
        self.assertEqual([], similar_profiles(p[3]) )

