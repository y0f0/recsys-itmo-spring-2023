from .recommender import Recommender
import random
from .toppop import TopPop

limit = 0.5


class CustomRecommender(Recommender):

    def __init__(self, tracks_redis, catalog, top_tracks):
        self.tracks_redis = tracks_redis
        self.fallback = TopPop(tracks_redis, top_tracks)
        self.catalog = catalog

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        previous_track = self.tracks_redis.get(prev_track)
        if previous_track is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        if prev_track_time >= limit:
            self.catalog.last_tracks[user] = previous_track
        else:
            previous_track = self.catalog.last_tracks.get(user)

        previous_track = self.catalog.from_bytes(previous_track)
        recommendations = previous_track.recommendations
        if not recommendations:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        return shuffled[0]
